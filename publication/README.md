# Publication pipeline

Publication is deliberately separate from the conceptual source on `main`.
`outline.md` remains authoritative; generated prose and site output live only in
Actions artefacts and the `gh-pages` publication branch.

## One-time repository setup

1. Add `OPENAI_API_KEY` as a GitHub Actions secret. Prefer placing it in a
   `paid-compile` environment and configuring that environment with a required
   reviewer if you want an approval gate in addition to the workflow's explicit
   paid-run confirmation checkbox.
2. Configure the `publication-release` environment with a required reviewer.
   The workflow references this environment before a release can be published.
3. After the first successful publication creates `gh-pages`, configure GitHub
   Pages to **Deploy from a branch**, branch `gh-pages`, folder `/docs`.

## Publishing

Run **Actions → Publish compiled essay → Run workflow** from `main`.

- Choose `draft` or `release`.
- For a draft, `source_ref` may name an explicitly selected branch, tag, or SHA.
- A release requires `source_ref=main`.
- Tick **I approve this paid compiled-prose run**. Without that explicit
  confirmation the workflow fails before any provider call.

The selected source ref is treated as data, not executable code: only
`outline.md` and `references.bib` are checked out from it. Publication scripts
come from the trusted `main` workflow commit, and `grantaj/compiled-prose` is
checked out at the SHA pinned in the workflow. The selected source files must be
regular Git blobs rather than symlinks or special entries.

The compiler's generated `final.tex` is also treated as untrusted renderer
input. Pandoc runs with `--sandbox`, so LaTeX include/resource directives cannot
read arbitrary runner files. Pandoc's structured warning log is checked after
rendering: only the known localization warnings caused by packaged translation
data being unavailable inside the sandbox are tolerated; unresolved citations,
blocked include attempts, and every other warning fail the build. Math is emitted
as native MathML, avoiding a runtime JavaScript or local MathJax dependency, and
the HTML template applies a restrictive content-security policy.

A compiler/render failure never touches `gh-pages`. On success, only the chosen
`docs/draft/` or `docs/release/` directory is replaced, the other channel is
preserved, and the change is pushed as one publication commit. Compiler output
and diagnostics are also retained as an Actions artefact for inspection.

## Updating the compiler pin

Changing `COMPILED_PROSE_SHA` is a dependency update and should receive explicit
review. Do not replace it with a floating branch. If a publication needs a
project-specific prompt or compiler workaround, fix the generic compiler
instead of adding hidden prompt configuration here.

## Provenance and variance controls

Each published channel includes `provenance.json` with the exact censorship and
compiled-prose commits, workflow run, backend/model, renderer versions, and
variance settings. At the pinned compiler revision, the OpenAI runner does not
apply temperature to `gpt-5` and the Responses API path ignores seed; provenance
therefore records both the requested values and the effective values (`null`)
rather than implying determinism that the backend does not provide.
