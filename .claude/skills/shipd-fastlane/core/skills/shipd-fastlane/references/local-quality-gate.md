# Local counterparts before every upload

The author-side validation loop is **capture → execute → review → repair → revalidate → audit evidence → upload if authorized**. Run candidate work on `shipd-local`; the Mac orchestrates and inspects returned lightweight evidence; plugin validation runs on the server. Never use a paid Shipd check to discover defects that an applicable local counterpart can catch.

## What is replicated

[quality-checks.json](../../../assets/quality-checks.json) defines 20 local counterparts, their mandatory rubric items, dependencies, evidence roles and limits. It is a versioned historical starting point. It does not contain Shipd's private implementation, prompts, similarity corpus or solver population. No live case panel was captured when this generic catalog was authored. The later [current general documentation receipt](current-general-contract.md) supplies dated artifact and process rules; it does not supply all case-specific fields or private grader behavior.

| Shipd check family | Required author-side counterpart |
|---|---|
| Eligibility, similarity/originality | Current denylist and repository rules; exact commit and licenses; open/closed/merged PR, issue, inverse-path and local case overlap searches |
| VCS+, artifact validation, Scope | Map the actual panel behavior; static artifact rules and isolated patch application; full reference, executable architectural hardness and frozen reduced-test map |
| Verify Tests / Verify Solution | Exact test discovery and per-case JUnit; every new test fails baseline for the intended reason and passes reference; base tests pass in both states; regression and failure-path diagnostics |
| Test Quality / Task Quality | Independent public-input inventory, input × role matrix, whole interactions, real assertions, natural depth and conformant-alternative acceptance |
| Test Fairness | Every assertion classified with prompt sentence or pinned repository file:line; zero unsupported assertions; public error-contract level |
| Solution Quality | Maintainer-style review, relevant lint, generated-code consistency, no shortcuts or unrelated changes, no tests hidden in the solution patch |
| Description Quality | Sentence-level necessity review followed by the fairness-dependency pass; resolve request_changes and HIGH findings |
| Docker / Environment / Verify Flakiness | Clean image/runtime rehearsal, evaluator UID/login environment, offline execution after dependency hydration, patch-triggered rebuilds, four-state repetitions and timing evidence |
| Quick Check | Rehearse its captured live behavior; aggregate matching local executions and run Forge's complete evidence/state validators |
| False Positive | Requirement-derived mutation inventory; executable plausible shortcuts; discriminators must fail the broken variant and pass reference plus conformant implementations |
| Agent pass rate / Difficulty | Replay saved genuine solves and authorized calibration; record sample, provenance and limitations; actual hosted pass rate still requires rollouts |
| Holistic / Auto Review | Separate cross-artifact and final-readiness reviews of the current bundle; close every blocker; list hosted checks still unproven |
| Rollout audit / final readiness | Once real rollouts exist, audit the complete cohort, replay all passers, check cheating/FP findings and reconcile actual hosted receipts and staleness |

Read the bundled Forge offline-validator's (`vendor/olympus-forge/skills/olympus-offline-validator/PROCEDURE.md`) **14a–14e full prompts**, not just this summary, when conducting quality, fairness, FP, description and solution reviews. Read the corresponding platform and local-validation references for deterministic checks. The currently selected live panel overrides historical names, thresholds and stage requirements. Interpret VCS+ and Quick Check from their actual displayed contract rather than guessing from their labels.

Under the workspace's one-agent rule, perform separate sequential read-only rubric passes, save each raw report, and explicitly record that their context is correlated. Do not claim independent judges or launch extra agents without authorization. Mutations and all experiments use isolated worktrees on the designated builder. One report may support multiple checks, but each check needs its own completed rubric and applicable evidence. Reuse an identical execution log; do not run the same command again just to populate another row.

## Three upload boundaries

- **scope — 12 counterparts:** complete reference and full-scope/hardness proof, frozen problem/solution, representative reduced tests, source-level four-state proof and reviews of the actual slice. Explicitly list deferred full-suite cells. The uploaded reduced test patch must match the frozen Scope patch. Full Docker/repetition/calibration work remains post-Scope.
- **full — 18 counterparts:** after the real Scope gate (or the explicitly recorded Forge exception), expand the full test suite; require full declared and executed coverage, offline image matrix, flakiness, mutations, genuine-solvability evidence and all quality reviews. No reduced-suite PASS can satisfy a full receipt.
- **final — 20 counterparts:** add complete real rollout audit and current hosted-receipt reconciliation before final review/submission. These require evidence that cannot exist before initial upload. A local substitute cannot invent it.

