---
name: olympus-rollout-auditor
description: Run the remaining Shipd/Olympus paid checks after the full-reference reduced-test Scope Gate and audit rollout batches. Use for token-budgeted check sequencing, fairness-bulb triage, rollout ZIP extraction, blind behavior clustering, replay, pass-rate analysis, difficulty-driver analysis, and false-positive reproduction.
---

# Olympus gate and rollout auditor — stages 15-15b

This is the paid-gate and rollout-analysis phase of `$olympus-workflow`. Keep the original stage numbering and firing order. Fill each prompt block's placeholders, apply its packaged laws, and complete its handoff before advancing.

Before any platform action or token spend, read [the shared laws](../olympus-workflow/references/shared-laws.md), [the evidence-first execution contract](../olympus-workflow/references/evidence-first-execution.md), [the platform contract](../olympus-workflow/references/platform-contract.md), [the state schema](../olympus-workflow/references/state-and-proof-schema.md), [the lessons ledger](../olympus-workflow/references/lessons-ledger.md), and [the hardness calibrators](../olympus-workflow/references/hardness-calibrators.md) completely. Verify the stage 5c Scope Gate PASS or explicit user-override record and the offline-validator handoff on the exact current hashes, then inspect the live panel for current requirements, costs, and result status. An override is not a gate result and does not itself authorize this LIVE phase.

## 15. Gate and upload (token discipline)

```
GOAL: spend the fewest tokens to get <PKG> approved.
LAW: shared Difficulty and rollout law. The live panel, not remembered numbers below, is authoritative for current gates and costs.

MODE: remain in `REVIEW` while preparing or auditing. Enter `LIVE` only for the one gate or panel action the user explicitly authorized, checkpoint its result immediately, then return to `REVIEW`.

BUDGET: copy the current panel costs into the case evidence, record the user-authorized ceiling with `case_state.py budget set`, and record every completed spend with its result ID through `case_state.py budget spend`. A remaining balance is not authorization for a different action. Do not spend when the result cannot change the next decision.

PRECONDITION: the dedicated `$olympus-scope-gate` phase already ran after complete reference construction and executable hardness proof but before test-only expansion, or the user explicitly waived it and the non-stale override record predates stage 6. This phase never retroactively owns that gate or upgrades an override into a PASS.

ORDER - use the current panel's exact sequence and costs:
1. Require `case_state.py validate --for-stage 15`; this enforces Scope Gate, current `local-validation`, `requirement-map`, `mutation-inventory`, and `grader-loop` proofs, the requirement-map file, zero blocking open items, and current hashes.
2. Re-gate the final scope once when the panel requires it, then freeze the candidate bytes for checks.
3. Run one clean required-check pass.
4. Run ONE Quick Check when available. Read the whole transcript before spending more.
5. If test and/or solution bytes changed after a rollout batch, inspect Re-eval before any fresh
   run. When title, description, repository/commit, and environment are unchanged, prefer an
   authorized Re-eval of the stale batch and bind its fresh verdicts to the current artifact set.
   Starting even one fresh run dismisses the offer, so make and record this decision first.
6. Continue in small increments, normally pairs, checkpointing after each increment. Buy the full required cohort only while fairness, environment, difficulty, and solvability evidence remain healthy.
7. Run false-positive review on every passing run, then Holistic and Auto Review only when all prerequisites are current.

EARLY DIFFICULTY STOP:
- One fast genuine pass does not measure the rate. If it exposes a compiler-guided, prompt-enumerated architecture, pause before the full batch and audit the hardness kill sheet; buy at most one confirming run when the live panel permits.
- Two independent fast genuine passes that converge on the same straightforward architecture are a rejection signal when the current assignment targets a materially harder band. Preserve them, record the literal 2/2 cohort, and pivot instead of buying the remaining runs or appending scope.
- Three of three genuine passes is a hard stop. Never call file count, LOC, tests, or messages proof of difficulty.

IRON RULES: any edit after checks start stales dependent checks, so fix everything in ONE pass. Read the Test Fairness lightbulb hints BEFORE running agents. After every increment, update structured `runs.json` and run `../olympus-workflow/scripts/rollout_metrics.py` with thresholds copied from the live panel; archive output with the artifact set. Confidence intervals and early-stop signals inform spend but never substitute for the panel's completed cohort.

A FAIRNESS COVERAGE BULB IS AN FP PREDICTION. The bulb says "this area is thin", the panel says "here is a broken implementation that survives" - one mechanism, because a thin area is exactly where one survives. The bulb is that finding arriving early and free; the panel fires only after a pass, and a finding there costs the pass.
So never triage a bulb as "is this a fair complaint". Ask WHAT BROKEN IMPLEMENTATION DOES THIS GAP LET THROUGH, and give every bulb a written verdict - a silent skip is not a verdict.
ACCEPT the moment you can name it. The naming IS the test: name it, then close it in the correct logical test scenario (block 16 step 5).
REJECT only with proof, and only for one of five:
- NOT CONSTRUCTIBLE - no input reaches the case, proven by execution, never by argument. (stoolap zero-estimate: the reference normalizes a missing stat to 1000; measured on three routes, asked seven times, same answer.)
- ALREADY COVERED - cite the test and the exact assertion. A different name for the same ground is not a gap.
- STALE - it quotes text the current files no longer contain.
- CONTRADICTS AN ACCEPTED FINDING - satisfy the one that breaks nothing, record the other invalid-by-contradiction.
- CLOSING IT WOULD BE UNFAIR - the only closing assertion pins an implementation choice the description does not mandate, trading a bulb for a 14a item-3 failure. Ground it in the prompt or a repo pointer instead.
NOT REASONS: "advisory only", "minor", "just a warning", "coverage weakness not unfairness", "does not threaten the submission", "false-negative so it cannot cost a solve". All used before, all wrong.
UNPROVEN IS AN ACCEPT. That third state collapsed into reject is how a bulb returns as a panel finding after a pass. Write the verdict and its evidence per bulb; that list is the handover.
```

