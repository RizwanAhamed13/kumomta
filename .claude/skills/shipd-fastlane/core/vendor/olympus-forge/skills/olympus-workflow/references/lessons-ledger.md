# Olympus lessons ledger

Read this ledger completely at the start of every Olympus Forge phase. Apply the rule, not the anecdote. When a new failure teaches a reusable rule, append `date | case | mistake | cost | rule` to the workspace `.olympus/lessons.md`; do not rewrite history or silently generalize an unproven hypothesis.

## L01 — Glauth: maintainer veto hidden in old comments

- Mistake: searched titles and obvious current issues but did not search old issue, PR, and discussion comment bodies or classify maintainer roles.
- Cost: a two-token gate and roughly one build day were spent before a 2021 maintainer comment killed the work.
- Rule: before building, search open, merged, and closed PRs and all comment bodies using issue number, feature synonyms, and conceptual terms. Read replies from OWNER, MEMBER, and COLLABORATOR accounts. Classify the result as DECLINED, WANTED, or SILENT.

## L02 — EVTX: public ecosystem erased discovery depth

- Mistake: treated a feature as repository-native even though a public format specification and an existing writer already exposed the rules.
- Cost: the candidate died at plagiarism screening.
- Rule: search public specifications, writers, readers, inverse tools, libraries, and implementations in other languages before Scope Gate. If a solver can obtain the hard rules outside the repository, reject the candidate.

## L03 — Stoolap: diagnostic and placement fragility

- Mistake: selected a feature whose main deliverable was attribution/placement, whose wrong internal behavior did not reliably change observable output, and whose prompt needed exact output wording.
- Cost: three FP rounds, eleven closed vectors, about two days, and one unclosable vector because no observable distinguished the claimed internal strategy.
- Rule: reject candidates when the deliverable is placement/diagnostic rather than a value, wrongness is not observable, exact output formatting is required, or difficulty lives in an unstated implementation choice. Prefer semantic result defects.

## L04 — Stoolap: sparse coverage shapes survive hardening

- Mistake: three earlier FPs were closed, but the suite still omitted boolean cells, points strictly between tested boundaries, and distinct statement shapes.
- Cost: six more surviving implementations were found.
- Rule: enumerate every relevant boolean pair's four cells, test values inside boundary gaps, and exercise each changed routing/statement shape. Apply this while authoring tests, not after paid checks.

## L05 — Stoolap: a translated probe stopped discriminating

- Mistake: the executable probe caught a collision using the same table pair, but the permanent test changed the pair and no longer killed the mutant.
- Cost: two agents shipped the same false positive.
- Rule: after moving any probe into the suite, rerun the exact reference and exact broken implementation. A passing prose argument is not evidence.

## L06 — Stoolap: post-edit proof drift

- Mistake: small solution or test edits were treated as local and earlier checks were carried forward.
- Cost: graded bytes and shipped bytes diverged, reopening fairness and FP findings.
- Rule: hash all four artifacts. Any edit refreshes the complete dependent proof set, including agent replay and the grader loop. Freeze only after the last proof.

## L07 — Music21 and VersityGW: local rates do not forecast platform rates

- Evidence: Music21 moved from about sixty percent locally to zero on platform; VersityGW moved from one of three locally to twenty-four of twenty-six on platform.
- Rule: use local agents to learn why implementations fail, never to assert the platform rate or a ceiling. Only completed platform runs measure the platform pass rate.

## L08 — Stoolap approval: difficulty needs a floor and a ceiling

- Evidence: a roughly twenty-percent platform pass rate was judged hard and approved.
- Rule: target at least one genuine solve and no more than fifty percent passing; aim below thirty percent when the task remains fair. Zero passing runs are a solvability failure, not success.

## L09 — Tonbo: author-theme repetition lowers novelty

- Mistake to avoid: selecting another schema-lineage or historical-version-read task after an earlier task by the same author used that theme.
- Rule: screen the author's previous submissions by concept, not only repository. Prefer a different subsystem and semantic core.

## L10 — Fjall: positive architecture pattern

- Evidence: engine-native semantics had to remain correct across several subsystems, with a deterministic observable oracle.
- Rule: prefer tasks where one value/invariant is threaded through forced multi-module stages and partial work breaks several behaviors.

## L11 — Root-enum overlap rejection: narrowing is still duplication

- Mistake: reused the same root-enum ORM feature with a narrower supported shape and different APIs/internal wiring after an older accepted candidate covered the difficult semantic core.
- Cost: overlap rejection.
- Rule: compare core solver work, data model, validation, persistence, querying, and CRUD semantics. Alternate decomposition or reduced scope does not create novelty. Burn that repository/concept combination and pivot.

## L12 — HTTP trailer hardening: cover valid-domain classes and path interactions

