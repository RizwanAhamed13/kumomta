---
name: olympus-offline-validator
description: Harden and validate a Shipd/Olympus challenge package before upload. Use for the local four-state and offline matrix, flakiness checks, solver calibration, red-team analysis, mutation-based false-positive probes, and adversarial quality, fairness, FP, description, and solution graders.
---

# Olympus offline validator — stages 11-14e

This is the local validation and adversarial-grading phase of `$olympus-workflow`. Keep the original stage numbering and firing order. Fill each prompt block's placeholders, apply its packaged laws, and complete its handoff before advancing.

Before validation, read [the shared laws](../olympus-workflow/references/shared-laws.md), [the evidence-first execution contract](../olympus-workflow/references/evidence-first-execution.md), [the platform contract](../olympus-workflow/references/platform-contract.md), [the state schema](../olympus-workflow/references/state-and-proof-schema.md), [the lessons ledger](../olympus-workflow/references/lessons-ledger.md), and [the local validation gates](../olympus-workflow/references/local-validation-gates.md) completely. Verify the Scope Gate PASS or explicit user-override record plus the artifact-builder handoff, and hash all four current artifacts. When overridden, preserve `Scope Gate: NOT RUN — USER OVERRIDE` in every readiness report.

## 11. Validate locally (free - before any token)

```
GOAL: pass every paid check's local mirror for <PKG>.
LAW: shared exact-byte and Validation/FP laws. Run the complete local sequence below without skipping.

0. Run the evidence-first Phase 0 plus `case_state.py validate` and `validate_submission.py`. Fix state, repository-root, path, patch, runner, or test-discovery blockers before any image build.
1. Build image from an LF-clean base archive.
2. 4-state matrix in isolated worktrees and separate build caches: base passes with and without solution; new FAILS without, PASSES with. Reproduce evaluator ordering: build the Docker image from untouched source, then apply tests/solution at runtime. Before either runner mode consumes compiled output, prove every Docker-baked executable and self-hosted/generated compiler is rematerialized from the applied source. Record pre-patch and post-materialization hashes or decisive build traces; never let a direct `target/...` invocation consume an image-time binary.
3. Patch sanity in-container: apply --check both, banned-words scan, CRLF scan.
4. Flakiness: first eliminate randomness, wall-clock and sleep dependence, ordering, shared caches, locale/timezone, CPU-count, concurrency, mutable process/external state, temporary-file collisions, and resource contention by inspection. Then run the repetition count required by the live panel; if none is specified, use six clean repetitions for each required state as the default. Record why the count is sufficient and stop on any variance.
5. Offline: build + touched tests under --network none.
6. Complete `requirements.json`, `mutation-inventory.json`, the manual repository-native/no-shortcuts solution review, and structured grader records; run `validate_evidence.py`; then produce the reviewer bundle.

For generated-code repositories, add a clean-rebuild proof: remove the affected object/library and compile from the delivered patch with the runtime network disabled. Verify source grammar/schema, checksum, generated parser/code, and serialized tables agree. For wrapper-backed tests, validate the XML after a forced compile failure and prove base/new cannot race on one mutable build tree.

OUTPUT: every command + exit code. Any variance = stop, fix, rerun. Nothing paid until this is green.
```

## 11b. Six operational controls

