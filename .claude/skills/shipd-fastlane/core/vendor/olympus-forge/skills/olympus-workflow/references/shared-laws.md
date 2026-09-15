# Olympus shared laws

Read this file completely whenever an Olympus Forge skill starts. These are the cross-phase laws that were previously hidden behind missing external filenames. The numbered stage blocks in each skill remain authoritative for phase-specific procedure.

## Source-of-truth order

1. The live Shipd/Olympus panel is authoritative for current required fields, eligible images, gates, costs, thresholds, and result status. Inspect it before spending tokens; never substitute remembered values.
2. The repository at the exact pinned commit is authoritative for existing behavior, public APIs, style, and discoverable requirements.
3. The four current artifacts and their hashes are authoritative for what was tested. A result attached to different bytes is stale.
4. This plugin supplies durable workflow policy and historical lessons. It must not override newer live platform rules.

A hosted adjudication is authoritative for that exact run and artifact set. Preserve a high-confidence `genuine pass`, `false positive`, or environment classification as the run's disposition; do not reverse it from static suspicion. A hosted disposition does not prove broader claims about edited artifacts or unexecuted tests.

If two sources conflict, stop the affected stage, record the conflict as an open item, and follow the higher source after verifying it directly.

## Persistent workspace state

Resolve `OLYMPUS_STATE` to `<workspace>/.olympus`. Follow [the state and proof schema](state-and-proof-schema.md). Before phase work, create or locate these records:

- `lessons.md`: append-only local lessons in the format `date | case | mistake | cost | rule`.
- `repo-scouting-results.md`: every repository and concept checked, including aliases, proof links, verdict, and reason.
- `portfolio.md`: case-level active, occupied, rejected, and archived summaries; never use this as the readiness blocker list.
- `active-case`: the one case selected by default in this workspace.
- `cases/<case>/case.json`: authoritative current stage, mode, repository URL/root, exact commit, license/activity/duplicate evidence, artifact paths and hashes, proof records, result identifiers, stale proofs, verdict, and next legal stage.
- `cases/<case>/open-items.json`: unresolved findings for this case only. It must contain no blocking findings before a readiness claim.
- `cases/<case>/events.jsonl`: append-only checkpoint history.
- `cases/<case>/state.md`: generated human-readable projection of `case.json`, never a competing source of truth.
- `cases/<case>/rollouts/<batch>/<agent>/`: permanent rollout transcript, verdict, and solution patch.

If state does not exist, initialize it with `scripts/case_state.py` before continuing. Never silently replace a ledger; append or make a new case record. Migrate a legacy global `open-items.md` into `portfolio.md` plus the active case's `open-items.json` before any readiness claim. The packaged [lessons ledger](lessons-ledger.md) is the seed and interpretation guide, not the writable case history.

## Exact-byte and staleness law

- Hash `problem.md`, `test.patch`, `solution.patch`, and `Dockerfile` at every handoff.
- Record the repository commit and working-tree cleanliness with those hashes.
- Verify that `git rev-parse --show-toplevel` equals the recorded source clone; never accept cleanliness inherited from an unrelated parent repository.
- Any artifact edit invalidates every proof that depends on that artifact: patch application, four-state matrix, offline run, flakiness, regression, format/lint, mutation evidence, fairness/quality/FP graders, saved-agent replay, Scope Gate, paid checks, rollouts, Holistic, and Auto Review as applicable.
- Use the artifact dependency map in the state schema. Invalidate the union of actual dependencies rather than either carrying proofs forward casually or declaring unrelated proofs stale.
- Never describe an old result as current. Name current proofs and stale proofs separately.
- After approval, freeze all four artifacts byte-for-byte.

## Candidate law

