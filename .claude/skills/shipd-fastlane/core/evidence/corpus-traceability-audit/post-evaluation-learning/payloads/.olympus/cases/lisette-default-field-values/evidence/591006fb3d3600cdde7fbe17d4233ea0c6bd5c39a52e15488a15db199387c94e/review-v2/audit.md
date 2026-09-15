# Review-v2 repair audit

- Exact artifact set: `591006fb3d3600cdde7fbe17d4233ea0c6bd5c39a52e15488a15db199387c94e`.
- Pinned source: `dc060ecd16224ad01cdb8d7bafe89230e477446a`.
- Reference new mode: 20 tests, 0 failures.
- Reference base mode: 9,053 tests, 0 failures, including workspace, CLI, LSP, manifest, syntax, formatter, emitter, and repository integration targets.
- Test patch without solution, base mode: 9,053 tests, 0 failures.
- Test patch without solution, new mode: 20 tests, 16 failures; exit 1.
- Normal workspace Clippy with `--workspace --all-targets --locked -- -D warnings`: pass.
- Previously adjudicated genuine Batch-82 Nova 2 solution replayed against the strengthened new suite: 20 tests, 0 failures; exit 0.

The first Nova replay used a Cargo target directory shared with the test-only worktree. Cargo reused baseline libraries and produced invalid missing-field compiler errors. That run is excluded. The recorded passing replay used the isolated target `/tmp/lisette-v2-nova2-target`.

The first reference workspace run externally redirected `CARGO_TARGET_DIR`. The pinned shebang integration test intentionally locates `target/debug/lis`, so it failed only under that validator override. The exact test passed with the repository-default target. Base mode now unsets `CARGO_TARGET_DIR`, and the complete final workspace run passes.

No Docker build or test loop was run. The Dockerfile change is static: it adds `cargo build --workspace --locked` after the existing locked fetch and still runs no tests during image creation.