The local checker never advances Forge state or grants permission to spend platform tokens. Forge's stage validation and any required hosted gate remain mandatory. If the current panel requires something earlier than this catalog supports, block, resolve the mapping and update the counterpart; do not silently defer it.

## Prepare the case bundle

1. Read the entire relevant live case panel using structured text. Record exact check labels, fields, stage order, gate costs, evaluator behavior, required repetitions and cohort criteria in a case-specific copy of [panel-contract.example.json](../../../assets/panel-contract.example.json). Retain the complete raw text as a hashed file. An unavailable setting stays explicitly unavailable with a reason; use the active Forge fallback only where it permits one. Every displayed check needs `label`, `local_ids`, `stages` and a semantic `rationale`. A new behavior needs a real local adapter/rubric, not a convenient unrelated mapping.
2. Resolve the case, exact commit and builder identity; freeze the canonical four artifacts and selection commands. Record tool/adapter versions, runtime flags, features, seeds, timeouts, cache policy and grading prompt/model versions. Create the input snapshot with `fastlane.py snapshot` as documented in [execution.md](execution.md).
3. Initialize the current-stage bundle. The command creates **PENDING** entries only; it refuses to overwrite existing evidence. Keep the panel capture and all attachment paths relative to the bundle directory.

```text
python3 <plugin-root>/scripts/quality_gate.py init --stage full --inputs <current-inputs.json> --panel <panel-contract.json> --output <case-evidence>/local-quality.json
```

4. Use the Forge case adapter and validators to execute every required deterministic item on `shipd-local`, then conduct the full rubric reviews. Preserve commands, expected/actual exits, per-case test inventory/JUnit, timing data, coverage reports and mutation/solver patches. Run `contract_check.py --stage full` for the full suite (`scope` only for the reduced slice), but also reconcile actual discovered/executed tests and inspect assertions. Declared coverage is not an execution result. Use Forge `validate_submission.py`, `validate_evidence.py` and `case_state.py validate --for-stage 15` at their applicable stages; this checker supplements them.
5. Resolve findings in one coherent batch. Re-run every affected executable check and read every changed assertion in the fairness/quality passes. Then run the mandatory final matrix on the final bytes. A review of the previous revision cannot approve a fix it has not read. Never promote a pending item to PASS based on expectation, a matching hash or an aggregate shell exit alone.

If numeric line/branch coverage cannot be collected with the supported toolchain, retain the reason and the executed requirement/cell denominators, discovery counts, mandatory integration paths and discriminating probes. Never fill in a fabricated percentage. A required behavior with no executable witness remains a blocker.

## Evidence record format

`init` supplies every required check, rubric item and dependency fingerprint. Complete each record only from the real run/review:

