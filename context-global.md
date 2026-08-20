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

- what makes an intervention censorial;
- how to reason about selection, gatekeeping, and other boundary cases without categorical shortcuts;
- what primary operational families censorship uses;
- how those operations vary across contexts;
- and how censorship can persist through ordinary infrastructure even without complete prohibition.

The essay does not attempt a general theory of morality, social control, political legitimacy, cybernetics, deliberative democracy, propaganda, or persuasion.

---

## 2. Core Synthesis

Censorship is analysed as selective intervention in an epistemic environment that advances or stabilises an epistemic preference. The preference is a target ordering of claims, topics, representations, or speakers with respect to credibility, legitimacy, admissibility, or entitlement to consideration. The intervention acts through control surfaces such as availability, access, circulation, timing, visibility, ranking, legibility, standing, and memory. The framework does not categorically identify selection with censorship or exempt selection from censorship: editorial judgment, library acquisition, moderation, ranking, curation, peer review, and institutional gatekeeping are boundary practices whose censorial character depends on function and context. The principal contribution is a mechanism-first organisation that groups operations into exclusion, attenuation, transformation, saturation/flooding, and induced self-censorship; separates these from strategies and descriptive dimensions; and treats ambiguity as analytic evidence rather than a defect to be defined away.

---

## 3. Methodological Commitments

1. **Mechanism-first**  
   Identify what happens to epistemic participation before relying on actor labels or evaluating justification.

2. **Target/surface separation**  
   Keep the epistemic preference being stabilised distinct from the control surface through which intervention occurs.

3. **Structural, not actor-defined**  
   State, platform, institution, editor, librarian, employer, community, technical system, or diffuse norm can instantiate the same operation. No role is automatically censorial or automatically exempt.

4. **Descriptive before evaluative**  
   Classification does not itself determine whether an intervention is justified, lawful, proportionate, harmful, necessary, democratic, professionally appropriate, or effective.

5. **Boundary discipline without false absolutes**  
   Do not allow censorship to expand into all influence or selection, but do not define difficult selection and gatekeeping cases away by institutional title.

6. **Level discipline**  
   Keep operational families distinct from subtypes, strategies, responses, descriptive dimensions, actors, and justification regimes.

7. **Revisability of the framework**  
   Ambiguous and poorly fitting cases are evidence about the taxonomy and should remain visible.

---

## 4. Authoritative Artefacts

- **`outline.md`** — authoritative argument and compilation input.
- **`context-claims.md`** — compact canonical claims index.
- **`context-definitions.md`** — canonical definitions and boundary factors.
- **`context-taxonomy.md`** — operational families, strategies, and descriptive dimensions.
- **`context-glossary.md`** — one-line terminology reference.
- **`context-evidence-tiers.md`** — evidence expectations.
- **`latex/main.bib`** — available bibliography; citation details must be verified before publication.
- **`context-method-note.md`** — provenance and AI-assisted writing methodology.

`outline.md` wins in any conflict among project files.

---

## 5. Scope Guardrails

When refining or rendering the essay:

- Keep censorship as the object of analysis.
- Do not claim novelty merely from extending censorship beyond bans; prior scholarship already recognises indirect and self-censoring forms.
- Frame novelty around mechanism-first organisation, boundary analysis, and separation of conceptual levels.
- Do not make categorical claims that editorial selection, library acquisition, curation, moderation, ranking, or peer review are either always censorship or never censorship.
- Treat contest and control as ideal types that can coexist in one intervention.
- Preserve explicit boundary factors and context sensitivity.
- Keep the primary taxonomy compact: exclusion, attenuation, transformation, saturation/flooding, induced self-censorship.
- Treat delay, containment, demotion, prevention, erasure, modification, and substitution as useful subtypes rather than inflating the number of primary families.
- Treat delegitimation, inversion, contradiction, selection, and curation as strategies or practices whose censorial significance depends on the operation they produce.
- Use **descriptive dimensions**, not claims of mathematical orthogonality.
- Do not create dedicated sections on morality or control theory.
- Do not reintroduce the censorship/morality homology as a required premise.
- The shortcut idea may be a brief lens for persistence but must not become a general causal theory.
- Do not derive a general theory of legitimacy from participation or revisability.
- Do not moralise by default.
- Do not add standalone political or historical case studies.
- Boundary examples should stress-test the framework, not arrive with predetermined verdicts.
- Do not introduce new conceptual content during prose rendering. New ideas belong in `outline.md` first.

---

## 6. Central Boundary

The most important discipline in the essay is the distinction between **epistemic contest** and **epistemic control**, while recognising that real practices can combine both.

Epistemic contest changes belief or judgment principally through claims, reasons, evidence, criticism, rebuttal, interpretation, or comparison within an existing field of participation.

Epistemic control changes the practical conditions under which participation in that field can occur.

Selection sits across this boundary rather than on one side of it. Scarcity and institutional remit are relevant contextual facts, not automatic exemptions. Analysis should consider differential treatment, control of a consequential resource or channel, mode of disadvantage, relation to epistemic preference, substitutability, pattern over time, opacity, and power.

The framework should preserve ambiguity where these considerations pull in different directions.

---

## 7. Relationship to Earlier Work

The `draft-zero` branch developed useful but broader ideas around morality, conduct, control theory, legitimacy, and shortcut collision. Those ideas helped expose the structure of the censorship argument but opened the essay beyond a tractable scope.

The narrowed essay therefore:

- retains epistemic preference but separates it clearly from control surfaces;
- retains the mechanism-first taxonomy in a smaller hierarchical form;
- retains descriptive contextual dimensions without claiming strict orthogonality;
- retains infrastructural and induced self-censorship;
- retains the shortcut idea only as a bounded allusion about routinisation;
- makes selection/gatekeeping ambiguity a central feature rather than defining it away;
- demotes morality and control theory to optional brief allusions;
- removes the control triangle from the argumentative spine;
- and removes the need to establish a general theory of legitimacy or social conflict.

Nothing in this narrowing declares the broader ideas false; they are simply not required for this essay.

---

## 8. Compilation Strategy

Use `grantaj/compiled-prose` as the prose-rendering pipeline, with `outline.md` as the supplied authoritative outline.

The censorship repository owns the argument, terminology, bibliography, and publication artefacts. Generic drafting/smoothing/revision/review prompts belong in `compiled-prose`, not here.

If successful rendering requires censorship-specific instructions that are not conceptual content, treat that as a possible `compiled-prose` prompt deficiency rather than adding ad hoc compiler prompts to this repository.
