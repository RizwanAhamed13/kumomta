# Build a complete test patch without wasting iterations

Use this procedure when generating, expanding or repairing `test.patch`. A short patch may contain a strong parameterized suite, or it may miss most of the contract. Inspect its behavioral obligations and discovered cases before deciding which. Do not impose a LOC target, duplicate assertions, or add requirements to inflate the patch.

## Plan coverage before writing tests

Read the prompt and pinned public interfaces independently of the reference solution. Record `inventory_sources` in `contract.json`, with exact prompt sections and repository commit/path references. Enumerate the public input families and meaningful semantic roles for each requirement. Then trace the relevant production paths to find branch and integration risks. Do not derive the inventory solely from the tests or solution diff.

Use [contract.example.json](../../../assets/contract.example.json) as a schema example, replacing its fictional requirements. Every applicable input-family × role cell needs an assertion witness. A `covers` entry declares the complete cross-product of its lists; use separate entries for sparse combinations. A scalar write and a composite read do not cover a composite write or a scalar read.

Represent genuinely inapplicable cells with `excluded_cells`, each containing `input_class`, `role`, `reason` and `grounding` (`kind`: `prompt` or `pinned-repository`, plus `source`). Inspect these decisions against the source. Missing coverage, runtime cost or an inconvenient implementation are not applicability reasons.

Review four risk families across the requirements: boundaries, errors/recovery, compatibility and interactions. Under each `risk_review` key (`boundary`, `error`, `compatibility`, `interaction`), list the relevant `scenario_ids`. When a family genuinely does not apply, record `not_applicable: {reason, grounding}`. One superficial example does not discharge all the risks in a family; enumerate each distinct contract-relevant failure mechanism.

Each `scenarios` entry has an ID, ordered `steps`, public `observable`, `grounding`, required `covers` cells and one concrete `test_id`. That test must execute the whole scenario and assert its result. A parameterized ID must identify the executed parameter case or a verified set executing that entire scenario for every declared input. Separate tests for the beginning and end cannot prove continuity of state.

## Grow the suite from missing behavior

After the authorized Scope Gate, expand the representative slice into the complete suite. Build shared public-API fixtures first, then parameterize independent input families and boundary values. Keep dedicated integration tests for transitions that need shared state in one execution. Use stable unique test IDs and show expanded parameter counts from actual runner discovery.

For each relevant family, cover normal behavior and its distinct failure mechanisms. Depending on the actual contract, these can include empty/singleton/multiple values, exact type/precision boundaries, rejected input with preserved state, legacy behavior, alternate public entry points, persistence/reopen, retry/fallback and subsequent consumption. Do not blindly require every item for every candidate.

Historical examples:

- **Scylla:** test `resume → preferred target rejected → fallback wins → next page uses the winner` in one scenario. Separate retry and next-page tests missed this connection. Isolate each policy predicate with sibling eligibility predicates satisfied; a disabled node can mask a broken latency predicate.
- **Rust Analyzer:** put a nonidentifier correspondence before a valid identifier in the same expansion and request actual completion. Separate expansion tests do not exercise the traversal-order failure. Preserve baseline-valid safety checks in base mode.
- **Storage cases:** write mixed values through each required public writer, commit/reopen and read multiple consecutive records. Assert exact values and identity so an offset or key-order defect cannot pass by accident.

These are historical risk patterns, not new mandatory product requirements. Consult [accepted patterns](accepted-patterns.md) and the cited lesson records only for relevant cases.

## Separate the Scope slice from full-suite readiness

Plan the full coverage obligations early; write the expanded suite only at the Forge stage that permits it. Preserve the reduced Scope patch and its hash in evidence. Keep the current platform artifact named `test.patch` in the canonical delivery directory and explicitly label its stage in the handoff.

For the reduced slice:

```sh
python3 <plugin-root>/scripts/contract_check.py contract.json --stage scope
```

`DECLARED_SCOPE_SLICE_PASS` permits declared omissions and lists them in `deferred_to_full`. It validates metadata consistency only; Forge still determines whether the slice is representative and executable. A pending scenario may have `test_id: null` until its test exists. An unknown `scenario_id` is a malformed plan, not a deferred test.

Before calling the expanded patch complete:

```sh
python3 <plugin-root>/scripts/contract_check.py contract.json --stage full
```

