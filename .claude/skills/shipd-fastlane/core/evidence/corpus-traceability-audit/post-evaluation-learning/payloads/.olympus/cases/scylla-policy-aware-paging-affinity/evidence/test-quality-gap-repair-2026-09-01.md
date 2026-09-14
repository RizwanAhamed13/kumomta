# Test-quality gap repair

- Repository: `scylladb/scylla-rust-driver`
- Commit: `611d43b595fb0ad7010f2bdbd887acae3d962d65`
- Execution host: `aswin`, LXC `ladybug-olympus`
- Unsolved worktree: `/tmp/scylla-v17-u.zFLgI6`
- Solved worktree: `/tmp/scylla-v17-s.GY86bD`

The six prompt-stated Test Quality suggestions were incorporated in one batch:

1. Automatic query and execute iterators now return a real node-marker row per logical page and assert all approved pages use the same node; the opt-out branch asserts rotation.
2. The active policy decision changes after page one and the next page must fall back, proving the current decision is consulted.
3. Prepared and caching page-two results assert the approved page-one coordinator actually served the request; unprepared paging also checks page three.
4. The retry-winner scenario asserts that the winner actually serves the following page.
5. Affinity and legacy errors are compared by variant discriminant; unprepared, prepared, and caching APIs exercise metrics, tracing, and deterministic speculative execution using a zero retry interval and 100 ms forged responses.
6. The duplicate private-predicate filter checks were replaced by separate real HostFilter and latency-awareness tests.

The follow-up v17 repair also removed direct mutation of `ClusterState::known_nodes`. Missing, replaced, and disabled topology variants are now constructed through `ClusterState::new` with normal metadata and a real `HostFilter`; only the test-only connectivity setter remains, feature-gated to the hidden-test fixture feature.

Clean application and transition evidence:

- `test.patch` alone applied cleanly at the pinned commit.
- `solution.patch` followed by `test.patch` applied cleanly at the pinned commit.
- Unsolved base: 1 test, 0 failures, 0 skips.
- Unsolved new: 12 tests, 12 failures, 0 skips.
- Solved base: 1 test, 0 failures, 0 skips.
- Solved new: 12 tests, 0 failures, 0 skips.
- Base and new testcase identity sets match across unsolved and solved states.
- Repeated solved suite: 20/20 full integration runs and 20/20 unit-filter runs on the final v17 bytes.

JUnit artifacts:

- `unsolved-base-coverage-v17.xml`
- `unsolved-new-coverage-v17.xml`
- `solved-base-coverage-v17.xml`
- `solved-new-coverage-v17.xml`

Artifact hashes at transfer:

- `problem.md`: `7cd6d8f7f070c6c98a5c1d5df2b41ddaff8c6b8cf654f20a6cbdd1f6d38d4d8b`
- `test.patch`: `bf15ffffa450df86e9858be304f8fc0f8792e502ed4458eccf504d1a1d6acd80`
- `solution.patch`: `1f78e5e760ef01f50f18be4b30296184233fdd94984e960d7887b5b7fe2eed3b`
- `Dockerfile`: `6f49f21fd05b62d1aab372384024c55e96bb9b0c825f0b5fe972fdb42fa26fc8`

All hosted Verify, quality, rollout, Holistic, and Auto Review results that depend on `test.patch` or `solution.patch` are stale and must be rerun on these bytes.
