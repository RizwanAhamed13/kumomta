# Local validation gates

Read this reference during candidate audit, artifact construction, and offline
validation. It records the free checks extracted from the Task Creation &
Validation Guide. These checks strengthen local evidence; they never stand in
for a live Scope Gate, VCS+, hosted Quality Check, Auto Review, rollout, or
submission result.

## Candidate-time checks

Before ranking a repository:

1. Enumerate every governing license file and package/workspace license field,
   including vendored or separately licensed source that will be part of the
   submitted repository. Every applicable license must be on the current live
   allowlist. A permitted root license does not override a disallowed nested
   license.
2. Inspect the repository's native test surface for deterministic structure,
   stable focused filters, offline feasibility, and useful per-test identity.
   Reject a candidate whose only meaningful oracle depends on timing, network,
   proprietary data, external services, or subjective/visual judgment.
3. Distinguish compile coverage from runtime-compatible feature profiles.
   `--all-features` may be a useful compile check while being an invalid test
   runtime when optional scheduler, sanitizer, allocator, or platform shims
   replace normal execution. Derive the executable feature matrix from the
   repository's CI and test configuration, and record excluded combinations
   with evidence rather than treating them as source failures.
4. Record production LOC as a heuristic, not a hardness proof. Roughly 30k
   primary-language LOC is a useful warning boundary; smaller repositories may
   pass only with concrete cross-cutting architecture evidence.
5. Write the smallest plausible correct design before polishing the task. Count
   effective executable production LOC only; exclude tests, imports, comments,
   blanks, braces, generated output, and padding. The task must naturally clear
   the current live successful-run horizon, with 200+ as a historical safety
   buffer only when the panel has not supplied a newer value.
6. Recheck P1-P6 locally: repository fit, no upstream solution, self-contained,
   clear and unambiguous, objectively verifiable, and non-prescriptive.

## Artifact-time checks

Before the four artifacts leave construction:

1. Keep hidden test files and `test.sh` free of comments. Use naming and small
   functions to make the harness self-explanatory. Shebangs are allowed.
2. Search `solution.patch` for shortcuts and non-native work: fixture-specific
   branches, hard-coded values, duplicated repository logic, swallowed errors,
   temporary fallbacks, TODO gaps, unnecessary public API, unrelated behavior,
   or new dependencies without repository precedent.
3. Map every prompt requirement to the exact production path that implements it
   as well as to its observable assertion. Passing tests alone does not prove a
   comprehensive reference solution.
4. Compare the solution with neighboring code for abstraction level, naming,
   error model, lifecycle, cleanup, module boundaries, and dependency policy.
5. Inspect the final description against both patches: remove implementation
   details, duplicated requirements, and unverified constraints; add only the
   behavioral information needed for fairness and determinism.

## Pre-Scope minimum profile

Run this profile after the full task scope is frozen and before any Scope Gate.
First complete the reference solution and prove from executable evidence that
the implemented task passes the shared accepted floor and comparison with every
accepted calibrator. The gate minimum applies only to the representative test
surface: use as few parameterized scenarios and fixtures as possible while the
full `problem.md` and `solution.patch` remain byte-for-byte frozen.

`validate_submission.py --pre-scope` owns deterministic rows. Supply a current
`compliance.json`, `hardness-proof.json`, `scope-gate-map.json`, a blind list of
predicted test paths made before reading the test patch, and `local-review.json`
for judgment rows. Preserve its JSON output as `scope-gate-prechecks`. Required
rows are:

Record a successful proof named `scope-gate-prechecks` with all four artifacts
as dependencies before checkpointing stage 5c. Any gate-package byte change
requires this proof and its source transition evidence to rerun.

The supplied `scope-gate-map.json` is executable evidence, not a planning
document. It must set `full_scope_frozen`, `full_solution_complete`,
`requirements_complete`, and a PASS calibrator verdict; contain
the current `problem_sha256` and `solution_sha256`, contain
`omitted_requirements: []`; and give every stable requirement ID nonempty full
production paths, subsystems, semantic barriers, an oracle, solution-review
evidence, and a `GATE_COVERED` or `POST_GATE_TEST_EXPANSION` status. Every
`GATE_COVERED` row must name test IDs and a scenario and reproduce a PASS
`FAIL_TO_PASS` or compatibility `PASS_TO_PASS` transition on Aswin. Every
`POST_GATE_TEST_EXPANSION` row must have a concrete expansion plan and still
prove the complete production behavior exists in the frozen solution. The
gate-covered union must span at least three subsystems and two semantic barriers
and include at least one `FAIL_TO_PASS` transition.

The supplied `hardness-proof.json` must PASS and record a complete reference,
the current frozen problem and solution hashes, measured effective production
LOC and production-file count matching `solution.patch`, executable
production-path evidence, at
least three executed wrong architectures or mutations, an every-accepted-task
calibrator matrix including Dora, two closest analogues, and a passing hardness
kill sheet. Estimates and skeleton evidence fail this row.

