# Prepared/caching paging flake repair — 2026-09-01

- Repository commit: `611d43b595fb0ad7010f2bdbd887acae3d962d65`
- Execution: `aswin` / `ladybug-olympus`
- Solution SHA-256: `c5a83c205851ef0c5c1084a84a4805d1cc4a12b534e8691558c5229557b1c9ac`
- Test SHA-256: `203b54457f26342c284ca413637f3b610a6e194500582dcdb8679cdc9b03686b`

## Root cause

`prepared_and_cached_manual_apis_carry_opaque_continuations` reused one session, policy counter, and proxy across prepared and caching phases. It also overconstrained transport observations:

- a paging-state byte could legitimately be observed more than once after retry/reprepare;
- a successful legacy raw paging call could legitimately complete the page instead of returning `HasMorePages`.

The hosted failure was therefore a nondeterministic test outcome, not a reference-solution behavior failure.

## Repair

- Prepared and caching scenarios now use independent sessions, policies, proxies, counters, and observation buffers.
- Paging-state integrity still requires state byte `31` to be observed at least once.
- Both legacy raw prepared and caching APIs are still executed and required to succeed, without forcing a particular page-completion outcome.
- The same repair is present in the durable regression test carried by `solution.patch`.

## Validation

- Exact test-only and solution-plus-test clean application passed.
- Combined `cargo fmt --all -- --check` passed.
- Repaired test: 100/100 isolated repetitions passed.
- Complete nine-test integration target: 50/50 repetitions passed.

| State | Exit | Cases | Failures | Evidence |
|---|---:|---:|---:|---|
| Unsolved base | 0 | 1 | 0 | `unsolved-base-flake-repair-v14.xml` |
| Unsolved new | 1 | 10 | 10 | `unsolved-new-flake-repair-v14.xml` |
| Solved base | 0 | 1 | 0 | `solved-base-flake-repair-v14.xml` |
| Solved new | 0 | 10 | 0 | `solved-new-flake-repair-v14.xml` |

Unsolved-new and solved-new contain exactly the same ten JUnit identities.

Both patches changed, so every hosted check and rollout result is stale until rerun on this artifact set.
