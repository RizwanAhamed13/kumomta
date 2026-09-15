# Verify Solution offline-runner repair

Date: 2026-08-30

## Hosted failure classification

The hosted reference run passed all 14 base groups and all 19 compile-rejection groups, but reported all 18 positive runtime groups as failed. The per-test output shows that those groups did not reach a Dora assertion: `uv run` attempted to build the local pytester environment, tried to fetch `hatchling` from PyPI, and failed because the evaluator has no DNS/network access. The same log also contains failures opening `/app/target/debug/.cargo-build-lock` under the evaluator user. This is an image/runner portability defect, not a description, oracle, or reference-semantics defect.

## Artifact repair

- `test.patch`: every runtime command now invokes the pytester executable already installed into `/opt/dora-pytester-venv/bin/pytester` during the image build. Runtime execution no longer invokes `uv`, resolves packages, or accesses the network.
- `Dockerfile`: declares `UV_OFFLINE=1`, uses the Rust toolchain already present in the required Olympus base image, and builds with `umask 000` so evaluator processes can update Cargo output without relying on UID 1000 ownership.
- The writable-mode policy is applied while the build output is created. It does not add a later recursive `chmod` layer, which would copy several gigabytes of compiled output into a second Docker layer.
- `problem.md`, all Dora fixtures and assertions, testcase names, and `solution.patch` are unchanged.

## Exact repaired hashes

- `problem.md`: `26d9c364c2afd044a405946ca6a7144dfd1dd72b27321921c6b635b8bdeb16c6`
- `test.patch`: `e2031f17c79fe3b3bdee9ff22506159ea12960bb2f3bc620d8a693a2792767b4`
- `solution.patch`: `756b9f1abdb7df50607441fca0a0d25d48b89583b077896820132de2fb3ccd15`
- `Dockerfile`: `a3785c4e9ca467422e24ec28add06b617abf4477b7455f786a442ddd8c449063`

## Verification

- Structural validator: PASS; both patches apply cleanly at pinned commit `5dd7d4dc79e26f9d9e039681d6bb42f385378c7b`; 29 test-patch files, 30 solution-patch files, and 699 estimated effective production LOC.
- Generated `test.sh`: `bash -n` PASS and supports the hosted order `./test.sh --output_path PATH base|new`.
- Aswin `podspub27`, `--network none`: direct `/opt/dora-pytester-venv/bin/pytester` execution of the reference runtime fixture passed (1/1) in Cannon mode. This proves the repaired invocation uses the preinstalled harness without package resolution or network access.
- The immediately preceding exact semantic matrix, before this runner-only substitution, was clean base 14/14, clean new 19/37, solved base 14/14, solved new 37/37. The runner substitution changes only how the same pytester is launched.
- The disposable failed repair-build container was removed after validation. Older Dora/Olympus evidence containers and images were left untouched.

The live Verify Solution result remains stale until the repaired `test.patch` and Dockerfile are uploaded and the platform rebuilds the image.
