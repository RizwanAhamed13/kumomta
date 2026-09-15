# v34 hosted flakiness repair

- Repository: `scylladb/scylla-rust-driver`
- Commit: `611d43b595fb0ad7010f2bdbd887acae3d962d65`
- Execution host: `codespaces-14482c`
- Remote audit root: `/workspaces/scylla-runs38-audit`
- Artifact set: `639850033c5f06631a075c0a11382c1719429c3ed07e239d1e4d0bd0c3c892c7`

Only `test.patch` changed. The description, reference solution, Dockerfile, behavioral scope, testcase count, and solver-facing APIs are unchanged.

## Root cause and repair

`default_policy_rejects_latency_penalized_current_replica` advanced the paused Tokio clock once and yielded once. That did not guarantee that the independently spawned latency-minimum updater had processed the controlled measurements before the policy assertion.

The repaired test advances only virtual time in bounded increments, yields to the updater after each increment, and stops when the public `is_coordinator_preferred` decision exposes the active penalty. It uses no wall-clock timeout. All sibling eligibility predicates remain asserted independently.

## Evidence

- Targeted latency test: 200/200 direct executions passed.
- Full solved `test.sh new`: 12/12 sequential runs passed, 16/16 each.
- Four-state matrix: base 1/1 before and after; new 0/16 before and 16/16 after.
- Exact latency-filter omission mutant still fails the stabilized test.
- Ten saved-agent patches applied and reverted cleanly. Nova 1 and Nova 7 pass; the remaining eight fail on their prior architectural gaps. Pass rate remains exactly 2/10 (20%).
- Evidence archive: `v34-evidence.tar.gz`, SHA-256 `d1104cf9c0c0771b4cc592a287bc2e052bf8cd5110b4a7698fd5911a2f5acf44`.

## Artifact hashes

- `problem.md`: `7cd6d8f7f070c6c98a5c1d5df2b41ddaff8c6b8cf654f20a6cbdd1f6d38d4d8b`
- `test.patch`: `6ea3728a2bc4b5aa8243f30ad54692e0b04a5ab003677800e8e0ea8ef9c86688`
- `solution.patch`: `b3624a960d4d76fe4475d6e319f6987690c3c39c07f36cc3f65874e54d214b44`
- `Dockerfile`: `d935b06286b10be4b1f847993baeed8723c01da1a5654ae91adcddb759398d71`

Hosted test-dependent checks are stale and must be rerun on v34 before readiness is claimed.