- Mistake: broad claims about header-typed trailers were initially exercised through only a few ordinary values and paths.
- Proven survivors: ordinary-header leakage; empty valid values; underscore-containing valid names; obs-text values; Base64 static-YAML input; binary reverse export; and path-specific conversion loss.
- Rule: derive equivalence classes from the stated public type domain and cross them with every changed serialization/conversion route. Each added case still needs executable proof: current suite passes the broken variant, reference passes the discriminator, and broken variant fails it. Stop after stated classes and changed paths are closed; arbitrary predicates are not a bounded contract audit.

## L13 — Graft: typed error matching can still be an unfair pin

- Mistake: hidden tests matched two exact Rust error variants and their expected/actual field layouts even though the prompt guaranteed only logical rejection, write rejection, and non-mutation; neither variant existed at the pinned commit.
- Cost: Test Fairness failed 2 of 23 assertions, and the test edit made the four-state matrix, mutation evidence, graders, and platform results stale.
- Rule: assign every failure path an error-contract level before writing tests: exact representation, existing public category, or rejection only. Match only the strongest prompt- or repository-grounded level, then test the promised observable aftermath. Never promote a representation invented by the golden into a hidden requirement merely because it is typed or public.

## L14 — Graft: many files can still be mechanically easy

- Mistake: treated a 17-file reference and broad persistence, remote, hydration, and SQLite coverage as evidence of solver difficulty.
- Cost: two independent Nova agents both produced legitimate solutions in about fourteen minutes, changing 19–21 source files; the observed cohort was 2/2 and further rollout spend could not meet the intended 30–40% profile without artificial hardening.
- Rule: reject tasks whose edit graph is compiler-guided propagation of one value through named paths. Before building, require interacting semantic barriers, a repository-native discovery decision, and three plausible complete-looking wrong architectures. After two fast independent passes converge on the same mechanical design, preserve the runs and pivot.

## L15 — Ladybug: suspicion is not a false-positive verdict

- Mistake: static code patterns and plausible regressions were sometimes treated as confirmed rollout FPs before the exact candidate/reference pair was executed; later hosted adjudication found genuine passes or reference-shared behavior.
- Cost: unnecessary hardening risked killing valid solvers, repeatedly staled paid evidence, and created confidence claims stronger than the proof.
- Rule: call a rollout FP only after four exact-byte facts: candidate passes the current suite, the discriminator is prompt- or repository-grounded, reference passes it, and candidate fails it for the alleged reason. Replay preserved genuine solves before shipping the test. Static review produces hypotheses only; a reference-shared failure is a golden/spec gap, and a current hosted adjudication controls that run's record.

## L16 — Ladybug: build artifacts can manufacture both passes and failures

- Mistake: base and new wrappers shared a mutable Ninja tree, generated parser objects survived from transient solver sessions, and synthesized JUnit failures were mistaken for executed tests.
- Cost: flaky process cases, a baseline that never ran, an apparent grammar pass not reproducible from the delivered patch, and multi-hour external-error runs.
- Rule: use isolated build directories or one build-wide lock; never configure/link base and new concurrently. For generated sources, ship consistent inputs, checksum, and generated output, preload the generator offline, delete the affected object, and prove a clean rebuild from delivered bytes. Parse raw JUnit: missing-output/process synthesis after a build race is contestable environment evidence, not an agent regression and not a pass.

## L17 — Ladybug: scalar-to-vector work needs a consumer-and-equality matrix

- Mistake: early suites validated the central tuple encoder but missed legacy singular consumers and equality differences across local CREATE, persistent lookup, batch COPY, optimizer, relationship binding, and catalog/export paths.
- Cost: successive passing implementations exposed distinct regressions: individual key components treated as unique, signed zero deduplicated on one path but not another, relationship property mapping displaced by positional endpoints, shared endpoint names colliding, and order lost on persistence routes.
- Rule: inventory every old scalar consumer and every new vector path. Cross declaration order versus schema order, arity, supported leading/trailing component types, local/persistent/batch uniqueness, no-index behavior, transaction and delete/reinsert visibility, optimizer uniqueness, update protection, relationship endpoint arity/name overlap, and catalog export/reopen. Preserve unrelated scalar behavior with focused regressions. Stop when this bounded path/class matrix is closed; do not append arbitrary combinatorial cases.

## L18 — Ladybug: regression breadth, solvability, and contesting have different jobs

- Mistake: an unrelated one-test baseline gave no regression protection; later broadening and FP hardening were discussed as if they could not affect pass rate, and environment contests were spoken of as solution evidence.
- Cost: Auto Review rejection, unstable broad tests, and unreliable pass-rate expectations.
- Rule: base mode runs a small deterministic set adjacent to every materially touched subsystem. Add a regression only when grounded and useful, then rerun fairness/flakiness. Never promise an unchanged rate after artifact edits and never tune toward zero solves; at least one durable genuine pass must survive. Contest text proves only that a run should be excluded or rerun, using exact logs showing no assertions ran and an unchanged successful retry.

## Logging rule

Record only lessons supported by an observed rejection, platform result, saved rollout, or executable reference-versus-mutant proof. Include the cost and an operational rule that changes a future stage. Do not turn speculation into policy.
