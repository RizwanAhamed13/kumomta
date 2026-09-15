# Review repair v31

Date: 2026-09-04

## Artifact identity

- Repository: `scylladb/scylla-rust-driver`
- Commit: `611d43b595fb0ad7010f2bdbd887acae3d962d65`
- Compute host: `codespaces-14482c`
- Codespace: `ra-punctuation-replay-v6gwrpjqjw67cp7qr`
- Artifact set: `871ca51ad3c0a5f90f6d3ff3462829b5fdce940e78a05fd2ca487bb31119d170`
- Problem SHA-256: `7cd6d8f7f070c6c98a5c1d5df2b41ddaff8c6b8cf654f20a6cbdd1f6d38d4d8b`
- Test SHA-256: `f188970207393e5b1b5fda72bae99f1318cebbafbb35f9c902052b72a5a5e7c2`
- Solution SHA-256: `b3624a960d4d76fe4475d6e319f6987690c3c39c07f36cc3f65874e54d214b44`
- Dockerfile SHA-256: `d935b06286b10be4b1f847993baeed8723c01da1a5654ae91adcddb759398d71`

## Root cause and repair

The source-free v29b draft removed the old production-source fixture hunks and eliminated the verifier merge/reset failure, but it also removed the DefaultPolicy eligibility matrix. Exact replay proved that Nova 4 and Nova 8 then passed despite distinct prompt-relevant defects.

v31 adds two public integration discriminators without any `scylla/src/*` test-patch changes:

1. `default_policy_keeps_same_dc_other_rack_replica_eligible` builds a two-node topology through public CQL metadata, obtains an actual successful coordinator, and proves that rack preference affects ordering within the local datacenter rather than rejecting another local rack.
2. `default_policy_uses_vnode_replicas_with_partial_table_catalog` proves that vnode replica eligibility remains derivable from the token ring and keyspace replication strategy when the table catalog is only partially available.

The hidden patch creates only:

- `scylla/tests/check_paging_continuation_opacity.py` — 64 insertions
- `scylla/tests/paging_affinity_1d7881.rs` — 2,218 insertions
- `test.sh` — 172 insertions, executable

## Exact discrimination

- Reference solution: both new public probes pass.
- Nova 4: rack probe passes; partial-table vnode probe fails.
- Nova 5: rack probe passes; partial-table vnode probe fails.
- Nova 8: partial-table vnode probe passes; rack probe fails.
- Preserved adjudicated genuine solutions Nova 1 and Nova 7: both probes pass.

## Four-state and stability matrix

- Unsolved base: 1/1 pass.
- Unsolved new: 0/12 pass; all 12 expected cases fail.
- Solved base: 1/1 pass.
- Solved new: 12/12 pass.
- Solved new repeated six times: 6/6 complete runs pass with no failure, error, or skip.

Key remote evidence:

- `/workspaces/scylla-runs38-audit/reference-v31-base.xml`
- `/workspaces/scylla-runs38-audit/reference-v31-new.xml`
- `/workspaces/scylla-runs38-audit/reference-v31-repeat-{1..6}.xml`
- `/workspaces/scylla-runs38-audit/unsolved-v31-base.xml`
- `/workspaces/scylla-runs38-audit/unsolved-v31-new.xml`

## Exact ten-agent replay

Every exact agent patch applied cleanly. v31 applied cleanly on top of every agent. Every base suite passed.

| Nova | Result | Failing behavior |
|---:|---|---|
| 1 | PASS | — |
| 2 | FAIL | rack eligibility, partial-table vnode eligibility, preferred-plan suppression |
| 3 | FAIL | rack eligibility, preferred-plan suppression |
| 4 | FAIL | partial-table vnode eligibility |
| 5 | FAIL | partial-table vnode eligibility |
| 6 | FAIL | preferred-plan suppression |
| 7 | PASS | — |
| 8 | FAIL | rack eligibility |
| 9 | FAIL | rack eligibility, partial-table vnode eligibility, preferred-plan suppression |
| 10 | FAIL | preferred-plan suppression |

Pass rate: 2/10 (20%). Environment blockers: 0/10. Patch-application failures: 0/10.

Replay manifest: `/workspaces/scylla-runs38-audit/v31-full-replay.tsv`, SHA-256 `e96fa37cc169e17ba75237ec6ac2b6773daebb01e2a35e6a54c922aea1c9747f`.

## Current status

The two known false positives and the old merge/reset environment blocker are closed locally for v31. Because `test.patch` changed, prior hosted Verify Solution, Verify Flakiness, test quality/fairness/false-positive, Auto Review, and rollout evaluations are stale and must be refreshed before readiness.
