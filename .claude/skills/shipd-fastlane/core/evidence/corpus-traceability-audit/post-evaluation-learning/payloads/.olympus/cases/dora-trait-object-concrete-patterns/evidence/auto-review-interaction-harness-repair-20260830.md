# Auto Review interaction and harness repair — 2026-08-30

## Preserved verdict

> Revision is required because the suite misses a promised, material nested Boolean exhaustiveness case. The solution otherwise implements the feature comprehensively, with one confined usefulness-warning regression, one harness reporting-status issue, and a minor formatting cleanup.

## Root-cause classification

- Nested Boolean exhaustiveness: promised-but-untested interaction cell. The prior graph joined `R4_OPEN_WORLD` to a nested-constructor assertion and to literal assertions, but did not require their composition: `outer constructor × erased field × finite Boolean literals`.
- Alternative usefulness: adjacent-analysis regression. The prior graph recorded exhaustiveness and usefulness as roles, but a coarse role edge did not prove recursive alternative expansion on the trait-object-specific route.
- JUnit reporting: harness failure-path omission. The happy writable-output path passed; no graph node required injected failure of parent creation, XML emission, or final status propagation.

The public problem description is unchanged. These repairs enforce existing scope and preserve existing repository behavior; they do not add a new feature contract.

## Exact artifact set

- commit: `5dd7d4dc79e26f9d9e039681d6bb42f385378c7b`
- problem.md: `26d9c364c2afd044a405946ca6a7144dfd1dd72b27321921c6b635b8bdeb16c6`
- test.patch: `4f0b187e57ad3cd369888d54b74f7f09e414434667fa9604d33ffbad764f626c`
- solution.patch: `9558963bacc46f4e8de4c2fc792b10d4a6f62e478b8c5533105e0ec238f5c201`
- Dockerfile: `a3785c4e9ca467422e24ec28add06b617abf4477b7455f786a442ddd8c449063`

## Exact four-state proof on Aswin

| State | Base | New |
|---|---:|---:|
| test patch only | 37/37 pass | 0/18 pass; 18/18 fail |
| test + solution | 37/37 pass | 18/18 pass |

Evidence: `dora-auto-base-before-v12.xml`, `dora-auto-new-before-v12.xml`, `dora-auto-base-after-v12.xml`, and `dora-auto-new-after-v12.xml`.

Focused solved probes:

- nested Boolean match: normal compile rejection status `1`, with missing `Envelope(_)` reported;
- `_ | _` followed by `_`: compile status `0`, exactly two `warning: unreachable pattern.` diagnostics;
- `./test.sh --output_path /dev/full new`: status `1` after all 18 tests passed;
- `./test.sh --output_path /proc/dora-no-parent/report.xml new`: status `1` after all 18 tests passed.

## Executed discriminating mutations

### M21 — close the nested Boolean literal domain

Mutation: in `convert_pattern`, force Boolean `Pattern::Literal` to `open: false` instead of propagating the erased input's open flag.

- exact reference: nested Boolean fixture exits `1` as required;
- mutant: nested Boolean fixture exits `0` and reports zero non-exhaustiveness diagnostics;
- result: killed by `nested-bool-open-exhaustiveness-rejection`.

### M22 — restore the top-level catchall shortcut

Mutation: replace `check_trait_object_useful` with the former direct-`Pattern::Any` matrix scan.

- exact reference: usefulness fixture exits `0` and emits two unreachable-pattern warnings;
- mutant: fixture exits `0` and emits zero warnings;
- result: killed by `catchall-usefulness-regression`.

Both mutations were compiled and executed on Aswin in the `dora-autoreview-mutants-20260830` LXC environment. They are bounded to the two verified Auto Review defects.

## Graph repair

`alignment_graph.py` now fails closed on:

1. blind, prompt-grounded analysis-interaction cells absent from the authored audit;
2. missing values or assertion/solution/evidence bindings for those cells;
3. missing injected-failure probes for output-parent creation, JUnit emission, and final status propagation.

The graph deliberately does not manufacture a full Cartesian product. Only finite interaction cells independently derived from the prompt and repository block, keeping the hardening bounded and avoiding speculative over-hardening.

## Staleness

The local structural, four-state, focused mutation, formatting, and harness-failure proofs above apply to the exact hashes. Hosted Test Quality, Solution Quality, Auto Review, rollouts, and any other platform result that saw earlier test or solution bytes remain stale and must be rerun before a readiness claim.
