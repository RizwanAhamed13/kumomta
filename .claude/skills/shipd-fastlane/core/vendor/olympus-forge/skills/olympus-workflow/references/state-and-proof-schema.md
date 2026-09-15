# Case state and proof schema

Read this reference before initializing, resuming, handing off, repairing, or freezing a case. Use `scripts/case_state.py`; do not maintain competing handwritten current-state summaries.

## Canonical layout

```text
.olympus/
  active-case
  lessons.md
  repo-scouting-results.md
  portfolio.md
  cases/<case>/
    case.json
    state.md
    open-items.json
    events.jsonl
    requirements.json
    alignment-audit.json
    independent-inventory.json
    fp-proof.json
    transition-proof.json
    mutation-inventory.json
    hardness-proof.json
    scope-gate-map.json
    scope-gate-prechecks.json
    grader-results/<prompt-version>/<grader>.json
    artifacts/
      problem.md
      test.patch
      solution.patch
      Dockerfile
    evidence/<artifact-set-id>/
    rollouts/<batch>/<agent>/
```

`case.json` is the current machine-readable state. `events.jsonl` is append-only history. `state.md` is regenerated from `case.json`. `open-items.json` contains unresolved findings for this case only. Use `portfolio.md` for active, rejected, occupied, or archived case summaries; never mix those records into open items.

Legacy packages outside this layout remain evidence. Select one canonical artifact directory before advancing and record any legacy paths; do not silently copy a newer-looking file over the canonical one.

## Required state

Every checkpoint contains:

- schema version, case identifier, operating mode, stage, verdict, and next legal stage;
- repository URL, exact commit, expected repository root, and cleanliness result;
- canonical artifact directory and SHA-256 for all present required artifacts;
- artifact-set identifier derived from the four hashes;
- completed proofs with command, exit, decisive output/JUnit path, timestamp, environment, and artifact-set identifier;
- stale proofs with reason and exact refresh action;
- requirement-map path, rollout/result identifiers, open-item count, and last blocker;
- authorized token budget, itemized spend, result identifiers, and remaining balance;
- live-panel snapshot identifier when any platform claim is made.

Allowed modes are `REVIEW` and `LIVE`. Allowed verdicts are `PASS`, `REJECT`, `CARVE`, `BLOCKED`, and `IN_PROGRESS`. `BLOCKED` follows the host agent's blocked-status rules; ordinary incomplete work remains `IN_PROGRESS`.

## Repository-root guard

Before accepting cleanliness or commit evidence, run `git rev-parse --show-toplevel` and require the resolved root to equal the recorded source clone. Require `HEAD` to equal the pinned commit before patch application. A package directory that merely inherits a parent worktree is not repository evidence.

## Artifact-set and staleness model

Hash the canonical four artifacts in fixed name order. Results belong to that artifact set, not merely to a case name.

Minimum dependency map:

| Changed artifact | Proofs made stale |
|---|---|
| `problem.md` | description, alignment/fairness grounding, scope/originality where wording matters, graders, rollouts that saw the old prompt, Holistic, Auto Review |
| `test.patch` | patch application, discovery, four-state matrix, flakiness, offline run, mutation/FP evidence, fairness/quality graders, saved-agent replay, Verify Tests/Solution, rollouts, downstream review |
| `solution.patch` | patch application, solved matrix, regression, format/lint/static analysis, mutation reference checks, solution quality, Verify Solution, saved-agent comparisons, downstream review |
| `Dockerfile` | image build, evaluator-user permissions, environment/offline matrix, environment quality, Docker-dependent verification and downstream results |

Some proofs depend on multiple artifacts; invalidate the union. Do not invalidate independent non-Docker source proofs after a Docker-only edit, and do not preserve a dependent proof because an edit appears small.

## Phase transition guards

- Stage 5 requires candidate PASS and exact commit. Its handoff requires a complete working reference solution, focused executable evidence, and an every-accepted-calibrator hardness comparison; paper architecture and estimates are not sufficient.
- Stage 5b requires current successful proofs named `full-reference` and `hardness-proof`, each depending only on the frozen full `problem.md` and complete `solution.patch`; a hash-locked complete `hardness-proof.json`; and a four-artifact gate package whose reduced `test.patch` does not narrow production scope.
- Stage 5c requires a complete `scope-gate-map.json`, a current successful `scope-gate-prechecks` proof, current full-reference and hardness proofs, clean four-artifact hashes, base-new failure, and full-solution-new success. Rows may defer only post-gate test expansion; every requirement already has an inspected full solution path and oracle.
- Stage 6 requires either Scope Gate PASS bound to the exact frozen `problem.md` and `solution.patch`, or an explicit current-user waiver recorded as `scope-gate-override` against those bytes. Record a PASS as `scope-gate`; record a waiver only through `case_state.py record-scope-override`, including the exact instruction and evidence reference. Both proofs depend on `problem.md` and `solution.patch`, so expected post-gate changes to tests or Dockerfile do not erase authorization. A problem or solution edit makes the proof stale, returns the case to stage 5, and requires executable hardness proof plus a new gate. A waiver is never a PASS and supplies no duplicate, scope, readiness, platform, or paid-action evidence.
- Stage 11 requires all four final artifacts and clean application alone and together.
- Stage 15 requires current successful proofs named `local-validation`, `requirement-map`, `mutation-inventory`, and `grader-loop`, an existing requirement-map file, and zero unresolved blocking items.
- Stage 17 additionally requires current proofs named `rollout-gates`, `duplicate-final`, and `auto-review`, completed current-panel criteria, zero open items, and exact approved hashes.

