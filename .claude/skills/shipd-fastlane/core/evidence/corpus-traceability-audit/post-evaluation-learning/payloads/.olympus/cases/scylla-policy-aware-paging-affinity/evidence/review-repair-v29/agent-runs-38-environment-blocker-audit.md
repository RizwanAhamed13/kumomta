# Agent-runs-38 environment-blocker audit

Date: 2026-09-04

## Execution identity

- Orchestration host: Mac (coordination and evidence only)
- Compute host: `codespaces-14482c`
- Codespace: `ra-punctuation-replay-v6gwrpjqjw67cp7qr`
- Remote audit root: `/workspaces/scylla-runs38-audit`
- Repository: `scylladb/scylla-rust-driver`
- Commit: `611d43b595fb0ad7010f2bdbd887acae3d962d65`
- Input ZIP SHA-256: `8b6da34a9ce71236be698e4e6b34f277c533f840b58c566127ca0faa8c29f99a`
- Evaluated source-free test patch: `/workspaces/v29b-test.patch`
- Test patch SHA-256: `9e6a9ce555a70fa19f67532d2f3012e14e8cbc568c05f0d7fe0a21d95be61a57`

## Root-cause verdict

The two prior `FAIL_TEST_BROKEN` results were genuine verifier/test-patch integration failures, not solver failures. The then-current hidden patch modified the same implementation files that normal solver patches modify, including `scylla/src/client/session.rs`, `scylla/src/cluster/worker.rs`, and `scylla/src/policies/load_balancing/default.rs`. When patch application conflicted, the verifier fallback reset those files and produced an uncompilable mixture of baseline and solver code.

The source-free v29b test patch removes that collision class. It creates only:

- `scylla/tests/check_paging_continuation_opacity.py` — 64 insertions
- `scylla/tests/paging_affinity_1d7881.rs` — 1,473 insertions
- `test.sh` — 170 insertions, executable

It has no `scylla/src/*` hunks.

## Exact replay result

Every one of the ten exact solver patches applied cleanly. The exact source-free hidden patch then applied cleanly on top of every solver. All ten base suites passed. There were zero patch-application failures, zero reset/fallback events, and zero environment blockers.

| Nova | Original result | Source-free replay | New-suite result |
|---:|---|---|---|
| 1 | Legitimate pass | PASS | 10/10 |
| 2 | Missed requirement | FAIL | preferred-plan suppression |
| 3 | Missed requirement | FAIL | preferred-plan suppression |
| 4 | Missed requirement | PASS | 10/10 |
| 5 | Test broken | PASS | 10/10 |
| 6 | Missed requirement | FAIL | preferred-plan suppression |
| 7 | Legitimate pass | PASS | 10/10 |
| 8 | Missed requirement | PASS | 10/10 |
| 9 | Missed requirement | FAIL | preferred-plan suppression |
| 10 | Test broken | FAIL | preferred-plan suppression |

Corrected pass count: 5/10 (50%). Genuine failures: 5/10. Environment blockers: 0/10.

The two formerly blocked runs now have meaningful outcomes: Nova 5 passes, while Nova 10 fails a behavioral test.

## Four-state and repetition evidence

- Clean unsolved base: 1/1 pass.
- Clean unsolved new: 0/10 pass; all ten expected tests fail.
- Solved reference base: 1/1 pass.
- Solved reference new: 10/10 pass.
- Solved reference repeated new runs: 6/6 runs pass with no failed, errored, or skipped testcase.

Remote evidence includes:

- `current-v29b-summary.json`, SHA-256 `b6604b5cfe840e8d5909311082e5d9e062841d5277d0b171394569df73283ade`
- `unsolved-v29b-base.xml`, SHA-256 `5570af1fad9bff6befbb6f0a126470dfea3d3df4cefae7837f80b94e5d0b5436`
- `unsolved-v29b-new.xml`, SHA-256 `95d0c1839879a35e4b1c0c01fe456ba7d2897e325c8c115246531d9f4212b7ac`
- Per-agent base/new JUnit and logs under `/workspaces/scylla-runs38-audit/Nova_Nova_<n>/`.
- Six solved repetition XML/log pairs under `/workspaces/scylla-runs38-audit/reference-v29b-new-r<1..6>.*`.

## Important coverage tradeoff

The environment-safe patch is not a coverage-equivalent replacement for the current canonical patch. It removes three private-source fixture tests, reducing the new suite from 13 to 10 tests and the test patch from 2,100 to 1,707 insertions (393 fewer insertions). In particular, it no longer directly grades the DefaultPolicy same-datacenter/different-rack eligibility boundary, real host-filter rejection, or latency-penalty rejection.

That loss explains why Nova 4 and Nova 8 change from failure to pass. Both previously failed the rack/locality eligibility test. Therefore the 50% pass rate is accurate for v29b, but promoting it would weaken alignment and make previous quality/review evidence stale.

## Promotion decision

Do not silently replace the canonical artifact with v29b. The current canonical patch retains coverage but can reproduce the merge/reset blocker; v29b removes the blocker but loses three important tests. A final artifact must choose a source-free, public-behavior replacement for those boundaries or explicitly accept and re-review the reduced coverage. All prior Verify Solution, Test Quality, Auto Review, false-positive, flakiness, and rollout conclusions are stale after such a test-patch change.