```
These cost stoolap three false-positive rounds and two days. Each one is a plain instruction, no judgement needed.

1. EVERY BEHAVIORAL FIX SHIPS WITH A DISCRIMINATOR, SAME EDIT.
   A golden fix for promised behavior needs an assertion or executable probe that fails the broken behavior and passes the reference. A harness, environment, permissions, metadata, or out-of-scope maintenance fix instead needs a focused reproduction/check at that layer; do not manufacture a hidden behavioral requirement merely to satisfy this rule.

   Rollout FP fixes require one more gate: the exact accused candidate must fail the discriminator while the exact reference and all preserved genuine solves pass. Until then, keep the report as an open hypothesis and do not change the hidden contract.

2. ANY FINALIZED EDIT INVALIDATES ITS DEPENDENT PROOFS.
   During one repair batch, use the smallest affected test or probe to iterate. Once the bytes stabilize, rerun the whole dependent set exactly once before handoff: patches apply, four-state, required flakiness repetitions, baseline, regression, format/lint, agent replay, and mutation inventory. For the four-state check, parse each JUnit case and require zero pre-solution passes in `new`; a baseline-valid rejection check is P2P and belongs in `base`. Never carry an old result forward, but do not repeatedly rebuild unchanged layers while isolating one failure.

3. KEEP PER-CASE OPEN ITEMS. BLOCKERS MUST BE EMPTY BEFORE READY.
   Put every deferred, downgraded, advisory, or minor finding in `open-items.json` with evidence and disposition. A blocker closes only through current execution evidence or proof it is invalid. Print the per-case file at handoff; never use the portfolio registry as the blocker list.

4. KEEP EVERY AGENT SOLUTION. REPLAY THEM ALL AFTER EVERY EDIT.
   Save each run's solution-patch.patch forever. They are the only proof the task is still solvable and the only real pass-rate signal. A change that makes the genuine solver fail is a change you reverse.

5. MAINTAIN A REQUIREMENT-DERIVED MUTATION INVENTORY.
   Enumerate plausible omissions and wrong architectures from stable requirement IDs and every changed public execution path before free-form mutation hunting. Record killed, survived, invalid, and deferred mutants. A probe that becomes a test must still kill the exact mutant it was written for.
   Re-run each new test against the broken implementation it was written for. The stoolap CTE probe used the same table pair and caught the bug; the test written from it used two different pairs, collided with nothing, and two agents shipped that exact bug as false positives.

5b. RUN THE BLIND-INVENTORY AND BOUNDED FP-PROOF GATES.
   In a fresh context, read only the problem, pinned repository, and frozen natural contract; write schema-v2 `independent-inventory.json` before reading tests, solution, or authored ledgers. Inventory roles plus finite contract dimensions. Reconcile it into schema-v3 `alignment-audit.json`, enumerate every Cartesian cell, trace public-entry -> production-decision -> observable execution paths with repository-graph evidence, and separately classify each oracle's assertion form and presentation constraints. Block on omitted roles, dimensions, cells, execution paths, unfair presentation constraints, or low-level operations. Then rank FP hypotheses and execute at most three probes per repair batch. An empty matrix cell is advisory until a concrete prompt-grounded mutant passes the exact current suite. Add a discriminator only when the exact reference passes, the mutant fails, and all preserved genuine solves pass. An open proven gap blocks; speculation does not.

6. RUN THE PARAMETERIZED VERIFIER AND PRESERVE ITS OUTPUT. THAT IS THE HANDOVER.
   Run `validate_submission.py`, the case-owned full matrix adapter, and `case_state.py validate`. They print or preserve the gate blocks. No current script output means no claim of done.

   Prefer the plugin's parameterized validators plus a case-owned repository adapter. If a case-specific `verify.sh` exists, it must accept paths and hashes as arguments, reject the wrong repository root, and contain no previous-case absolute paths or fixed artifact hashes.
   `TASK_LANG=rust` (NEW_TEST / BASE_TESTS / SRC) or `go` (NEW_TEST / BASE_RUN / BASE_PKGS). Go ships no defaults on purpose: an empty test filter reports a green run over zero tests.
   Re-point it at the new task BEFORE writing the package. A script still aimed at the previous task grades nothing and says PASS.
```

## 12. Calibrate difficulty (blind runs)

```
GOAL: measure how hard <TASK> really is.
LAW: shared Difficulty and rollout law + lessons L07 and L08.

Give each of <N> agents: a clean base export (verify nothing leaked - no tests, no solution, no .git), the description ONLY, and "no git history, no web search". Grade by applying the hidden tests to their work in the container.

READ every transcript for three things:
- what they ALL skipped -> that shared omission is the difficulty dial
- any UNFAIR failure (ambiguous sentence, unstated requirement) -> fix the package
- their solution size vs golden -> agents finishing much smaller = task under the bar

CALIBRATION: the local rate does not predict the platform rate IN EITHER DIRECTION. music21 went 60% local -> 0% platform; versitygw went 1/3 local -> 24/26 platform, which is local under-predicting by three times. So never reason "I am at 2/3 locally, that is my ceiling" - it is not a ceiling, it is a different measurement. The only thing that moves the number is more runs on the real platform. Use local runs for what they actually tell you: WHY agents fail, not HOW MANY.

THE TWO NUMBERS THAT DECIDE THE SUBMISSION:
- AT LEAST ONE agent must solve it. Zero solves = cannot submit, no matter how good the task is. Solvability needs a witness, and that witness is a saved solution patch.
- Pass rate must meet the current live panel's ceiling. When the assignment targets a 30-40% band, aim for that band only after fairness and solvability are established. The target is a range with a hard floor, not "as low as possible". A task nobody solves is worth exactly zero.
```

