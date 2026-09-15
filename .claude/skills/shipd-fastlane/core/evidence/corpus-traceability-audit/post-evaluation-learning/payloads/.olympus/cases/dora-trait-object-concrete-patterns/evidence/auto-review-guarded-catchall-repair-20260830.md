# Auto Review guarded catchall repair — 2026-08-30

## Preserved verdict

> The description and implementation are clean and substantive. Revision is requested solely because the tests omit the central guarded-catchall exhaustiveness case, allowing a plausible incorrect implementation to pass.

## Classification and scope

- Root cause: prompt-stated test gap.
- `problem.md`, `solution.patch`, and `Dockerfile` are unchanged.
- No behavior was added or removed. The repair crosses the already stated wildcard/variable catchall requirement with Dora's existing guard semantics.
- Error contract: rejection only. The tests require normal compile status 1 but do not inspect diagnostic wording.

## Fair paired discriminator

Two logical tests each compile a positive and negative source:

1. unguarded wildcard compiles; otherwise identical guarded wildcard rejects;
2. unguarded variable compiles; otherwise identical guarded variable rejects.

The positive half prevents a status-only rejection from passing on the unimplemented base. The pair also allows any conforming diagnostic and implementation strategy.

## M25 executable proof

Mutation: remove `arm.cond.is_none()` from the trait-object catchall scan so any wildcard or variable counts as exhaustive.

- Reference: all 24 new logical tests pass.
- Exact mutant: the 22 former new tests pass; only `guarded-wildcard-exhaustiveness` and `guarded-variable-exhaustiveness` fail.
- Test-only base: both paired logical tests fail because even their unguarded positive controls cannot use concrete trait-object patterns.

Evidence: `v14-mutant-new.xml`, `v14-testonly-new.xml`, and `v14-solved-new.xml`.

## Exact four-state matrix

| State | Mode | Result |
|---|---|---:|
| test patch only | base | 45/45 pass |
| test patch only | new | 0/24 pass, 24 fail |
| test + solution | base | 45/45 pass |
| test + solution | new | 24/24 pass |

Current hashes:

- `problem.md`: `26d9c364c2afd044a405946ca6a7144dfd1dd72b27321921c6b635b8bdeb16c6`
- `test.patch`: `d9a36d89425c57a060eefc28520571167cc8a54935acedf3ae03e8f1f5586064`
- `solution.patch`: `fb7f9e860d9f9b11e523e81e971df71541078dda79f3d2e70b618ccb5fe04d07`
- `Dockerfile`: `a3785c4e9ca467422e24ec28add06b617abf4477b7455f786a442ddd8c449063`

## Graph lesson

The previous graph modeled catchall representation and usefulness but omitted the Boolean `guarded × unguarded` dimension for both wildcard and variable forms. The reusable analyzer now requires all four cells whenever a trait-object contract combines guards, wildcard/variable catchalls, and exhaustiveness. Missing any cell blocks alignment.

All hosted checks and rollouts attached to the previous test hash are stale and require rerun. The current local matrix and M25 proof are exact-byte evidence for this artifact set.
