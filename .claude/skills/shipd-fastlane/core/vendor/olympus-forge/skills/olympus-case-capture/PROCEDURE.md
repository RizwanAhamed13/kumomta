---
name: olympus-case-capture
description: Freeze and preserve an approved Shipd/Olympus challenge package. Use after Auto Review approval to snapshot exact artifact hashes, preserve approval evidence, record pass rate and difficulty findings, wait for manager confirmation without artifact drift, and start scouting the next distinct task.
---

# Olympus case capture — stage 17

This is the post-approval freeze and evidence-capture phase of `$olympus-workflow`. Keep the original stage numbering and firing order. Fill each prompt block's placeholders, apply its packaged laws, and complete its handoff before advancing.

Before freezing, read [the shared laws](../olympus-workflow/references/shared-laws.md), [the platform contract](../olympus-workflow/references/platform-contract.md), [the state schema](../olympus-workflow/references/state-and-proof-schema.md), and [the lessons ledger](../olympus-workflow/references/lessons-ledger.md) completely. Repeat the duplicate-work audit against the final architecture. Confirm approval belongs to the exact current hashes, all currently required platform runs and successful-run medians completed, every passing run survived false-positive review, and the case's `open-items.json` contains no blocking findings.

## 17. After approval (the freeze)

```
GOAL: keep an approved package approved.

Auto Review approving is NOT the end. Manager confirmation follows, on a stated date (stoolap: approved 2026-08-03, confirmation due 2026-08-08).

FREEZE ALL FOUR ARTIFACTS. Zero edits - not a typo, not a comment, not whitespace. There is no such thing as a safe one-word change: any edit stales every check already cleared, and the approval was granted against exact bytes. A fix you think is free costs the entire check pipeline plus a fresh review.

WHAT TO DO INSTEAD, while the window runs:
- Snapshot the approved bytes with hashes so you can prove nothing moved.
- Record current proofs named `duplicate-final` and `auto-review` on the exact artifact set, then require `case_state.py validate --for-stage 17` before freezing.
- Write the record: pass rate, gate scores, the difficulty driver the reviewer named, what the rubric deducted and why. That is your evidence for the next task.
- Start scouting the NEXT repo (block 1). Different subsystem, different theme - no repeat concept from any prior task by this author.

IF THE MANAGER REJECTS: block 16, unchanged. Name the root cause, fix in ONE batch, rerun everything. Do not argue the verdict.
```
