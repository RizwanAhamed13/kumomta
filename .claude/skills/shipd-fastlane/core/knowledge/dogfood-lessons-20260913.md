# Lessons from the accepted-case reconstruction

**Final synthesis: 13 September 2026. Further candidate experiments stopped at the user's request.**

Nine accepted statuses were observed in the live panel, including rust-analyzer and Scylla. The archived revisions are not yet bound to historical accepted artifact bytes. Historical acceptance, archive evaluation and fresh local readiness are distinct evidence.

## Findings that change the workflow

| Case | Preserved result or limitation | Preventive rule |
|---|---|---|
| Lisette | First archive evaluation 25/25. Later runner and partition repairs are source-prepared; revised runtime/image validation remains pending. | Reconcile actual events and setup failures; separate fresh feature coverage from existing coverage. |
| Scylla | First archive evaluation 19/19 new and 18/18 base. Earlier tests-only baseline compilation executed zero tests. Later latency witness and runner revision unexecuted. | Prove sequential winner propagation; isolate the latency predicate; compile failure is not behavioral discrimination. |
| Dora | First archive evaluation 24/26; R2 26/26 plus 45 base. R3 preparation exists but its worker never ran. | Test match × tuple-rest and adjacent unit forms; assert actual diagnostics and preserve backend compatibility. |
| rust-analyzer | First archive evaluation 22/26; repaired R3 25/26 plus 747 base. The remaining gen-keyword case is preserved as a failing evaluation with a contract-grounding dispute. | Inspect traversal ordering, non-identifier predecessors, fallback branches and edition-sensitive compatibility. Never relabel the remaining failure as a pass. |
| KiteSQL | First archive evaluation 5/5. Later assertion/partition and Docker revisions remain runtime-unvalidated. | Assert exact error categories; generic error acceptance can let wrong baseline behavior pass. |
| Calyx | First archive evaluation could not compile Cider, so zero feature cases executed. R5 is an unvalidated draft and its solution patch accidentally includes historical profraw outputs. | Compile every affected consumer early; construct release patches from explicit allowed paths. High compiler-library coverage does not prove Cider readiness. |
| DataFusion Parquet | Own clean matrix: 243 existing and 26 fresh tests; seven planned mutations killed. Changed-line coverage has a profiler-warning qualification. No clean image completion or archive replay. | Preserve exact types/precision and nested metadata; test Boolean pruning semantics. OCI import heat is an environment failure, not candidate behavior. |
| Ladybug | Implementation and 20 API cases prepared; compilation, matrix and coverage pending. Historical payload remains withheld. | Include every storage writer/reader, version boundary, reopen path and consecutive operation. Draft test count proves no execution. |
| DataFusion Aggregate | Implementation and 42 consumer tests prepared; none compiled. Native downcasts, live mutable state and exact error transport have unresolved contract gaps. Historical payload remains withheld. | Prove native representation and public producer/consumer feasibility before implementing a broad FFI promise. |

Six first archive evaluations were attempted. Three had all selected archive checks pass at first evaluation: Lisette, Scylla and KiteSQL. That is a narrow descriptive result, not a nine-case pass rate, one-shot readiness rate or accepted-byte replay. Earlier own validations and later integrity findings qualify those results. Thermal holds, caches and changed quotas prevent a defensible overall speedup claim.

## Coverage explains why LOC alone fails

These observations concern added changed executable-line mappings, not branch coverage. The detailed scorecard retains source/tool/selection identities.

| Case | Added lines | Mapped executable lines | Existing selection | Fresh selection | Combined |
|---|---:|---:|---:|---:|---:|
| Lisette | 485 | 391 | 50.13% | 84.14% | 97.44% |
| Scylla | 306 | 248 | 7.26% | 90.32% | 90.32% |
| Dora | 388 | 312 | 16.35% | Unmeasured separately | 92.31% |
| rust-analyzer | 393 | 304 | 90.79% | 93.75% | 97.04% |
| KiteSQL | 362 | 285 | 50.18% | 83.16% | 96.49% |
| Calyx | 376 | 278 | 6.47% | Unmeasured separately | 87.41% |
| Parquet | 463 | 312 | 18.27% | 91.99% | 92.31% |

Fresh selection means the measured fresh-suite selection in that case; it is not uniformly a feature-only partition. Later partition repairs do not retroactively change these measurements. Dora's figure is R2 AOT; Parquet's export carries a warning qualification. Ladybug and Aggregate remain unmeasured. Unmapped and non-counter lines require separate inspection; the subtraction from added LOC is not itself an uncovered executable count.

The useful target is complete grounded behavior with discriminating witnesses, supported by fresh-suite coverage and valid mutations. It is not maximum LOC or an arbitrary combined-coverage threshold.

## Historical inspection boundary

The inventory covered 11,706 files across 42 case records and 195 lesson records. It cataloged 455 proof records, 119 artifact directories, 89 complete sets, 86 unique sets, 2,346 patches (1,974 unique), 161 ZIP files and 2,126 ZIP member names.

Fourteen transferred distinct solution revisions from the first five evaluated cases were inspected through changed hunks and canonical deltas. That does not mean all unchanged context was read. The persisted selected narrative ledger reports 88/94 fully read; the final agent reported three additional reads (91/94), but their addendum was not persisted before the stop. Treat 88 as the persisted count and preserve the distinction.

ZIP payload semantic inspection is zero. Calyx historical solution reading had been authorized after evaluation but had not started. Parquet, Ladybug and Aggregate payloads remain withheld. Generic reference gaps and canonical-path mapping gaps remain. The final workflow is a synthesis of inspected evidence and recorded observations, not a claim that every stored byte was understood.

Relevant plugin evidence: `evidence/corpus-traceability-audit/`, its `post-evaluation-learning/` subdirectory, and the provenance/completeness references. The canonical task report and per-case evidence remain under `/home/admin/olympus-work/fastlane-dogfood-20260912`; Mac report mirror: `/Users/rizwanahamed/Documents/Shipd/output/shipd-fastlane-dogfood-20260912`.

## Runtime and release limits

The source-preparation supervisor passed 11 harmless real-scope fixtures after a detached-descendant false-success was repaired. Its SHA-256 is `5f0d8190dbc94f6ea575a2d9f93ceeb284a8141c4e6bf07e5609da85fb4f6304`. The fixture receipt SHA-256 is `6a4eb263d6ff319c0a59928391d58ad3bbbebfc3779c11ad3c2b9bda3f33e693`. Abrupt supervisor death still lacks an independent watcher.

The final plugin fixture/manifest/skill results are recorded in `evidence/workflow-release/validation.json` after execution. Plugin fixtures validate those tools on synthetic inputs; they do not validate repaired candidate images or private graders.

Dora and Parquet candidate containers remain paused, competing work remains preserved, and unrestricted Docker/containerd daemon operations remain held. No paid Shipd check, rollout or reset credit was used for this synthesis.
