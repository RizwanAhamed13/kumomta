# Shipd Fastlane: the optimized delivery workflow

**Final synthesis · 13 September 2026 · local execution on shipd-local**

The objective is a correct, complete artifact package that avoids preventable review cycles. The method is to reject weak candidates early, make every promise observable, test the architectural boundaries most likely to be missed, and reuse evidence only while its inputs remain unchanged.

This is our strongest current workflow, not a guarantee of one-shot acceptance. Local execution can reproduce public behavior and rehearse published rubrics. It cannot reproduce undisclosed Shipd graders, the private similarity corpus, future panel changes, or manager decisions. The live panel controls the actual submission contract.

**Operating sequence**

Qualify → prove feasibility → map requirements → implement a complete reference → prove hardness → freeze Scope package → authorized Scope Gate → expand tests → verify clean/offline execution and local quality → authorized hosted checks → audit rollouts → repair confirmed defects → freeze approved bytes.

Resume at the first unproven stage. Use Olympus Forge for the detailed stage procedure and Fastlane for the preparation, evidence checks and lessons below. A user-authorized local reconstruction may finish its offline work without spending on Scope; record that exception and leave the hosted gate NOT_RUN.

## 1. Establish one source of truth

Start from the selected case's pinned commit, original prompt or current description, canonical artifacts, latest handoff, live status and unresolved findings. Resolve similarly named revisions explicitly. Retrieve relevant lessons; do not reread the whole corpus for every case.

Record:

- Repository, full commit, license/activity and issue/PR provenance.
- Current description, solution.patch, test.patch, Dockerfile, test-runner form and their SHA-256 hashes.
- Exact selected commands, discovered tests, toolchain/dependency identities, image identity and runtime contract.
- Which actions the user authorized, applicable usage limits and current execution routing.
- Each result as STRUCTURAL, EXECUTED, REVIEWED, HOSTED or ACCEPTED, with its input hashes and evidence path.

A static lint is STRUCTURAL. A reconciled native run is EXECUTED. A rubric audit is REVIEWED. A real panel receipt is HOSTED. Manager-confirmed acceptance is ACCEPTED. One label cannot substitute for another.

Capture case-specific live fields, allowed language image, gate sequence, costs and staleness before upload or paid work. The dated general contract in this plugin is a starting point. Any newly displayed check needs a mapped local counterpart or an explicit blocking gap.

## 2. Reject unsuitable candidates before expensive work

Run the validated repository denylist checker before ranking, claiming or building, and again immediately before Scope. Transfer the checker and list to the server when their original paths are on the Mac; verify both hashes. Retain normalized repository, list SHA-256, entry count, date and output. A match is a terminal rejection; a missing or unverifiable checker/list means REVIEW.

Check upstream issues, merged/open PRs and existing implementation at the exact commit. Record originality limits: public searches do not reproduce private similarity checks. An ambiguous or already-solved candidate is a no-go until resolved.

Prefer one coherent behavior that naturally crosses meaningful subsystems. Reject cosmetic expansion, unrelated requirements bundled for size, artificial complexity and candidates whose difficulty depends on ambiguity. Record the smallest plausible solution and why it cannot satisfy the complete contract without the required architectural work.

## 3. Prove feasibility before promising broad behavior

Create a feasibility table before implementation:

| Prompt clause | Native API and representation | Producer → transport/state → consumer | Observable witness | Decision |
|---|---|---|---|---|
| Exact typed values survive a boundary | Concrete supported type and codec | Actual public path | Consumer checks type and value | Supported / core change required / unresolved |
| Later state changes remain visible | Shared ownership and identity mechanism | Mutate after transport, observe through alias | Identity and live-update assertions | Supported / core change required / unresolved |

Use a small vertical witness to establish the hardest boundary early, then complete the reference before Scope. Compile every affected consumer when changing shared types, enum variants, serialization, ABI or trait interfaces. A library-only green build does not establish that downstream tools still compile.

For FFI or plugin contracts, separately build the producer and consumer with distinct library identities. Exercise public consumer APIs, private producer implementations, callbacks, closure behavior, lifetime and release. Same-library roundtrips can hide ABI and identity defects.

Do not silently turn a concrete type into a proxy, a structured error into a string, or shared live state into a snapshot. If the promised behavior needs a core change, implement and test that change within legitimate scope or resolve the contract before freeze. Unresolved feasibility blocks a completeness claim.

## 4. Design the test inventory independently of the solution

