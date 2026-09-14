# Olympus hardness calibrators

Read this file during candidate selection and before interpreting a fast solver pass. Difficulty must come from fair semantic interaction, not size, hidden clauses, or implementation checklists.

## Live-verified accepted calibrators

The signed-in Submissions page showed the first six accepted tasks on 2026-08-26. On 2026-08-31 the user confirmed that the Dora concrete trait-object-pattern task was also accepted; its final approved artifact evidence is preserved locally, while its displayed rate and challenge ID still need a fresh live-page capture. These seven tasks are the current positive set for this workspace until the live accepted list changes.

| Accepted task | Repository | Displayed rate | Semantic core and forced chain |
|---|---|---:|---|
| Preserve invoke combinational scopes during component inlining | `calyxir/calyx` | 10% | A new dynamic control scope had to round-trip through parser/printer, survive cloned-control inlining, remain live in analyses/cleanup, and lower through sequential, branching, looping, parallel, and separately compiled control without lifetime leakage. |
| Support Composite Primary Keys for Native Node Tables | `LadybugDB/ladybug` | 15% | Ordered tuple identity had to remain collision-free across DDL/catalog, storage/index encoding, CREATE/MERGE/MATCH, transactions/delete/reinsert, relationship COPY endpoint binding, schema export/import, and reopen while preserving scalar keys. |
| Add ownership-safe defaults to record fields | `ivov/lisette` | 30% | Declaration-owned defaults crossed parsing/formatting, type and zero-value analysis, enum recursion, package privacy/name resolution, construction/spread precedence, lint/usage behavior, incremental cache, and cold/warm builds. |
| Support expressions in CREATE INDEX | `KipData/KiteSQL` | 30% | Complete structural expression identity constrained validation, catalog persistence, key construction, DML/NULL maintenance, optimizer matching, range/equality scans, covering-index rules, explain output, and reopen. |
| Use Parquet Map Leaf Metadata for Row-Group Pruning | `apache/datafusion` | 40% | Map key/value leaf selection, flattened statistics, null counts, Bloom filters, candidate quantification, AND/OR three-valued conservatism, SQL planning, and Parquet scan pruning had to agree without false positive pruning. |
| Preserve Aggregate UDF Overrides Across FFI Boundaries | `apache/datafusion` | 20% | Producer-defined callbacks and metadata crossed ABI representation, ownership/lifecycle, concrete expression downcasting, errors/absence, aggregate-returning hooks, ordering/reversal reconfiguration, codecs, loading, and execution without consumer access to the private implementation. |
| Support Concrete Patterns Over Trait Objects | `dinfuehr/dora` | not captured | Static compatibility and unique implementation selection crossed trait arguments, associated bindings, generic specialization and ambiguity; lowering added type-test-before-extraction semantics; bytecode representation, writer/reader/verifier/dumper, Cannon JIT/AOT closure, the self-hosted Boots compiler on x64/arm64, open-world exhaustiveness, identity, mutation visibility, and GC safety all had to agree. |

Evidence: live accepted challenge IDs `kh763xwhkq11gc38ata5g1rn358cgw9m`, `kh7037hnydbvan6167ssq2cwrx8c7425`, `kh7ctmnq19q2qn7sn2sf5nektx8c63ks`, `kh76cw7dz3e4cm5wg4nwzdfjyh8bkwj7`, `kh7b3bb3afj470xz4vyyt1q2kn8b3zeq`, and `kh7dzpzqdxx7wyg8zz12e9673s8atwq5`. Dora acceptance is user-confirmed and backed by its preserved final approved report; capture its live ID and displayed rate before using those fields in a platform claim. Rates are historical evidence, not forecasts or quotas.

### Shared accepted floor

Every selected candidate must satisfy all of these before construction:

1. One repository-native invariant changes the design of at least three materially distinct subsystems; independent adapter coverage does not count.
2. At least two semantic barriers interact, such as identity plus persistence, lifecycle plus ABI, scope lifetime plus lowering, or conservative logic plus metadata routing.
3. Operation order, state transition, lifetime, structural identity, or conservative proof changes an observable public result.
4. A material rule must be discovered from pinned repository code or behavior. A prompt-enumerated checklist, public spec, compiler-guided propagation, or known textbook algorithm is below the floor.
5. At least three plausible complete-looking architectures compile and run yet deterministically produce a wrong public result.
6. A solver can obtain tight deterministic feedback from public behavior; difficulty cannot depend on timing, diagnostic placement, exact prose, or hidden implementation choices.

Implement the complete natural reference solution before Scope Gate. Paper
architecture, a skeleton, or a reduced solution is not hardness evidence.
Measure the working production diff, execute representative cross-subsystem
behavior, and compare the actual implementation chain and discovery decisions
to the calibrators. Freeze the full `problem.md` and `solution.patch` only
after that executable comparison passes. A later compact gate suite may reduce
test repetition, never production behavior. Conversely, do not inflate the
solution with unrelated work merely to approach a LOC target. Favor natural
goldens around 500 or just above when the semantic floor is already met; LOC
remains a horizon signal, never a pass.

