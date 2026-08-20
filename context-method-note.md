# Methodology
## AI-Assisted Development and Compiled Prose

The conceptual framework, definitions, taxonomy, scope decisions, and final judgments in this project are authored by the human researcher. AI tools are used to support structure, consistency, stress-testing, citation organisation, and prose rendering.

The project treats `outline.md` as the primary authored argument. Prose is a compiled artefact: a rendering of explicit conceptual structure into publication-quality language. Different models or runs may realise the prose differently, but they should preserve the same claims, scope, terminology, order, and citation constraints.

Generic prose compilation is delegated to `grantaj/compiled-prose`. This repository should not maintain a parallel project-specific prompt stack unless a genuinely censorship-specific requirement cannot be represented as conceptual content in the outline. If the compiler needs extra generic instructions to render this outline faithfully, that should be treated as a possible `compiled-prose` issue rather than solved by adding ad hoc prompts here.

AI assistance is also used dialectically before compilation: to identify overreach, inconsistent definitions, category collapse, weak boundaries, unsupported causal claims, and citation gaps. Those findings are resolved in the outline and context files before prose generation wherever possible.

Citation standards and reference verification remain part of the research task. A citation key appearing in the outline indicates intended support; it does not by itself certify that the source establishes the exact claim or that the bibliographic record is correct.

The aim is methodological transparency and separation of concerns:

conceptual work -> authoritative outline -> prose compilation -> typesetting/publication.