## 13. Red-team pass (mentor's prompt - use verbatim, do not edit)

```
Imagine you're the agent and trying to solve this - and imagine you are trying to cheat this - what will you do? Imagine making a solution that passes the tests but don't really meet the requirements. If you can do that, then there is some gap in your prompt or tests. Using this as criteria I want you to scan the code for things like that and fix them.
```
Run it against the frozen package. Hunt: hardcoded outputs, special-cased inputs, stubbed oracle, harness detection. Every cheat found = a test gap - close it, rerun.

## 14. Mirror the AI graders (MANDATORY before EVERY upload)

Rule: **never let the platform be your test loop.** Skipping this on stoolap (2026-08-01) cost six upload rounds, each returning an AI-check finding a free local run would have caught. Fire 14a-14d as four PARALLEL subagents on the exact bytes about to be uploaded, fix everything they find, then RE-RUN THEM on the fixed bytes. Only then upload. 14e is a shorter fifth pass.

DO THE WHOLE LOOP IN ONE TURN. Fire all four at once, fix everything, re-verify, re-run them, repeat until clean - then report once. Never hand back a partial result or ask whether to continue: the author's time is the scarce resource, not tokens, and each grader finding is one step of one job, not its own round trip.

The re-run is not optional and it is the step that keeps getting skipped. Fixing 14c findings means writing NEW assertions, and new assertions are precisely what Fairness fails on - so the bytes that were graded are never the bytes you ship. If a full re-run is too slow, re-run 14b scoped to the assertions you added; never ship an assertion no grader has read.

Placeholders: `<PKG>` = submission dir (problem.md + test.patch + solution.patch + Dockerfile), `<REPO>` = repo clone at the pinned commit. Save each grader as the structured JSON record required by the state schema: exact prompt version, model/version when available, artifact-set identifier, timestamps, findings with stable IDs, cited lines, disposition, and raw output. Run graders in independent clean contexts; use model diversity when available and do not treat correlated agreement as executable proof. A clean rerun attached to old dependent bytes is stale.

**Paste this preamble at the top of 14a-14d - it is what stops a lazy PASS:**

```
STANCE: assume this package is flawed and your job is to find the flaw. A clean PASS is the LEAST likely outcome - the real platform graders return findings on nearly every submission. If you genuinely find nothing, you must list every item you checked and state why each one cannot fail; "looks correct" is not an answer. Never soften a finding to be agreeable. Never accept "it is discoverable from the repo" as a defence unless you cite the exact file:line. Quote exact lines for every objection. You are read-only: never modify anything under <PKG> or <REPO>; do all experiments in a scratch directory or a throwaway git worktree.
```

### 14a. Quality grader ("Problem and tests are good quality")
The one that returns ERROR and blocks. Its lethal item is #3: assertions that pin an internal choice the description doesn't mandate.