### Every-accepted-task comparison

For every candidate, create a matrix with one row per accepted task and these columns:

`calibrator | analogous invariant | shared forced subsystems | interacting barriers | repository-only discovery | plausible wrong architectures | deterministic oracle | five-dimension weaker/match/stronger scores | evidence`

Compare every current accepted calibrator. Then name the two closest architectural analogues. PASS requires:

- the shared accepted floor is met without exceptions;
- the ordinary 8/10 kill sheet passes with no zero in the first four dimensions;
- the candidate is `match` or `stronger` than both closest analogues on at least four of the five scored dimensions and is not weaker on semantic coupling or repository discovery;
- no anti-mechanical, fragility, overlap, maintainer-veto, or already-implemented rejection applies.
- the complete reference implementation and focused executable probes confirm the predicted cross-cutting chain; a skeleton-only comparison cannot PASS.

If fewer than two accepted tasks are meaningfully analogous, return `REVIEW`, not `PASS`. Acquire executable architecture evidence or scout a better candidate. This is an evidence gate, not permission to enlarge scope.

The machine-readable `hardness-proof.json` hash-locks `problem.md` and
`solution.patch`. Each calibrator row contains `evidence` and a
`scored_dimensions` object with exactly `semantic_coupling`,
`state_order_interaction`, `repository_discovery`, `wrong_architectures`, and
`deterministic_feedback`, each rated `weaker`, `match`, or `stronger`. The two
exactly named `closest_analogues` must be match-or-stronger in at least four of
five dimensions and may not be weaker in semantic coupling or repository
discovery.

## Rejected calibrators

| Task | Observed genuine passes | Classification | Transferable reason |
|---|---:|---|---|
| Graft per-volume page size | 2/2 in about 14 minutes each | easy negative | Solvers changed 19–21 source files, but most work was compiler-guided propagation of one value through named paths and constants. |
| HTTP response trailers | 3/3 | easy negative | The prompt enumerated the architecture, so broad path coverage did not leave a difficult design decision. |

Use the positive examples as structural bars, not target pass rates. Only completed platform cohorts measure a new task's rate. Do not count a draft, Scope Gate pass, completed package, Auto Review approval, or saved genuine solve as an accepted positive unless the live Submissions page shows `Accepted`.

When the current live assignment targets 30–40%, paper-audit candidates for a 20–40% plausible interval with a 30–40% center when evidence supports it. Otherwise copy the current target from the panel. Never tune toward zero solves, and never claim a precise rate before the required platform cohort.

## Anti-mechanical rejection

Reject regardless of LOC, files, tests, or message estimates when the implementation can be summarized as:

`add a field/value -> serialize it -> thread it through call paths -> replace a constant -> update adapters`

Compiler errors revealing the next edit are navigation, not difficulty. Independent path coverage is breadth, not semantic coupling.

## Hardness kill sheet

Before artifact construction, write and score all five dimensions from 0–2:

1. **Semantic coupling:** at least two concerns constrain the same design choice.
2. **State/order interaction:** operation order, persistence/reopen, rollback, remapping, or identity changes the result.
3. **Repository discovery:** a material rule must be inferred from this repository rather than the prompt, compiler errors, or a public specification.
4. **Wrong architectures:** at least three plausible full-looking implementations compile and run but yield observably wrong results.
5. **Deterministic feedback:** solvers can discover wrongness through public behavior without hidden requirements or timing.

Require at least 8/10 and no zero in dimensions 1–4. The score never overrides the anti-mechanical rejection. Also state the forced order and why partial work breaks multiple behaviors rather than only the omitted path.

## Candidate origin tracks

- **ISSUE-LED:** use an open, maintainer-accepted issue with no active or prior equivalent implementation.
- **FEATURE-PIONEER:** an issue URL is optional. Evidence must come from a TODO, explicit unsupported combination, asymmetric inverse operation, documented invariant gap, or executable public-behavior probe. The feature must strongly fit the README purpose, have a finite deterministic contract, introduce repository-native semantics, and have no public solution to copy.

Feature pioneering is a scouting route, not a way to append scope to an easy candidate. Once fast independent solves converge on the same mechanical architecture, reject and pivot.

## Early cohort stop

- One fast genuine pass does not establish the rate. If its architecture is mechanical, pause the full batch and audit the candidate.
- Two independent fast genuine passes using the same straightforward architecture are a rejection signal when the current assignment targets a materially harder band; do not buy the remaining batch or add artificial scope.
- Three of three genuine passes is a hard stop.

Preserve all runs and report the observed cohort literally. Never extrapolate an exact platform rate from a small sample.
