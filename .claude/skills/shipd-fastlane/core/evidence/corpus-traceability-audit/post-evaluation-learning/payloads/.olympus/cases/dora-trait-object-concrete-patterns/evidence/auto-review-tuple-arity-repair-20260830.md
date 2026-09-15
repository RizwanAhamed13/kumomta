# Auto Review tuple-arity repair — 2026-08-30

## Verbatim verdict

> The description and tests are clean, and the implementation is substantial and mostly cohesive. Revision is required because nested trait-object tuple arms with distinct concrete arities can trigger a compiler panic in exhaustiveness checking.

## Classification

- Root cause: golden/reference solution defect plus one missing prompt-grounded regression.
- Scope disposition: unchanged. The existing description already names tuple (including unit), nested patterns, mismatch-before-payload behavior, and Cannon/Boots parity.
- Repair: retain tuple arity in `ConstructorId` during usefulness specialization; add one nested `Envelope(Inspect)` fixture with uniquely resolved two-field and three-field tuple implementations.

## M26 discriminator

The exact v14 reference compiled the new source on Aswin with:

`target/debug/dora compile --cannon test/rt/trait/trait-object-concrete-nested-tuple-arities-dfb210.dora -o /tmp/nested-tuple-arities-dfb210`

It panicked at the retained exhaustiveness assertion with `left: 3` and `right: 2`. After arity became part of tuple constructor identity, the same source passed through pytester under both Cannon and Boots. This is the smallest public discriminator for `M26_COLLAPSE_TUPLE_ARITY_IN_SPECIALIZATION`.

## Exact four-state matrix

Environment: Aswin `podspub27`, LXC `dora-autoreview-mutants-20260830`, exact test-only and solved host trees each mounted at evaluator-required `/app`.

| State | Mode | Result | JUnit |
|---|---|---:|---|
| test patch only | base | 45/45 pass | `v15-testonly-base.xml` |
| test patch only | new | 0/26 pass | `v15-testonly-new.xml` |
| test + solution | base | 45/45 pass | `v15-solved-base.xml` |
| test + solution | new | 26/26 pass | `v15-solved-new.xml` |

The failed attempt from `/app-testonly-v15` was discarded because the repository pytester requires `/app`; it was an environment-path error and is not used as evidence.

## Graph workflow repair

The previous same-column composition law varied arity only across different nominal constructors. That did not prove that kind-local metadata survived when the constructor family itself stayed constant. The reusable graph analyzer now requires a `same_tuple_family_distinct_arity` cell whenever a nested trait-object tuple contract changes exhaustiveness/usefulness. Its deterministic self-test remains 22/22, and the current v15 graph passes with 8 requirements, 41 assertions, 26 proven mutations, 16 semantic roles, no orphans, and full transition coverage.