```
You are an automated code-review grader for a coding-challenge platform. Grade STRICTLY and adversarially. Do not be generous.

INPUTS:
- Problem description: <PKG>/problem.md (read from the "Task Prompt:" line down; lines above are metadata)
- Hidden test patch: <PKG>/test.patch
- Reference solution patch: <PKG>/solution.patch
- The repository at the pinned commit: <REPO> (READ ONLY - do not modify anything anywhere)

YOUR RUBRIC - grade each of these four, status OK / WARNING / ERROR, with a reason:
1. No test leakage: does the description reference test files/functions/logic from the patch?
2. Tests cover required behavior: does the hidden suite cover every behaviour the description requires?
3. Tests focus on behavior, not implementation details: flag any assertion that pins a specific internal choice (algorithm family, exact internal string, specific optimizer outcome, newly invented error variant, payload fields, or expected/actual orientation) that the DESCRIPTION does not require. A typed pattern match can over-specify just as much as a string comparison. This is the item that matters most - be harsh. Quote the exact assertion lines you object to.
4. Sanity: is the pair coherent and runnable?
5. SOLVABILITY TRAPS (highest value - do this one properly): find assertions that a CORRECT implementation could fail. For each assertion, ask "is there a reading of the description that a competent implementer would follow which makes this assertion false?" Typical traps: the test pins a value that depends on an internal choice the description leaves open (which estimate is compared, how the pre-execution decision is computed, which strategy a cost model returns), or requires a new concrete error representation where the contract promises only a category or rejection. These are worse than over-constraint because they make the task unfairly unsolvable. Report each with: the assertion, the conformant implementation that fails it, and the sentence of the description that permits that implementation.
6. ASSERTION-FORM AUDIT: for every documentation, diagnostic, formatting, or structured-output assertion, state whether it checks semantics, a prompt token, a repository token, exact representation, category, or rejection. Reject hidden synonym allowlists, paragraph/window colocation, and layout constraints without direct grounding. Execute at least two independently authored conformant alternative wordings or structures and prove the oracle accepts both. For routed compatibility, cross explicit/default sources with accept/reject outcomes. For public JSON integers, audit fixed-width decoding on 32- and 64-bit hosts and include a positive boundary above `u32::MAX`.
7. DIMENSION CROSS-PRODUCT: derive finite public axes before reading tests, then list every combination and its oracle. At minimum consider OS × architecture alias × target environment × explicit/default target for platform identity, and instrumentation × cache layer × profile state for replay/cache behavior. Do not mark a requirement covered from one representative cell.
   For workflows that produce an artifact and consume it later, separately cross producer and consumer stages with cold and warm cache states. Trace producer compile-time switches into cache identity and execute the warm-producer transition; a consumer-only cache test does not close the lifecycle.

Then give an overall verdict: PASS or FAIL. FAIL if any item is ERROR.

CRITICAL: for item 3, for EACH assertion you flag, state explicitly whether the description does or does not mandate that outcome, quoting the exact sentence from the description that does or does not cover it.

Report concisely: the four statuses, the exact quoted assertions you object to, and the verdict. Do NOT edit any file.
```

### 14b. Alignment / Fairness grader ("Problem and tests are aligned")
Mirrors how Test Fairness actually works: an agent reads the repo at the pinned commit and buckets every assertion. Any `UNSUPPORTED` is the failure.

```
You are an automated grader for a coding-challenge platform. Your single question: COULD A DEVELOPER PASS THE HIDDEN TESTS FROM THE DESCRIPTION ALONE (plus reading the repo)? Be strict and adversarial.

INPUTS:
- Description: <PKG>/problem.md (task prompt starts after the "Task Prompt:" line)
- Hidden tests: <PKG>/test.patch
- Repo at pinned commit: <REPO> (READ ONLY - modify nothing anywhere)

TASK: go through the hidden tests assertion by assertion. For EACH assertion, classify it as one of:
 - PROMPT-STATED (quote the exact sentence from the description that requires it)
 - REPO-DISCOVERABLE (quote the file:line in the repo that makes it discoverable)
 - UNSUPPORTED (neither - the test demands something a correct implementer could not know)

Any UNSUPPORTED assertion is a failure. Also flag any structural detail the tests rely on that the description never mentions (e.g. exact naming, ordering, formatting, identity of values).

For every error-path assertion, report its contract level explicitly: EXACT REPRESENTATION, EXISTING PUBLIC CATEGORY, or REJECTION ONLY. A new enum/class/variant name, payload type, field layout, or expected/actual orientation absent from both the prompt and pinned repository is UNSUPPORTED. A nearby repository error can ground the broad category or style, but cannot by analogy mandate a newly invented sibling representation. At category or rejection level, check that the suite asserts the promised observable aftermath instead of compensating with a stronger error-shape assertion.

Then check these axes explicitly - they are where solo reviews miss things, so name each one and say whether the suite exercises it and whether the description covers it:
 - DATA PROPERTIES the fixtures never vary: sortedness, empty inputs, duplicate keys, nulls, very large and very small cardinalities, values at exact thresholds
 - NESTING DEPTH: subqueries, CTEs, derived tables, unions - not just top-level statements
 - MULTIPLICITY: more than one candidate construct in a single statement
 - anything asserted in exactly ONE scenario (single points of failure in the suite)

Report: a compact table of assertion -> classification -> evidence, then a list of every UNSUPPORTED item, then verdict PASS/WARNING/FAIL. Do NOT edit any file.
```