- Qualify repository activity, permissive license, language, project fit, exact issue/task, and commit before building.
- Search two origin tracks: ISSUE-LED work from a real accepted issue, and FEATURE-PIONEER work from a strong repository-native seam. Pioneer evidence must be a TODO, explicit unsupported combination, asymmetric inverse operation, documented invariant gap, or executable public-behavior probe; issue URL is optional, but strong README fit, finite semantics, and no public solution are mandatory.
- Search the local scouting ledger and submissions under repository aliases and concept synonyms.
- Search live open, merged, and closed pull requests plus issue, PR, and discussion comment bodies. Read maintainer-role replies.
- Search public specifications, writers, libraries, inverse implementations, and equivalent features in other languages. A public solution that erases repository discovery depth is a collision.
- Repeat the duplicate-work search after the reference solution reveals its actual architecture and immediately before final delivery.
- Treat an overlap or duplicate rejection as a burned repository/concept combination. Do not narrow the same feature or swap internal wiring and resubmit it.
- Prefer observable correctness/semantics work over diagnostics, placement, exact strings, or hidden implementation requirements.
- Scope must plausibly sustain at least two files, twenty agent messages, and two hundred changed lines in the median successful run. Treat a reference near the threshold as risk, not proof.
- LOC, files, tests, and messages prove only horizon. Reject compiler-guided propagation and require the hardness kill sheet in `hardness-calibrators.md` before artifact construction.
- Feature pioneering is a discovery track, never permission to append unrelated scope after a candidate proves easy.

## Artifact law

- Pin one exact base commit before authoring.
- Before Scope Gate, implement the complete natural task, exercise its real production paths, and prove its architecture is comparable to every accepted calibrator. A skeleton, partial solution, or estimated LOC is not hardness evidence and cannot advance.
- Freeze the exact full `problem.md` and complete `solution.patch` after executable hardness PASS. The Scope Gate package may reduce only `test.patch` to a compact representative suite; all four artifacts remain populated and the complete solution must pass the gate tests.
- Keep a `full-scope requirement -> full solution path -> observable oracle -> gate coverage status` map. A row may defer additional hidden-test coverage until after the gate, but it may not defer production behavior, description scope, or solution code. Gate-covered rows must collectively span the architecture and include a base-fail/solution-pass transition.
- Use the dedicated stage 5c Scope Gate before post-gate test expansion by default. Bind `scope-gate` and any direct current-user `scope-gate-override` to the frozen `problem.md` and `solution.patch`, not the reduced `test.patch`. After PASS, expand tests only. Any problem or solution edit returns to full reference construction and executable hardness proof and requires a new gate. Never infer a waiver or treat it as duplicate, scope, readiness, platform, or paid-action evidence.
- Keep `solution.patch` to production changes and unavoidable existing-test updates. Keep `test.patch` to hidden tests and `test.sh`; do not leak solution code.
- State behavioral requirements only. Every stated requirement needs an enforcing assertion, and every assertion needs prompt or pinned-repository grounding.
- Prefer repository-native round trips and parsed-value oracles. Avoid exact bytes, incidental ordering, implementation families, and exact error wording unless the public contract requires them.
- Classify each failure contract before testing it: exact representation, existing public category, or rejection only. Assert no more than the strongest level grounded by the prompt or pinned repository. A variant, payload type, field name, or expected/actual orientation introduced only by the reference solution is an implementation choice, even when it is public and strongly typed.
- When the contract promises only a category or rejection, pair that assertion with the promised observable aftermath: unchanged state, preserved contents, stable counts, or another public result. A neighboring repository error variant can establish a category convention; it does not mandate the name or layout of a newly invented sibling variant.
- Use enough input classes and path interactions to reject plausible partial implementations without manufacturing difficulty.
- Docker must start from a currently allowed Olympus/Mars `:latest` base and must never add an `@sha256` digest to `FROM`. Record the resolved digest in evidence only. Use `WORKDIR`, install dependencies at build time, build from untouched base bytes, run no tests during build, reproduce the evaluator's unprivileged runtime user and login-shell environment, and support runtime network isolation.
- `test.sh` must support the live panel's required modes and `--output_path`, run nonzero tests, preserve individual failures, accumulate status, and return nonzero when new tests fail. It must emit valid per-test JUnit even when setup or compilation fails; a synthetic process failure supplements diagnostics but never substitutes for discovered test cases.
- Base mode must execute a genuine, deterministic regression set adjacent to the changed architecture. A single unrelated smoke test is insufficient, while a broad unstable suite is not a substitute for focused coverage.
- Base and new modes must not configure, rebuild, or link concurrently in one mutable build tree. Serialize the build once or use isolated build directories, then execute tests from stable binaries.
- When source generators are involved, the delivered patch must contain a mutually consistent source grammar/schema, recorded generator checksum, and generated outputs. Prove a clean compile from delivered bytes after deleting the affected object; cached transient outputs are not evidence.
- Patches use LF endings, apply cleanly alone and together, preserve executable mode for `test.sh`, and contain none of the platform-name leakage terms required by the current panel.
- Before Scope Gate, run the deterministic pre-Scope profile and the structured local review profile in `local-validation-gates.md`. A local review is preparation, not a hosted plagiarism, quality, or scope verdict.

