# Section Contract Template
## Scaffold for Outline Sections

Each section in `context-outline.md` should follow this contract to prevent drift and keep the outline as the primary argument.

### Required Fields

- **Purpose**: one sentence stating why the section exists.
- **Inputs**: specific concepts/claims it must use (from `context-claims.md`, taxonomy, axes).
- **Outputs**: what the reader should understand or be able to do after the section.
- **Dependencies**: earlier sections it assumes.
- **No-Go**: what the section must avoid (e.g., moral evaluation, policy prescriptions).
- **Coverage**: which canonical claims this section must cover; across the outline, all claims must be covered.
- **Causality**: avoid acausal reasoning; allow forward signaling/roadmapping, but keep causal claims explicit and warranted.

### Use Rule

If a section cannot satisfy this contract, it should be revised, moved, or removed. Rendering prose should be nearly deterministic once the contract is satisfied.
