# Review-v3 repair audit

- Exact artifact set: `db75b1c6c1165e4152756d7052246a9d4f23f84460293a8c0c4aa451432a310d`.
- Pinned source: `dc060ecd16224ad01cdb8d7bafe89230e477446a`.
- Fairness repair: Amber now asks whole-package analysis to reject each forbidden field shape and separately checks that the recovered AST retains the following `Tail`. It does not require parser-stage errors.
- Base repair: base mode excludes only `local_source::tests::gate_keeps_old_stamp_when_eviction_fails`, an unrelated Unix permission test that passed both prior complete workspace runs and failed once in the hosted evaluator. All other normal workspace targets remain enabled.
- Test-only new mode: 20 tests, 16 failures; exit 1.
- Reference new mode: 20 tests, 0 failures; exit 0.
- Test-only base mode: 9,052 tests, 0 failures, 0 errors; exit 0.
- Reference base mode: 9,052 tests, 0 failures, 0 errors; exit 0.
- Previously adjudicated genuine Batch-82 Nova 2 replay: 20 tests, 0 failures; exit 0 with an isolated worktree and target directory.

The first focused Amber command used the platform-qualified JUnit name and discovered zero tests; it is excluded. The corrected Rust filter discovered one test and passed.

One attempted standalone permission-test reproduction in the persistent Cloud Shell clone was invalid because the linker crashed with a transient bus error before producing a test executable. It is excluded. The classification instead rests on two prior complete 9,053-test passes on the same pinned repository plus the single hosted failure.

No Docker build or paid action was run during this repair.
