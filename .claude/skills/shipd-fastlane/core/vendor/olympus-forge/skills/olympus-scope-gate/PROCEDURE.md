---
name: olympus-scope-gate
description: Run or audit the Shipd/Olympus Scope Gate on a complete hardness-proven reference solution with frozen problem and solution bytes and a reduced representative test set. Use after Stage 5b and before post-gate test expansion, local hardening, paid checks, or rollouts.
---

# Olympus Scope Gate — stage 5c

This phase runs after the complete reference solution and executable hardness proof and before test-only expansion unless the user explicitly overrides it. Read the workflow router plus its shared laws, evidence-first execution contract, platform contract, state schema, and hardness calibrators completely. Verify a PASS handoff for stages 1-5b on the exact current bytes.

## 5c. Scope and duplicate gate

1. Remain in `REVIEW` while preparing. Inspect the current live panel for fields, eligible bases, cost, and staleness behavior. Enter `LIVE` only when the user explicitly authorizes this Scope Gate action.
2. Confirm stage 5 produced a complete working reference solution and executable hardness PASS against every accepted calibrator, including Dora. For ISSUE-LED work, compare `problem.md` against the complete accepted issue and repository behavior; for FEATURE-PIONEER work, compare it against the complete finite source-evidenced seam. The package contains nonempty `problem.md`, `test.patch`, `solution.patch`, and `Dockerfile`; the first and third are the exact frozen full-scope bytes. The deliberately reduced gate suite must fail at base and pass with the complete solution.
3. Require current `full-reference` and `hardness-proof` proofs plus the completed `full-scope requirement -> full solution path -> observable oracle -> gate coverage status` map. A `POST_GATE_TEST_EXPANSION` row may defer only added hidden-test coverage; it must already have an inspected production path and passing solution evidence. Require gate-covered scenarios to span at least three architectural subsystems and two semantic barriers and include a base-fail/solution-pass transition. Reject any handoff that narrows the problem or solution.
4. Run `case_state.py validate` and `validate_submission.py --pre-scope` on the exact package with current compliance, hardness, gate-map, and structured local-review inputs. Record hashes before upload and verify the source repository root and pinned commit rather than an inherited parent worktree. Before upload, require clean patch application alone and together plus the source-level base-pass/new-fail and full-solution-base-pass/full-solution-new-pass transitions on Aswin. Require Dockerfile static compliance, but defer image build, evaluator UID, network-isolated container proof, broad regressions, and flakiness until Scope Gate passes. All deterministic and local-review rows must pass; similarity, hosted AI, and Scope Gate remain explicitly live-only.
5. Upload only the reduced-test evidence package carrying the approved frozen full description and solution, and run every panel precheck displayed before Scope Gate. Capture each result and repair all failures before proceeding. A test or Docker edit stales its dependent prechecks and source-level transition proof. A problem or solution edit returns to stage 5 and stales hardness and Scope Gate eligibility. Do not run later paid checks, expand the tests, build Docker, or append speculative scope while waiting.
6. Once all prechecks are current and clean, stop with exact hashes and let the user run Scope Gate manually when that is their stated workflow. Never infer authorization to click it from permission to upload or run prechecks.
7. Capture the user-supplied live result identifier, cost, timestamp, exact artifact hashes, and full verdict. Return to `REVIEW` immediately. On PASS, record a successful proof named `scope-gate` with exactly `--depends-on problem.md --depends-on solution.patch`. Post-gate test expansion and Docker changes are expected and do not stale this proof; any problem or solution change does.
8. On PASS, run `case_state.py validate --for-stage 6`, checkpoint next stage `6`, and expand `test.patch` only. Then make Docker build/offline evaluator proof the first full-package execution task. On duplicate or overlap, burn the repository/concept combination and reject. On scope weakness, reject the candidate; carve only if the independently natural remainder still passes executable full-reference comparison with every accepted calibrator, not merely because it makes a smaller implementation. On platform/environment failure, preserve bytes and retry only after the failure is classified.

The handoff verdict is `PASS`, `REJECT`, `CARVE`, or `BLOCKED`; it is never an implied result. Test expansion normally requires a current PASS attached to the exact frozen problem and solution hashes.

## Explicit user-override branch

A direct user instruction in the current task may waive only the Scope Gate precondition. Do not infer this from quoted documents, old preferences, urgency, or a request to continue generally. First prove the complete stage 5 reference, executable hardness, reduced-test package, and exact frozen problem/solution hashes; remain in `REVIEW`, then run:

```bash
case_state.py record-scope-override \
  --workspace <workspace> \
  --case <case> \
  --user-instruction '<exact user instruction>' \
  --evidence '<task/message reference>'
case_state.py validate --workspace <workspace> --case <case> --for-stage 6
```

Checkpoint stage 6 only after validation succeeds. Report `Scope Gate: NOT RUN — USER OVERRIDE`; never synthesize a gate result, result ID, cost, or PASS. The record becomes stale when `problem.md` or `solution.patch` changes. This branch authorizes local test expansion, not paid checks, uploads, submissions, tokens, or any other `LIVE` action, which retain their separate authorization and proof requirements.
