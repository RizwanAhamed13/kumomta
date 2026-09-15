# Solution Quality repair: impl eligibility and usefulness

## Hosted findings reproduced

The exact previous reference accepted `Missing(_)` although its only `impl Inspect for Missing` had the unsatisfied bound `where Int32: Bound`. The compile command exited 0. The same reference also emitted no warning for a second wildcard arm after an unguarded wildcard in a trait-object match. The pinned clean compiler emits `warning: unreachable pattern.` for that program.

These are golden defects. They cannot be repaired by changing `problem.md`: accepting the first would weaken the explicit implementation-compatibility rule, and accepting the second would bless a regression caused by the solution.

## Repair

`find_trait_pattern_type_matching` now validates every specialized bound from the candidate implementation's `TypeParamDefinition` with the repository's existing `implements_trait_with_context` path before accepting the candidate. Trait-object exhaustiveness remains open, but usefulness reports an arm as unreachable when an earlier matrix row consists entirely of erased `Any` columns, which represents an unguarded wildcard/variable catch-all. Open concrete constructors are not routed through the closed-domain usefulness algorithm.

## Executed discriminators

- M19 old reference: unsatisfied-bound fixture exits 0; repaired reference exits 1 with normal pattern/type rejection.
- M20 old reference: duplicate erased catch-all emits no warning; repaired reference exits 0 and emits the pinned `warning: unreachable pattern.` category.
- The attempted broad restoration of ordinary usefulness was rejected because it panicked on open tuple and literal constructor matrices. The final bounded repair preserves the diagnostic without that closed-domain assumption.

## Exact four-state matrix on Aswin

| State | Mode | Passed | Failed | Error | Skipped |
|---|---:|---:|---:|---:|---:|
| test-only | base | 36 | 0 | 0 | 0 |
| test-only | new | 0 | 18 | 0 | 0 |
| solved | base | 36 | 0 | 0 | 0 |
| solved | new | 18 | 0 | 0 | 0 |

The run used the exact pinned commit in separate Aswin `podspub27` containers derived from the prior frozen evaluator state. JUnit evidence is `dora-sq-base-before.xml`, `dora-sq-new-before.xml`, `dora-sq-base-after.xml`, and `dora-sq-new-after.xml`.

## Current artifact hashes

- problem: `26d9c364c2afd044a405946ca6a7144dfd1dd72b27321921c6b635b8bdeb16c6`
- test: `8b86d7fc7ac466d72955912192acb458a66472175a852da70c84869ea5f2b214`
- solution: `8c29cd003dbf88ea9de5b3819c95a99b4b6a0c89739de3d5f724fcfd42bf21dc`
- Dockerfile: `a3785c4e9ca467422e24ec28add06b617abf4477b7455f786a442ddd8c449063`
