#!/usr/bin/env bash
set -euo pipefail

if (( $# != 3 )); then
  echo "usage: $0 FINAL_TEX REFERENCES_BIB OUT_DIR" >&2
  exit 64
fi

final_tex=$1
references_bib=$2
out_dir=$3
script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
pandoc_bin=${PANDOC:-pandoc}

: "${SOURCE_SHA:?SOURCE_SHA is required}"
: "${COMPILED_PROSE_SHA:?COMPILED_PROSE_SHA is required}"
: "${WORKFLOW_RUN_URL:?WORKFLOW_RUN_URL is required}"
: "${BUILD_TIMESTAMP:?BUILD_TIMESTAMP is required}"

if [[ ! -f "$final_tex" ]]; then
  echo "final LaTeX not found: $final_tex" >&2
  exit 66
fi
if [[ ! -f "$references_bib" ]]; then
  echo "bibliography not found: $references_bib" >&2
  exit 66
fi

mkdir -p "$out_dir"
cp "$script_dir/style.css" "$out_dir/style.css"
pandoc_log=$(mktemp)
trap 'rm -f "$pandoc_log"' EXIT

"$pandoc_bin" "$final_tex" \
  --sandbox \
  --quiet \
  --standalone \
  --toc \
  --toc-depth=2 \
  --mathml \
  --citeproc \
  --bibliography="$references_bib" \
  --template="$script_dir/template.html" \
  --css=style.css \
  --log="$pandoc_log" \
  --metadata="source_sha:$SOURCE_SHA" \
  --metadata="compiled_prose_sha:$COMPILED_PROSE_SHA" \
  --metadata="workflow_run_url:$WORKFLOW_RUN_URL" \
  --metadata="build_timestamp:$BUILD_TIMESTAMP" \
  --output="$out_dir/index.html"

# Pandoc's sandbox intentionally cannot read packaged translation data unless
# the binary embeds it. Debian/Ubuntu Pandoc therefore emits two harmless
# localization warning classes in sandbox mode. Preserve fail-closed warning
# semantics for everything else by inspecting Pandoc's structured log.
python - "$pandoc_log" <<'PY'
import json
import sys

with open(sys.argv[1], encoding="utf-8") as handle:
    events = json.load(handle)

allowed_sandbox_warnings = {"CouldNotLoadTranslations", "NoTranslation"}
unexpected = [
    event
    for event in events
    if event.get("verbosity") == "WARNING"
    and event.get("type") not in allowed_sandbox_warnings
]
if unexpected:
    print("Pandoc emitted publication-blocking warnings:", file=sys.stderr)
    for event in unexpected:
        print(json.dumps(event, sort_keys=True), file=sys.stderr)
    raise SystemExit(3)
PY
