# Publication pipeline

Compilation and publication are deliberately separate from the conceptual source
on `main`. `outline.md` remains authoritative; generated prose and site output
live only in retained Actions artefacts and the `gh-pages` publication branch.

## One-time repository setup

1. Put `OPENAI_API_KEY` in the `paid-compile` GitHub Environment. The compile
   workflow is the only workflow allowed to reference it.
2. Configure the `publication-release` environment with a required reviewer.
3. After the first successful publication creates `gh-pages`, configure GitHub
   Pages to **Deploy from a branch**, branch `gh-pages`, folder `/docs`.

## Compile a candidate

Run **Actions → Compile essay candidate → Run workflow** from `main`.

- `source_ref` selects the censorship branch, tag, or SHA whose authored source
  will be compiled. Only `outline.md` and `references.bib` are read from it.
- Choose an allowlisted OpenAI model and compilation target.
- Tick **I approve this paid compiled-prose run**. Without that explicit
  confirmation the workflow fails before any provider call.

The workflow checks out `grantaj/compiled-prose` from its `main` branch, records
the exact compiler commit that resolves for the run, passes `references.bib`
explicitly to the compiler, runs the full pipeline, validates generated LaTeX
stages, and produces a final PDF. A successful run retains a self-contained
candidate for 90 days containing the complete compiler build, the exact source
files, and machine-readable metadata for the source SHA, compiler SHA, model,
target, source ref, workflow run, and variance controls. A successful compilation
does **not** publish anything.

Failed compilations retain diagnostics and any partial build evidence, but they
are never eligible for publication.

## Publish the paper

Run **Actions → Publish paper → Run workflow** from `main`.

Publication makes no provider call and cannot access `OPENAI_API_KEY`. It finds
the newest non-expired successful `journal_academic` candidate, validates its
metadata against the compile run, and requires that it was compiled from
`source_ref=main` with `outline.md` and `references.bib` still byte-identical to
current `main`. The `publication-release` environment then provides the human
approval gate.

On success, the rendered paper replaces the entire `docs/` site tree in one
publication commit. GitHub Pages therefore serves the current paper directly at
`https://grantaj.github.io/censorship/`; there are no draft/release channels or
publication landing page.

The compiler's generated `final.tex` is treated as untrusted renderer input.
Pandoc runs with `--sandbox`, and its structured warning log is checked after
rendering. Only known localization warnings caused by packaged translation data
being unavailable inside the sandbox are tolerated; unresolved citations,
blocked include attempts, and every other warning fail the build. Math is emitted
as native MathML and the HTML template applies a restrictive content-security
policy.

A compiler, renderer, validation, or approval failure never touches `gh-pages`.

## Compiler tracking during active development

For now the compile workflow deliberately follows `grantaj/compiled-prose@main`
rather than pinning a particular commit. The exact resolved compiler SHA is still
captured in every candidate, so a particular result remains auditable and
reproducible from its provenance.

Project-specific prompt or compiler workarounds should still be fixed in the
generic compiler rather than added as hidden prompt configuration here.

## Provenance and variance controls

The published site includes `provenance.json` with the exact censorship and
compiled-prose commits, compilation run, backend/model, academic target, renderer
versions, and variance settings. The compiler omits temperature for GPT-5-family
models and the OpenAI Responses API does not accept seed, so provenance records
the requested values while explicitly recording their effective values as
`null` rather than implying deterministic generation.
