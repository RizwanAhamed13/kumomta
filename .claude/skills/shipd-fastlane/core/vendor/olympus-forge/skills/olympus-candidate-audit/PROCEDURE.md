---
name: olympus-candidate-audit
description: Scout, rank, screen, and qualify Shipd/Olympus repository candidates before full artifact construction or paid gates. Use for repository hunting, candidate selection, plagiarism and overlap checks, maintainer and pull-request screening, project-fit checks, and candidate rejection decisions.
---

# Olympus candidate audit — stages 1-4

This is the candidate-qualification phase of `$olympus-workflow`. Keep the original stage numbering and firing order. Fill each prompt block's placeholders, apply its packaged laws, and complete its handoff before advancing.

Before taking candidate action, read [the shared laws](../olympus-workflow/references/shared-laws.md), [the platform contract](../olympus-workflow/references/platform-contract.md), [the state schema](../olympus-workflow/references/state-and-proof-schema.md), [the lessons ledger](../olympus-workflow/references/lessons-ledger.md), [the hardness calibrators](../olympus-workflow/references/hardness-calibrators.md), and [the local validation gates](../olympus-workflow/references/local-validation-gates.md) completely. Also read the workspace `.olympus/lessons.md`, `.olympus/repo-scouting-results.md`, `.olympus/portfolio.md`, and non-collision claim registry completely before ranking. The workspace ledger is append-only evidence: apply every reusable rule, but do not promote hypotheses, unfinished packages, or unaccepted cases into positive calibrators. Initialize any missing state as specified by the shared references.

Before ranking or claiming any repository, run `python3 <core-root>/vendor/eligibility/scripts/check_disallowed_repo.py --repo <owner/name>`. A match is a terminal repository-level rejection. Missing or invalid denylist evidence blocks selection at `REVIEW`. Preserve the normalized repository, denylist SHA-256, entry count, date, and checker output in the scouting ledger and candidate record, and repeat the check immediately before Scope Gate.

## 1. Scout repos

```
GOAL: find 3-5 obscure repos worth an ISSUE-LED or FEATURE-PIONEER Olympus task.
LAW: shared Candidate law + lessons L02, L09, L10, and L11 + the workspace scouting ledger.

DROP on any fail:
- repository appears in the authoritative disallowed-repository list
- under 500 stars (600-3000 ideal; less famous = better)
- default-branch HEAD older than 12 months. Read `repos/<r>/commits/<default_branch>`, not "updated at" and not "pushed at". Also check the commit authors and report the last HUMAN commit date - dependabot merges are not development.
- license not clearly permissive - enumerate and READ every governing root, package/workspace, and applicable nested license; one disallowed license drops a multi-license repository (NCSA, conditional BSD = drop)
- language not Rust/Go (C++ only for an exceptional find; never Python/TS)
- already in the burned/killed lists

Before KEEP, inspect the native test surface for deterministic focused filters, offline feasibility, per-test identity, and an objective public oracle. KEEP only repos with a code-only subsystem: its own file format, its own invariants, its own semantics - rules a solver can ONLY learn by reading this repo. If the rules are Googleable (public spec, standard protocol, textbook), the repo is useless.

PROVE every positive claim with live repository/web evidence - stars, dates, license, and discovered overlaps. For absence claims, record the exact search surfaces, aliases, queries, dates, and bounded-confidence verdict; never represent a finite search as absolute proof that nothing exists.

SEARCH BOTH ORIGIN TRACKS:
- ISSUE-LED: a real open maintainer-accepted issue with no active implementation.
- FEATURE-PIONEER: a missing repository-native capability evidenced by a TODO, explicit unsupported combination, asymmetric inverse operation, documented invariant gap, or executable public-behavior probe. Issue URL optional; README fit, finite contract, and absence of a public solution are mandatory. Never create an issue or contact a maintainer without user authorization.

NO-IMPLEMENTING-OR-ANNOUNCED-WORK VETO: before KEEP, search open, merged, and closed-unmerged PRs, issue timelines, linked branches, referenced commits, named forks, and equivalent feature synonyms. Reject when any public PR or patch implements either the complete capability or its central solver lesson. PR status, abandonment, and non-merge do not rescue the candidate. Reject as well when a maintainer explicitly says the capability is already being implemented or actively worked on, even if the implementation is not public yet. A prerequisite PR is non-colliding only when concrete source evidence proves that the full candidate's semantic core, repository-discovery decision, and observable state transition remain unimplemented; record that boundary explicitly.

OUTPUT per repo: name + link, stars, license, HEAD date, language, the code-only subsystem, origin track, issue/source-evidence links. Present the TOP 3 ranked to the user (they pick); log EVERY candidate checked into `.olympus/repo-scouting-results.md` so no hunt is wasted.
```

