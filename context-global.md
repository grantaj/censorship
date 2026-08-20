# Project Context
## Structural Account of Censorship

### Status

Canonical project context for the narrowed censorship essay.

`outline.md` is the authoritative source for argument structure and is intended to be rendered using `grantaj/compiled-prose`.

The older `outline-working.md`, `context-outline.md`, and `compile-prompt-*.md` files record the earlier project-specific compilation approach. They are retained for provenance on `draft-zero` and in git history, but they are **not authoritative inputs** for the narrowed essay.

---

## 1. Project Orientation

This project develops a structural, descriptive-first framework for analysing censorship.

The essay asks:

- what makes an intervention censorial,
- how censorial mechanisms operate,
- how structurally similar operations vary across contexts,
- and why censorship can persist in ordinary and formally open epistemic environments.

The essay does not attempt a general theory of morality, social control, political legitimacy, cybernetics, deliberative democracy, or social conflict.

---

## 2. Core Synthesis

Censorship is analysed as the enforcement of epistemic preference through intervention in the practical conditions under which expressions, claims, records, or speakers can appear, circulate, persist, remain visible, or count as admissible. This definition deliberately reaches beyond explicit prohibition while preserving a boundary with ordinary disagreement: persuasion, criticism, rebuttal, and counter-speech do not become censorship merely because they influence belief. They become relevant to censorship when they function as control of practical participation, standing, availability, or hearability rather than as contest over the merits of a claim. The framework classifies censorship through composable operational modes and keeps those modes separate from orthogonal axes such as scale, power, participation, persistence, visibility, justification, and domain. This makes it possible to analyse explicit and infrastructural censorship using the same vocabulary without deciding in advance whether any particular intervention is justified.

---

## 3. Methodological Commitments

1. **Mechanism-first**  
   Classify what the intervention does before classifying the actor or judging the justification.

2. **Structural, not actor-centric**  
   A mechanism can be state, institutional, economic, technical, communal, or distributed. Intentionality by a single censor is not required.

3. **Descriptive before evaluative**  
   Classification does not itself determine whether censorship is justified, lawful, proportionate, harmful, necessary, democratic, or effective.

4. **Boundary discipline**  
   Do not allow the concept of censorship to expand into all influence, criticism, disagreement, persuasion, or curation.

5. **Separation of concerns**  
   Keep operational modes distinct from axes, actors, domains, justification regimes, and moral evaluation.

6. **Revisability of the framework**  
   Borderline cases and poor fits are evidence about the taxonomy and should remain visible.

---

## 4. Authoritative Artefacts

- **`outline.md`** — authoritative argument and compilation input.
- **`context-claims.md`** — compact canonical claims index.
- **`context-definitions.md`** — canonical definitions and boundary conditions.
- **`context-taxonomy.md`** — operational modes and orthogonal axes.
- **`context-glossary.md`** — one-line terminology reference.
- **`context-evidence-tiers.md`** — evidence expectations.
- **`latex/main.bib`** — available bibliography; citation details must be verified before publication.
- **`context-method-note.md`** — provenance and AI-assisted writing methodology.

`outline.md` wins in any conflict among project files.

---

## 5. Scope Guardrails

When refining or rendering the essay:

- Keep censorship as the object of analysis.
- Do not create dedicated sections on morality or control theory.
- Do not reintroduce the censorship/morality homology as a required premise.
- Do not use positive/negative-feedback terminology to characterise morality and censorship.
- The shortcut idea may explain persistence, but must not become a general systems theory.
- Do not derive a general theory of legitimacy from participation or revisability.
- Participation, persistence/revisability, power, visibility, and justification remain descriptive axes.
- Do not moralise by default.
- Do not reduce censorship to legal bans or speech alone.
- Do not use actor categories as the primary taxonomy.
- Do not add standalone political or historical case studies.
- Examples should identify modes and axes, then stop.
- Do not introduce new conceptual content during prose rendering. New ideas belong in `outline.md` first.

---

## 6. Central Boundary

The most important discipline in the narrowed essay is the distinction between **epistemic contest** and **epistemic control**.

Ordinary disagreement occurs within an epistemic environment: claims are answered, criticised, defended, rejected, or revised on their merits.

Censorial intervention changes the practical conditions of participation in that environment: availability, access, circulation, visibility, persistence, admissibility, standing, hearability, attention, or memory.

This distinction is functional and may be context-sensitive. Ambiguity should be preserved where warranted, particularly for contradiction, delegitimation, and inversion.

---

## 7. Relationship to Earlier Work

The `draft-zero` branch developed useful but broader ideas around morality, conduct, control theory, legitimacy, and shortcut collision. Those ideas helped expose the structure of the censorship argument but opened the essay beyond a tractable scope.

The narrowed essay therefore:

- retains epistemic preference,
- retains censorship-as-shortcut as a limited explanatory lens,
- retains the operational taxonomy,
- retains the kinds-versus-axes distinction,
- retains infrastructural and internalised forms,
- demotes morality and control theory to optional brief allusions,
- removes the control triangle from the argumentative spine,
- and removes the need to establish a general theory of legitimacy or social conflict.

Nothing in this narrowing declares the broader ideas false; they are simply not required for this essay.

---

## 8. Compilation Strategy

Use `grantaj/compiled-prose` as the prose-rendering pipeline, with `outline.md` as the supplied authoritative outline.

The censorship repository owns the argument, terminology, bibliography, and publication artefacts. Generic drafting/smoothing/revision/review prompts belong in `compiled-prose`, not here.

If successful rendering requires censorship-specific instructions that are not conceptual content, treat that as a possible `compiled-prose` prompt deficiency rather than adding ad hoc compiler prompts to this repository.
