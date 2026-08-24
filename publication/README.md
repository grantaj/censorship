# Publication pipeline

Compilation and publication are deliberately separate from the conceptual source
on `main`. `outline.md` remains authoritative; generated prose and site output
live only in retained Actions artefacts and the `gh-pages` publication branch.

## One-time repository setup

1. Put `OPENAI_API_KEY` in the `paid-compile` GitHub Environment. The compile
   workflow is the only workflow allowed to reference it. A required reviewer on
   this environment is optional because the workflow also requires an explicit
   paid-run confirmation.
2. Configure the `publication-release` environment with a required reviewer.
   Draft publication is keyless and does not use this environment; release
   publication must pass it.
3. After the first successful publication creates `gh-pages`, configure GitHub
   Pages to **Deploy from a branch**, branch `gh-pages`, folder `/docs`.

## Compile a candidate

Run **Actions → Compile essay candidate → Run workflow** from `main`.

- `source_ref` selects the censorship branch, tag, or SHA whose authored source
  will be compiled. Only `outline.md` and `references.bib` are read from it.
- Choose an allowlisted OpenAI model and compilation target.
- Tick **I approve this paid compiled-prose run**. Without that explicit
  confirmation the workflow fails before any provider call.

The workflow checks out `grantaj/compiled-prose` at the exact SHA pinned in
`compile.yml`, passes `references.bib` explicitly to the compiler, runs the full
pipeline, validates generated LaTeX stages, and produces a final PDF. A
successful run retains a self-contained candidate for 90 days containing the
complete compiler build, the exact source files, and machine-readable metadata
for the source SHA, compiler SHA, model, target, source ref, workflow run, and
variance controls. A successful compilation does **not** publish anything.

Failed compilations retain diagnostics and any partial build evidence, but they
are never eligible for publication.

## Publish a retained candidate

Run **Actions → Publish compiled essay → Run workflow** from `main`.

- Choose `draft` or `release`.
- Choose the target to publish.

Publication makes no provider call and cannot access `OPENAI_API_KEY`. It finds
the newest non-expired candidate artifact for the selected target whose
**Compile essay candidate** workflow run completed successfully, validates the
candidate metadata against that run, renders it, and then replaces only the
selected `docs/draft/` or `docs/release/` channel.

A draft may promote a candidate compiled from any explicitly selected
`source_ref`. A release is stricter: the retained candidate must have been
compiled with `source_ref=main`, and its `outline.md` and `references.bib` must
still be byte-identical to current `main`. The `publication-release`
environment then provides the human release approval gate. This lets harmless
workflow or documentation changes occur after compilation without silently
publishing stale conceptual source or bibliography metadata.

The compiler's generated `final.tex` is treated as untrusted renderer input.
Pandoc runs with `--sandbox`, so LaTeX include/resource directives cannot read
arbitrary runner files. Pandoc's structured warning log is checked after
rendering: only the known localization warnings caused by packaged translation
data being unavailable inside the sandbox are tolerated; unresolved citations,
blocked include attempts, and every other warning fail the build. Math is emitted
as native MathML, avoiding a runtime JavaScript or local MathJax dependency, and
the HTML template applies a restrictive content-security policy.

A compiler or renderer failure never touches `gh-pages`. On publication success,
only the chosen channel is replaced, the other channel is preserved, and the
change is pushed as one publication commit.

## Updating the compiler pin

Changing `COMPILED_PROSE_SHA` is a dependency update and should receive explicit
review. Do not replace it with a floating branch. If a compilation needs a
project-specific prompt or compiler workaround, fix the generic compiler
instead of adding hidden prompt configuration here.

## Provenance and variance controls

Each published channel includes `provenance.json` with the exact censorship and
compiled-prose commits, compilation run, backend/model, selected target,
renderer versions, and variance settings. The pinned compiler omits temperature
for GPT-5-family models and the OpenAI Responses API does not accept seed, so
provenance records the requested values while explicitly recording their
effective values as `null` rather than implying deterministic generation.