Full is the default. It fails on missing cells, missing whole-scenario witnesses, missing risk reviews and missing inventory sources. Older contracts must add these fields. Its `DECLARED_COVERAGE_PASS` means only that declared obligations have declared witnesses; it cannot inspect assertions, prove that all public forms were inventoried, or certify any runtime coverage.

## Prove the generated patch on the builder

Apply the exact delivery patches to the exact clean commit on `shipd-local`, using the active Forge four-state procedure. Reconcile contract test IDs against actual runner discovery and JUnit: include expected/discovered/executed/passed/failed/skipped counts and parameter IDs. Resolve every missing, unexpectedly skipped or undiscovered required test. Keep baseline-valid checks in base and establish the feature-dependent public prerequisite for new tests.

On the reference solution, measure changed production line and branch coverage with the repository's supported tooling when practical. Target affected packages and required integrations; record tool/version, commands, exact artifact hashes and covered/total denominators. Review uncovered contract-relevant branches and add a discriminating case or justify unreachable/inapplicable code. If instrumentation is unavailable, report coverage as unmeasured and use explicit path witnesses; never substitute declared-cell percentages for measured coverage. Instrumented timing must be separate from normal Verify Solution timing.

For each critical failure mechanism, use a small targeted incorrect implementation or saved false-positive candidate: the reference must pass and the probe must fail the specific public assertion. Prioritize missing predicates, first-item-only handling, wrong ordering, stale state/cache and omitted propagation when relevant. Distinguish a behavioral kill from compilation/harness failure. A surviving meaningful probe is a coverage gap even if line coverage is high. Reuse still-valid probe evidence; do not run a broad mutation campaign by default.

Batch the confirmed missing tests, then run the required matrix once on the final bytes. Record test-only added LOC separately from fixtures/runner changes, actual case counts, applicable/witnessed cells, scenario witnesses, changed-line/branch coverage, probe outcomes, and runtime. LOC is a size diagnostic and trend; no minimum LOC or synthetic coverage target establishes readiness. Do not call the final suite complete while a required behavior, critical interaction or execution result remains unproven.

All candidate source inspection that needs a checkout, patch construction, instrumentation, tests and probes use the designated builder. Metadata checks can run on the Mac. Test edits stale affected validation, paid checks, rollouts and reviews; use fingerprint comparison and report the exact remaining gates. Paid execution still requires explicit authorization.

## Lessons measured during fresh reconstruction

Keep original-prompt solves separate from archive replay. Freeze the first complete four-file package, source commit, tests, matrix, coverage and probe evidence before opening historical tests. Record every first-run failure and timing. Later repairs get new artifact directories; never relabel their results as first-pass outcomes. Historical test bytes alone do not prove those bytes were manager-accepted.

Coverage needs an explicit denominator and attribution. Parse actual patch prefixes (including Git-configured i/w prefixes); reject an empty or unexpectedly partial changed-file mapping. Report added production lines, executable mapped lines, lines without counters and unresolved mappings separately. An uncovered executable line differs from a declaration without a counter. Report pinned-existing tests, fresh feature tests, fresh compatibility tests and their union separately. Use matching compiler/LLVM tools, per-selection profile directories and exact source/binary hashes. High union coverage can conceal a weak new suite.

A repair is incomplete until the unchanged compatibility suite and the clean four-state matrix pass on the repaired bytes. In rust-analyzer, a repair passed all fresh tests and then added an unintended completion keyword in an existing macro regression. The final matrix caught it. Preserve the failing repaired revision as evidence.

For archived failures, reproduce the untouched native runner first. If a fixture falls outside the original prompt, preserve its failure and show a separate minimal diagnostic for the in-scope form. Rust edition keyword tokens can differ from ordinary and raw identifiers; a syntactically similar fixture does not establish the same contract. Do not edit archived tests to manufacture a passing historical result.

A mutation counts as a behavioral kill only after proving that its changed source reached a rebuilt executable and that a stated public assertion failed. Compilation errors, harness failures, inactive transformations, crashes without a relevant diagnostic and missing tests are separate outcomes. Restore both source bytes and rebuild freshness; a restored source hash does not prove the last mutant binary was replaced.

For the bounded later-learning review of completed cases and its explicit unread scope, see [post-evaluation learning](post-evaluation-learning.md). Its historical examples do not replace prompt-grounded obligations or current gate evidence.
