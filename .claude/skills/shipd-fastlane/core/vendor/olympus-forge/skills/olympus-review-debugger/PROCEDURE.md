---
name: olympus-review-debugger
description: Repair a Shipd/Olympus package after false positives, failed checks, fairness findings, review feedback, or rejection. Use to classify the root cause, strengthen the correct existing test, batch fixes, rerun the full verification and grader loop, replay saved agents, and record a burned duplicate or candidate.
---

# Olympus review debugger — stage 16

This is the review and rejection repair phase of `$olympus-workflow`. Keep the original stage numbering and firing order. Fill each prompt block's placeholders, apply its packaged laws, and complete its handoff before advancing.

Before modifying a package, read [the shared laws](../olympus-workflow/references/shared-laws.md), [the evidence-first execution contract](../olympus-workflow/references/evidence-first-execution.md), [the platform contract](../olympus-workflow/references/platform-contract.md), [the state schema](../olympus-workflow/references/state-and-proof-schema.md), and [the lessons ledger](../olympus-workflow/references/lessons-ledger.md) completely. Copy the verdict verbatim into the case event log, hash the current artifacts, and use the dependency map to mark every dependent proof stale.

## 16. Fix loop (after FP / failed check / rejection)

```
GOAL: turn this feedback into one clean fix pass: <PASTE VERDICT VERBATIM>.

1. Run Phase 0 and reproduce the verdict with the smallest discriminating command. Name the root cause: environment/platform | harness/runner | test gap (promised, untested) | prompt gap (tested, unstated) | unfair pin (asserts an implementation choice) | golden bug | duplicate concept. For an environment contest, prove that no real assertion ran, identify synthesized JUnit entries, cite the exact configure/build/link race, and preserve an unchanged successful rerun. Ask only for exclusion or isolated rerun; never claim that this proves solution correctness.
2. For every unfair error assertion, classify the actual contract as exact representation | existing public category | rejection only. Remove any stronger enum/class/variant or payload match that comes only from the golden; preserve the strongest grounded error assertion plus the promised observable aftermath. Do not add prompt wording merely to legalize the golden's representation.
3. Separate blocking Fairness findings from advisory coverage suggestions. Classify each suggestion as PROMPT-STATED, REPO-DISCOVERABLE, REQUIRES CONTRACT EXPANSION, ALREADY COVERED, or STALE/CONTRADICTORY. Implement only fair, useful gaps; record the disposition of every suggestion.
4. For FPs: do not edit from the review prose alone. First reproduce the exact candidate passing the current suite, the exact reference passing a fair discriminator, and the candidate failing it for the reported reason; then run the red-team prompt (#13), add the exact candidate defect or faithful mutant to `mutation-inventory.json`, and bind the discriminator to stable requirement IDs. If the reference shares the failure or the hosted panel adjudicates the exact run genuine, record that result and do not harden from speculation. For harness, environment, permission, metadata, or platform failures, add a focused layer-specific reproduction instead of inventing a hidden behavioral assertion.
5. STRENGTHEN THE CORRECT LOGICAL TEST SCENARIO.
   Prefer extending the existing scenario that already reaches the behavior. Add a new test function when isolation, clarity, or an otherwise unreachable public path requires it; record why and let proof/test counts update normally. Test organization is not a quality gate. Every new assertion receives requirement grounding, reference-versus-mutant discrimination, fairness review, and current JUnit evidence.
6. Fix EVERYTHING in one batch - every edit after checks means re-paying them.
7. While editing, run targeted affected checks. Update `requirements.json`, `mutation-inventory.json`, structured grader dispositions, and proof dependencies in the same batch. When stable, rerun the full dependent local mirror (#11) once, re-fire 14a-14e on fixed dependent bytes, replay every saved agent batch (15b step 3), and close the mutation inventory. This is 11b rule 2, and this block is where it gets skipped - you are mid-rejection, the fix looks small, and "it was only one test" is how the next round starts.
8. Log the burn in `.olympus/lessons.md` as `date | case | mistake | cost | rule`; update `.olympus/repo-scouting-results.md` if a repo or concept died.

DUPLICATE VERDICT = the repo is burned repo-level. Record it, pivot to a fresh repo. Never argue, never reshape the same concept.
```