1. **Repository compliance:** the GitHub URL and exact commit resolve; stars are
   at least 500; the primary language is supported by the current panel; every
   applicable license is permissive and allowed; and the pinned commit is no
   more than one year old. Record actual values, timestamps, and evidence URLs.
2. **Description mechanics:** target 100-200 words; 201-500 warns, 501-1000
   warns strongly, and above 1000 fails. Decode as UTF-8 and fail at the first
   non-ASCII or non-printable character unless Unicode is itself the contract.
   Fail ordinary external URLs because solver agents cannot fetch them.
3. **Patch structure:** both patches are genuine unified diffs with file and
   hunk headers and valid hunk prefixes. `git apply --check` must pass alone and
   together at the exact commit. `solution.patch` contains production work;
   `test.patch` contains no production or solution code.
4. **Runner sanity:** `test.sh` is mode 100755, has distinct `base` and `new`
   modes plus `--output_path`, contains no package installation, fail-fast,
   destructive/malicious command, solution code, or platform marker, and
   passes `bash -n`. Prove both modes discover nonzero, distinct tests.
5. **Collision screen:** before seeing the patch, predict the paths a solver is
   likely to create. Fail exact predicted-path collisions and names containing
   current banned markers. A randomized or repository-native non-obvious hidden
   path is preferred; filename novelty must not make behavior unfair.
6. **Docker static rules:** current allowed language image with `:latest` and no
   digest, `WORKDIR /app`, build-time dependencies, no tests in build, no
   redundant installation of tools already in the base, pinned added package
   versions when the ecosystem permits it, interactive Bash command, and the
   evaluator's unprivileged `model:1000` runtime setup and safety constraints.
7. **Python install rule:** editable project installation passes. A non-editable
   or absent install requires `problem.md` to state the repository-native test
   invocation so agents do not execute a stale site-packages copy.

Run these judgment rows from clean context and store each as structured
`PASS|WARN|FAIL` with cited evidence in `local-review.json`:

- category fit, including the better category and reason when mismatched;
- bounded local duplicate/plagiarism search with candidate titles and scores;
- description/test quality: no test leakage, behavioral rather than
  implementation assertions, adequate coverage, and coherent pair;
- necessity: every removable sentence tagged HIGH, MEDIUM, or LOW;
- bidirectional alignment: a solver can derive every assertion from the prompt
  or pinned repository, and every requirement has a full solution path and
  observable oracle;
- blind predicted test-file collision review;
- Docker guideline review, including redundant tools, dependency pinning,
  runtime user, and malicious/safety concerns.

Every local row must pass before upload. A warning needs an explicit accepted
disposition. These records are rehearsal only: hosted similarity, hosted AI
quality/category/alignment judgments, and Scope Gate remain live-only and
unproven until their exact panel runs complete.

## Pre-Scope source execution

Run these checks on Aswin on the exact artifact hashes before the first panel
precheck upload. Docker execution is deliberately deferred until Scope Gate passes:

1. Exact commit and clean root; the complete Pre-Scope minimum profile; patch
   application alone and together; LF, executable mode, banned terms, shell
   syntax, collision, and nonzero discovery.
2. In isolated source worktrees and mutable build caches, prove the four-state
   transition: base passes before and after the solution; new fails before and
   passes after. Preserve per-test JUnit or the repository-native equivalent and
   decisive compile/test output.
3. Run only the focused deterministic regressions required to prove the reduced
   gate tests and complete solution did not break their touched paths. Broad
   regressions, repetition, evaluator UID,
   network isolation, and container proof are post-Scope work.

## Post-Scope execution-time checks

After a current Scope Gate PASS and before Verify Tests or any later live quality
funnel, run these on Aswin on the exact hardened artifact hashes:

1. Build the untouched repository image first when that matches the evaluator,
   then repeat the isolated four-state transition inside the evaluator image.
2. Run as the evaluator UID and login-shell environment with `--network none`.
   Validate JUnit structure, distinct base/new identities, per-test transition
   classes, and failure-path reports after forced setup or compile failure.
3. Inspect flakiness hazards before repetition: wall clock, sleeps, random seeds,
   iteration/order dependence, locale/timezone, CPU count, concurrency, shared
   caches, mutable process state, temporary-file collisions, and resource
   contention. Then run the required repetition count in clean isolated states.
4. Run focused pre-existing regressions adjacent to every touched subsystem plus
   format, lint, warnings-as-errors, generated-source clean rebuild, and offline
   canonical build/test commands when applicable.
5. Complete the two-way requirement map, cross-component combinations, mutation
   inventory, reference-solution self-review, and saved-solver replay.

## Live-only boundary

The following are not local proofs and must never be inferred from the checks
above: platform similarity verdict, Scope Gate, VCS+, Verify Tests, Verify
Solution, Test/Task/Solution/Description Quality, Verify Flakiness, Auto Review,
agent pass rate, false-positive adjudication, Holistic, acceptance, or submission.
Use the current panel order and costs only after the specific live action is
authorized.
