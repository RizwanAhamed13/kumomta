# Solution Quality tuple/unit repair

Date: 2026-08-30

## Hosted verdicts on the preceding artifact set

- Test Quality: `PASS`, “all 32 logical test groups are fair; unfairTestCount is 0.”
- Solution Quality: `FAIL`, comprehensiveness `1/3`, code quality `3/3`. Blocking issue: “Tuple concrete patterns cannot match trait-object contents.” The grader demonstrated that tuples can implement traits and be erased, while the reference rejected a tuple pattern before lowering.

The root cause was a golden completeness defect plus an incomplete requirement ledger. The problem's broad “existing pattern syntax” contract included tuple and unit patterns, but the ledger enumerated only nominal constructors and literals. The prior alignment graph therefore proved consistency against an incomplete model; it did not prove semantic completeness against every repository pattern form.

## Scope-preserving repair

The public description now explicitly names class, struct, enum, tuple (including unit), and literal forms. This makes the existing scope precise; it does not exclude or weaken any former behavior.

The reference now:

- finds a unique compatible erased tuple or unit implementation by tuple arity and the full trait arguments/associated bindings;
- rejects absent, incompatible, or ambiguous tuple implementations;
- records the resolved concrete tuple type for specialized component checking and lowering;
- performs the existing concrete-shape test before extracting the tuple payload;
- expands tuple rest patterns for exhaustiveness analysis using the resolved arity;
- keeps tuple/unit patterns over trait objects open-ended.

The hidden suite adds one two-backend runtime scenario covering tuple, unit, mismatch, scalar and managed-reference fields, typed compatibility, rest, identity, mutation, and forced collection. Four isolated compile probes cover tuple trait-argument mismatch, associated-binding mismatch, same-arity ambiguity, and open-world exhaustiveness. Filenames use the independently generated suffix `0b8de1`.

## Executed evidence on Aswin

Environment: host `aswin`, LXC `podspub27`.

- M18 / old-reference discriminator: the preceding reference plus the new tuple runtime file failed under Cannon with tuple-expected diagnostics (`OLD_STATUS=1`).
- Repaired reference build: `cargo build --locked -p dora` passed.
- Repaired new mode: 37 tests, 0 failures, valid JUnit.
- The trait-argument and associated-binding rejection fixtures were replayed with empty `main` functions; each exited exactly 1 from the pattern incompatibility alone, with no independent call-site or cast error.
- Clean base: 14 tests, 0 failures, valid JUnit.
- Clean new: exit 1, 37 tests, 18 failures, valid JUnit.
- Repaired base: 14 tests, 0 failures, valid JUnit.

The complete matrix was replayed again after the isolated-fixture cleanup on final `test.patch` SHA-256 `312bee013aceee1f5f92c68735bcd1e6eab64ccea002d2f4db03cb577346ed81`: clean base 14/14, clean new exit 1 with 18/37 failures, solved base 14/14, and solved new 37/37.

The failure and pass occur on the same public tuple behavior, so M18 is a proven, fair discriminator. The hosted Test Quality PASS and Solution Quality FAIL belong to the preceding artifact hashes and are stale after this problem/test/solution edit. Both graders must rerun on the repaired bytes before a current hosted-green claim.