Before writing tests, enumerate observable requirements from the prompt and pinned-repository compatibility. Do not derive the inventory solely from the implementation you happened to write.

For each requirement, record:

| ID | Grounding | Input family × semantic role | Expected behavior | Public witness | Existing regressions | Plausible wrong implementation |
|---|---|---|---|---|---|---|

Inspect positive behavior, boundaries, negative/error behavior, compatibility and interactions. Trace each requirement through its producer, representation/transport and final consumer. Cover applicable forms, including empty/single/multiple values, absent/present metadata, nesting, alternatives/fallbacks and repeated operations where relevant. Mark inapplicable cells individually with a reason.

Use at least one whole-scenario witness for each required subsystem interaction. Isolated unit tests cannot establish that two individually correct features compose. Avoid an indiscriminate Cartesian product: select interactions that exercise distinct branches, state transitions or representations.

Every stated requirement must have a witness or be removed before freezing the contract. Every feature test must be grounded. Compatibility checks may be grounded in required pinned-repository behavior; they must not smuggle in a new feature demand.

**Improving small, low-coverage test patches:** expand missing behavior families and interactions, not lines. Use parameterized cases and shared fixtures where clear; count their independently executed cases. Separate production LOC, test LOC, fixture/data LOC and generated content. There is no useful universal test-patch LOC quota. Any actual platform size rule must come from the live contract; never pad to satisfy an assumed threshold.

## 5. Build the full reference and freeze the correct Scope package

Implement the complete natural reference solution, not a deliberately inflated version. Prove the hardest mechanism with executable witnesses and plausible shortcut probes. Audit all affected consumers and required integration paths before treating the solution as complete.

Before an authorized Scope Gate:

1. Freeze the full description and full reference solution.
2. Select a reduced, representative test slice that demonstrates the core behavior and natural hardness.
3. Preserve the full requirement/test plan and explicitly list deferred full-suite obligations.
4. Check the Scope contract, clean patch application, representative before/after execution and all local Scope counterparts.
5. Hash the exact upload bytes and repeat the denylist check.

Reduced Scope tests do not prove complete hidden-test coverage. After successful authorized Scope, expand tests within the frozen behavior. A description or solution change reopens affected earlier gates. Test expansion must preserve the reduced Scope obligations and introduce no concealed requirement.

## 6. Partition tests by what they actually prove

Use independently discovered complete test IDs. Split baseline-valid compatibility checks from feature-dependent checks without overlap or unexplained omissions.

- **Base/compatibility:** expected to pass before and after the solution.
- **Feature:** each selected new feature test must execute on baseline and fail for the intended missing behavior, then pass with the solution.
- **Additional integration or regression selections:** include their actual IDs and reconcile them into the complete inventory.

Compilation failure, setup error, timeout, crash, skip or an unstarted test is not a behavioral baseline failure. New APIs that prevent baseline compilation require a valid baseline-executable public witness or an explicitly unresolved validation gap. Do not invent trivial shims that manufacture a red result.

Check precise outcomes. A generic `is_err()` can accept the wrong error and hide a defect. Assert the relevant error kind, category, value, state and side effects. For a predicate with several guards, make all sibling conditions valid so that the intended guard is the only explanation for the result.

## 7. Make execution reports trustworthy

Before costly runs, check patch applicability, Docker syntax/contract, runner dispatch, test discovery and partition integrity.

Retain independently discovered IDs, actual native start and terminal events, process exit status, raw logs and per-test JUnit diagnostics. Reconcile all of them. Reject missing/duplicate IDs, selected skips, missing terminal events, inconsistent counters, unexplained exclusions and report/process disagreement.

Do not create a named failed testcase for every intended test when compilation failed before tests started. Record the setup/compiler failure separately and retain zero executed feature tests. Preserve assertion logs even when a command exits nonzero. Encode XML-invalid characters safely in JUnit while retaining the original raw bytes.

Bind receipts to exact source, relevant executable, test selection and environment identities. Green XML alone does not establish truthful execution. The supplied report and partition tools inspect consistency; they cannot independently certify that discovery or raw inputs were honestly produced.

## 8. Run the clean four-state matrix

Use isolated clean worktrees at the exact commit. Check each patch alone and compatible application orders; do not reuse a dirty worktree from another case.

| Source state | Required evidence |
|---|---|
| Baseline | Required existing/base selection passes |
| Baseline + test patch | Base/compatibility passes; each feature case executes and fails behaviorally as intended |
| Baseline + solution patch | Required existing/base regressions pass |
| Baseline + solution + test patches | Every required selected case passes; no skipped or missing obligations |

