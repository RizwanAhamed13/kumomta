# Prove what actually ran

A green process is not enough. Preserve a test-discovery inventory independently of the JUnit report. For libtest, use the selected executable's `--list` output before execution and record the filter and binary hash. For custom runners, enumerate selected fixture IDs from the runner's discovery phase before running them. Do not generate the inventory by reading the completed JUnit.

Use canonical IDs `classname::name`. A discovery JSON has a nonempty `tests` list and an optional `excluded` list of objects with `id`, `reason`, and prompt/repository `grounding`. Exclusions remain unverified until the [partition gate](partition-result-gate.md) resolves them against a complete independently discovered inventory and matching source/executable identity. Required integration cannot be excluded to make the result green.

Run on the designated builder:

```sh
python3 <plugin-root>/scripts/test_result_gate.py --junit evidence/combined.xml --inventory evidence/combined-discovery.json --events evidence/combined.jsonl --event-classname project.tests --exit-code 0 --expected pass --output evidence/combined-reconciliation.json
```

Repeat for each required matrix selection. For expected baseline failure, pass the real nonzero exit code and `--expected fail`. The gate checks complete selected execution, duplicate and unexpected IDs, counters, XML validity, skipped cases, harness errors and process/report consistency. A failure to compile the test harness is an API absence or environment observation, not an executed behavioral fail-to-pass witness. A candidate-language compiler diagnostic can be the public behavior under test when an executing harness asserts the expected diagnostic; retain the test identity, diagnostic and prompt grounding. Add a baseline-compatible behavioral witness where the contract permits it; otherwise keep the limitation explicit and block any gate requiring behavioral discrimination.

Every assertion failure still needs semantic triage. A panic is not automatically a clean mutation kill. A signal-terminated process is a harness failure even if some assertion terminals were emitted before it died. Distinguish a deliberate public panic contract from an unrelated compiler/runtime crash. This reconciliation tool checks the supplied reports for consistency; it cannot authenticate arbitrary files or prove execution from XML alone. Actual assertion quality, prompt coverage and private grader results remain separate.

Preserve raw events captured directly from the test process, the actual command/exit, binary hash and independent discovery. For Rust libtest JSON, add `--events <events.jsonl> --event-classname <canonical-classname>`; the gate reconciles start and terminal outcomes and rejects fabricated JUnit failures with no executed events. Every started test must have a terminal outcome, including starts absent from the XML; libtest ignored terminals may legitimately lack a preceding start, while a selected ignored test still fails the selected-execution check. Other frameworks require a reviewed native adapter and direct execution evidence. A receipt without raw evidence remains provenance-unverified even if XML consistency passes. The current script can return `EXECUTION_RECONCILED` for an XML-only consistency check: inspect `raw_event_evidence` and `execution_provenance`, not the status label alone. For libtest execution evidence, supply both event arguments in the example and require reconciled raw events; even that checks consistency rather than authenticating arbitrary files.

When a suite is split, follow [partition-result-gate.md](partition-result-gate.md). Do not call individually passing subsets a complete pass before their union matches independent full discovery. Harness compiler/setup failures remain errors with zero executed tests, and expected baseline assertion failures require prompt-grounded behavioral triage.

## Coverage with a denominator

Measure the same selected changed executable lines under existing tests and expanded tests. Retain raw profiles, toolchain/LLVM versions, exact commands and source/patch hashes. Report covered/mapped counts and unmapped added lines separately. A whole-file percentage includes unrelated legacy code and does not substitute for changed-line coverage. New lines with no instrumentation are not silently counted as covered. Report unavailable branch/JIT instrumentation explicitly.

Use the prompt's public forms and semantic roles to build a requirement matrix before implementation. Include interaction witnesses such as tuple-rest patterns used through both `is` and `match`; a successful isolated feature test does not prove every consumer. Low test LOC triggers this review, never padding.

## Prevent expensive first failures

1. Before constructing artifacts, run a small pinned-source baseline smoke with the chosen toolchain and capture the real compiler version. Rust source can require features absent from the nominal image compiler. Pin a compatible toolchain; keep the required base-image `:latest` tag.
2. Apply `test.patch` to untouched base immediately. Recheck after adding new APIs or context hunks. Test both patch orders and compare resulting source bytes when both orders are supported by the platform.
3. Match repository fixture conventions: parsed offsets can omit leading fixture whitespace; rendered labels can depend on existing parentheses; result collections can include multiple public kinds. Confirm fixture semantics before changing production code to satisfy a mistaken expectation.
4. Inventory AST constructors and every consuming backend before adding a syntax field or bytecode. Exercise allocation/register conventions in every required backend.
5. Keep fake UUIDs, retry counters and speculative winners deterministic. Test actual branch semantics. Serialize shared-port fixtures or allocate isolated ports; classify unavailable database integration explicitly.
6. Parse JUnit during runner development. Sanitize forbidden XML control characters while retaining raw logs. Reconcile discovery before accepting counters.
7. Install compiler-matched LLVM tools and their shared libraries before coverage; smoke their version and profile compatibility first.
8. Set RUSTC_BOOTSTRAP only on the libtest process when JSON output needs it, not globally on Cargo; changing Cargo-visible environment can invalidate reusable dependencies.
9. Record setup, compilation, image export/unpack and test execution separately. On the current shared HDD, export can dominate compilation. Reuse a development container/cache for iterations and build the frozen delivery image after convergence. Never use stale pre-patch binaries. After restoring a frozen source tree between mutants or patch states, refresh affected source mtimes or clean affected packages; verify rebuilding and record the executable hash. Identical source hashes alone do not invalidate a timestamp-based build cache. Shared-load observations are not controlled speedup benchmarks.

10. Supervise the thermal watcher independently throughout each long operation. A guard process can exit before work completes; pause the exact owned container and retain the pause result. Persist the first test outcome before cleanup, so a failed stop or watcher wait cannot erase it. Follow [thermal-safety.md](thermal-safety.md).

These checks come from fresh-case development and held-out replay during the September 12 benchmark. First attempts, harness repairs, production repairs and post-holdout revisions remain separate. The nine-case trial is still in progress; no success-rate improvement has been established.

Exact first-run results and validation limits are recorded in [fresh-execution-findings.md](fresh-execution-findings.md).

Precreate nested host evidence directories before a root container writes into a bind mount, or send host-side gate reports to an existing writable directory. A launcher must propagate a failed reconciliation gate after persisting its native result; outer exit zero alone cannot establish success. If reporting fails after native tests complete, preserve the first error and reconcile the unchanged raw evidence separately without rerunning already-passing tests.