## 2. Pick the problem

```
GOAL: the TOP 3 candidate tasks in <REPO> (ranked, user picks), each plausibly inside the current panel's difficulty band when the evidence supports it. If the current target is 30-40% over ten valid runs, treat 2-4 plausible solves as a paper hypothesis only. Never tune toward zero solves.
LAW: shared Candidate law + hardness calibrators + lessons L03, L08, L09, L10, and L14. Fill the full scorecard below; skip no line.

THE ONE QUESTION: where must the solver DISCOVER the rules by reading this repo's code? "Nowhere" = REJECT. Public specs and standard semantics are compliance, not discovery.

INSTANT REJECT: textbook algorithm; feature that plugs into existing machinery (glue); one clever self-contained module; anything a strong engineer finishes in an afternoon; anything where coding could start 5 minutes after reading the issue; same theme as a prior task by this author (task #1 tonbo = schema-lineage / historical-version reads).

ANTI-MECHANICAL REJECT: if the reference is mainly “add a field/value, serialize it, thread it through call paths, replace a constant, update adapters,” reject even when it spans 15-20 files and 300+ LOC. Graft page-size propagation produced 2/2 genuine solves in about 14 minutes despite 19-21 changed source files. Breadth and compiler-guided edits are not difficulty.

FRAGILITY TEST - run it here, not after building. REJECT on ANY of these four (user rule 2026-08-03, "we will not pick fragile task from next time"):
 F1 the deliverable is a PLACEMENT or DIAGNOSTIC, not a VALUE or RESULT. "Emit exactly one correctly-attributed line" opens a fresh false-positive vector for every shape the language allows - CTE body, subquery, view body, UNION branch, nested tree, same-name collision, comma-joined pair. "This query returns X" opens none.
 F2 getting it WRONG does not change observable output. Then the agent gets no signal from its own testing, and no hidden test can catch an implementation that reports correctly while behaving wrongly.
 F3 the prompt must prescribe an output string or format - reliably draws over-specification flags from Quality and Alignment.
 F4 the difficulty is a HIDDEN requirement rather than algorithmic depth. Hidden difficulty evaporates the moment one clause is added, and a grader may call it unfair.

EVIDENCE (stoolap adaptive-join, task #2): hit F1+F2+F3 together. Three false-positive rounds, 11 vectors closed by mutation, one PROVABLY unclosable (no observable exists for "the strategy that actually executed"), ~2 days lost. Every agent ran the test suite, saw green, and shipped a wrong attribution - because F2 means the code cannot tell you.

PREFER INSTEAD: a correctness or semantics defect - wrong results under some condition. Same LOC, same multi-file coordination, same discovery depth, but wrongness is visible in the result, so tests can catch cheats and the difficulty cannot be argued away.

MUST PROVE (one concrete sentence each, naming real subsystems):
- forced order: A must be built before B before C
- partial work fails MANY tests, not its share
- one value must stay correct across 2+ subsystems
- two semantic barriers interact, rather than forming independent checklist rows
- three plausible complete-looking wrong architectures compile/run but change public results
- one material design rule must be discovered from repository code, not the prompt, compiler, or public spec

HARDNESS KILL SHEET: score semantic coupling, state/order interaction, repository discovery, plausible wrong architectures, and deterministic feedback from 0-2. Require 8/10 and no zero in the first four. A passing score never rescues a mechanical-propagation task.

ACCEPTED-ENVELOPE GATE: compare every candidate against every accepted calibrator in `hardness-calibrators.md`, currently Calyx invoke scopes, Ladybug composite node keys, Lisette field defaults, KiteSQL expression indexes, DataFusion Map-leaf pruning, DataFusion aggregate-UDF FFI, and Dora concrete trait-object patterns. Fill every comparator row; do not cherry-pick the easiest or closest example. PASS only when the candidate clears the shared accepted floor, matches or exceeds both closest architectural analogues, and is not weaker on a core dimension merely because it has more files or LOC. If fewer than two calibrators are meaningfully analogous, return REVIEW and gather more evidence instead of selecting. Historical accepted pass rates describe evidence, never a target to tune.

NUMBERS: aim 500-1100 real logic lines (platform gate = 200 EFFECTIVE-LOC agent-median; under 500 OK when measurably hard - 1100 hard cap), 4+ files, 2+ modules, 15+ behaviors, and no single trick that collapses the work toward the 200 gate.

MODEL TO COPY (fjall keyspace precedent): engine-native semantics threaded through several subsystems, deterministic oracle, many interacting behaviors.

OUTPUT per candidate: origin track and evidence, filled scorecard, hardness kill sheet, complete accepted-envelope matrix, two closest analogues and why, biggest shortcut, lessons applied, PASS / REVIEW / REJECT-because-<reason>. A paper PASS authorizes only a full reference implementation and executable hardness proof; it does not qualify the candidate for Scope Gate. Only a post-implementation hardness PASS may advance.
```

