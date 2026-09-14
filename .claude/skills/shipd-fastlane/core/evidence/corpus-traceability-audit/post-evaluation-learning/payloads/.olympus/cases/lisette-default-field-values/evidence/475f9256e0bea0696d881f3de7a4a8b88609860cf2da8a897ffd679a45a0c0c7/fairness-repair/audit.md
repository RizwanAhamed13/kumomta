# Generated-name fairness repair

Artifact set: `475f9256e0bea0696d881f3de7a4a8b88609860cf2da8a897ffd679a45a0c0c7`

## Root cause

`Test Fairness` failed 1 of 32 checks because the collision test enforced generated-name hygiene while the problem did not state that invariant. This was a **prompt gap (tested, unstated)**. The runtime oracle itself was valid and had already been proven against the exact reference and FP candidate.

## Repair

- Added one behavioral sentence: `Adding a default must not turn otherwise valid user declarations into generated-name collisions.`
- Renamed the hidden test from its rollout-specific `b90_...` name to `indigo_defaults_preserve_user_declaration_names`.
- Kept the source identifier and runtime oracle because they are now one representative input for an explicit hygiene contract.
- Did not mention helpers, symbol spellings, collision-pass internals, or a lowering strategy.
- Did not change `solution.patch` or `Dockerfile`.

The assertion is now prompt-stated and architecture-neutral: a solver may inline defaults, allocate fresh names, reuse collision machinery, or use any other strategy, provided valid user declarations still compile and run.

## Exact replays

Google Cloud Shell, non-root, pinned commit `dc060ecd16224ad01cdb8d7bafe89230e477446a`, Rust 1.97.0, Go 1.25.10:

| State | Focused hygiene test | Full new suite |
|---|---:|---:|
| exact Batch 90 FP candidate | exit 101; duplicate `LisetteDefaultConfigCount` | not rerun; focused test is decisive |
| exact reference | 1/1 pass | 21/21 pass |
| preserved genuine Batch 88 Nova 10 | 1/1 pass | 21/21 pass |

Logs and JUnit are stored beside this audit as `fairness-*.log`, `fairness-*.exit`, and `fairness-*-new.xml`.

Clean application of the renamed `test.patch` alone and together with the unchanged reference solution passed, followed by `git diff --check`.

## Advisory suggestions

- **True cache-hit parity:** prompt-stated and useful, but advisory to this fairness result. Existing tests cover cache creation, stable diagnostics, and cold/rebuild runtime equality; a dedicated positive cache-hit discriminator should be considered in the next completeness pass rather than mixed into this one-assertion fairness repair.
- **File-order invariance:** prompt-stated and useful, but advisory. The current suite exercises a later-file declaration; a two-order equivalence test can be considered in the next completeness pass.

No advisory test was added here, avoiding unreviewed scope expansion while repairing the sole blocking fairness finding.

## Status

Local alignment audit: **PASS** for the repaired assertion. Removing the added hygiene sentence would again unground the test, so it is fairness-dependent and not redundant. The hosted Test Fairness result remains stale until rerun on this exact artifact set.
