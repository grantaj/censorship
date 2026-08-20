# Revision Log
## Rationale and Impact Tracker

This log records *why* the outline or core context changed, not just *what* changed. Git handles diffs; this log preserves intent.

### Template

- **Date**: YYYY-MM-DD
- **Files**: affected project files
- **Change Summary**: brief description
- **Rationale**: why the change was needed
- **Impact**: which claims/sections are affected

---

### Entries

- **Date**: 2026-01-31
- **Files**: `context-outline.md`, `context-claims.md`, `context-section-contract.md`, `context-glossary.md`, `context-evidence-tiers.md`, `context-revision-log.md`, `context-global.md`, `context-definitions.md`, `context-taxonomy.md`
- **Change Summary**: Added scaffolding files (claims, section contract, glossary, evidence tiers, revision log) and aligned outline, guardrails, and taxonomy framing.
- **Rationale**: Strengthen long-form coherence, enforce a deterministic rendering pipeline, and make separation of concerns explicit.
- **Impact**: Claims index introduced; outline structure updated; guardrails and pointer table expanded.

- **Date**: 2026-08-21
- **Files**: `outline.md`, `outline-working.md`, `context-outline.md`, `context-claims.md`, `context-global.md`, `context-definitions.md`, `context-taxonomy.md`, `context-glossary.md`, `context-method-note.md`
- **Change Summary**: Narrowed the essay from a broad censorship/morality/control framework to a structural account focused on censorship; introduced a new authoritative `outline.md` designed for `grantaj/compiled-prose`.
- **Rationale**: The broader framework contained valuable ideas but imposed several independent argumentative burdens (morality homology, control theory, general legitimacy theory, shortcut collision) that were not necessary to establish the censorship thesis. Narrowing reduces scope while preserving the strongest original contributions: epistemic preference, mechanism-first taxonomy, kinds-versus-axes separation, infrastructural censorship, and censorship-as-shortcut as a limited explanatory lens.
- **Impact**: Sixteen broad sections collapse to eight censorship-focused sections; morality/control theory are demoted to optional allusions; legitimacy is no longer a canonical claim; an explicit contest-versus-control boundary is added to prevent the definition from expanding into ordinary disagreement; `outline-working.md` and `context-outline.md` are superseded as compilation inputs.

- **Date**: 2026-08-21
- **Files**: `outline.md`, `context-claims.md`, `context-global.md`, `context-definitions.md`, `context-taxonomy.md`, `context-glossary.md`, `context-evidence-tiers.md`, `latex/main.bib`
- **Change Summary**: Applied adversarial review: strengthened the selection/control boundary, separated epistemic preference from control surfaces, reduced the taxonomy to five operational families, replaced claims of orthogonal axes with descriptive dimensions, narrowed the persistence argument, and repositioned novelty against existing censorship scholarship.
- **Rationale**: The first narrowed outline still risked arbitrary classification of editorial and curatorial selection, mixed operations with tactics and downstream responses, overstated novelty in moving beyond explicit bans, and retained too much of the earlier shortcut/complexity theory. Boundary practices such as library acquisition and editorial selection are substantively interesting precisely because they can be censorial in some contexts and ordinary selection in others; categorical exemption would erase the central tension.
- **Impact**: Selection and gatekeeping are now explicitly non-binary boundary cases governed by multiple factors; prevention/erasure become exclusion subtypes, delay/containment become attenuation subtypes, contradiction is folded into saturation when it functions environmentally, delegitimation/inversion become strategies, and internalisation is sharpened to induced self-censorship. The outline now has seven sections and makes mechanism-first organisation, not breadth beyond bans, the central contribution.

- **Date**: 2026-08-21
- **Files**: `.gitignore`, `README.md`, `context-global.md`, `context-revision-log.md`, `references.bib`; removed historical compiler prompts, LaTeX/manuscript output, and publication-template files.
- **Change Summary**: Established a clean source/build boundary for the narrowed essay.
- **Rationale**: Generated LaTeX, section drafts, reviews, project-specific compiler prompts, and publication scaffolding were artefacts of the superseded workflow and created stale competing sources of truth. `compiled-prose` now owns generic prose compilation, while any future LaTeX/publication infrastructure should be introduced intentionally as separate work.
- **Impact**: The narrowed branch now tracks only conceptual source, project context, and `references.bib`; generated prose and publication outputs are ignored under build/output directories. Historical files remain recoverable on `draft-zero` and in git history.