Use the actual platform patch order as the runtime authority and verify the supported alternate order where required by Forge. Capture application output and distinguish patch failures from implementation failures.

Compile all affected local components after runtime patches. If a shared representation changes, include each affected consumer, even when the primary library's tests pass. Include required architectural integration with real interfaces; mocks may simplify unrelated dependencies but cannot replace the behavior under test.

For expensive suites, run a cheap focused failure reproducer while developing, then execute the complete mandatory matrix once the confirmed fixes are batched. Do not rerun an unchanged passing check without invalidation or an unresolved concern.

## 9. Measure whether the new tests carry their weight

Measure changed executable-line coverage for these selections separately:

1. Existing tests.
2. New baseline-valid compatibility tests.
3. New feature tests.
4. The relevant combined selection.

Report added/changed executable lines, mapped counters, covered/missed lines, unmapped lines and lines without executable counters. If the instrumentation only supports added lines, say so. Do not label line coverage as branch coverage. Include branch coverage where supported and useful.

High combined coverage can come almost entirely from existing tests. It does not prove that the new test patch targets the feature. Review uncovered changed behavior, required branches and the requirement map together. All critical contract gaps block; an arbitrary percentage such as 90% is not sufficient or a universal Shipd rule.

Use coverage to find missing observations, then add the smallest distinct public scenario that closes the gap. Retain the measured denominator and tool warnings. Unavailable or invalid instrumentation remains UNMEASURED; it must not be silently converted to zero gaps.

## 10. Challenge the suite with plausible wrong solutions

Choose targeted semantic mutations from the requirement map: omit a propagation step, select the wrong nested field, lose metadata, use the wrong error category, coerce exact values, break a fallback, or snapshot state that should stay live.

For each mutation:

- State the public requirement and expected discriminating testcase.
- Establish a passing reference and valid fixture prerequisites.
- Apply one coherent wrong behavior, rebuild the affected component and retain binary identity.
- Require an executed assertion failure attributable to that behavior.
- Restore exact source bytes and confirm the reference remains passing.

Compiler failures, harness failures, inactive source paths and crashes are invalid probes, not mutation kills. A surviving mutant requires analysis: equivalent behavior, inactive mutation, out-of-contract behavior or a real test gap. Do not increase a kill percentage with trivial mutants.

Check conforming alternative implementations where practical. A fair test checks the promised observable result, not the reference's internal layout or incidental implementation choices.

## 11. Build a fast, platform-compatible offline package

Use the live language-specific allowed base image and required `:latest` tag. Never insert a digest into Dockerfile `FROM`; record its resolved identity in evidence.

Follow the live workspace, user/UID, shell and runner contract. Keep challenge patches out of image-build layers when the platform applies them at runtime. Install dependencies and compile reusable components during image construction where permitted. The September 13 general documentation requires compilation rather than test commands in build layers; prefer the build command appropriate to the repository and recheck current rules.

Order stable dependency manifests before volatile source. Cache keys must include relevant commit, dependency lockfiles, toolchain, flags and artifact identities. Runtime-applied patches must rebuild every affected local component. A cache hit is valid only when those dependencies remain valid.

Use challenge-relevant packages while retaining all required consumer and integration coverage. Combine compatible commands to avoid repeated startup, dependency resolution and code generation. Use deterministic fixtures, condition-based readiness and bounded deadlines instead of fixed sleeps. Validate offline behavior in the actual image/runtime, including failure reporting, permissions and required runner modes.

Measure wall time and test time separately. Record cache state, CPU quota, affinity, hardware, image, instrumentation, queueing and thermal pauses. An image manifest or static Docker lint is not a successful clean build or offline runtime receipt.

## 12. Rehearse every applicable quality family locally

The current catalog has 20 families. Scope uses 12, full-package readiness uses 18, final review uses all 20. Refresh this mapping from the live case panel. An unknown displayed check blocks readiness until mapped; a catalog count alone does not prove completeness.

