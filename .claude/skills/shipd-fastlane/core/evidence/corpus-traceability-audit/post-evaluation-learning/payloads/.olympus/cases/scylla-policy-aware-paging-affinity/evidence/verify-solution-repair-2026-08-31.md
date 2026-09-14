# Verify Solution and Solution Quality repair

## Hosted findings

- Verify Solution failed before executing tests because the evaluator invoked `./test.sh --output_path /var/artifacts/junit_base.xml base`, while the runner treated its first argument as the mode and rejected the XML path as an unknown argument. Attachment SHA-256: `935f39445e0b15460c6009dc7388f6e44245b7a95fc9ad8e1aa350a6aaccd4e0`.
- Solution Quality failed on a stray `x` after the `Plan` iterator item type, a stale automatic-pager `ClusterState` snapshot, and duplicate emission when an unspecified fresh-plan shard materialized to the sharded preferred target. Attachment SHA-256: `812032eaa21bb9d95b96fb1164bc723d1e4383091c9929b4010352c9450ec60e`.

## Root causes and repairs

- Harness/runner: parse `base|new` and `--output_path <path>` in either order and always write JUnit, including compile failures.
- Golden syntax: removed the stray iterator token.
- Golden current-state semantics: `PagingExecutor` now retains the cluster state's `ArcSwap` handle and calls `load_full()` when constructing every later-page plan.
- Golden shard semantics: materialize an unspecified shard once before comparing it with the preferred target.
- Discriminator: the existing preferred-plan scenario now checks that an unspecified fresh-plan shard cannot reproduce preferred `(node, shard 0)`.

## Local parser reproduction

With a fake Cargo executable, both invocations exited 0 and produced parseable `<testsuites>` XML:

- `./test.sh --output_path /tmp/scylla-parser-base.xml base`
- `./test.sh base --output_path /tmp/scylla-parser-base-reversed.xml`

## Aswin/LXC matrix

Environment: `aswin`, container `ladybug-olympus`, pinned commit `611d43b595fb0ad7010f2bdbd887acae3d962d65`.

| State | Mode | Exit | JUnit |
|---|---|---:|---|
| test only | base | 0 | 1 case, 0 failures |
| test only | new | 101 | synthetic compile-failure case, 1 failure, zero behavioral passes |
| test + repaired solution | base | 0 | 1 case, 0 failures |
| test + repaired solution | new | 0 | 7 cases, 0 failures |

`cargo check --locked -p scylla --lib` passed. `cargo fmt --all -- --check` passed after import/order formatting. The only warning is the pinned repository's pre-existing future-incompatibility recursion-depth warning.

The executed test patch and final test patch materialize identical files; their only textual patch difference is the non-semantic `index` hash line for `test.sh`.
