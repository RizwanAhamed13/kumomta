# Platform and evaluator contract

Read this reference before environment work, any live-panel action, or final delivery. It preserves the useful evaluator controls from the archived monolithic workflow while keeping the live panel authoritative.

## Authority and capture

1. Read the live panel immediately before an authorized action. Copy the current required fields, allowed image/base, check order, cost, minimum runs, pass-rate ceiling, cheating limit, and successful-run medians into the case checkpoint.
2. Treat numbers below as historical examples only. Never reuse them without a current panel record.
3. Capture each result identifier, timestamp, artifact hashes, displayed cost, status, decisive output, and whether the result is current or stale. Record the authorized ceiling and every spend through `case_state.py budget`; stop before exceeding it.
4. Never infer a hosted PASS from a local mirror. Never automate login, OTP, reservation, clocking, acceptance, or submission.

## Repository and originality

- Verify public URL, exact resolvable commit, current activity, supported language, governing licenses, project fit, and any current size/star rule.
- Search open, merged, and closed pull requests, issue cross-references, discussions, comment bodies, public specifications, inverse tools, and equivalent implementations.
- Run the duplicate audit before construction, after the reference is complete, and immediately before final delivery. A prior or unmerged equivalent implementation is a collision.
- Record search queries, aliases, surfaces, dates, links, maintainer roles, and confidence. Absence is bounded search evidence, not absolute proof.

## Artifact and environment checks

- Use the exact artifact names required by the live panel. The current workflow canonical names are `problem.md`, `test.patch`, `solution.patch`, and `Dockerfile`; accept a legacy description filename only when the panel explicitly does.
- Use the current allowed `:latest` base image. Never put an `@sha256` digest in the submitted Dockerfile; record the resolved image digest in evidence or build logs.
- Build from the untouched exact commit. Apply patches only after image creation when that matches the evaluator.
- Set `WORKDIR /app`, install or hydrate dependencies at build time, run no tests during image build, and end with the required Bash command.
- Reproduce the evaluator user, UID, login-shell environment, file permissions, cache homes, locale, timezone, and runtime network isolation. Do not validate solely as root when the platform runs as an unprivileged user such as `model:1000`.
- Make canonical repository test commands discoverable from standard project files and usable offline. Narrow exclusions require evidence of unrelated network, resource, or pre-existing flaky behavior.
- Run the four-state matrix in clean, isolated states with separate build caches: every base testcase passes before and after solution; every new testcase fails before and passes after. Parse JUnit per testcase and require the pre-solution `new` passing count to equal zero. A wrapper-level nonzero exit is insufficient because it can hide baseline-valid cases mixed into `new`.
- Produce valid JUnit for every required mode and preserve individual failures.
- Run one controlled build at a time. Never launch base and new wrappers that mutate the same Ninja/Make/Cargo build directory concurrently. A lock that covers only part of configure/build/link is insufficient.
- If solver edits can trigger code generation, provision the generator and runtime offline or require complete generated output in the patch. Force a clean rebuild of the generated translation unit during validation so an inherited object cannot hide missing generated data.
- Distinguish real test failures from harness synthesis. JUnit cases such as `missing from JUnit` or a generic process case after an object/link race mean the tests did not execute; preserve the logs and request an isolated rerun rather than blaming the agent.

## Fairness and integrity

- A developer must be able to pass from the brief plus the pinned repository.
- Every requirement maps to an observable assertion; every assertion maps to prompt or repository grounding.
- Tests never inspect the solution, detect the evaluator, hardcode reference artifacts, install dependencies, fabricate reports, or pin an internal design absent from the public contract.
- Exact formulas, rounding, precision, ordering, or representation are stated only when exact outcomes are truly contractual.
- Failure assertions use the strongest grounded contract level: exact representation, existing public category, or rejection only, plus the promised observable aftermath.

## Paid checks and adaptive rollout order

Use the exact order displayed by the current panel. The durable default is:

1. Scope Gate on the frozen complete `problem.md` and `solution.patch` with a reduced representative `test.patch`, unless the current user explicitly waived only that gate and the exact instruction plus frozen problem/solution hashes are recorded as `scope-gate-override`. A waiver is not a paid result or PASS.
2. Full local deterministic validation and grader loop on stable bytes.
3. Cheap structural/image checks, Verify Tests, and Verify Solution.
4. Fairness, environment, flakiness, task, solution, and description quality checks.
5. One Quick Check when available; inspect the full transcript.
6. Continue in small increments, normally pairs, only while the evidence supports further spend.
7. False-positive review for every passing run, then Holistic and Auto Review when all prerequisites are current.

Pause when ambiguity, platform failure, cheating, a false positive, mechanical architecture, insufficient/absent genuine solves, or a spend whose result cannot change the next decision appears. Batch artifact fixes; every dependent hosted result becomes stale after an edit.

## Rollout accounting

- Treat rollout re-evaluation as a separate paid path. After a `test.patch` and/or
  `solution.patch` edit, rerun the required checks and inspect the live panel for a Re-eval offer
  **before starting any fresh rollout**, because even one fresh run dismisses the offer.
- Re-evaluation is eligible only when every solver-visible input is unchanged: title,
  `problem.md`/description, repository and commit, and environment. Record a
  solver-visible-input fingerprint for the source batch and current version. A test- or
  solution-only edit may preserve eligibility; a title, description, repository/commit, or
  environment edit requires fresh solving.
- A successful Re-eval supplies fresh grading/evaluation verdicts for the current artifact set
  while reusing the prior agent solutions. Bind each result to both the current hashes and its
  source rollout/batch ID. Do not charge or rerun solutions that already received a fresh verdict.
- A failed Re-eval is a refunded platform action when the panel says so; record the failure and
  refund, confirm the button returned, and retry only with authorization. Never count it as a
  rollout pass or fail.
- The announced approximate discount is historical guidance only. Capture the displayed current
  cost and obtain authorization before clicking Re-eval.
- Classify every run as genuine pass, genuine agent defect, task ambiguity/unfairness, cheating/gaming, or environment/platform failure. Only panel-valid pass/fail runs enter the denominator.
- Compute pass rate from all valid runs. Compute LOC, file, and message medians from genuine successful runs only. Reference-solution size is an early warning, never the reported median.
- A passing run is durable only after its false-positive review passes and its patch/transcript are preserved and replayable.
- A false-positive disposition is durable only after exact candidate/reference reproduction. If the reference shares the failure, classify a reference/spec gap; if the alleged candidate failure was never executed, keep it as a hypothesis. A current high-confidence hosted adjudication controls the run record.
- Record model/version, elapsed time, patch metrics, transcript messages, architecture fingerprint, verifier result, and any contest status.
- Use `scripts/rollout_metrics.py` with thresholds copied from the live panel. Its confidence interval and early-stop signals support judgment; the completed platform cohort remains authoritative.

Historical 2026-07 examples included 10 valid runs, a 40% ceiling, two successful files, 40 successful messages, 250 effective successful LOC, and cheating below 20%. These are examples, not defaults.

## Final acceptance

Do not claim acceptance until current panel evidence proves every required check, minimum valid cohort, at least one durable genuine solve, pass-rate and median thresholds, acceptable cheating, no unresolved environment blocker, no false positive, Holistic, Auto Review, and any manager confirmation. Freeze exact approved bytes.
