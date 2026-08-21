from pathlib import Path
import os
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def render_env() -> dict[str, str]:
    env = os.environ.copy()
    env.update(
        {
            "PUBLICATION_CHANNEL": "draft",
            "SOURCE_SHA": "a" * 40,
            "COMPILED_PROSE_SHA": "b" * 40,
            "WORKFLOW_RUN_URL": "https://example.invalid/run/1",
            "BUILD_TIMESTAMP": "2026-08-21T00:00:00Z",
        }
    )
    return env


class WorkflowHardeningTests(unittest.TestCase):
    def test_selected_source_rejects_symlinks_and_full_pipeline_is_clean(self) -> None:
        workflow = (ROOT / ".github/workflows/publish.yml").read_text(encoding="utf-8")
        self.assertIn('mode_type=$(git -C source-input ls-tree "$source_sha"', workflow)
        self.assertIn('[[ -L "source-input/$source_file" ]]', workflow)
        self.assertIn("make -C compiler clobber", workflow)
        self.assertLess(
            workflow.index("make -C compiler clobber"),
            workflow.index("make -C compiler \\\n            BACKEND=openai"),
        )

    @unittest.skipUnless(shutil.which("pandoc"), "pandoc is not installed")
    def test_real_pandoc_resolves_citation_and_uses_native_math(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            tex = root / "fixture.tex"
            bib = root / "references.bib"
            out = root / "out"
            tex.write_text(
                "\\documentclass{article}\n"
                "\\title{Publication fixture}\n"
                "\\begin{document}\n"
                "\\maketitle\n"
                "A cited claim \\cite{fixture}. Inline math $x^2$.\n"
                "\\end{document}\n",
                encoding="utf-8",
            )
            bib.write_text(
                "@article{fixture,\n"
                "  author = {Example, Alice},\n"
                "  title = {A Fixture Reference},\n"
                "  journal = {Test Journal},\n"
                "  year = {2020}\n"
                "}\n",
                encoding="utf-8",
            )
            subprocess.run(
                [str(ROOT / "publication/render.sh"), str(tex), str(bib), str(out)],
                check=True,
                env=render_env(),
            )
            rendered = (out / "index.html").read_text(encoding="utf-8")
            self.assertIn("Example", rendered)
            self.assertIn("Fixture Reference", rendered)
            self.assertIn("<math", rendered)
            self.assertNotIn("MathJax", rendered)
            self.assertIn('href="style.css"', rendered)
            self.assertIn("Content-Security-Policy", rendered)
            self.assertIn("script-src 'none'", rendered)

    @unittest.skipUnless(shutil.which("pandoc"), "pandoc is not installed")
    def test_missing_citation_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            tex = root / "missing.tex"
            bib = root / "references.bib"
            out = root / "out"
            tex.write_text(
                "\\documentclass{article}\n"
                "\\title{Missing citation}\n"
                "\\begin{document}\n"
                "A bad citation \\cite{does-not-exist}.\n"
                "\\end{document}\n",
                encoding="utf-8",
            )
            bib.write_text("", encoding="utf-8")
            result = subprocess.run(
                [str(ROOT / "publication/render.sh"), str(tex), str(bib), str(out)],
                check=False,
                env=render_env(),
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("CiteprocWarning", result.stderr)

    @unittest.skipUnless(shutil.which("pandoc"), "pandoc is not installed")
    def test_sandbox_blocks_unlisted_latex_include(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            secret = root / "secret.tex"
            tex = root / "attack.tex"
            bib = root / "references.bib"
            out = root / "out"
            marker = "DO_NOT_LEAK_PUBLICATION_SECRET"
            secret.write_text(marker + "\n", encoding="utf-8")
            tex.write_text(
                "\\documentclass{article}\n"
                "\\title{Sandbox attack}\n"
                "\\begin{document}\n"
                f"Before. \\input{{{secret.with_suffix('')}}} After.\n"
                "\\end{document}\n",
                encoding="utf-8",
            )
            bib.write_text("", encoding="utf-8")
            result = subprocess.run(
                [str(ROOT / "publication/render.sh"), str(tex), str(bib), str(out)],
                check=False,
                env=render_env(),
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("CouldNotLoadIncludeFile", result.stderr)
            if (out / "index.html").is_file():
                self.assertNotIn(
                    marker, (out / "index.html").read_text(encoding="utf-8")
                )


if __name__ == "__main__":
    unittest.main()
