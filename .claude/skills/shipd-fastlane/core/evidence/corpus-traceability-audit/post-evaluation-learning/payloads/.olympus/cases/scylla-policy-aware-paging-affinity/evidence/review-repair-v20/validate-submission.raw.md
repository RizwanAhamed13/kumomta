# Deterministic validator result

Command ran on `aswin` in `ladybug-olympus` against commit `611d43b595fb0ad7010f2bdbd887acae3d962d65` and artifact set `243668e4bf1e44d4fa84ef5077447de8f41e92029acc5609da45cd4e16f99225`.

Exit: 1

```text
ERROR: test.patch appears to modify production code: ['scylla/src/client/session.rs', 'scylla/src/cluster/node.rs', 'scylla/src/cluster/worker.rs', 'scylla/src/policies/load_balancing/default.rs', 'scylla/src/response/coordinator.rs']
```

These paths contain feature-gated test fixtures and inline unit tests. The runtime four-state and hosted-format runner evidence passes, but the current path-based validator has no exemption for feature-gated test scaffolding. This result blocks declaring the package ready.
