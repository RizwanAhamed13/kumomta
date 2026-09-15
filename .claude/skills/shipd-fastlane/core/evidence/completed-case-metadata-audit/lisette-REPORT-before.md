# Lisette fresh offline benchmark

Fresh solution for ivov/lisette at dc060ecd16224ad01cdb8d7bafe89230e477446a. The original prompt was the only case-specific input before the first complete freeze. No historical solution was read; no paid or live check was launched.

The first complete package took **50m25s**, changes **19 production files (+485/-30 lines)** and adds **16 tests**:14 feature and2 adjacent regressions. The test patch adds517 lines including runner/configuration. A later own-validation revision adds one collision regression and changes no production code. The immutable first package remains separate.

First behavioral run: **11/14**, followed by one fixture correction batch. Three failed compile invocations required two source repair batches. No production behavior repair followed the initial behavioral run. Original failed fixtures/logs remain preserved.

| Clean state | Existing/adjacent | Feature |
|---|---:|---:|
| Base | 7449/7449 | — |
| Base + test | 7451/7451 | 0/14 |
| Solution | 7449/7449 | — |
| Solution + test | 7451/7451 | 14/14 |

First mutation pass: **6/7 killed**, with the collision survivor preserved. A complete valid type-name regression then killed that mutant. Revised replay: **7/7 killed**, reference **7451/7451 +15/15**, baseline **0/15**. Every replay has raw-event reconciliation, source restoration hashes and rebuilt CLI/test binary hashes.

Added executable line coverage on frozen-first: **381/391 (97.44%)** combined; **329/391 (84.14%)** from14 fresh feature tests; **196/391 (50.13%)** from7449 existing tests. **94 added lines lack executable mapping**, explicitly listed. Branch coverage was not measured.

Frozen image: Rust1.98.1, Cargo1.98.1, Go1.25.10, LLVM22.1.8. Compiler layer147.5s; image export1231.7s on shared HDD. Clean matrix containers690s total; coverage build/runs329s. Individual test/run timings are retained.

Archived test-only holdout: **25/25 passed on the first frozen solution**, with no repair. Unmodified archived runner took **72.0s**. Separate raw-event replay passed25/25, matched independently discovered test names, and reconciled both suites. The supplied test patch matches the initial benchmark bytes; accepted artifact-byte identity remains unverified.

Frozen runner compile errors use failure nodes. Verified runs have genuine libtest start/terminal events, so these receipts do not use that path. Future runners must distinguish setup errors and scope RUSTC_BOOTSTRAP to libtest to avoid Cargo cache churn.

See artifacts/, frozen-first/, revision-own-1/, evidence/final-metrics.json, evidence/workflow-lessons.json and raw logs/JUnit/inventories/gate receipts/mutation binary evidence/coverage summaries. Live eligibility, Scope/Verify, rollouts, platform review and acceptance remain unproven.
