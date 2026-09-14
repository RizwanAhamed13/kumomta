# Post-evaluation historical learning audit

Recorded after the five cases' first archived test evaluations. This is later learning exposure, with no changes to fresh artifact bytes, first outcomes, elapsed measurements or chronology receipts. It is not a claim that any selected saved solution is the accepted upload.

## Inspection coverage

The checksummed bounded transfer contains 118 files (1,597,355 bytes), including 14 distinct solution patches. The semantic-inspection ledger records exact paths, measured hashes and read extents: one complete solution patch (Scylla), four partially inspected patches (Lisette, Dora, Rust Analyzer, KiteSQL v5), and nine patches inspected only for structure. Of 96 selected Markdown narratives, 51 were fully inspected, one partially inspected and 44 remain without established semantic inspection. Eight other transferred records were not fully inspected. Truncated tool output is explicitly qualified, including earlier emission logs; it does not count as a full read.

The original 42-case / 195-lesson synthesis is a historical reported read claim. This pass independently inspected its metadata links and selected payloads; it did not reread every lesson or understand every one of the inventory's 1,974 distinct patch hashes. The full searchable corpus metadata and ZIP member inventory remain attached by provenance, not replaced by this sample.

No ZIP payload was opened. Calyx, Parquet, Ladybug and Aggregate historical payloads remain withheld. Remote-only material and unexported conversations remain outside the local corpus. Exact per-read timestamps are retained where receipts exist; the consolidation time is not a substitute for unknown read times.

## Per-case read coverage and remaining work

Counts below cover the 118 selected files only. Every selected source path, measured hash, read extent and report title is retained in per-case-inspection-coverage.json and semantic-inspection-ledger.json. Corpus-wide paths and ZIP members remain searchable through the completeness ledger.

| Case | Full solution / partial / structure only | Narratives full / partial / unread | Other records not fully inspected |
|---|---:|---:|---:|
| Lisette | 0 / 1 / 2 | 9 / 0 / 0 | 2 |
| Scylla | 1 / 0 / 2 | 14 / 0 / 27 | 2 |
| Dora | 0 / 1 / 0 | 13 / 0 / 3 | 2 |
| Rust Analyzer | 0 / 1 / 3 | 12 / 1 / 12 | 2 |
| KiteSQL | 0 / 1 / 2 | 3 / 0 / 0 | 0 |

KiteSQL's three narratives are descriptions, not reviewer/FP/rollout reports. Two additional shared reference narratives are unread. No ZIP payloads were inspected for any case: the current pass prioritized the selected revision and review records after evaluation, without executing historical code. Reported historical test/rollout outcomes remain attributed claims until their raw receipts and artifact identities are independently checked.

The remaining plan follows deduplicated revision deltas and actual reviewer outcomes, not one read per duplicate path. Complete the four partial canonical patches, inspect the nine distinct saved revisions against their own contract, then finish the selected raw reviews and trace relevant solver/ZIP members. Keep every duplicate's provenance even when semantic reading is shared. Broader selected-file coverage does not establish that the inventory contains every remote or unexported iteration.

## Findings by completed case

| Case | Historical behavior and iterations inspected | Comparison with fresh evidence / remaining gap |
|---|---|---|
| Lisette | Typed defaults propagate across registration, inference, cache representation, owner-qualified constant/enum emission, formatting and autofill linting. Review narratives identify zero-executed skips, owner namespace cases, collision fairness, nonroot cache paths and baseline-valid new checks. | Fresh own suite grew from 14 to 15 feature tests after a surviving collision mutant, with two adjacent checks. First archived 25/25 is preserved. Current mapped-line union coverage does not prove cache/path portability or all compatibility: 286 excluded existing tests remain explicit. Complete historical patch and two saved variants were not fully reviewed. |
| Scylla | Full canonical patch covers current Arc identity, opt-in policy, lazy preferred-plan suppression, current ArcSwap reads and successful coordinator propagation. Reviews v19–v38 selected here document retry→fallback→next page, wrong-shard suppression, latency-only rejection, current-node replacement, virtual-clock flakiness and representation-neutral opacity. | Fresh eight tests cover the shared predicate pipeline and many three-page/API transitions. The fresh requirement map explicitly does not exercise a time-dependent latency estimator; historical v33 shows why a generic filter witness cannot close that gap. Tests-only cannot build the Rust harness due to absent APIs: zero executed tests, not behavioral F2P. Sixteen external-database tests are excluded. |
| Dora | Selected full sections span trait/associated-binding inference, constructor identity, open-ended usefulness, tuple arity, shape check before extraction and both backend lowerings. Fully read repairs expose missing tuple/unit forms, guard×catchall interactions, nested heterogeneous forms, baseline-valid rejection partitions and stale Boots binaries after rebuilding only Rust. | Fresh R2 fixed unit rest-only destructuring and reports 42/42 new command cases, 31/31 base and archived 26/26 new plus 45/45 base. Tests-only reports ten passes and sixteen candidate-language compile rejections. Those rejections can be behavioral, unlike a harness compiler failure; exact diagnostic and inventory triage is still needed. Ten baseline-valid checks need explicit compatibility partitioning. JIT remains unverified. |
| Rust Analyzer | Selected canonical code handles multiple contexts, terminal budget, direct-attribute provenance and completion identity. Reviews cover markerless budget consumption, first viable nonidentifier, empty sibling behavior, public-label dedup and stale replay cohorts. Later narratives describe merger/fallback changes absent from the selected canonical patch. | Fresh R3 has 23/23 feature tests, 772 combined and 25/26 archived; the retained failure is the independently diagnosed out-of-scope keyword fixture. Earlier 22/26, legacy regression and empty-shorthand repairs stay distinct. Canonical path naming does not establish latest or accepted bytes; three variants remain structure-only. |
| KiteSQL | v5 selected code stores/rebinds expressions across arenas, preserves structural cast identity, matches predicates, persists versioned metadata and falls back to legacy decoding. Three descriptions distinguish core composite/nonunique scope, wider scoped literal behavior and narrower v5 single-key bounds. | Fresh 422 combined and archived 5/5 are unchanged. Four of 23 fresh selections pass the baseline (two explicitly adjacent); compatibility classification is required before Verify Tests readiness. Historical persistence/matching paths are source observations, not extra measured fresh coverage. Core/scoped solution payloads and remaining v5 sections are unaudited. |

