---
name: olympus-artifact-builder
description: Design and build aligned Shipd/Olympus challenge artifacts for a qualified candidate. Use for the complete pre-Scope reference solution and executable hardness proof, frozen problem and solution artifacts, reduced Scope Gate tests, expanded hidden tests, Dockerfile, and offline test runner.
---

# Olympus artifact builder — stages 5-5b and 6-10

This is the artifact-construction phase of `$olympus-workflow`. Keep the original stage numbering and firing order. Fill each prompt block's placeholders, apply its packaged laws, and complete its handoff before advancing.

Before editing artifacts, read [the shared laws](../olympus-workflow/references/shared-laws.md), [the platform contract](../olympus-workflow/references/platform-contract.md), [the state schema](../olympus-workflow/references/state-and-proof-schema.md), [the lessons ledger](../olympus-workflow/references/lessons-ledger.md), [the hardness calibrators](../olympus-workflow/references/hardness-calibrators.md), and [the local validation gates](../olympus-workflow/references/local-validation-gates.md) completely. Verify that stages 1-4 have a PASS handoff for the exact repository and pinned commit. Stop after stage 5b and route to `$olympus-scope-gate`; resume stage 6 only after a current Scope Gate PASS bound to the frozen full `problem.md` and `solution.patch`, or a current explicit user override recorded by `case_state.py record-scope-override`.

## 5. Complete reference and executable hardness proof

```
GOAL: implement and prove the full natural <TASK> before any Scope Gate request.
LAW: shared Candidate and Artifact laws + lessons L03, L08, and L10.

Write the complete behavioral contract and the complete working reference solution. A skeleton, partial implementation, or estimated line count cannot PASS this stage. Exercise the real production paths with focused deterministic probes, measure effective production logic from the implemented diff, and repeat the duplicate-work audit against the pinned commit.

The frozen contract is the complete natural repository task, normally the complete accepted issue rather than a convenient sub-bullet. For FEATURE-PIONEER work it is the complete finite behavior implied by the source-evidenced seam. Do not drop a material subsystem, semantic barrier, lifecycle phase, compatibility rule, or state transition to make the Scope Gate package smaller. Record exclusions only when repository evidence proves they are independent future work rather than part of the capability.

Then run an ARCHITECTURE-COMPRESSION CHECK against the working implementation. Ask whether a competent solver can reduce the task to a named checklist, follow compiler errors from one edit to the next, or express the implementation as add/propagate/serialize/replace. Produce and execute at least three complete-looking wrong implementations or mutations and record the deterministic public behavior that separates each. When available and free, obtain one or two blind solution plans from clean context; use them to learn convergence, not to predict platform pass rate.

Compare the actual implementation against every accepted calibrator in `hardness-calibrators.md`, including Dora, and identify the two closest architectural analogues. PASS requires the shared hardness floor, an 8/10 or stronger architecture score, and comparable cross-cutting depth to those closest accepted tasks.

RETURN: complete full-scope contract | complete working solution | executable probe results | every-accepted-task calibrator matrix and two closest analogues | files touched | modules crossed | measured real-logic lines (no blanks, comments, imports, braces, tests) | distinct behaviors | invariants spanning 2+ subsystems | three executed wrong architectures or mutations | the single biggest shortcut | architecture-compression verdict | duplicate-work verdict.

VERDICT: PASS / REJECT / CARVE (name what to drop). On PASS, freeze the exact bytes of `problem.md` and `solution.patch`. If the implemented task compresses below the accepted hardness envelope, reject or carve and rerun this stage; do not proceed to Scope Gate.

Record successful `full-reference` and `hardness-proof` proofs with exactly `--depends-on problem.md --depends-on solution.patch`. They must remain valid while only gate or post-gate tests change.
```

## 5b. Build the frozen-solution, reduced-test Scope Gate package

