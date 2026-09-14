# Auto Review nested heterogeneous specialization repair — 2026-08-30

## Preserved verdict

> The description is clean and the tests are strong with one minor direct-pattern preservation gap. The implementation is broad and coherent across both backends, but valid nested trait-object matches can crash exhaustiveness checking because the top-level workaround leaves old homogeneous-column assumptions active at nested depths. Revision is required.

## Classification and scope

- Root cause: golden/reference defect plus one prompt-stated preservation-test gap.
- Public description SHA-256 remained `26d9c364c2afd044a405946ca6a7144dfd1dd72b27321921c6b635b8bdeb16c6`.
- Dockerfile SHA-256 remained `a3785c4e9ca467422e24ec28add06b617abf4477b7455f786a442ddd8c449063`.
- No production requirement was added or removed. The two new discriminators exercise the existing nested-pattern, constructor/literal, mismatch-fallthrough, and backend-parity clauses. The four added base pattern groups preserve the already stated direct-value behavior.

## Reproduction and repair

The exact previous reference was reproduced on Aswin in LXC `dora-autoreview-mutants-20260830`.

- M23: `Envelope(One(x))`, then `Envelope(Two(x, y))`, then `_` exited 101 during frontend compilation because unrelated class constructors both exposed local variant ID zero and the old specializer asserted arity 2 equals 1.
- M24: `Envelope(One(x))`, then `Envelope(7)`, then `_` exited 101 at the old constructor/literal `unreachable!()` branch.

The repair passes full `ConstructorId` identity into constructor specialization and treats unrelated constructor/literal rows as nonmatching instead of impossible. Both discriminator programs pass under Cannon and Boots. Existing direct Bool, Char, String, and new direct unit programs also pass under both backends.

## Exact current artifacts

- `test.patch`: `10bdb408b770baea92bd98a44332ea3733cc3ce0937334c6dfea6a84deb5abef`
- `solution.patch`: `fb7f9e860d9f9b11e523e81e971df71541078dda79f3d2e70b618ccb5fe04d07`

## Exact four-state evidence

Executed on Aswin against pinned commit `5dd7d4dc79e26f9d9e039681d6bb42f385378c7b`:

| State | Mode | Result | JUnit |
|---|---|---:|---|
| test patch only | base | 45/45 pass | `v13-testonly-base.xml` |
| test patch only | new | 0/22 pass, 22 fail | `v13-testonly-new.xml` |
| test + solution | base | 45/45 pass | `v13-solved-base.xml` |
| test + solution | new | 22/22 pass | `v13-solved-new.xml` |

## Graph lesson

The earlier graph enumerated nested constructor and nested literal behavior separately, but it did not represent **same-column composition** after the feature made formerly homogeneous exhaustiveness columns heterogeneous. The graph now has two mandatory cells:

1. nested heterogeneous constructor identities/arity;
2. nested constructor plus literal specialization.

The analyzer is fail-closed when a nested pattern contract and exhaustiveness solution path exist without these composition cells. This prevents isolated feature-family nodes from falsely implying their interactions are covered.

## Staleness

All hosted Verify Solution, Test Quality, Solution Quality, Holistic, Auto Review, and rollout results attached to older test or solution hashes are stale. The local exact four-state proof and structural validation are current; hosted graders must rerun on these bytes.
