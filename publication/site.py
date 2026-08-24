#!/usr/bin/env python3
"""Small, deterministic helpers for censorship publication state.

This module deliberately has no network or model dependencies. The paid compiler
runs before these helpers are invoked; this code only records provenance and
updates a staged Pages tree.
"""

from __future__ import annotations

import argparse
import html
import json
import shutil
from pathlib import Path
from typing import Any

CHANNELS = ("draft", "release")
REQUIRED_PROVENANCE = (
    "censorship_source_sha",
    "compiled_prose_sha",
    "backend",
    "model",
    "target",
    "workflow_run_id",
    "workflow_run_url",
    "publication_channel",
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


def validate_provenance(data: dict[str, Any], channel: str | None = None) -> None:
    missing = [key for key in REQUIRED_PROVENANCE if key not in data]
    if missing:
        raise ValueError("missing provenance fields: " + ", ".join(missing))
    recorded = data["publication_channel"]
    if recorded not in CHANNELS:
        raise ValueError(f"invalid publication channel in provenance: {recorded!r}")
    if channel is not None and recorded != channel:
        raise ValueError(
            f"provenance channel {recorded!r} does not match requested {channel!r}"
        )


def write_provenance(args: argparse.Namespace) -> None:
    if args.channel not in CHANNELS:
        raise ValueError(f"invalid channel: {args.channel!r}")
    data: dict[str, Any] = {
        "censorship_source_sha": args.source_sha,
        "compiled_prose_sha": args.compiler_sha,
        "backend": args.backend,
        "model": args.model,
        "target": args.target,
        "workflow_run_id": args.run_id,
        "workflow_run_url": args.run_url,
        "publication_channel": args.channel,
        "build_timestamp": args.timestamp,
        "requested_temperature": args.requested_temperature,
        "requested_seed": args.requested_seed,
        "effective_temperature": (
            None
            if args.effective_temperature == "none"
            else args.effective_temperature
        ),
        "effective_seed": None if args.effective_seed == "none" else args.effective_seed,
        "variance_controls_note": args.variance_note,
        "pandoc_version": args.pandoc_version,
        "openai_sdk_version": args.openai_sdk_version,
    }
    validate_provenance(data, args.channel)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def _channel_summary(site_root: Path, channel: str) -> dict[str, Any] | None:
    provenance_path = site_root / channel / "provenance.json"
    index_path = site_root / channel / "index.html"
    if not provenance_path.is_file() or not index_path.is_file():
        return None
    try:
        data = _load_json(provenance_path)
        validate_provenance(data, channel)
    except (OSError, ValueError, json.JSONDecodeError):
        return None
    return data


def render_root_index(site_root: Path) -> str:
    cards: list[str] = []
    for channel in CHANNELS:
        data = _channel_summary(site_root, channel)
        label = channel.capitalize()
        if data is None:
            cards.append(
                f'<section class="channel unavailable"><h2>{label}</h2>'
                "<p>No successful publication yet.</p></section>"
            )
            continue
        source = html.escape(str(data["censorship_source_sha"]))
        compiler = html.escape(str(data["compiled_prose_sha"]))
        built = html.escape(str(data["build_timestamp"]))
        model = html.escape(str(data["model"]))
        target = html.escape(str(data["target"]))
        cards.append(
            f'<section class="channel"><h2><a href="{channel}/">{label}</a></h2>'
            f"<p>Built {built}</p>"
            f"<dl><dt>source</dt><dd><code>{source[:12]}</code></dd>"
            f"<dt>compiler</dt><dd><code>{compiler[:12]}</code></dd>"
            f"<dt>model</dt><dd>{model}</dd>"
            f"<dt>target</dt><dd>{target}</dd></dl></section>"
        )
    return """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Censorship — publications</title>
<style>
:root{color-scheme:light dark;--bg:#f8f7f3;--fg:#171717;--muted:#666;--line:#d6d2c8;--card:#fff}
@media(prefers-color-scheme:dark){:root{--bg:#111;--fg:#eceae4;--muted:#aaa;--line:#393939;--card:#181818}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:17px/1.55 system-ui,sans-serif}
main{max-width:760px;margin:0 auto;padding:9vh 24px}h1{font:700 clamp(2.3rem,8vw,4.6rem)/.98 Georgia,serif;margin:0 0 .5rem}
.intro{color:var(--muted);max-width:56ch;margin-bottom:3rem}.channels{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:1rem}
.channel{background:var(--card);border:1px solid var(--line);padding:1.2rem 1.3rem}.channel h2{margin:.1rem 0 .8rem}.channel a{color:inherit}
dl{display:grid;grid-template-columns:auto 1fr;gap:.25rem .7rem;margin:0;color:var(--muted)}dt{font-weight:600}dd{margin:0}.unavailable{color:var(--muted)}
</style>
</head><body><main><h1>Censorship</h1><p class="intro">Published compiled-prose builds. Draft and release are independent channels; failed builds leave the previous publication untouched.</p>
<div class="channels">""" + "".join(cards) + """</div></main></body></html>\n"""


def update_site(site_root: Path, channel: str, build_dir: Path) -> None:
    if channel not in CHANNELS:
        raise ValueError(f"invalid channel: {channel!r}")
    for required_file in ("index.html", "style.css", "provenance.json"):
        if not (build_dir / required_file).is_file():
            raise ValueError(f"build directory lacks {required_file}: {build_dir}")
    provenance = _load_json(build_dir / "provenance.json")
    validate_provenance(provenance, channel)

    site_root.mkdir(parents=True, exist_ok=True)
    target = site_root / channel
    staged = site_root / f".{channel}.next"
    if staged.exists():
        shutil.rmtree(staged)
    shutil.copytree(build_dir, staged)

    # Replacement occurs only after a complete build has been copied and
    # validated. Remote publication is a later single git commit/push.
    if target.exists():
        shutil.rmtree(target)
    staged.rename(target)
    (site_root / ".nojekyll").touch()
    (site_root / "index.html").write_text(
        render_root_index(site_root), encoding="utf-8"
    )


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
    prov.add_argument("--channel", choices=CHANNELS, required=True)
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
    update.add_argument("--channel", choices=CHANNELS, required=True)
    update.add_argument("--build-dir", required=True)

    args = parser.parse_args()
    if args.command == "provenance":
        write_provenance(args)
    else:
        update_site(Path(args.site_root), args.channel, Path(args.build_dir))


if __name__ == "__main__":
    main()
