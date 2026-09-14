# Accepted patterns and provenance

Evidence snapshot: the workspace's Olympus Forge approved-candidate and hardness-calibrator references, updated August 31, 2026. The first six were recorded as live-verified August 26; Dora was user-confirmed August 31. The owner additionally confirmed Rust Analyzer and Scylla as accepted on September 12; see `knowledge/user-acceptance-confirmation-20260912.md`. These are historical acceptance records, not a fresh panel check or proof that a nearby local patch is the accepted patch. Preserve that distinction.

| Accepted task | Historical agent pass rate | Architectural interaction to learn |
|---|---:|---|
| Calyx — Preserve invoke combinational scopes during component inlining | 10% | Parse/print control intent, clone inline scopes, preserve analysis/cleanup and liveness, then lower sequential, branch, loop and parallel lifetimes correctly. A parser-only fix cannot carry scope ownership through the pipeline. |
| Ladybug — Support Composite Primary Keys for Native Node Tables | 15% | Ordered tuple identity crosses DDL/catalog, index/storage, DML, transactions, delete/reinsert, relationship COPY endpoints and persistence/export. Preserve existing scalar semantics. |
| Lisette — Add ownership-safe defaults to record fields | 30% | Declaration-owned defaults cross parse/format/type checking, zero values, enum/recursive cases, privacy/name resolution, construction/spread and lint/incremental cold/warm behavior. |
| KiteSQL — Support expressions in CREATE INDEX | 30% | Structural expression identity connects validation, catalog persistence, index keys, DML/NULL semantics, optimizer range/equality/covering choices, EXPLAIN and reopen. |
| DataFusion — Use Parquet Map Leaf Metadata for Row-Group Pruning | 40% | Key/value metadata paths, leaf statistics/null counts, Bloom filters and quantifiers interact with AND/OR three-valued semantics and conservative SQL scan pruning. No false pruning. |
| DataFusion — Preserve Aggregate UDF Overrides Across FFI Boundaries | 20% | Callback metadata and ABI ownership cross downcasts, error/absence handling, ordering/reversal hooks, codecs, loading and execution with producer-private implementations. |
| Dora — Support Concrete Patterns Over Trait Objects | Unknown | Unique implementation compatibility with trait arguments/associated bindings/generics, ambiguity, type-test-before-extract, bytecode producer/reader/verifier/dumper, Cannon/JIT/AOT and Boots x64/arm64, open-world exhaustiveness and object identity/GC. |
| Rust Analyzer — Aggregate macro-argument completions across mapped expansion positions | Unknown | Actual/speculative token correspondence, nested declarative and enclosing attribute expansions, independent receiver analysis, bounded traversal, aggregation and original-invocation edits interact. Preserve supported siblings after empty or unsupported branches. |
| Scylla — Preserve policy-aware coordinator affinity across paging | Unknown | Active policy eligibility, node/shard target ordering, retry and speculative winners, opaque manual continuations, prepared/caching APIs and subsequent-page state replacement interact. Test each eligibility reason independently and compose fallback with the next continuation consumption. |

`knowledge/accepted-cases.json` preserves IDs, local source references and explicit unknowns. `knowledge/original-approved-candidates.md` and `original-hardness-calibrators.md` preserve the full historical reference detail; retrieve relevant sections only. Historical source instructions do not override current workspace rules.

## Candidate decision before expensive construction

First clear denylist, repository fit, license/activity, exact commit, public issue/PR status, already-implemented alternatives, and internal occupancy/semantic duplicates. A subset of a previously occupied broader task can still be a duplicate. Repository eligibility is not task acceptance.

Require one observable behavior whose natural implementation involves at least three distinct subsystems and two interacting semantic barriers. Identify public-result dependence on state, order, lifetime, identity or proof. Require real repository discovery, three plausible compiling wrong architectures, and a deterministic behavioral oracle. File count and LOC are supporting observations, never the target.

Compare against all nine rows, then substantiate the two closest analogues on five axes: semantic coupling; state/order interaction; repository discovery; credible wrong architectures; deterministic feedback. Follow the full Forge hardness rubric: at least four of five axes must match the analogues, with no weakness hidden in coupling or discovery. Complete its 8/10 kill sheet with no zero in its first four criteria. If evidence is unavailable, record unproven instead of inventing scores.

Construct the complete natural reference before Scope. Use its real control/data flow and an executable wrong-architecture discriminator as evidence. A reduced Scope test set is representative testing of that full reference; it is not permission for a skeleton implementation.

## Stop lessons

Graft and an HTTP-mock task produced broad quick genuine passes; Godot's natural solution stayed mechanically concentrated despite a large-looking scope. These are signals to retire weak candidates early. They do not justify adding unrelated requirements, verbose scaffolding or test tricks.

A zero-pass rollout is not automatically high-quality difficulty. Classify infrastructure failures, contract ambiguity, genuine incomplete solutions and false positives. Any coherent contract reduction requires explicit scope reasoning, a valid reference, retained discriminating cases and newly invalidated gates. Never delete a failed case merely to rescue a score.

## Reuse boundaries

Reuse the semantic questions and public counterexample shapes, not accepted code as a generic template. The local `calyx-inline-invoke-comb-second` record says the concept was already an accepted submission and rejects it for occupancy; its folder name does not bind its patch to that acceptance. The local `datafusion-ffi-custom-physical-expr` is a different task from either accepted DataFusion reference. Accepted artifact hashes remain unknown until matched to an acceptance receipt.