```
GOAL: package the already-proven full <TASK> for Scope Gate while reducing only the test set.
LAW: shared Artifact law and exact-byte law. Use the current live panel for Scope Gate fields and eligibility.

ALL 4 files filled, none missing: `problem.md` and `solution.patch` are the exact frozen full-scope bytes from stage 5; Dockerfile is statically valid for untouched-source build and offline runtime; and `test.patch` contains executable `test.sh` plus the fewest real, preferably parameterized gate scenarios.

Map every material requirement to its full solution path and observable oracle in `scope-gate-map.json`. A row may be `GATE_COVERED` or `POST_GATE_TEST_EXPANSION`; the latter defers only additional hidden-test coverage, never production behavior, description scope, or solution code. Every row must have an inspected full production path and passing focused evidence. Collectively the gate-covered scenarios must cross at least three architectural subsystems and two semantic barriers, and include at least one base-fail/solution-pass transition.

PROVE on Aswin before upload, without requiring Docker: base fails the reduced new tests, the complete frozen solution passes them, focused affected base regressions pass in both states, and the full-reference and hardness proofs remain current. Docker build and evaluator-container proof begin only after a current live Scope Gate PASS.

Checkpoint the gate package with `case_state.py`. Run `validate_submission.py --pre-scope` with current compliance evidence, `hardness-proof.json`, `scope-gate-map.json`, a blind predicted-test-path list, and the structured local-review report described in `local-validation-gates.md`; then run the local reduced four-state matrix. Preserve the successful validator result and transition evidence as the `scope-gate-prechecks` proof depending on all four current artifacts before checkpointing stage 5c. Hand off to `$olympus-scope-gate` only when every required local row is PASS and all live-only rows are explicitly marked unproven. Do not continue to stage 6 unless a live Scope Gate PASS exists for the frozen full `problem.md` and `solution.patch`, or the user directly instructs the current task to override it and that instruction is recorded against those exact bytes. An override leaves Scope Gate unrun and supplies no gate evidence.
```

## 6. Expand tests only

```
GOAL: expand the hidden-test coverage for the already-frozen full reference solution.
LAW: shared Artifact law + lessons L06 and L10.

PRECONDITION: stage 5c Scope Gate PASS bound to the frozen full `problem.md` and `solution.patch`, or a non-stale `scope-gate-override` record containing the current user's explicit instruction for those exact bytes. If both are absent, stop and route to `$olympus-scope-gate`. If overridden, continue in `REVIEW`, label Scope Gate `NOT RUN — USER OVERRIDE`, and keep every gate-dependent claim unproven.

- Edit `test.patch` and test evidence only. Expand each `POST_GATE_TEST_EXPANSION` row into deterministic hidden tests and strengthen mutation discrimination.
- Keep `problem.md` and `solution.patch` byte-for-byte fixed. Do not add production behavior or repair the solution here.
- If either frozen artifact must change, return to stage 5, invalidate the executable hardness and Scope Gate proofs, and request a new Scope Gate after the full implementation is proved again.
- Repeat the duplicate-work audit if new test evidence reveals an existing equivalent implementation.
- Build the evaluator Docker image at stage 10 after the expanded tests and patch split stabilize; no pre-Scope image is assumed.
```

## 7. Complete and audit the expanded hidden tests