| Local family | Required local evidence or boundary |
|---|---|
| Eligibility | Pinned repository, denylist, license/activity and task-fit records |
| Originality | Public issue/PR/implementation search; private corpus remains unknown |
| Artifact contract | Exact files, patch paths, formatting, runner and Docker contract |
| Scope | Complete reference, grounded task size/hardness, reduced representative witnesses |
| Verify Tests | Clean test application, discovery, expected baseline behavior and truthful reports |
| Verify Solution | Clean solution application and complete passing solution matrix |
| Test Quality | Requirement map, assertions, interactions, coverage and valid mutation probes |
| Fairness | Every behavior grounded; deterministic fixtures; conforming alternatives |
| Task Quality | Coherent meaningful behavior and natural architectural depth |
| Solution Quality | Complete maintainable implementation and affected-consumer regression evidence |
| Description Quality | Unambiguous observable contract with no untested promises |
| False Positive | Reproduced plausible wrong solutions rejected for stated behavior |
| Image/Runtime | Actual clean image and offline runtime on the exact package |
| Flakiness | Appropriate repeated/varied-seed execution after identifying nondeterministic risks |
| Quick Check | Current public quick-check semantics rehearsed; label unavailable internals |
| Solvability | Independent reasoning or authorized local solver evidence without hidden requirements |
| Holistic | Combined consistency review of prompt, tests, solution, environment and evidence |
| Auto Review | Local adversarial rubric rehearsal; actual private approval remains hosted |
| Rollout Audit | Real authorized cohort, exact replay, clustering and false-positive triage |
| Final State | Current actual hosted receipts, exact artifact identity and approval state |

The last two require real cohort/hosted evidence and cannot be fabricated before the first upload. Local rubric reviews are approximations of private reviews. Run Forge's applicable adversarial graders, attach findings and raw execution evidence, resolve defects, and then require `LOCAL_EVIDENCE_GATE_PASS` for the appropriate boundary.

The checker validates supplied evidence metadata and dependencies; it does not run the candidate or establish the truth of a review. Missing, failed, unknown, stale or misbound applicable evidence blocks upload. The plugin's local expiry policy is conservative workflow policy, not a claimed Shipd rule.

## 13. Repair one root cause, then invalidate precisely

Classify a failure as contract, implementation, test fixture, harness/reporting, environment, packaging, stale evidence or genuine task difficulty. Preserve the original result.

Reproduce the smallest public counterexample. Inspect adjacent forms and consumers, then batch related confirmed corrections. Do not broaden scope merely to force difficulty. A repeated failure with unchanged evidence calls for root-cause analysis, not another paid retry.

| Changed input | Evidence to reconsider |
|---|---|
| Description | Grounding, scope, fairness, task/description review and dependent hosted gates |
| Solution | Builds, consumer regressions, matrix, coverage, mutation reference and dependent checks |
| Test patch or selection | Discovery, partitions, baseline discrimination, solution pass, coverage, mutations and dependent checks |
| Runner | Dispatch, failure handling, event/JUnit reconciliation, matrix/runtime and dependent verification |
| Docker/environment | Clean image, offline runtime, timings, reproducibility and dependent hosted verification |
| Only unrelated evidence prose | No automatic code rerun; verify that no tested input or claimed result changed |

Use exact dependency fingerprints and current panel staleness. A matching hash permits reuse of an otherwise complete passing receipt; it is not itself a passing receipt. Report which Verify, rollout, false-positive, Holistic and review results are stale after every artifact edit.

## 14. Release exact bytes and preserve approval

Package from an explicit path allowlist. Inspect every diff path and added binary; exclude profiling files, build outputs, temporary evidence and unrelated untracked content. Preserve old failed drafts separately. Do not rename a draft as validated.

Before each upload, verify the canonical four artifacts and exact runner form, filename/test-name requirements, patch cleanliness and all applicable local gates. Use checksummed rsync and verify SHA-256 on both hosts. Upload only the reviewed package.

Read live costs and obtain authorization for the specific paid operation if it has not already been authorized. Do not treat routing authorization as spending authorization. Reuse still-valid hosted evidence, execute the smallest authorized next gate and stop on the first actionable failure.

For authorized rollouts, preserve the real cohort and revisions, replay exact candidates, separate implementation failures from environment problems and investigate false positives with public counterexamples. A measured success rate applies only to that cohort and bytes.

After Auto Review approval, freeze exact artifacts and approval evidence. Manager acceptance is a separate state. Preserve acceptance proof, task identity, hashes, remaining limitations and any later drift; never change an approved package silently.

## 15. Keep the workflow fast through selective work

Use one compact case plan and handoff. Read only relevant source/graph paths and lesson records. Prefer indexed graph discovery when available; fall back to targeted rg when insufficient.

Front-load cheap rejection, contract and compile-boundary checks. Do not spend hours measuring coverage for a package whose consumer cannot compile. Keep source preparation, fixture construction, image construction and runtime validation as separately recorded phases.

