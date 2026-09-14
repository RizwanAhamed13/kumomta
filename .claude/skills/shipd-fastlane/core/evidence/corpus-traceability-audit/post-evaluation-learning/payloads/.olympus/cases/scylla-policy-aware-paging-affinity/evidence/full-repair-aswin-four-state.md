# Full repair clean four-state validation

- Artifact set: `ff4d8d1aa8c9e070539062f30f502e88ca885a3e74a7375fb9a54f666d06bda3`
- Environment: `aswin` / LXC `ladybug-olympus`
- Repository commit: `611d43b595fb0ad7010f2bdbd887acae3d962d65`
- Clean unsolved tree: `/tmp/scylla-full-unsolved-clean5-ff4d8d1a`
- Clean solved tree: `/tmp/scylla-full-solved-clean5-ff4d8d1a`

## Matrix

| State | Mode | Result | JUnit observation |
|---|---|---|---|
| Unsolved | `new` | Expected failure | Compilation rejects missing public APIs; synthetic `cargo-test` failure, zero behavioral tests execute |
| Unsolved | `base` | PASS | `plan_calls_fallback_even_if_pick_returned_none` passes |
| Solved | `base` | PASS | `plan_calls_fallback_even_if_pick_returned_none` passes |
| Solved | `new` | PASS | 6/6 runtime behavioral tests pass |

This evidence belongs only to its recorded artifact set and is stale after the graph-micrograde edits.
