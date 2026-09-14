# Test Quality bulb expansion — 2026-09-01

- Repository: `scylladb/scylla-rust-driver`
- Commit: `611d43b595fb0ad7010f2bdbd887acae3d962d65`
- Execution host: `aswin`
- Container: `ladybug-olympus`
- Exact test patch SHA-256: `d4a494c483de5bf47a79bd19d5be59ee095c4fa622b8017657da76373ba35da0`
- Exact solution patch SHA-256: `312f1fa80e630127d1bf13d17651a0946f28c576e0e6cbe1149fd85581e8cd0d`

## Added coverage

The expanded patch contains ten logical new tests covering every prompt-grounded Test Quality bulb:

1. Default-policy coordinator eligibility: one positive current connected local replica, with distinct negative assertions for remote, non-replica, removed identity, replaced identity, disabled, disconnected, host-filtered, latency-filtered, missing-token, and missing-table cases.
2. Automatic and manual paging over three page boundaries.
3. Opaque continuation bytes for unprepared, prepared, and caching APIs.
4. Preferred-target failure followed by fresh-plan fallback, with the failed preferred target attempted only once.
5. Deterministic retry replacement, asserting three attempts and two successful requests.
6. Compatibility of metrics, tracing IDs, history listeners, speculative execution, request timeouts, and ordinary errors.
7. Exact public return type `Result<(QueryResult, Option<PagingContinuation>), ExecutionError>` for all three affinity APIs.
8. Preferred-plan ordering and duplicate suppression.
9. Policy-gated acceptance and rejection of retained coordinators.
10. Automatic paging consulting the same policy hook.

The private default-policy fixture is gated by the test-only `paging-affinity-test-fixtures` Cargo feature, enabled only in `test.sh new`, so `test.sh base` remains a genuine regression check before the solution exists.

## Exact-byte checks

- `test.patch` applies cleanly to the pinned commit.
- `solution.patch` applies cleanly to the pinned commit, followed by `test.patch`.
- `bash -n test.sh` passes.
- Each matrix state used a separate `TMPDIR` and Cargo target to prevent cache contamination.

## Four-state JUnit matrix

| State | Exit | Cases | Failures | Evidence |
|---|---:|---:|---:|---|
| Unsolved base | 0 | 1 | 0 | `unsolved-base-bulb-v9.xml` |
| Unsolved new | 1 | 10 | 10 | `unsolved-new-bulb-v9.xml` |
| Solved base | 0 | 1 | 0 | `solved-base-bulb-v9.xml` |
| Solved new | 0 | 10 | 0 | `solved-new-bulb-v9.xml` |

The Rust compiler emitted an existing future-incompatibility recursion-depth warning from metadata code; it did not affect any exit code or JUnit result.

## Staleness

Because `test.patch` changed, all previous test-dependent hosted checks and local proofs are stale. In particular, hosted Verify Solution, Problem/Test Alignment, Test Quality, false-positive, fairness, and rollout conclusions must be rerun on artifact set containing the hash above. Problem, solution, and Dockerfile bytes did not change.
