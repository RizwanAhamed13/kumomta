# Prevent the next review cycle

Search `knowledge/lessons.json` for the case or terms below. It retains all 195 distinct dated ledger rows discovered in the September 12 audit, with every duplicate source location. These check families are a synthesis, not independent measured frequencies.

## 1. Build the contract before the test architecture

For patch generation and coverage expansion, use the concrete gates in [test-coverage.md](test-coverage.md). The checker validates applicable input/role cells and one test witnessing each whole scenario; the full-suite status is distinct from the reduced Scope status.

Inventory public forms independently: accepted syntax/API variants, value families, call sites, compatibility behavior and externally visible failure/recovery. Then connect requirement → public boundary → input family → semantic role → assertion → production path → exact execution evidence. A graph derived from the tests can be perfectly connected and still omit a whole family.

Choose interaction cells by semantic risk. For a stateful feature, include failure → recovery → nonterminal state → next consumer within one scenario. Add reopen, transaction commit/rollback, mixed row origins, cold/warm paths, inverse operations, repeated positions and nonadjacent order where the contract requires them. Do not substitute isolated happy-path examples for these transitions.

Keep every sibling eligibility guard true while isolating one failing guard. A negative test must first establish a valid feature-dependent state, or the baseline may reject it for an unrelated reason. Preserve an independent conforming implementation when checking whether the oracle overfits the reference.

## 2. Separate base from new behavior

Every new-mode test must have a public prerequisite absent from the baseline and a documented fail-to-pass reason. Baseline-valid rejection/preservation belongs in base. IDs and discovery must be disjoint between modes. Inspect discovered test inventories, not just filenames. If a base-only prerequisite is skipped for a new case, record why and prove the new assertion still discriminates.

For each new test, retain its baseline failure type and solution success. Compilation failures caused by broken harness packaging do not prove behavioral discrimination. A proposed false-positive probe must fail the accused solution and pass the reference on a stated requirement; also retain known genuine passes.

## 3. Choose a fair observable oracle

Prefer public behavior, required public schemas and pinned regression contracts. Exact internal error enums, storage counters, AST snapshots, printer spacing, private opaque ownership layouts or documentation word windows are unfair unless specifically mandated and justified. Review unrestricted English documentation semantically; reserve structural checks for required paths, identifiers, schemas and links.

Preserve repository scalar equality rules; do not invent NaN/signed-zero policy. Check DECIMAL/INT128 precision beyond binary64 and differences between bulk-loading and uniqueness paths. For ordering, vary insertion/mutation order and persisted reopen. For storage evolution, cover every writer/version predicate and at least two consecutive records where boundary errors could hide.

For compilers and runtimes, trace each producer, encoding, decoder, verifier and runtime consumer. Cover child arity/identity, guarded and catchall constructors, exhaustiveness and object lifetime when relevant. For FFI, validate producer-private types, absence/error channels, real serialization and callbacks across the ABI. For generated output, cover cold/warm caches, default/flag routes, architecture widths and content-based invalidation.

For asynchronous systems, observe automatic behavior; manually invoking the expected callback can mask the bug. Distinguish disabled topology from lower priority. Use real protocol round trips for observable wire behavior. Cover acknowledgement/negative acknowledgement and metrics in every required lane. Replace sleeps with observable readiness and deterministic deadlines.

## 4. Validate the delivered runner as a public interface

Before expensive execution, verify the live-required `base` / `new` and output-path CLI forms, including supported option order. JUnit must contain actual per-test results, stable unique IDs, accurate failures/errors/skips and a nonempty intended suite. Successful setup is not a passing test. Preserve the real process status and treat failing XML as failure even if the wrapper exits zero.

Exercise missing output parents, failed commands, missing XML, malformed XML/ANSI control characters, and final wrapper status. Synthesize failure XML only for a missing result, retaining diagnostics; never overwrite a real suite with an empty success. Capture individual timings and total runtime.

## 5. Make clean delivery a gate

Freeze exactly `problem.md`, `solution.patch`, `test.patch` and `Dockerfile` in one canonical directory. Include the runner in the artifact form required by the live panel. Hash all four. Use standard `a/` and `b/` diff prefixes; inventory intended new/untracked files before patch creation. New hidden test names need a task-specific random six-hex suffix; when a fixture basename is fixed, isolate its parent path.

Apply only the delivered patches to the exact pristine commit on the designated builder. Check solution/test path collisions and ensure the harness never overwrites a natural implementation module. Hydrate dependencies and compile from the actual artifact-only state, including native headers, exact lockfiles and generated sources. A development checkout success is insufficient.

Use `fastlane.py preflight` for a small static subset. Its PASS does not replace patch application, runner interface checks, allowed-image verification, baseline/solution execution or the Forge grader loop.

## 6. Repair once per confirmed failure family

Create a finding record with receipt hashes, public requirement, reproducer, root-cause family, affected adjacent roles, proposed fix and invalidated evidence. Verify the finding is current before touching code. Batch related confirmed fixes; do not repeatedly reapply stale review comments.

After an edit, compare fingerprints, rerun affected checks plus any mandatory full matrix, and replay saved accused and genuine solutions when the oracle changed. Keep historical official pass rates separate from new local replay rates. Exclude infrastructure-invalid runs from behavioral conclusions and report denominators.

Do not repeat a paid gate until there is new evidence addressing its cause and the user authorizes that gate. A repeated unchanged failure is a reason to revisit the hypothesis or retire the candidate, not consume another batch.

See the [Ladybug storage repair example](repair-case-study.md) for a concrete writer/header mismatch introduced by a partial repair, and the unfair version-number assertion that followed.