## 3. Plagiarism screen (before anything else)

```
GOAL: kill <TASK CONCEPT> in <REPO> now, before it costs tokens.
LAW: shared Candidate law + lessons L02 and L11 + the workspace scouting ledger.

1. LOCAL: search `.olympus/repo-scouting-results.md` and submissions/ for the repo under ALL its names, and for the concept. Any hit on built/burned/off-limits = STOP.
2. LIVE SEARCH (never memory): does this feature/inverse already exist anywhere, in any language? Search "<feature> writer", "<feature> library", "<repo> <feature> PR". A public spec or existing implementation = the discovery gap is fake = REJECT. (EVTX died exactly here: a public format spec + xml2evtx already existed.)
3. TEXTBOOK TEST: would a second contributor independently build this exact thing? Famous algorithm name = REJECT.
4. The platform pool is invisible - only the 2-token Scope Gate truly dedups. This screen exists so the gate is not wasted on an obvious collision.

OUTPUT: CLEAN or COLLISION, with evidence links, all PR states searched, issue/timeline/branch/commit/fork surfaces searched, synonyms used, prerequisite-versus-implementation boundaries, confidence, and expiry. Repeat this screen after the complete reference reveals the real architecture and immediately before final delivery.
```

## 4. R2/R3 sweep (PRs + maintainer veto)

```
GOAL: prove nobody built <FEATURE> and no maintainer killed it.
LAW: shared Candidate law + lessons L01 and L11.

R2 - existing work: search open, MERGED, and CLOSED PRs, linked branches, referenced commits, and named contributor forks. Closed-unmerged still kills. Any public implementation of the complete capability or central solver lesson is terminal prior art even when the issue remains open. Search by issue number, feature keywords, similar names, verb-object-invariant phrases, and production-surface names.
R3 - veto: search issue/PR/discussion COMMENT BODIES (GitHub API, in:comments), not titles. Read every OWNER/MEMBER/COLLABORATOR reply. Verdicts hide in old threads. ISSUE-LED requires acceptance; FEATURE-PIONEER requires no conceptual veto plus strong source evidence and does not invent maintainer approval.
R4 - fit: quote the README sentence stating the project's purpose. Grade the task STRONG / MODERATE / WEAK against it. WEAK = reject.

Classify R3: DECLINED = dead. WANTED = best. SILENT = ok.
OUTPUT: verdict per rule, with links and exact quotes.
```