```
GOAL: tests that only a real solution passes.
LAW: shared Artifact and Validation/FP laws + lessons L04, L05, L07, and L12.

- Round-trip oracle wherever possible: feed output back through the repo's own reader, compare parsed VALUES. Never exact bytes, never exact error text.
- For every failure path, add an error-contract row to the two-way map: grounding source | exact representation, existing category, or rejection only | promised post-failure observation. If an enum variant or payload layout exists only in the golden, do not match it. Assert the existing category only when the contract promises that category; otherwise assert rejection and the public state/result that must remain correct.
- 100% fail at base, 100% pass with the frozen reference. No timing, no ordering, no randomness, no network.
- Cover every promised behavior + obvious edges. Test NOTHING the description doesn't state or the repo doesn't show.
- Enough input variety that hardcoding costs more than solving.
- Enough independent cases that a partial solution fails loudly.
- No comments in hidden test files or `test.sh`; keep the harness self-explanatory through naming and structure. A required shebang is allowed.
- For a scalar-to-vector or single-to-composite migration, inventory every legacy singular consumer before writing cases: parsing/validation, catalog versioning and export/reopen, local and persistent uniqueness, no-index fallback, lookup/MERGE/update/delete, optimizer uniqueness assumptions, batch/COPY deduplication, and relationship endpoint binding. Cross declaration order against schema order and cross relevant equality classes against each distinct uniqueness path; do not assume one encoder covers them all.
- Preserve existing named/reordered property binding when adding positional endpoint components. Include overlapping endpoint property names or self-reference when those are valid public schemas, and require unique internal aliases without asserting those aliases.
- Apply the three coverage rules in 14c step 4b (all four boolean cells, strictly between tested points, statement shapes) WHILE WRITING. A stoolap suite already hardened against 3 FPs failed all three and gave up 6 more, and assertions added late stale every check already paid for.

OUTPUT: tests + a two-way map (description sentence -> tests that pin it). An unpinned sentence or an unstated assertion are both bugs - fix before returning.
```

## 8. Audit the frozen description

```
GOAL: verify that the frozen `problem.md` remains fully aligned with the expanded tests.
LAW: shared Artifact law. Follow the current live panel's description limits. When it gives no tighter rule, target 150-230 words and cap at 250. Use behavioral maintainer prose, normally without code, headings, bullets, or examples. Prefer printable ASCII unless the contract itself requires Unicode. Open with the ask ("Add ..."). Clarity and fair grounding outrank a proxy word count.

Do not edit `problem.md` in this stage. If an edit is required, return to stage 5 and invalidate the hardness and Scope Gate proofs.

SELF-CHECK before returning. Any failure returns the case to stage 5 rather than authorizing an edit here:
- Any sentence saying HOW instead of WHAT?
- Any list of cases that all derive from one principle?
- Any API named that tests could live without?
- Would a maintainer plausibly have typed this as an issue?
```

## 9. Generate the patches

```
GOAL: solution.patch + test.patch for <REPO> at <COMMIT>.
LAW: shared Artifact, exact-byte, and Validation/FP laws.

- solution.patch remains the exact frozen source changes + existing-test updates established at stage 5.
- test.patch = new hidden tests + test.sh. Zero solution code inside.
- LF-only endings. test.sh mode 100755 inside the diff.
- Banned words scan, word-bounded: olympus | shipd | datacurve | quest | challenge | mars. Patches must read like a normal PR.
- PROVE both patches apply cleanly on a fresh base checkout - alone and together.

OUTPUT: the patches + the exact verification commands run.
```

## 10. Dockerfile + test.sh

```
GOAL: the offline harness for <TASK>.
LAW: shared Artifact law. Check the live panel for the currently allowed base-image prefix and runner interface.

Dockerfile: FROM the currently allowed `olympus-base-<lang>:latest` image; never add an `@sha256` digest. Record the resolved digest in evidence. WORKDIR /app. Every dependency installed at BUILD time - runtime has zero network and zero IPv6. No tests in build. Builds WITHOUT patches. Reproduce the evaluator's unprivileged user, UID, login shell, cache permissions, locale, and toolchain environment. Ends CMD ["/bin/bash"]. If a normal patch can touch generated sources, preload the exact generator/runtime and its inputs for offline rebuilds.

test.sh: modes base|new + --output_path JUnit XML. base = real regression tests for the touched architecture, scoped to deterministic cases that work offline; an unrelated smoke test is not enough. No fail-fast. No -skip (filter by -run/name instead). Accumulate exit status, never mask it. Emit valid per-test XML on setup/build failure, but keep discovered test identity and the underlying command failure visible. Rebuild once under an all-build lock or in a mode-specific tree; never let base/new race on a shared tree.

PROVE: image builds, base passes, before handing off.
```
