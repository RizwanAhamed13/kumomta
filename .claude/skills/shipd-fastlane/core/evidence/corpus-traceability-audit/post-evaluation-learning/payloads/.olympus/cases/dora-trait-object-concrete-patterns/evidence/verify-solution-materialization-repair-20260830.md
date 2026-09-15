# Verify Solution materialization repair — 2026-08-30

Artifact set: `8843bc2ced0dd26eed5ebee3bf1a632ab6e6f83506e2e6f0bc563e099cf83fba`

Pinned commit: `5dd7d4dc79e26f9d9e039681d6bb42f385378c7b`

## Hosted failure reproduced

The hosted result reported 14/14 base tests passing, 19 rejection tests passing, and all 18 positive runtime groups failing after `solution.patch`.

In evaluator order on Aswin, applying the solution left both image-time executables unchanged:

- base `target/debug/dora`: `95d1f3ade2d37242adb4fdd5254172f4826919a979d9f15e619e593b83750205`
- base `target/debug/dora-boots-compiler`: `aa4241de4525eb1a552510c8a0ed340961abdbc93fa4a9775e0be12bbf92c47e`
- both hashes were identical immediately after applying `solution.patch`

The stale Dora executable rejected the positive reference fixture with `Pattern does not match type`. Rebuilding only the Rust `dora` package made Cannon pass but left all nine Boots groups failing. Running the repository-native `tools/bootstrap` rematerialized both compiler layers and made the full new suite pass.

## Repair

Only `test.patch` changed. `test.sh` now computes a deterministic source-tree key and runs `uv run --script tools/bootstrap` when that key has not been materialized. The stamp is stored below `target/`, so:

- test-only and solved source trees receive different stamps;
- Docker-baked executables cannot satisfy a post-solution run;
- a second mode on unchanged source reuses the completed bootstrap.

No problem wording, hidden behavioral assertion, production solution, or Dockerfile changed.

## Exact Aswin four-state matrix

Backend: `aswin` → LXC `podspub27` → disposable container `dora-fixed-runner-work-20260830`, evaluator path `/app`.

| State | Mode | Exit | JUnit |
|---|---|---:|---|
| test-only | base | 0 | 14 tests, 0 failures |
| test-only | new | 1 | 37 tests, 18 failures |
| solved | base | 0 | 14 tests, 0 failures |
| solved | new | 0 | 37 tests, 0 failures |

After solution-side materialization:

- `target/debug/dora`: `1a3170e8456d63906847f09e8f47ecebe674590389c2ace94af8b52ea18e455d`
- `target/debug/dora-boots-compiler`: `ee1bf8c8d84fd42f796cf38bfd865e13b85dfb5bb19856021efe9d9881bba697`
- stamp count advanced from one base-source key to two total keys;
- solved `new` reused the solution stamp and did not run bootstrap again.

JUnit evidence:

- `evidence/dora-final-base-before.xml`
- `evidence/dora-final-new-before.xml`
- `evidence/dora-final-base-after.xml`
- `evidence/dora-final-new-after.xml`

## Current artifact hashes

- `problem.md`: `26d9c364c2afd044a405946ca6a7144dfd1dd72b27321921c6b635b8bdeb16c6`
- `test.patch`: `0364dd1600a90a8c0ec666ef79c86f524693f38cef0ea15fab50112ed499cfc2`
- `solution.patch`: `f532c5527665e387af6b09f29e3ddb928e1617a49882052b8e352ce6c343a36e`
- `Dockerfile`: `a3785c4e9ca467422e24ec28add06b617abf4477b7455f786a442ddd8c449063`

Structural validation passed with 29 test-patch files, 31 solution files, and 718 estimated effective production LOC. Alignment graph v7 passed at 1.0 description/test/solution/triad coverage with zero audit blockers.

## Staleness

The test-patch edit stales the live Scope Gate, Verify Tests, Verify Solution, Test Quality, flakiness, mutation/FP replay, saved-solver replay, and downstream reviews. The local four-state matrix and structural/alignment proofs above are current; hosted gates remain authoritative and must be rerun.
