# v33 Auto Review repair

- Repository: `scylladb/scylla-rust-driver`
- Commit: `611d43b595fb0ad7010f2bdbd887acae3d962d65`
- Execution host: `codespaces-14482c`
- Remote audit root: `/workspaces/scylla-runs38-audit`
- Artifact set: `a41085d197cd7fdf5b24433180e560ae8c1159e176f6c91a89c5e58dfd55aa32`

Only `test.patch` changed. `problem.md`, `solution.patch`, and `Dockerfile` are byte-identical to v32.

## Repairs

1. Added `default_policy_rejects_latency_penalized_current_replica`. It records controlled fast and slow measurements through the public policy callback, advances a paused Tokio clock through the latency updater, proves that the retained target remains current, enabled, connected, local, and a routed replica, and then requires the DefaultPolicy hook to reject it solely through the active latency predicate.
2. Replaced the disconnected-node five-second polling loop with the proxy reaction's explicit feedback channel, query completion, and a direct connectivity assertion.
3. Changed the JUnit merger so a simultaneous integration-report failure and opacity failure preserve both diagnostics in the existing opacity testcase without duplicating testcase identity or inflating the failure count.

## Executed evidence

- Four-state matrix: unsolved base 1/1; solved base 1/1; unsolved new 0/16; solved new 16/16.
- Stability: six consecutive solved `test.sh new` runs, all 16/16 with no failures, errors, or skips.
- Disconnect transition: ten consecutive targeted passes after removing wall-clock polling.
- JUnit merger probe: invalid integration JUnit plus an independent opacity failure produced exactly 16 unique cases and retained both distinct diagnostics.
- Active-filter mutant: the exact connectivity-preserving implementation that omits only the active latency predicate passed v32 15/15, then failed only the new latency testcase under v33 (15/16).
- Saved-agent replay: all ten patches applied and reverted cleanly. Nova 1 and Nova 7 passed 16/16; the other eight remained failing. Pass rate is unchanged at 2/10 (20%).

The evidence archive `v33-evidence.tar.gz` has SHA-256 `923149e19f3ed5a3f883da3988e64757a3d3c0b38abe2f1b4e90d5a3269606b3`; its internal `SHA256SUMS` verifies all 61 files.

## Artifact hashes

- `problem.md`: `7cd6d8f7f070c6c98a5c1d5df2b41ddaff8c6b8cf654f20a6cbdd1f6d38d4d8b`
- `test.patch`: `3bae0890504e68303514928a7503afd370d0f77f38ae0b9cc20ccddb5bd03945`
- `solution.patch`: `b3624a960d4d76fe4475d6e319f6987690c3c39c07f36cc3f65874e54d214b44`
- `Dockerfile`: `d935b06286b10be4b1f847993baeed8723c01da1a5654ae91adcddb759398d71`

## Staleness

The current local matrix, stability, focused mutant, harness, and saved-agent replay evidence is fresh for v33. All hosted checks depending on `test.patch` remain stale and must be rerun: Verify Tests/Solution, Verify Flakiness, Test Quality/Fairness, false-positive review, Holistic, Auto Review, and rollout re-evaluation.