Fresh comparison inputs include scylla/frozen-first-complete/requirement-matrix.md, scylla/evidence/final-matrix-results.json, dora/frozen/first/requirement-map.json and dora/evidence/results-revision-2.json under the dogfood root. Lisette/Kite delivered reports and root-supplied RA R3 receipts remain the measurement authorities. This review adds no test execution.

## Generic lessons and current gate mapping

1. Build the input/role inventory from the prompt and pinned repository before coding. Tuple/unit, guarded catchalls, zero-element rest and mixed sibling roles were omitted even when a declared alignment graph was complete. Map to test-coverage.md / contract_check.py; metadata consistency alone cannot discover missing forms.
2. Test whole state transitions and isolate each predicate. A rejected preferred target followed by a fallback winner must continue to another page in the same scenario. A latency test must keep connectivity, locality, replica membership and identity valid. Map to whole-scenario and interaction requirements; do not add unrelated product scope.
3. Keep oracles neutral to legal representation. Private tuple carriers or aliases can be opaque; public enum construction can violate opacity. Test observable constraints and explicit privacy laws, not a preferred source shape. Map to fairness and mutation review.
4. Partition tests using actual baseline outcomes. Preserve baseline-valid negative/compatibility assertions in base; do not weaken or delete them. Candidate-language diagnostics may be the public behavior under test. Rust/C++ harness compilation, setup failure, missing tests and synthetic XML failure rows are separate. Map to execution-integrity.md, partition-result-gate.md and local-quality-gate.md.
5. Rebuild every affected compiler/code-generation layer after runtime patching. Bind source, binary and selection identity; a hash of restored source is insufficient. Exercise actual offline/nonroot runner argument order and preinstalled dependencies. Map to runtime, execution-integrity and thermal-safety references.
6. Preserve contract revision identity and first results. Kite revisions have different literal/key scope; RA canonical paths lag selected review narratives. Hosted status cannot bind saved bytes. Map to corpus-completeness/provenance and freeze chronology fields.
7. Preserve historical report limitations. Old Scylla reports synthesized failing XML for missing execution; the current event gate rejects that practice. Old Dora Stage5b explicitly used an incomplete reference; it is not a precedent for the current full-reference Scope requirement. Old Aswin/Codespaces paths are historical provenance, never current execution authorization.

## Completion and readiness

This bounded learning pass is complete as a documented sample, not as a complete payload audit. Fresh local workflow completion, full compatibility evidence and platform upload readiness are different outcomes. Coverage and a passing selected matrix do not establish all 20 local quality families, current Forge Verify Tests partitioning, private graders or hosted approval. No live check was launched.

Remaining review can proceed in bounded post-evaluation batches: first complete the four partial canonical patches and inspect the nine saved variants with their exact contract revision; then read the 44 uninspected selected narratives and raw receipts referenced by claims; then select relevant solver/ZIP members using the existing searchable inventory. Record each exposure and hash without changing first-freeze measurements. Pending cases require their own first-evaluation release before historical payload review. Remote-only and malformed/unhashed archives remain explicit gaps.

The current Buildx readiness lesson remains provisional in buildx-harness-pending.json: three reported pre-build harness iterations, no proven repair receipt yet. The running thermal helper was not changed.
