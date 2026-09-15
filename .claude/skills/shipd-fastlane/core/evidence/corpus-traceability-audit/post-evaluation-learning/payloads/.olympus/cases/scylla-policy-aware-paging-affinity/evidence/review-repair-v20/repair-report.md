# Auto Review repair v20

Repository: `scylladb/scylla-rust-driver`  
Commit: `611d43b595fb0ad7010f2bdbd887acae3d962d65`  
Execution: `aswin`, LXC `ladybug-olympus`  
Artifact set: `243668e4bf1e44d4fa84ef5077447de8f41e92029acc5609da45cd4e16f99225`

The description, reference solution, and Dockerfile are unchanged. The hidden test patch is `f34b227ab3b8aa102baaec043926b3bfe4444b0375156934f28e4098b739b8bc`.

## Findings closed

- Node-wide suppression for an unsharded preferred coordinator now uses a fallback plan that contains the same node at shards 0 and 1, plus another node. The oracle requires the preferred node once and preserves only the other node in the tail.
- DefaultPolicy eligibility now derives the routed replica shard, accepts the matching shard, and rejects a different shard on the same current local replica.
- Prepared, caching, unprepared, and automatic paging now exercise resumed-page observability. The integration suite checks tracing, history, deterministic speculation, exact metrics, and resumed failure compatibility.
- `PagingContinuation` opacity is checked from Rustdoc JSON: the exact public struct path must expose no public fields and must report stripped fields.
- Manual paging request/error metric deltas are asserted exactly in isolated deterministic scenarios.

## Clean transition matrix

| State | Base | New |
|---|---:|---:|
| test patch only | 1/1 pass | 0/13 pass |
| solution + test patch | 1/1 pass | 13/13 pass |

JUnit hashes:

- unsolved base: `5570af1fad9bff6befbb6f0a126470dfea3d3df4cefae7837f80b94e5d0b5436`
- unsolved new: `f94fc609cccf424dc507cc0fcaab84ddd4b7ede99604b925e899cdb13d143930`
- solved base: `5570af1fad9bff6befbb6f0a126470dfea3d3df4cefae7837f80b94e5d0b5436`
- solved new: `520799714052aa23c5a70eca76569e33a24befb9f6c02ebb7a523746476df460`

Three clean stability repetitions each passed 13/13. Their JUnit hashes differ only in timing/order serialization and are preserved under `remote/v20-stability-clean-*.xml`.

## Mutation and survivor evidence

- Shard-blind DefaultPolicy: killed by the wrong-shard assertion.
- Exact-pair-only suppression for an unsharded preference: killed because the second shard of the preferred node leaks into the tail.
- Public continuation fields: Rustdoc builds, then the opacity oracle rejects the API.

Saved genuine Nova 2, 4, and 8 solutions all apply and pass 13/13. Exact patch and JUnit/log evidence is preserved in this directory.

## Staleness

Because `test.patch` changed, all prior hosted verification, test-quality/fairness, false-positive, Holistic, Auto Review, and rollout results are stale. No hosted pass is claimed for artifact set `243668e4bf1e44d4fa84ef5077447de8f41e92029acc5609da45cd4e16f99225`.

## Deterministic validator blocker

The current path-based validator rejects the feature-gated fixtures and inline Rust unit tests because they touch five `scylla/src/**` files. This is preserved in `validate-submission.raw.md`. The five Auto Review gaps are dynamically closed, but the package is not declared ready while this structural blocker remains.
