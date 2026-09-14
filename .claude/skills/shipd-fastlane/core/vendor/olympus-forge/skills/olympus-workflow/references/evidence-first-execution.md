# Evidence-first execution

Read this file whenever an Olympus Forge skill will run commands, use the live panel, resume a case, or report a verdict. It defines how to make progress without repeating expensive work or claiming more than the evidence proves.

## Operating modes

- Default to `REVIEW`: inspect, diagnose, prepare local artifacts, and run free local checks only.
- Enter `LIVE` only when the user explicitly authorizes the specific external or paid action and the current panel has been inspected. Authorization for one action does not authorize later gates, acceptance, or submission.
- Do not automate account login, OTP retrieval, reservation, clocking, acceptance, or submission. Never capture, export, or persist passwords, OTPs, tokens, cookies, or browser session material.
- Prefer an already signed-in browser for explicitly requested panel work. Stop for manual authentication when needed.

Record the active mode in `case.json` through `scripts/case_state.py`. A resumed case returns to `REVIEW` unless the user explicitly authorizes a new live action.

## Phase 0: cheapest discriminating preflight

Before building an image, running a full suite, or spending platform tokens:

1. Run `scripts/case_state.py validate`, load the case state, verify the recorded repository root, and compare the pinned commit plus all current artifact hashes with the last checkpoint.
2. Confirm the intended paths, test target, runner mode, and JUnit destination. Prove the selected test filter discovers a nonzero number of tests.
3. Run `scripts/validate_submission.py` for cheap static checks first: artifact presence, description mechanics, LF and banned-term scans, unified-diff syntax, shell safety, Docker rules, predicted filename collisions, and clean patch application alone and together in disposable states. Before Scope Gate use `--pre-scope` with current compliance and structured local-review inputs.
4. Reproduce the reported failure with the smallest command that can distinguish environment, harness, test, solution, or platform failure. Inspect raw build logs and JUnit: separate real test assertions from synthesized missing-output/process cases.
5. Stop at the first blocker, record the exact command, exit code, decisive output, and classification, then repair that layer only.

For build-backed runners, prove that base and new cannot race on one build tree. Prefer separate build directories; otherwise acquire one build lock, finish the rebuild, and only then run modes. When a grammar or generated source can change, delete its object and rebuild in a clean offline state so cached solver-session output cannot make an incomplete patch pass.

During iteration, use affected tests and the smallest fair probe. Run the complete dependent matrix once the edit batch is stable and before a handoff, upload, paid gate, or readiness claim. Do not repeatedly full-build unchanged layers while diagnosing one known failure.

## Evidence-bound findings

Every material claim must cite at least one direct proof:

- repository behavior: `file:line` at the pinned commit;
- execution behavior: exact command, exit code, and decisive output or JUnit path;
- artifact identity: commit and SHA-256 hashes;
- false-positive status: exact candidate patch, current-suite result, fair discriminator grounding, reference discriminator result, candidate discriminator result, and preserved-genuine-solve replay;
- platform status: the current live-panel result identifier or preserved output.

Label an inference as an inference. Do not convert absence of evidence, an old result, or a nearby implementation pattern into a PASS.

Treat a platform FP adjudication as exact-run evidence, not as a reusable theory about similar patches. Treat a platform genuine-pass adjudication the same way: preserve it and do not contradict it without a new executed, fair, exact-byte discriminator. An environment contest asks the reviewer to exclude or rerun a non-test failure; it never proves the solution correct.

## Coverage completeness recheck

Maintain a compact table before advancing from artifact construction or validation:

`requirement -> public path/input class -> observable oracle -> fails before -> passes after -> partial/broken implementation rejected -> evidence`

- Every problem requirement needs an observable oracle or must be removed from the description.
- Every assertion needs prompt or pinned-repository grounding.
- Cross changed response-definition, serialization, conversion, persistence, and protocol paths only when the stated behavior applies there.
- Mark missing cells `OPEN`; never hide them inside prose or a generic test-count claim.

At stage 5b, the table covers the frozen full task and complete reference
solution even though the gate test set is intentionally small. Reduce duplicated
fixtures and combine related gate assertions; do not reduce the production
contract or solution to make the table short. Rows deferred to post-gate test
expansion still require an inspected full solution path and executable evidence.

## Resume checkpoint and reviewer bundle

At every stage boundary, checkpoint `cases/<case>/case.json`, append `events.jsonl`, and regenerate `state.md` with mode, stage, exact hashes, completed commands and result paths, open items, stale proofs, last blocker, and next legal action. On resume, hash first. If bytes drifted, preserve old results under their artifact-set identifier and mark only dependent proofs stale.

Produce one human-readable bundle for handoff containing:

1. repository URL and pinned commit;
2. four artifact paths and hashes;
3. requirement-to-oracle coverage table;
4. commands, exits, JUnit/log paths, and mutation evidence;
5. current versus stale platform results;
6. open items and the next legal action.

The bundle summarizes evidence; it never replaces the raw logs, saved agent patches, rollout transcripts, or live panel.
