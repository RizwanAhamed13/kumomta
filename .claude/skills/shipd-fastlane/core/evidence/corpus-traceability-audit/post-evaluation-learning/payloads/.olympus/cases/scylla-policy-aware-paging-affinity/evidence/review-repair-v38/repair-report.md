# Review repair v38

- Repository: `scylladb/scylla-rust-driver`
- Commit: `611d43b595fb0ad7010f2bdbd887acae3d962d65`
- Execution: Codespace `codespaces-14482c`, `/workspaces/scylla-runs38-audit/v38`
- Artifact set: `c8fb443ea7d9519bb8d795563c59dabfa2e942a70b4174fa5379e115efade41f`

## Changes

- Extended the existing invalid-target test with an absent-host ClusterState, separately proving removed-coordinator rejection.
- Added a shard-aware public-topology test with a matching-shard positive control and mismatching-shard rejection for DefaultPolicy.
- No description, solution, Dockerfile, API, or product-scope change.

## Proof

- Exact shard-blind DefaultPolicy mutant fails only the new wrong-shard test.
- Exact absent-host-permissive mutant fails the extended invalid-target test.
- Test patch applies alone and after the reference; it contains only two test files plus `test.sh`, with no production-source hunks.
- Four-state JUnit: base `1/1` before and after; new `0/18` before and `18/18` after.
- Stability: twelve sequential solved-new runs, all `18/18`.
- Saved agents: exactly `2/10` still pass. Nova 1 and 7 pass `18/18`; all other saved solutions fail their same pre-existing semantic cases.

## Hashes

- `problem.md`: `7cd6d8f7f070c6c98a5c1d5df2b41ddaff8c6b8cf654f20a6cbdd1f6d38d4d8b`
- `test.patch`: `95a847bbd0753b0854e31fd37289894355892cbb5abe68a06128c87bdecd62c8`
- `solution.patch`: `b3624a960d4d76fe4475d6e319f6987690c3c39c07f36cc3f65874e54d214b44`
- `Dockerfile`: `d935b06286b10be4b1f847993baeed8723c01da1a5654ae91adcddb759398d71`

Hosted checks depending on `test.patch` remain stale until rerun against v38.