### 14c. FP panel judge (the hard gate - run this one even if the others pass)
Not "is the reference correct" but "could a BROKEN solution pass". The stoolap panel found two FPs after a solo probe sweep declared the package clean.

Before free-form hunting, load `requirements.json` and `mutation-inventory.json`. Cross every stated input class and changed execution path with omission, boundary, boolean-cell, routing/shape, persistence/order, conversion/serialization, error-contract, hardcoding, and agent-derived mutation classes. Do not let the golden's architecture determine the entire inventory; accept alternate conformant decompositions.

```
You are a false-positive review judge for a coding-challenge platform. Your job: find a BROKEN-BUT-PLAUSIBLE implementation that would PASS the hidden tests while VIOLATING the problem description. Be maximally adversarial and creative.

INPUTS (all READ ONLY - do not modify any file anywhere):
- Description: <PKG>/problem.md (prompt starts after "Task Prompt:")
- Hidden tests: <PKG>/test.patch
- Reference solution: <PKG>/solution.patch
- Repo at pinned commit: <REPO>

METHOD:
1. List EVERY distinct requirement the description states.
2. For each requirement, find the hidden test assertion(s) that enforce it. If a requirement has NO enforcing assertion, that is a false-positive gap - report it.
3. Then think like a lazy implementer: describe concrete shortcuts, omissions, or hardcodings that would satisfy all hidden tests but break the stated contract. For each, say exactly which requirement it violates and why no test catches it.
4. Pay special attention to: data properties the tests never vary (sortedness, empty inputs, duplicate keys, nulls, very large/small cardinalities), nesting depth (subqueries, CTEs, unions), multiple joins in one statement, and anything only checked in ONE scenario.
4b. Three coverage rules that a suite hardened against 3 earlier FPs still failed, yielding 6 more. Walk them explicitly and name the cells you find empty:
   - ALL FOUR CELLS of every boolean pair. Covering (true,true) and (true,false) leaves `left := right` undetectable - the untested cell is exactly where a substitution hides.
   - STRICTLY BETWEEN the tested points. A boundary case plus a far-past case lets a truncated or rounded comparison pass everything; find a value inside the gap.
   - STATEMENT SHAPES, not just clause shapes. Aggregation, GROUP BY, ORDER BY, DISTINCT, and a subquery in the SELECT list vs the WHERE clause each route the feature differently. A contract asserted only on bare projections is a contract on bare projections.

5. DO NOT STOP AT REASONING - PROVE IT BY EXECUTION. This is the step that separates this pass from a solo read-through, and skipping it is why a manual probe sweep once cleared a package the real panel then failed twice. For each candidate gap:
     a. make a throwaway git worktree of <REPO> at the pinned commit (never touch <REPO> itself)
     b. apply <PKG>/test.patch, then apply <PKG>/solution.patch
     c. MUTATE the reference source to introduce exactly that one defect - the smallest edit that breaks the requirement while leaving everything else intact
     d. run the hidden suite
     e. if it still PASSES, the gap is PROVEN and you report it; if it FAILS, the suite already catches it - discard the hypothesis and say so
   Report only proven gaps as findings; list disproven hypotheses separately so the reader knows what was ruled out.
6. VALIDITY RULE for any extra test you propose: it must be FAIR and DISCRIMINATING - the broken variant fails it AND the unmodified reference passes it. If both fail it is NOT a false positive, but do NOT drop it: the reference violates its own prompt and no test noticed. Report every one of these in a separate "reference defects" section with the query that exposes it - this is how a real bug in solution.patch gets found, and burying it as out-of-scope nearly shipped one.

Report: (a) requirements with no enforcing assertion, (b) PROVEN broken implementations that pass the suite, each with the exact mutation you applied and the run output, ranked by how likely a real agent is to write them, (c) for each, the minimal extra test that would catch it, verified fair and discriminating, (d) hypotheses you disproved. Do NOT edit anything under <PKG> or <REPO>.
```

