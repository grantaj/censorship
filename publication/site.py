#!/usr/bin/env python3
"""Deterministic helpers for publishing the current censorship paper."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any

REQUIRED_PROVENANCE = (
    "censorship_source_sha",
    "compiled_prose_sha",
    "backend",
    "model",
    "target",
    "workflow_run_id",
    "workflow_run_url",
    "build_timestamp",
    "requested_temperature",
    "requested_seed",
    "effective_temperature",
    "effective_seed",
    "variance_controls_note",
    "pandoc_version",
    "openai_sdk_version",
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def validate_provenance(data: dict[str, Any]) -> None:
    missing = [key for key in REQUIRED_PROVENANCE if key not in data]
    if missing:
        raise ValueError("missing provenance fields: " + ", ".join(missing))


def write_provenance(args: argparse.Namespace) -> None:
    data: dict[str, Any] = {
        "censorship_source_sha": args.source_sha,
        "compiled_prose_sha": args.compiler_sha,
        "backend": args.backend,
        "model": args.model,
        "target": args.target,
        "workflow_run_id": args.run_id,
        "workflow_run_url": args.run_url,
        "build_timestamp": args.timestamp,
        "requested_temperature": args.requested_temperature,
        "requested_seed": args.requested_seed,
        "effective_temperature": (
            None if args.effective_temperature == "none" else args.effective_temperature
        ),
        "effective_seed": None if args.effective_seed == "none" else args.effective_seed,
        "variance_controls_note": args.variance_note,
        "pandoc_version": args.pandoc_version,
        "openai_sdk_version": args.openai_sdk_version,
    }
    validate_provenance(data)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def update_site(site_root: Path, build_dir: Path) -> None:
    """Replace the published site with one complete, validated paper build."""
    for required_file in ("index.html", "style.css", "provenance.json"):
        if not (build_dir / required_file).is_file():
            raise ValueError(f"build directory lacks {required_file}: {build_dir}")
    provenance = _load_json(build_dir / "provenance.json")
    validate_provenance(provenance)

    site_root.parent.mkdir(parents=True, exist_ok=True)
    staged = site_root.parent / f".{site_root.name}.next"
    if staged.exists():
        shutil.rmtree(staged)
    shutil.copytree(build_dir, staged)
    (staged / ".nojekyll").touch()

    # The validated build is complete before the existing site is removed.
    # Publication is still transactional remotely: the workflow commits and
    # pushes this replacement as one git commit after the local swap succeeds.
    if site_root.exists():
        shutil.rmtree(site_root)
    staged.rename(site_root)


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    prov = subparsers.add_parser("provenance")
    prov.add_argument("--output", required=True)
    prov.add_argument("--source-sha", required=True)
    prov.add_argument("--compiler-sha", required=True)
    prov.add_argument("--backend", required=True)
    prov.add_argument("--model", required=True)
    prov.add_argument("--target", required=True)
    prov.add_argument("--run-id", required=True)
    prov.add_argument("--run-url", required=True)
    prov.add_argument("--timestamp", required=True)
    prov.add_argument("--requested-temperature", required=True)
    prov.add_argument("--requested-seed", required=True)
    prov.add_argument("--effective-temperature", required=True)
    prov.add_argument("--effective-seed", required=True)
    prov.add_argument("--variance-note", required=True)
    prov.add_argument("--pandoc-version", required=True)
    prov.add_argument("--openai-sdk-version", required=True)

    update = subparsers.add_parser("update")
    update.add_argument("--site-root", required=True)
    update.add_argument("--build-dir", required=True)

    args = parser.parse_args()
    if args.command == "provenance":
        write_provenance(args)
    else:
        update_site(Path(args.site_root), Path(args.build_dir))


if __name__ == "__main__":
    main()
