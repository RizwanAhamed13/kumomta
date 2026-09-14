# Stage 5b verification

Date: 2026-08-29

## Exact patch replay on Aswin

Pinned repository commit: `5dd7d4dc79e26f9d9e039681d6bb42f385378c7b`.

The submitted `test.patch` and `solution.patch` were copied byte-for-byte to Aswin and replayed in a new detached worktree. Host compilation used Aswin's Rust toolchain and C compiler shim. No Docker build was used.

Results:

- `./test.sh base`: exit 0, 1 passed.
- clean repo plus `test.patch`, `./test.sh new`: exit 1, hidden test failed with the expected two compatible-pattern diagnostics.
- test patch plus `solution.patch`, `./test.sh new`: exit 0, 1 passed.
- `git diff --check`: exit 0.
- JUnit files were emitted for all three states.

## Deterministic prechecks

- Repository: 511 stars, MIT, supported Rust, active human commit within one day of qualification.
- Problem length: 175 words.
- Problem text: printable ASCII, no URLs, no hard wrapping, no em dash, no four-blank-line run.
- Test patch: unified diff, executable `test.sh`, distinct `base` and `new` modes, no dependency installation, no solution source.
- Test filename: randomized suffix `3856af`; no banned marker.
- Test and solution patches apply cleanly in order at the exact pin.
- Local Olympus problem search found no concrete-trait-object-pattern match.

## Current proof boundary

This is a minimal compile-time vertical slice for the early Scope Gate. It is not the hardened reference solution. Runtime identity checks, extraction, generic recovery, exhaustive hidden cases, flakiness, false-positive probes, solution-quality review, paid checks, and rollouts remain unrun and stale by design until the Scope Gate passes.
