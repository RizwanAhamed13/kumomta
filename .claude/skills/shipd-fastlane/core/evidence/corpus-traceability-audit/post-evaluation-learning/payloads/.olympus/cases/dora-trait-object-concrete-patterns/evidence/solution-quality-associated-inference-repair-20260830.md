# Solution Quality repair: associated inference and bytecode invariants

Date: 2026-08-30

## Classification

The hosted Solution Quality failure identified two reference defects on the prior artifact set: a prompt-stated semantic role was missing from the golden, and two new bytecode consumers lacked the neighboring verifier invariant. Neither defect is related to the Docker/runtime-network failure. `problem.md` remains unchanged.

## M08 discriminator

The existing generic runtime fixture now includes a trait with no ordinary type arguments, an implementation whose generic parameter appears in its associated type, and a trait-object scrutinee whose `Item=Int64` binding uniquely determines that parameter.

- Previous reference, Aswin Docker, Cannon: exit 1 with `Pattern does not match type AssociatedOnly[Item = Int64]`.
- Repaired reference, same fixture: Cannon 1/1 PASS and Boots 1/1 PASS.
- This is the existing `A_GENERIC` scenario and the existing R1 compatibility contract, not a new task requirement or a new hidden file.

## Golden repair

- `dora-frontend/src/sema/matching.rs`: expose the repository's existing contextual type matcher within the `sema` module.
- `dora-frontend/src/sema/impl_matching.rs`: match associated-type equalities before rejecting unresolved implementation parameters. This lets associated equalities bind parameters, then retains the existing all-bound and ambiguity checks.
- `dora-bytecode/src/verifier.rs`: assert `trait_ty.is_trait_object()` in both `TestTraitObjectType` and `LoadTraitObjectValue`, matching `NewTraitObject` before either backend consumes object layout.

## Aswin evidence

Backend: `aswin`, LXC `podspub27`, disposable Docker container `dora-sq-repair-20260830`, network disabled.

- Fixed Rust sources pass toolchain `rustfmt --check`.
- Offline Cargo build of Dora, frontend, runtime, startup, and Boots compiler: PASS.
- Targeted associated-only generic fixture: Cannon PASS, Boots PASS.
- `cargo test --locked -p dora-bytecode`: 20 passed, 0 failed.
- Solved `test.sh` JUnit: base 14 tests, 0 failures; new 37 tests, 0 failures.
- Previous-reference discriminator: failed as expected before the repair.

## Alignment-v2 result

The strengthened role/invariant graph now reports PASS with 1.0 description, test, solution, and triad coverage; no incomplete semantic roles; no architecture-invariant blockers; and no orphan clauses, assertions, or test files. This result is alignment-only. Hosted Verify Solution, Test Quality, Solution Quality, and every downstream dependent result remain stale until rerun on the repaired artifact hashes.
