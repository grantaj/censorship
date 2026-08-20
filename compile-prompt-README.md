# Multi-Pass Compilation Workflow

This project uses a five-pass approach to render outline sections into high-quality LaTeX prose.

## 1) Draft Pass (strict fidelity)
Use: `compile-prompt-draft.md`

Goal: produce a faithful draft that follows the outline exactly and includes citations tied to claims.

Example command:
"Read compile-prompt-draft.md and compile section latex/sections/shortcuts.tex (Section 5) leaving other sections alone."

## 2) Smooth Pass (readability)
Use: `compile-prompt-smooth.md`

Goal: improve flow and cohesion without introducing new concepts or examples. Citations may be redistributed across adjacent sentences to reduce monotony.

Example command:
"Read compile-prompt-smooth.md and smooth section latex/sections/shortcuts.tex leaving other sections alone."

## 3) Revise Pass (coherence)
Use: `compile-prompt-revise.md`

Goal: strengthen coherence and integrate paragraphs so the section reads smoothly before peer review.

Example command:
"Read compile-prompt-revise.md and revise section latex/sections/shortcuts.tex leaving other sections alone."

## 4) Peer Review Pass (comments only)
Use: `compile-prompt-peerreview.md`

Goal: produce reviewer comments only; no edits to the section.

Example command:
"Read compile-prompt-peerreview.md and peer review section latex/sections/shortcuts.tex leaving other sections alone."

## 5) Final Review Pass (apply comments)
Use: `compile-prompt-finalreview.md`

Goal: apply peer review comments and produce a final, publication-ready section.

Example command:
"Read compile-prompt-finalreview.md and finalize section latex/sections/shortcuts.tex leaving other sections alone."

## Notes
- Each pass should only edit the target section file, except the peer review pass which outputs comments only.
- If the outline is insufficient during the draft pass, request clarification rather than guessing.
- Citations should always remain tied to the claims they support.
