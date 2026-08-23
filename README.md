# Censorship

This repository contains the source for an essay developing a structural account of censorship.

The repository is deliberately small:

- `outline.md` is the sole authoritative conceptual source and the input to `grantaj/compiled-prose`.
- `references.bib` supplies bibliographic metadata for citations authored in the outline; it is not an independent source of claims.
- `.github/`, `publication/`, and `tests/` are build, verification, rendering, and publication infrastructure.

The conceptual framework, scope choices, definitions, taxonomy, and final judgments are human-authored. AI tools may assist with structure, consistency checks, adversarial review, citation organisation, and prose rendering, but conceptual defects are repaired in `outline.md` rather than delegated to generated prose. Historical planning, context material, old compilation prompts, and LaTeX source scaffolding remain available in Git history rather than as parallel source or process layers.

Generated prose, LaTeX, HTML, PDFs, review outputs, and other publication artefacts are build products. They are not tracked on `main`; successful explicitly approved builds are published by the repository's publication workflow.
