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


def provenance(channel: str, source: str = "a" * 40) -> dict[str, object]:
    return {
        "censorship_source_sha": source,
        "compiled_prose_sha": "b" * 40,
        "backend": "openai",
        "model": "gpt-5.6-sol",
        "target": "journal_academic",
        "workflow_run_id": "123",
        "workflow_run_url": "https://example.invalid/run/123",
        "publication_channel": channel,
        "build_timestamp": "2026-08-24T00:00:00Z",
        "requested_temperature": "0.2",
        "requested_seed": "42",
        "effective_temperature": None,
        "effective_seed": None,
        "variance_controls_note": "unsupported by backend",
        "pandoc_version": "pandoc 3.x",
        "openai_sdk_version": "1.x",
    }


def write_build(path: Path, channel: str, marker: str) -> None:
    path.mkdir(parents=True)
    (path / "index.html").write_text(marker, encoding="utf-8")
    (path / "style.css").write_text("body{}\n", encoding="utf-8")
    (path / "provenance.json").write_text(
        json.dumps(provenance(channel)), encoding="utf-8"
    )


class SiteUpdateTests(unittest.TestCase):
    def test_draft_update_preserves_release(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            site = root / "docs"
            old_release = root / "old-release"
            new_draft = root / "new-draft"
            write_build(old_release, "release", "release-sentinel")
            write_build(new_draft, "draft", "new-draft")
            update_site(site, "release", old_release)
            update_site(site, "draft", new_draft)
            self.assertEqual((site / "release/index.html").read_text(), "release-sentinel")
            self.assertEqual((site / "draft/index.html").read_text(), "new-draft")
            index = (site / "index.html").read_text()
            self.assertIn('href="draft/"', index)
            self.assertIn('href="release/"', index)
            self.assertIn("journal_academic", index)

    def test_release_update_preserves_draft(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            site = root / "docs"
            draft = root / "draft"
            release1 = root / "release1"
            release2 = root / "release2"
            write_build(draft, "draft", "draft-sentinel")
            write_build(release1, "release", "old-release")
            write_build(release2, "release", "new-release")
            update_site(site, "draft", draft)
            update_site(site, "release", release1)
            update_site(site, "release", release2)
            self.assertEqual((site / "draft/index.html").read_text(), "draft-sentinel")
            self.assertEqual((site / "release/index.html").read_text(), "new-release")

    def test_mismatched_provenance_fails_before_replacement(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            site = root / "docs"
            good = root / "good"
            bad = root / "bad"
            write_build(good, "draft", "good")
            write_build(bad, "release", "bad")
            update_site(site, "draft", good)
            with self.assertRaises(ValueError):
                update_site(site, "draft", bad)
            self.assertEqual((site / "draft/index.html").read_text(), "good")

    def test_incomplete_build_fails_before_replacement(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            site = root / "docs"
            good = root / "good"
            broken = root / "broken"
            write_build(good, "draft", "good")
            write_build(broken, "draft", "broken")
            (broken / "style.css").unlink()
            update_site(site, "draft", good)
            with self.assertRaises(ValueError):
                update_site(site, "draft", broken)
            self.assertEqual((site / "draft/index.html").read_text(), "good")


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
                    "PUBLICATION_CHANNEL": "draft",
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
            self.assertTrue((out / "style.css").is_file())
            self.assertTrue((out / "index.html").is_file())


class WorkflowSafetyTests(unittest.TestCase):
    def test_paid_compile_is_manual_only_pinned_and_separate(self) -> None:
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
            "a153c2b19f8b95ba5063947aeeccb072ba862bf6", compile_workflow
        )
        self.assertNotIn("grantaj/compiled-prose@main", compile_workflow)
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

    def test_publish_promotes_retained_candidate_without_provider_access(self) -> None:
        workflow = (ROOT / ".github/workflows/publish.yml").read_text(encoding="utf-8")
        self.assertIn("workflow_dispatch:", workflow)
        self.assertNotIn("\n  push:", workflow)
        self.assertNotIn("\n  pull_request:", workflow)
        self.assertIn("actions/github-script@v8", workflow)
        self.assertIn('run.path !== ".github/workflows/compile.yml"', workflow)
        self.assertIn("censorship-candidate-${process.env.TARGET_ID}-", workflow)
        self.assertIn("environment: publication-release", workflow)
        self.assertIn('metadata["requested_source_ref"] != "main"', workflow)
        self.assertIn("candidate_path.read_bytes() != current_path.read_bytes()", workflow)
        self.assertIn("SOURCE_SHA: ${{ needs.assemble.outputs.source_sha }}", workflow)
        self.assertIn('[[ ! "$SOURCE_SHA" =~ ^[0-9a-f]{40}$ ]]', workflow)
        self.assertNotIn("confirm_paid_run", workflow)


if __name__ == "__main__":
    unittest.main()