## 15b. Read the agent rollout zip

```
GOAL: learn everything the batch <ZIP> can tell you, before changing one byte.
LAW: block 11b rule 4 - these solutions are kept forever and replayed after every edit.

1. EXTRACT to a permanent fixture dir: scratch/runs<N>/<AGENT>/. Never delete an old batch; old batches replay against new suites and that is how you prove a change did not break solvability.

2. BLIND CLASSIFICATION before fingerprinting. Read each verdict, transcript, and patch in a clean pass and summarize only public behaviors handled, omitted paths, and architectural decisions without preselected marker vocabulary. Cluster independently by behavior and design. Only then derive two or three code markers that efficiently reproduce those clusters. Markers are navigation evidence, never correctness criteria; alternate conformant structures must remain acceptable.

3. REPLAY ALL of them against the CURRENT suite - every batch, not just the newest. Print pass/fail
   per agent. Distinguish batches with an unchanged solver-visible-input fingerprint from batches
   whose title, description, repository/commit, or environment changed. The former are eligible
   for platform Re-eval after test/solution-only edits; the latter are historical replays and
   cannot receive fresh rollout verdicts without fresh solving.

4. DIFF THE PASSERS AGAINST THE FAILERS after the blind clustering. What public semantic decision does every passer handle that failers omit? Name the difficulty driver in one sentence and report any architecture diversity instead of forcing all solutions into the reference decomposition.

5. FOR EVERY FALSE POSITIVE, reproduce before you believe it. Apply that agent's exact patch to the exact artifact set, first confirm it passes the current suite, then run the judge's fair probe and confirm the candidate fails for the alleged reason while the reference passes. Replay preserved genuine solves. A finding you have not reproduced is a hypothesis; static suspicion and unrelated mutant breakage are not FP evidence. If the hosted adjudicator marks that exact run a high-confidence genuine pass, record that disposition unless a new fair exact-byte execution overturns it.

6. THE FIX IS AN ASSERTION, NOT A PROMPT CLAUSE. Fold the judge's probe into the correct logical test scenario (block 16 step 5). Verify three ways: reference passes, the exact false positive fails, and every known genuine solve still passes. If it kills a genuine solve without proving that solve violated a grounded requirement, it does not ship.

7. FOR ENVIRONMENT FLAGS, inspect whether any test assertion actually ran. A baseline JUnit made only of synthesized missing-output cases, paired with a build log showing a generated/object/link race and an unchanged successful retry, is a contestable environment failure. Preserve both logs and request an isolated or serialized rerun. Do not count the run as pass or fail until the platform adjudicates it.

OUTPUT: table of agent -> model/version -> verdict -> elapsed time -> patch metrics -> blind behavior/design cluster -> derived markers -> replay result; the one-sentence difficulty driver; per FP the reproduction and the test that closes it; current pass-rate/median/confidence calculation; budget spent/remaining; checkpoint paths and any stale or incomplete results. This table is part of the reviewer bundle. Record current proof `rollout-gates` only when the live panel's entire cohort, medians, cheating, environment, and false-positive requirements pass.
```
