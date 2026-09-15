# Review v4 — per-test F2P repair

- Artifact set: `c9a97f2b33bb42848cf30fb46f75f0b0a19556a09c2c5cfa5ac8751ebfce5cc5`
- Exact commit: `dc060ecd16224ad01cdb8d7bafe89230e477446a`
- Changed artifact: `test.patch` only
- Unchanged: `problem.md`, `solution.patch`, `Dockerfile`

The hosted verifier rejected four new-mode tests because they passed individually on the pinned base. The repair preserves each original assertion and adds the smallest prompt-grounded positive feature prerequisite to the same native test:

- `maple_zero_fallback_keeps_maps_writable` now combines the existing writable-map zero fallback with an exact declared scalar default.
- `amber_route_keeps_following_named_shape` still checks rejection and recovery for all three forbidden positions, then requires one recovered named-field default to analyze successfully.
- The two `umber` package-analysis tests first accept a matching payload-less enum value or constructor-function default, then independently reject the existing wrong-type form.

Fairness classification: every added assertion is prompt-stated. No error code, diagnostic stage, AST shape, generated identifier, or formatting layout is asserted.

Exact Google Cloud Shell matrix (offline Cargo, isolated worktrees/targets):

- Base + tests, `new`: expected failure, 20 tests / 20 failures / 0 unexpected passes.
- Reference + tests, `new`: pass, 20 / 20.
- Base + tests, `base`: pass, 9052 / 9052.
- Reference + tests, `base`: pass, 9052 / 9052.
- Previously adjudicated genuine Nova + tests, `new`: pass, 20 / 20.

`cargo fmt --all -- --check`, `git diff --check`, clean forward application, and clean reverse application all pass. No Docker build was run.