Reject illegal transitions. A generated status may say `IN_PROGRESS`; it may not say `ready` unless every guard for the requested action passes.

## Requirement and evidence identifiers

Maintain stable internal requirement IDs outside the solver-facing prose. In `requirements.json`, map each ID to public path/input class, observable oracle, prompt/repository grounding, before/after evidence, and mutants or agent patches it rejects. Include a reverse assertion-to-requirement map. Test names may change without losing requirement identity. Record proof `requirement-map` only after both directions have no orphaned entry.

Maintain `alignment-audit.json` schema version 3 beside the requirement ledger. Give every requirement a repository-derived role row with input classes, assertion IDs, solution paths, `execution_paths`, evidence, an `oracle_contract`, dimensions, and complete Cartesian cells. Each execution path records a public `entry`, production `decision`, public `observable`, and repository-graph evidence connecting them; changed-file lists alone are insufficient. The oracle contract records `kind`, grounding, layout independence, presentation constraints, and conformant alternatives. A presentation constraint needs direct prompt/repository grounding; hidden vocabulary, paragraph colocation, sliding windows, and fixed layout are otherwise invalid. Dimensions must exactly match the blind inventory; every combination is covered or explicitly out of scope with grounding. When the solution changes bytecode/opcode/instruction/IR paths, include a complete operation inventory spanning producer, representation, encoding, decoding, verification, runtime consumers, post-patch materialization, and validation-to-consumption invariant evidence. Materialization records the runner command that rebuilds ordinary and self-hosted/generated consumers after patch application. Any `open` role, missing cell, missing stage, stale executable, or incomplete invariant is a blocking finding; a 100% requirement-level triad score cannot override it.

Before author-ledger reconciliation, create `independent-inventory.json` schema version 2 in a fresh blind context using only the exact problem, pinned repository, and natural contract. Hash-lock the problem, record the pinned commit and excluded artifacts, and list independently derived roles, input classes, execution paths, low-level operation IDs, and contract-relevant dimensions with their finite values and grounding. A missing independent row, dimension, value, or reconciliation difference blocks alignment.

Maintain `fp-proof.json` schema version 1 beside the mutation inventory. Hash-lock the problem/test/solution triad; cap each repair batch at three risk-ranked probes; and classify rows as `hypothesis`, `advisory`, `disproven`, `proven_gap`, `killed`, or `invalid`. Only `proven_gap` blocks as an open FP. `killed` requires prompt grounding and execution evidence that the reference passed and mutant failed. Hypotheses never authorize new tests.

Maintain `transition-proof.json` schema version 1 from exact per-test JUnit. Hash-lock `test.patch`, `solution.patch`, and `Dockerfile`; reconcile authored counts against parsed XML; require stable testcase identities across states, all base cases green before and after, zero passing new cases before the solution, and all new cases green after it. This ledger is execution evidence, not author assertion: missing XML, count drift, or state mismatch blocks alignment.

## Mutation inventory

Build `mutation-inventory.json` from requirements and changed execution paths before declaring the suite hardened. Each entry contains a stable ID, requirement IDs, mutation class, exact change, plausibility, affected public path/input class, current-suite result, reference-discriminator result, mutant-discriminator result, status, and evidence paths. Status is one of `killed`, `survived`, `invalid`, or `deferred`; a deferred entry is an open item. Include omission, boundary, boolean-cell, routing/shape, persistence/order, conversion/serialization, error-contract, hardcoding, and agent-derived classes when applicable. Record proof `mutation-inventory` only when every in-domain entry is killed or proven invalid and every incorporated discriminator still kills its source mutant.

## Grader result records

Store each grader result as JSON with grader/prompt version, model/version when available, artifact-set identifier, started/completed timestamps, verdict, structured findings, cited file/lines, raw-output path, and execution evidence. A finding has stable ID, severity, category, requirement/assertion IDs, status, and disposition. Never merge results from different artifact sets into one clean verdict. Record proof `grader-loop` only after every required grader reruns on current dependent bytes and all blockers are closed.

## Spend ledger

Use `case_state.py budget set` to record the user-authorized token ceiling and live-panel snapshot before spending. Use `case_state.py budget spend` after each action with the displayed cost and result ID. Authorization for a budget does not authorize every live action; retain the separate action-specific authorization rule. Stop when the next action would exceed the ledger or when its expected information cannot change the decision.

Store large raw logs under the artifact-set evidence directory and maintain a manifest containing each relative path, SHA-256, producer command/result ID, and timestamp. Put only paths plus decisive excerpts in state. Preserve agent patches and transcripts permanently with hashes. Never embed secrets, cookies, tokens, OTPs, or browser session material.