## Validation and FP law

- Prove the four states per JUnit testcase: base passes before and after solution; `new` has zero passing cases before solution and all cases pass after solution. Do not accept a merely nonzero pre-solution wrapper exit. Move any baseline-valid rejection or preservation testcase to `base`; classify by state transition, not by whether its fixture file is new.
- Use isolated worktrees and separate build caches for base and solved states so compiled artifacts cannot cross-contaminate the matrix.
- Repeat the matrix enough to detect flakiness, then run affected regressions, formatting, differential linting, and the final Docker network-isolated matrix.
- Decompose the prompt into atomic requirements and map each requirement both ways to assertions.
- Decompose each atomic requirement again by semantic role. Positive validation, negative validation, inference, ambiguity resolution, runtime use, and preservation are distinct cells when applicable; one covered role never proves another.
- For every role, derive contract-relevant dimensions blindly and enumerate the full Cartesian product before reconciling tests. OS, architecture aliases, ABI/target environment, explicit/default routing, instrumentation state, cache layer, input shape, and lifecycle phase are separate axes when the contract distinguishes them. Missing cells block; out-of-scope cells require prompt/repository grounding.
- Trace every role through the repository graph from public entry to the production decision and then to the public observable. A list of changed files or a test-to-requirement edge is not solution alignment; missing decision-path evidence blocks.
- For a documented producer-to-artifact-to-consumer workflow, audit producer and consumer as separate lifecycle stages and cross each with cold and warm cache states. Every compile-time producer switch that changes the artifact must participate in cache identity, and the warm-producer transition must execute; consumer cache bypass alone is insufficient.
- When a solution adds a parallel finder, matcher, validator, resolver, or selector, compare every admission and rejection predicate with the pinned canonical path. Record trait/type head checks, inference completeness, arbitrary bounds, associated constraints, ambiguity, and any other canonical predicate separately; a broad semantic edge does not prove predicate parity.
- When one analysis is opened or relaxed, audit adjacent analyses sharing its representation. Exhaustiveness, usefulness and unreachable-arm detection, guard handling, and diagnostics are separate invariants; disabling one to implement another is a blocker unless the public contract explicitly removes it.
- Audit the assertion mechanism separately from the requirement mapping. Record whether each oracle is semantic, prompt-token, repo-token, exact representation, category, or rejection; name conformant alternatives. Hidden synonym sets, paragraph colocation, sliding windows, incidental ordering, and presentation layout are unsupported unless directly mandated.
- Cross each explicit/default routing source with both accept and reject outcomes. Default acceptance plus explicit rejection does not prove explicit acceptance. For a public JSON-integer domain, audit 32- and 64-bit representation and a positive value above `u32::MAX`; pointer-width storage is invalid unless publicly bounded. A semantic prose oracle must execute against at least two independently authored conformant variants; listing alternatives without running them is not evidence.
- For every new low-level operation, inventory producer, representation, encoding, decoding, verifier, runtime consumers, and post-patch materialization, and trace every consumed safety invariant back to an explicit validation site. Materialization must rebuild all Docker-baked executables and self-hosted/generated compiler stages after solution application. Missing role, freshness, or invariant cells block alignment and description controls.
- Before reconciling authored requirements, derive a blind inventory in a fresh context from only the problem, pinned repository, and natural contract. It must not read tests, the golden patch, or authored ledgers. Any independently derived role or operation absent from the authored audit blocks; do not edit the blind inventory merely to make the graphs agree.
- A false-positive finding is proven only when the exact candidate patch passes the current exact hidden suite, a fair prompt- or repository-grounded discriminator passes the exact reference, and that discriminator fails the exact candidate for the alleged reason. Static source suspicion, a nearby code pattern, or a hypothetical mutant is not a rollout FP verdict.
- Bound ordinary FP hardening to at most three risk-ranked execution probes per repair batch. Empty combinations, symmetry cells, and static concerns remain nonblocking hypotheses until a concrete prompt-grounded mutant survives the exact suite. Promote a test only after the reference passes, the mutant fails, and preserved genuine solves still pass. This boundary prevents speculative completeness work from over-hardening the task or tuning it toward zero solves.
- A reference defect is not an FP: if the proposed discriminator also fails the reference, record and repair the golden or contract instead.
- Before adding a test from rollout feedback, reproduce all three states: current reference passes, accused candidate fails, and every preserved genuine solve still passes. If any state is missing, record an open hypothesis and do not edit the artifacts.
- Strengthen the existing scenario that reaches the defect. Add a new test function only when no existing scenario can reach it, and record why.
- After incorporating a probe, rerun it against the exact mutant it was designed to kill.
- Accept alternate conformant structures. Mutation review must not force one internal decomposition.
- Bound adversarial hunting by the public input equivalence classes and changed execution paths. Do not generate endless arbitrary predicates after all stated classes and proven gaps are closed.
- Classify evaluator failures from raw logs and JUnit, not the summary label. If no baseline assertion ran and JUnit contains only synthesized missing-output failures after a build-system race, contest or rerun it as environment evidence; do not count it as an agent regression or as a pass.