Use parallel read-only analysis only when authorized by current instructions and helpful. Serialize material server work under the current thermal policy. Avoid competing builds, repeated unchanged polling and speculative branches. Honor a user-specified usage cap and its duration; do not impose the removed 50% cap on this task or alter global model settings.

At an authorized stage boundary, persist the result and next action. Continue across stages when the user requested it. Efficient context use must not turn incomplete required work into a completed claim.

## 16. Execute safely on the designated Arch server

All repositories, code generation, patches, dependencies, builds, tests, Docker, benchmarks and mutations run through:

```sh
ssh -o BatchMode=yes -o ConnectTimeout=10 shipd-local
```

Use `/home/admin/olympus-work`. The Mac handles orchestration, lightweight records and transfers. Stop on SSH, Docker, workspace or intended filesystem failure; no silent fallback.

Before every computational phase, record hostname/IP, real working directory, full commit, input SHA-256 hashes, free disk, Docker availability and destination filesystem/mount. Hostname must be `arch`. Directory names do not establish storage: the observed `/mnt/ssd/docker` is on Linux HDD Btrfs. Windows partitions and `/mnt/windows` remain untouched/read-only. Partitioning, formatting or mount reconfiguration requires separate explicit approval and current partition-table inspection.

**Current host controls:** one material phase, one build job, 0.25 CPU and verified affinity 16–31. Source preparation starts below 65°C through the scoped supervisor. Existing-container continuation additionally requires 120 continuous seconds below 65°C, explicit coordinator handoff and an independent guard. Sample CPU temperature every second; at 75°C, sensor failure or watcher failure, stop/hold the exact owned work. Do not automatically resume after a hot event.

No Docker create/start/pull/build/load/export until Docker and containerd daemon controls are applied and verified; their work can escape a build container's quota. The requested temporary daemon limits could not be applied without interactive privileges, so those operations remain held as of this synthesis.

The current source supervisor proves quota/affinity and scope cleanup and passed 11 harmless real-scope fixtures. It lacks an independent watcher for abrupt supervisor SIGKILL or host loss. The standalone container thermal helper normally auto-resumes; it must be wrapped by the hard-hold supervisor for this policy. Do not present either helper alone as a universal safety guarantee.

When other workloads need pausing under the user's instruction, identify exact owned task/process/container identities, preserve state and record what was paused. Never blindly stop services or resume unrelated saved workloads. Thermal holds and interrupted experiments remain evidence, not failed candidate tests.

## 17. Learn without rewriting the experiment

For fresh reconstruction, record original prompt/commit and prior metadata exposure. Withhold historical tests until the new package finishes its agreed own validation and is frozen with verified hashes. Withhold historical solutions until the first archive evaluation.

Record initial snapshot, own-validation completion, validated freeze, historical exposure and first historical evaluation as distinct events. Unknown times remain unknown. Preserve the first result before repairs; do not retrospectively promote an early snapshot to a validated first-complete package.

Classify iterations separately: solution changes, test-fixture fixes, harness repairs, environment failures and thermal pauses. Later repairs on exposed cases are learning-set results, not unseen generalization. No broad success-rate or speedup claim follows from incomplete or thermally confounded runs.

Capture each confirmed lesson as **trigger → public counterexample → root cause → preventive check → evidence hashes**. Add it to the targeted knowledge index and update the corresponding checklist. Inventory is not semantic reading; live acceptance is not accepted-byte identity.

## 18. Required delivery and invocation

Deliver the canonical artifacts, exact hashes, requirement/test map, reconciled matrix, relevant coverage/mutation evidence, runtime/image receipt, local quality report, staleness list and compact handoff. State the first unproven gate and its concrete next action.

Use the [delivery checklist](assets/delivery-checklist.md), [case plan](assets/case-plan.md), [dogfood findings](knowledge/dogfood-lessons-20260913.md) and the phase-specific references under the skill.

Start a new case with:

> Use $shipd-fastlane for this candidate and pinned commit. Follow WORKFLOW.md and Olympus Forge. Prove feasibility, map every required behavior, build the full reference and the correct stage-specific test package, validate all applicable local counterparts on shipd-local, and deliver exact artifacts plus evidence. Resume at the first unproven stage. No paid Shipd operation without my explicit authorization for that gate. Honor the current task's usage and thermal policies.

**Release boundary:** the user ended further experiments on 13 September and requested this consolidated workflow. Candidate drafts and unresolved dogfood gates remain incomplete. The companion lesson ledger names the evidence limits rather than claiming every historical detail was read or every candidate passed.
