# Test Quality repair v22

Repository: `scylladb/scylla-rust-driver`  
Commit: `611d43b595fb0ad7010f2bdbd887acae3d962d65`  
Artifact set: `a2a6e8b446653f27cc32e742a5d34a54322c75660c716cde79971b9b326576de`  
Execution: `aswin`, LXC `ladybug-olympus`

## Root cause

The v21 Rustdoc opacity oracle accepted private named and tuple structs but still selected only a public path whose Rustdoc item kind was `struct`. The prompt requires an opaque public `PagingContinuation` type, so a public type alias resolving to an opaque private carrier is conformant.

Classification: **unfair implementation-kind pin**.

## Repair

The oracle now selects the exact public path without requiring an item kind, resolves local type-alias chains with cycle and unresolved-target rejection, and applies the existing opacity test to the resolved carrier.

Accepted representations:

- direct private named-field struct;
- direct private tuple struct;
- public alias to either private named or private tuple carrier.

Rejected representations:

- direct or aliased structs with public representation fields;
- unit/no-state carriers;
- cyclic, unresolved, external, or non-struct alias targets.

## Executed evidence

- Oracle probes: seven expected outcomes matched exactly.
- Clean matrix: base 1/1 before and after; new 0/13 before solution and 13/13 after solution.
- Preserved genuine Nova 2, Nova 4, and Nova 8 solutions: each 13/13 PASS.
- Canonical `test.patch` is byte-identical to the Aswin-validated patch.

## Advisory coverage dispositions

- Current-routing re-evaluation: PROMPT-STATED, advisory/unproven; no discriminating survivor supplied, so no edit.
- Second token/table routing point: PROMPT-STATED, single-point advisory; no proven current-suite survivor, so retained as a hypothesis.
- Nonzero explicit shard suppression: PROMPT-STATED, single-point advisory; no proven discriminator, so no edit.
- End-to-end manual shard retention: PROMPT-STATED, advisory/unproven; no candidate/reference discrimination, so no edit.
- Prepared automatic policy rejection: PROMPT-STATED, advisory/unproven; no candidate/reference discrimination, so no edit.

## Remaining blocker and stale proofs

`VALIDATOR20-PRODUCTION-TEST-SCAFFOLD` remains open: the workspace validator rejects feature-gated fixtures and inline tests placed in production-source paths. This v22 repair does not address that independent packaging constraint.

Because `test.patch` changed, hosted Test Quality, Verify Solution, solution/test/description quality, Auto Review, Docker/offline verification, grader-loop, and prior rollout claims are stale for the new artifact set. The v22 clean matrix and three saved-solver replays are current.