## Difficulty and rollout law

- Local agent runs explain failure modes; they do not predict platform pass rate.
- Submission needs the current live panel's completed platform cohort, pass-rate ceiling, successful-run medians, cheating limit, and at least one durable genuine successful run. Zero success is not desirable difficulty. Historical numbers in references are examples only.
- Preserve every agent patch and transcript. Replay all saved genuine solutions after every artifact edit.
- Never harden merely to lower the pass rate. A genuine solve is required evidence of solvability; kill it only with a fair, candidate-discriminating requirement violation.
- Before changing artifacts, fingerprint passers and failers, reproduce each alleged FP, and identify the common difficulty driver.
- One fast genuine pass does not establish a rate, but it can expose a mechanical architecture. Two independent fast genuine passes converging on that architecture are a candidate-rejection signal when the current assignment targets a materially harder band; three of three is a hard stop. Preserve the runs and pivot rather than buying the remainder or manufacturing scope.
- A fairness hint is a potential FP until execution proves it unreachable, already covered, stale, contradictory, or unavoidably unfair to test.
- Use paid gates only in the order and at the costs shown by the live panel. Never infer a paid result from local evidence.

## Required handoff

Every phase handoff reports:

- stage completed and next legal stage;
- exact repository commit and artifact hashes;
- evidence produced, with commands/result identifiers;
- open items;
- stale proofs and the actions needed to refresh them;
- explicit PASS, REJECT, CARVE, or BLOCKED verdict.

Do not use `ready` when the active case's `open-items.json` contains a blocking finding, required proofs are missing, bytes have drifted, the live panel's required cohort is incomplete, successful-run medians or false-positive reviews are incomplete, or a live platform gate is pending.
