# Verify Solution gate-classification repair — 2026-08-30

Pinned commit: `5dd7d4dc79e26f9d9e039681d6bb42f385378c7b`

## Hosted root cause

The repaired compiler and runner completed successfully: the hosted solved run reported 14/14 existing regression groups passing and all 37 challenge behavior groups passing. The gate still failed because, without `solution.patch`, 19 clean-rejection groups already passed. Verify Solution requires every testcase reported by `new` to fail, error, or skip before the solution.

Those 19 groups assert preserved rejection behavior for incompatible, ambiguous, and non-exhaustive patterns. They are therefore pass-to-pass regression checks, not feature-unlocking fail-to-pass checks.

## Repair

Only `test.patch` changed:

- the same 19 rejection commands and names moved unchanged from `new` to `base`;
- the 18 positive Cannon/Boots runtime groups remain in `new`;
- no fixture, assertion, expected exit status, problem requirement, solution code, or Dockerfile changed;
- `materialize` removes only the generated `target/debug/dora-boots-compiler` before repository-native bootstrap, allowing the model user to recreate it instead of failing during `shutil.copy2(...).copystat` on the root-owned image artifact.

The authoritative hosted partition proves the corrected gate shape deterministically:

| State | Mode | Expected groups | Result implied by the exact hosted testcase outcomes |
|---|---|---:|---|
| test-only | base | 33 | 14 existing + 19 rejection groups pass |
| test-only | new | 18 | all 18 positive feature groups fail |
| solved | base | 33 | all 33 pass |
| solved | new | 18 | all 18 pass |

## Focused execution

On Aswin (`podspub27`) with the Docker-baked compiler state and platform-like model user, the corrected base mode emitted valid JUnit with `tests="33" failures="0"`. Bootstrap completed without the prior `PermissionError` or traceback, and one source-key materialization stamp was created.

Structural validation passed: 29 test-patch files, 31 solution files, and 718 estimated effective production LOC. Alignment graph v8 passed with 1.0 description, test, solution, and triad coverage; it reported no blockers, incomplete roles, orphan clauses, or orphan tests.

## Staleness

Because `test.patch` changed, the earlier live Scope Gate, Verify Tests, Verify Solution, Test Quality, flakiness, false-positive replay, and downstream reviews are stale. The platform must rerun them against this exact artifact set.
