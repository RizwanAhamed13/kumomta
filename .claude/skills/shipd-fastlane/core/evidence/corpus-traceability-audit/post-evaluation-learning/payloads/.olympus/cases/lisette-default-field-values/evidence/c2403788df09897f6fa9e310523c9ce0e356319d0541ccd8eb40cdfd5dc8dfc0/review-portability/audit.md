# Review portability repair

Artifact set: `c2403788df09897f6fa9e310523c9ce0e356319d0541ccd8eb40cdfd5dc8dfc0`

## Exact artifacts

- `problem.md`: `1b3f82b1d177ce9874e3c550f313ccc866afedc66180cdba82f6aaf08f774724`
- `test.patch`: `b2a805cd733594209829fa98975bc69c5da6d128bee852c5979843285017567e`
- `solution.patch`: `7f2f8b78ddcac53558ea2580ed0c3a00d4cbb865be0b65b5bfe77887cd3d2c99`
- `Dockerfile`: `e1363394bf8461647c3d93dd31ba5a48f6f0462757c22630bdf430215e213a7b`

## Repair

- Replaced the ambiguous foreign-autofill phrase with explicit declaration-package evaluation behavior.
- Installed Rust state under `/opt/rustup` and Cargo state under `/opt/cargo`.
- Exposed Rust 1.97.0 and Go 1.25.10 through `/usr/local/bin`, so login-shell PATH resets do not hide them.
- Removed dependence on root-built `/app/target`; the runner uses separate `/tmp/lisette-field-defaults-target-{mode}-{uid}` directories and UID-specific Go caches.
- Made `/app` and `/opt/cargo` writable to the evaluator user and the Rust toolchain readable/executable.
- Kept the submitted `:latest` base tag. The build resolved it to `sha256:211a2e3aeff24b410f2c982723e9314992833f4633c764217eab87552f1d1477`; this digest is evidence only and is not embedded in the Dockerfile.

## Verification

- Structural validator: PASS. Clean application, LF, shell, repository-root, base-image, and artifact checks all passed. See `validate-submission.json`.
- Exact saved genuine Nova candidate (`1cd57728b58a1ae03163aaf108dc8d91e37952cee7bd473232a4489e5c5e0964`) against the current `test.patch`: PASS, 20 tests, 0 failures, 0 errors. JUnit is preserved under artifact-set evidence `d1666134.../non-root-replay/lisette-replay-47ce-nova10-new.xml`; its `test.patch` bytes are identical to this set.
- Final Dockerfile build: PASS. Rust 1.97.0, Cargo 1.97.0, Go 1.25.10, locked fetch, and locked workspace build completed. Final image manifest list: `sha256:e9026b5ab29a0a1af5ff1ed5c251fc221889409907e297bc6a1ff33a87a9c809`.
- UID 4242 smoke before the final permission-only `/app` layer: PASS, with Rust/Cargo/Go visible in a login shell, no `/app/target`, and the saved Nova suite at 20/20. The final layer only broadens `/app` write permission.
- A full UID 4242 base run on the final image began successfully and produced native JUnit, but Google Cloud Shell restarted before the long workspace run completed. The authoritative live Verify Solution base result therefore remains stale and must be rerun.

No behavioral assertion, hidden fixture, or reference-solution byte changed in this repair.
