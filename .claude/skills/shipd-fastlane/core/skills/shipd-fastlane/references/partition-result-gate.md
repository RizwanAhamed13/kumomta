# Reconcile a complete suite across partitions

Use this check whenever multiple runs collectively claim one required suite. First discover the complete inventory independently of JUnit and of the chosen partition filters. Keep canonical classname::name IDs in a JSON tests list; the complete inventory has no exclusions.

Each partition must already have an EXECUTION_RECONCILED receipt from test_result_gate.py, with raw libtest events, independent selected discovery, the actual process exit code and JUnit. Preserve the actual relevant source snapshot and test executable. Build a source manifest from that snapshot independently: a JSON files mapping from relative source filenames to SHA-256 values. List all relevant source inputs, not only conveniently unchanged files. Hash the manifest bytes and binary. This gate rehashes every declared source file and executable; missing or changed files fail, and a receipt cannot substitute for retained identities.

Create a manifest with a partitions array. Each object has these fields:

| Field | Value |
|---|---|
| id | Unique partition name |
| expected | pass or fail, matching its receipt |
| receipt / receipt_sha256 | Individual reconciliation path and hash |
| junit / inventory / events | Current JUnit, selected discovery and raw JSONL paths |
| identity.source_manifest / identity.source_sha256 | Source manifest path and exact-byte hash |
| identity.source_root | Retained source root used to rehash declared files |
| identity.binary / identity.binary_sha256 | Retained test executable path and hash |

Paths resolve relative to this manifest. Run on the authorized builder:

    python3 scripts/partition_result_gate.py --inventory complete.json --partitions partitions.json --output complete-reconciliation.json

Require PARTITIONS_RECONCILED, exit zero, and retain the receipt. The gate reruns individual reconciliation on current input bytes, checks saved receipt hashes and fields, and rejects duplicate IDs, overlap, missing or excess executed IDs, stale evidence and XML-only receipts. A passing subset remains incomplete even if it declares no exclusions.

All partitions must name the same exact source-manifest hash. Disjoint passing subsets from different source revisions cannot establish one complete result.

Each excluded ID must execute in another reconciled partition with the exact same source-manifest and executable hashes. Disjoint test binaries may form a complete suite, but an exclusion from one binary cannot be justified by a different binary. Preserve per-binary full discovery when constructing the combined inventory; class names must identify their true suites consistently.

An expected-fail baseline feature partition can contribute when its actual nonzero exit and assertion outcomes reconcile, with no harness errors or skipped selected tests. Add triage and triage_sha256 to that partition. The hashed triage JSON must contain raw_events_sha256 and a failures array covering every actual failed test exactly once. Each entry requires its canonical id, classification set to behavioral, nonempty prompt/repository grounding, and a diagnosis of the actual assertion mismatch.

Review that diagnosis against the raw output. Compilation failure, missing events, wrong fixture expectations and unrelated crashes cannot establish behavioral discrimination. The script's module documentation contains complete JSON examples for both manifests and triage.

This tool establishes consistency of supplied evidence. It cannot authenticate the discovery process, completeness of a declared source manifest, claimed process exit, truth of triage, or actual production execution; its receipt explicitly reports production provenance as unverified. Coverage, requirement completeness, native-adapter trust and private Shipd checks remain separate. Do not relabel an old partial receipt as complete when retained source/binary identity is unavailable.
