# Review repair v37

- Repository: `scylladb/scylla-rust-driver`
- Commit: `611d43b595fb0ad7010f2bdbd887acae3d962d65`
- Execution: Codespace `codespaces-14482c`, `/workspaces/scylla-runs38-audit/v37`
- Artifact set: `4dddffa116daf20d0e11dc098f96dc365a63ea47ac72f6734964a43ef30a6d40`

## Change

Added one end-to-end shard-aware paging testcase for an already stated requirement. The dry proxy negotiates real Scylla shard metadata. Page one succeeds on node N/shard 1; the preferred page-two attempt fails; a fresh-plan target for another shard of N remains eligible and succeeds. The same oracle runs through manual query, manual prepared execution, caching execution, automatic query paging, and automatic prepared paging.

No description, solution, Dockerfile, API, or product-scope change was made.

## Discrimination and validation

- Exact node-only mutant: changes retained coordinator mapping from `coordinator.shard()` to `None`; old v36 suite passes, new shard testcase fails.
- Patch application: test patch applies alone and after the reference solution.
- Test patch: only `scylla/tests/*` and `test.sh`; no production-source hunks.
- Four-state JUnit: base `1/1` before and after; new `0/17` before and `17/17` after.
- Stability: twelve sequential solved-new runs, all `17/17`.
- Saved agents: unchanged `2/10` pass profile. Nova 1 and 7 pass `17/17`; all other saved solutions still fail.

## Hashes

- `problem.md`: `7cd6d8f7f070c6c98a5c1d5df2b41ddaff8c6b8cf654f20a6cbdd1f6d38d4d8b`
- `test.patch`: `5110a838636718581fc9db93b6ca168aebc9dd9998a417fba8f2217d4b5fafbb`
- `solution.patch`: `b3624a960d4d76fe4475d6e319f6987690c3c39c07f36cc3f65874e54d214b44`
- `Dockerfile`: `d935b06286b10be4b1f847993baeed8723c01da1a5654ae91adcddb759398d71`

Hosted checks depending on `test.patch` are stale and must be rerun against v37.
