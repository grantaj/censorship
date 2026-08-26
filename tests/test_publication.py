from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

import sys
sys.path.insert(0, str(ROOT))
from publication.site import update_site  # noqa: E402


def provenance(source: str = "a" * 40) -> dict[str, object]:
    return {
        "censorship_source_sha": source,
        "compiled_prose_sha": "b" * 40,
        "backend": "openai",
        "model": "gpt-5.6-sol",
        "target": "journal_academic",
        "workflow_run_id": "123",
        "workflow_run_url": "https://example.invalid/run/123",
        "build_timestamp": "2026-08-24T00:00:00Z",
        "requested_temperature": "0.2",
        "requested_seed": "42",
        "effective_temperature": None,
        "effective_seed": None,
        "variance_controls_note": "unsupported by backend",
        "pandoc_version": "pandoc 3.x",
        "openai_sdk_version": "1.x",
    }


def write_build(path: Path, marker: str) -> None:
    path.mkdir(parents=True)
    (path / "index.html").write_text(marker, encoding="utf-8")
    (path / "style.css").write_text("body{}\n", encoding="utf-8")
    (path / "provenance.json").write_text(json.dumps(provenance()), encoding="utf-8")


class SiteUpdateTests(unittest.TestCase):
    def test_update_replaces_entire_site_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            site = root / "docs"
            build = root / "build"
            (site / "release").mkdir(parents=True)
            (site / "release/index.html").write_text("legacy-release", encoding="utf-8")
            (site / "draft").mkdir()
            (site / "draft/index.html").write_text("legacy-draft", encoding="utf-8")
            write_build(build, "current-paper")

            update_site(site, build)

            self.assertEqual((site / "index.html").read_text(), "current-paper")
            self.assertTrue((site / "style.css").is_file())
            self.assertTrue((site / "provenance.json").is_file())
            self.assertTrue((site / ".nojekyll").is_file())
            self.assertFalse((site / "release").exists())
            self.assertFalse((site / "draft").exists())

    def test_incomplete_build_fails_before_replacement(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            site = root / "docs"
            build = root / "broken"
            site.mkdir()
            (site / "index.html").write_text("old-paper", encoding="utf-8")
            write_build(build, "new-paper")
            (build / "style.css").unlink()

            with self.assertRaises(ValueError):
                update_site(site, build)

            self.assertEqual((site / "index.html").read_text(), "old-paper")

    def test_invalid_provenance_fails_before_replacement(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            site = root / "docs"
            build = root / "bad"
            site.mkdir()
            (site / "index.html").write_text("old-paper", encoding="utf-8")
            write_build(build, "new-paper")
            (build / "provenance.json").write_text("{}", encoding="utf-8")

            with self.assertRaises(ValueError):
                update_site(site, build)

            self.assertEqual((site / "index.html").read_text(), "old-paper")


class RenderTests(unittest.TestCase):
    def test_render_invokes_sandboxed_citeproc_and_copies_local_css(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            tex = root / "final.tex"
            bib = root / "references.bib"
            out = root / "out"
            fake = root / "pandoc"
            args_file = root / "args.txt"
            tex.write_text("\\section{Test}\n", encoding="utf-8")
            bib.write_text("", encoding="utf-8")
            fake.write_text(
                "#!/usr/bin/env bash\n"
                "printf '%s\\n' \"$@\" > \"$FAKE_ARGS\"\n"
                "while (($#)); do\n"
                "  case $1 in\n"
                "    --output=*) touch \"${1#--output=}\" ;;\n"
                "    --log=*) printf '[]\\n' > \"${1#--log=}\" ;;\n"
                "  esac\n"
                "  shift\n"
                "done\n",
                encoding="utf-8",
            )
            fake.chmod(0o755)
            env = os.environ.copy()
            env.update(
                {
                    "PANDOC": str(fake),
                    "FAKE_ARGS": str(args_file),
                    "SOURCE_SHA": "a" * 40,
                    "COMPILED_PROSE_SHA": "b" * 40,
                    "WORKFLOW_RUN_URL": "https://example.invalid/run/1",
                    "BUILD_TIMESTAMP": "2026-08-24T00:00:00Z",
                }
            )
            subprocess.run(
                [str(ROOT / "publication/render.sh"), str(tex), str(bib), str(out)],
                check=True,
                env=env,
            )
            args = args_file.read_text(encoding="utf-8")
            self.assertIn("--sandbox", args)
            self.assertIn("--quiet", args)
            self.assertIn("--citeproc", args)
            self.assertIn("--mathml", args)
            self.assertNotIn("--mathjax", args)
            self.assertIn("--log=", args)
            self.assertIn(f"--bibliography={bib}", args)
            self.assertNotIn("publication_channel", args)
            self.assertTrue((out / "style.css").is_file())
            self.assertTrue((out / "index.html").is_file())


class WorkflowSafetyTests(unittest.TestCase):
    def test_paid_compile_is_manual_only_tracks_compiler_main_and_separate(self) -> None:
        compile_workflow = (ROOT / ".github/workflows/compile.yml").read_text(
            encoding="utf-8"
        )
        publish_workflow = (ROOT / ".github/workflows/publish.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("workflow_dispatch:", compile_workflow)
        self.assertNotIn("\n  push:", compile_workflow)
        self.assertNotIn("\n  pull_request:", compile_workflow)
        self.assertIn("confirm_paid_run", compile_workflow)
        self.assertIn(
            "repository: grantaj/compiled-prose\n          ref: main", compile_workflow
        )
        self.assertNotIn("COMPILED_PROSE_SHA:", compile_workflow)
        self.assertIn(
            'compiler_sha=$(git -C compiler rev-parse HEAD)', compile_workflow
        )
        self.assertIn('WORKFLOW_REF: ${{ github.ref }}', compile_workflow)
        self.assertIn('SOURCE_REF: ${{ inputs.source_ref }}', compile_workflow)
        self.assertIn("environment: paid-compile", compile_workflow)
        self.assertIn("OPENAI_API_KEY", compile_workflow)
        self.assertNotIn("OPENAI_API_KEY", publish_workflow)
        self.assertIn(
            'BIBLIOGRAPHY="$GITHUB_WORKSPACE/compiler/build/references.bib"',
            compile_workflow,
        )
        self.assertIn('TARGET_STYLE="$TARGET_STYLE"', compile_workflow)
        self.assertIn("gpt-5.6-sol", compile_workflow)
        self.assertIn("journal_academic", compile_workflow)

    def test_publish_is_single_academic_release_without_provider_access(self) -> None:
        workflow = (ROOT / ".github/workflows/publish.yml").read_text(encoding="utf-8")
        self.assertIn("workflow_dispatch:", workflow)
        self.assertNotIn("channel:", workflow)
        self.assertNotIn("inputs.target", workflow)
        self.assertIn("TARGET_ID: journal_academic", workflow)
        self.assertIn("actions/github-script@v8", workflow)
        self.assertIn('run.path !== ".github/workflows/compile.yml"', workflow)
        self.assertIn("censorship-candidate-${process.env.TARGET_ID}-", workflow)
        self.assertIn("environment: publication-release", workflow)
        self.assertIn('metadata["requested_source_ref"] != "main"', workflow)
        self.assertIn("candidate_path.read_bytes() != current_path.read_bytes()", workflow)
        self.assertIn("SOURCE_SHA: ${{ needs.assemble.outputs.source_sha }}", workflow)
        self.assertIn('[[ ! "$SOURCE_SHA" =~ ^[0-9a-f]{40}$ ]]', workflow)
        self.assertIn("--site-root site-repo/docs", workflow)
        self.assertNotIn("--channel", workflow)
        self.assertNotIn("OPENAI_API_KEY", workflow)
        self.assertNotIn("confirm_paid_run", workflow)


if __name__ == "__main__":
    unittest.main()