- `status`: PASS only after every rubric item passes. PENDING, SKIP, WARN and FAIL block. A non-applicable subtopic needs a concrete reason in the rubric report, not a skipped whole counterpart.
- `started_at`, `completed_at`: actual timezone-aware timestamps. Preserve original run timestamps when reusing evidence.
- `inputs`, `catalog_sha256`, `contract_sha256`: bind the run to its actual dependency bytes and rules. Do not refresh these hashes on an old result just to make it current.
- `evidence`: nonempty files with `path`, `sha256`, and one of the required roles printed by `init`. Keep raw reports, logs and machine outputs; never attach an empty placeholder. Each rubric item needs a reason and an `evidence` list referencing these paths.
- `commands`: stable selected `id`, actual `command`, integer `exit_code`, integer `expected_exit_code`, and attached log `evidence`, with `phase_id` and timezone-aware `started_at`/`completed_at`. IDs, exact command text and expected exits must match the hashed schema-1 command inventory for this check/stage, with no missing, extra or duplicate outcomes. Commands must share the observed preflight phase, start after that preflight, and remain within the receipt interval. A baseline-failure command can legitimately expect 1; its JUnit and report must prove the intended per-case failure. Test-harness compilation or setup failure is not that proof; an executed compiler diagnostic test may use a candidate-language compile rejection as its behavioral witness after exact diagnostic triage.
- `execution`: `phase_id` matching the observed preflight, `ssh_alias: shipd-local`, observed `host`, `ip: 100.105.254.33`, remote `workdir`, exact `commit`, plus `identity_evidence`, `transfer_hash_evidence`, `preflight_evidence` and `selection_evidence` paths and the observed `preflight` object described in [execution.md](execution.md). Match the observed environment snapshot. Transfer evidence must record compared artifact hashes before execution and on return, including their match results.
- `review`: `reviewer`, `model_version` (use an explicit unavailable explanation when genuinely unavailable), `rubric_version`, `context`, `limitations`, attached `raw_output`, and exact file:line `citations`. A clean report lists every checked item and why it passes. Do not substitute a generic endorsement.
- `findings`: an explicit list, empty only when none were found. Each finding has a stable `id`, `status` of `fixed` or `rejected_with_evidence`, reasoned `disposition`, and attached `evidence`. Unresolved or unsupported dispositions block.
- `replica_limit`: the remaining difference from the hosted implementation; keep this even when the local counterpart passes.

Missing adapter, inaccessible builder, missing genuine solve, incomplete panel inventory or insufficient evidence means **BLOCK_UPLOAD**, with the smallest remedy recorded. Do not synthesize success. Fresh solver batches need separate authorization; first reuse valid saved work.

## Enforce immediately before upload

```text
python3 <plugin-root>/scripts/quality_gate.py check <case-evidence>/local-quality.json --artifacts <canonical-artifacts> --commit <full-commit> --environment <environment.json> --selection <selection.json> --scope-tests <frozen-scope-test.patch> --output <case-evidence>/local-quality-result.json
```

This command rehashes the actual artifacts and current execution inputs, verifies attachments, requires every applicable counterpart and rubric item, checks outcomes/identity, rejects open findings and detects stale dependent receipts. Changed rules or rubric versions invalidate their bound receipts. Unchanged dependency evidence may be reused with its original provenance. Eligibility, originality and final-state receipts expire after 24 hours; the panel capture also has a 24-hour maximum. These are conservative local limits, **not Shipd rules**. Recheck the live panel immediately before the action even within that window.

Only exit 0 with `LOCAL_EVIDENCE_GATE_PASS` permits proceeding to the separately authorized upload step in this workflow. Any failure blocks it. Preserve the result and its hash in the handoff; rehash delivery bytes immediately before transfer. This is a workflow guard, not a browser/server lock: it cannot prevent a person or unrelated tool from uploading outside the workflow.

The checker audits evidence structure and integrity. It does not execute candidate tests, verify the truth of arbitrary prose, know whether someone omitted a panel row, or replace the Forge validators and actual reviews. Quality comes from those executed checks; metadata makes omissions and staleness visible. Hosted checks must still run when authorized, and hosted approval/manager acceptance remain separate states. For the [fresh reconstruction benchmark](fresh-reconstruction-benchmark.md), report locally reproducible families and limitations without inventing live-panel evidence. An unrun hosted check is `NOT_RUN`; unknown private behavior is `UNPROVEN`. These do not prevent completion of the agreed offline work, but local completion does not establish platform upload readiness.


## Execution receipt integrity

Before marking any executable matrix/check receipt PASS, follow [execution-integrity.md](execution-integrity.md). Run `test_result_gate.py` against actual JUnit, actual process exit code and an independently captured discovery inventory. Preserve raw discovery, direct test-process terminal events, XML and logs with hashes. XML reconciliation alone cannot establish execution provenance; use the libtest event adapter or a reviewed native equivalent. Compilation errors and empty suites cannot prove behavioral baseline failure. For split suites, run [partition-result-gate.md](partition-result-gate.md) against independent complete discovery. Every exclusion remains unverified until another successful reconciled partition executes that ID with the same source and executable identity; expected-failure partitions also need behavioral triage. Unresolved exclusions block a complete-suite claim and cannot remove required integration. This is an additional report-integrity gate, not a replacement for Forge behavioral validation.
