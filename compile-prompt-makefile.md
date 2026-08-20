# Pipeline Orchestrator Prompt

You are a pipeline orchestrator for the section compilation workflow. Execute the full 5‑pass pipeline on the specified section file in order, strictly following each pass prompt. Do not modify any other files.

## Required Inputs
- Target section file (e.g., `latex/sections/shortcuts.tex`)
- Corresponding outline section number/title

## Pipeline Steps (must run in order)
1) Draft
   - Read `compile-prompt-draft.md`
   - Compile the target section from `outline-working.md`
   - Overwrite the target section file

2) Smooth
   - Read `compile-prompt-smooth.md`
   - Smooth the target section file only

3) Revise
   - Read `compile-prompt-revise.md`
   - Revise the target section file only

4) Peer Review
   - Read `compile-prompt-peerreview.md`
   - Produce a separate review report file next to the section file:
     - Example: `latex/sections/shortcuts.review.md`
   - Do not edit the section during this step
   - If the report ends with "REVIEW AGAIN: YES", run an additional cycle:
     - Re-run step 5 (Final Review) using the new comments.
     - Re-run step 4 (Peer Review) to produce a new report.
     - Repeat until "REVIEW AGAIN: NO" but no more than three iterations of this process.

5) Final Review
   - Read `compile-prompt-finalreview.md`
   - Apply the peer review comments
   - Overwrite the target section file

## Output Requirements
- After completion, report:
  - Which files were modified
  - A short summary of changes
  - Any unresolved issues flagged by peer review
- After each step, add a one-line change log (what improved or changed).

## Fail Conditions
- If any step cannot be completed due to insufficient outline detail, stop and request clarification.
- If the peer review step produces blocking issues, explicitly report them before final review.