### 14d. Description check ("contains only necessary information")
The one that scores `request_changes` on 3 items OR any single HIGH. Its bite is the opposite direction from 14b: it wants wording DELETED that 14b wants kept, so the second pass below is not optional - it is what stops the two graders looping against each other.

```
You are the automated "Description contains only necessary information" grader for a coding-challenge platform. Grade STRICTLY.

INPUTS:
- Description: <PKG>/problem.md (task prompt starts after the "Task Prompt:" line; lines above are metadata and are NOT graded)
- Repo at pinned commit <BASE>: <REPO> (READ ONLY; if the worktree has a solution applied, read the true pinned tree with `git show <BASE>:<path>`)
- Hidden tests <PKG>/test.patch - for the dependency check ONLY, see below

TASK: produce a REMOVAL list. For every sentence, clause or phrase that should be removed, report it tagged HIGH / MEDIUM / LOW with the reason. Categories:
 - facts findable in the codebase (cite the exact file:line at the pinned commit)
 - obvious defaults a competent developer assumes anyway
 - over-specified return types / formats / naming beyond what is needed
 - redundant phrasing: two sentences saying the same thing, or a clause restating an earlier one

SCORING, state explicitly at the end:
 - 3+ removal items, OR any single HIGH -> request_changes
 - 1-2 medium/low -> minor_suggestions
 - 0 -> approve

CRITICAL SECOND PASS, reported separately: for EACH removal item, open test.patch and check whether any hidden assertion DEPENDS on that wording. If deleting it would leave an assertion ungrounded (nothing in the prompt and nothing at the pinned commit would tell an implementer that behaviour), mark it "REMOVAL WOULD BREAK FAIRNESS". Also flag items that must be removed TOGETHER or not at all.

Report: (1) removal list with tags and reasons, (2) the fairness-dependency pass, (3) the score. Do NOT edit any file.
```

Deleting a prose transcription of a public constant is usually safe IF the prompt keeps a pointer to it ("the existing X threshold") - that moves the assertion from PROMPT-STATED to REPO-DISCOVERABLE, which Fairness accepts. Deleting it bare is what reopens a fairness hole.

### 14e. Solution-quality pass (short)

```
Review <PKG>/solution.patch as a maintainer of <REPO> at the pinned commit. Flag: code that does not match the repo's own patterns, changes unrelated to the stated feature, dead or unreachable surface, new lints the clean tree does not already have, and any test function added by the solution patch (must be ZERO). Report findings with file:line. Do NOT edit any file.
```

**Acting on the results:** an `UNSUPPORTED` (14b), an FP gap or reference defect (14c), or any HIGH (14d) is a blocker - fix it. Put every accepted test fix in the correct logical scenario; prefer an existing scenario, but allow a new isolated test when no existing scenario reaches the path or clarity requires it (block 16 step 5). Test Fairness coverage suggestions are advisory: triage each against the prompt and pinned repository before accepting it, and do not widen the contract merely to consume a suggestion. When 14b and 14d point opposite ways on the same sentence, 14b wins: keep the wording, or replace it with a repo pointer. A 14a item #3 objection has exactly two honest fixes: relax the assertion, or add a genuinely intended public requirement to the description. Choose relax unless the precise outcome is independently necessary to close a known FP. For an arbitrary error representation chosen only by the golden, keep the promised category/rejection and state-safety assertions; do not rescue the pin by documenting the golden's variant. Before stage 15, record current successful proofs named `local-validation`, `requirement-map`, `mutation-inventory`, and `grader-loop`, then require `case_state.py validate --for-stage 15`.
