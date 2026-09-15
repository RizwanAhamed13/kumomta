# Accepted Olympus candidate calibrators

This bundled snapshot contains all seven candidates confirmed accepted for the workspace as of 2026-08-31. Use these as structural hardness calibrators, not as pass-rate targets. Recheck the live Submissions page before making a current platform claim.

| # | Accepted task | Repository | Displayed rate | Semantic core and forced chain |
|---:|---|---|---:|---|
| 1 | Preserve invoke combinational scopes during component inlining | `calyxir/calyx` | 10% | Dynamic control scope round-trips through parsing/printing, cloned-control inlining, analysis and cleanup liveness, and lowering through sequential, branch, loop, parallel, and separately compiled control without lifetime leakage. |
| 2 | Support Composite Primary Keys for Native Node Tables | `LadybugDB/ladybug` | 15% | Ordered tuple identity stays collision-free across DDL/catalog, storage and index encoding, CREATE/MERGE/MATCH, transactions and delete/reinsert, relationship COPY endpoint binding, schema export/import, reopen, and scalar-key compatibility. |
| 3 | Add ownership-safe defaults to record fields | `ivov/lisette` | 30% | Declaration-owned defaults cross parsing/formatting, type and zero-value analysis, enum recursion, privacy/name resolution, construction and spread precedence, lint/usage behavior, incremental cache, and cold/warm builds. |
| 4 | Support expressions in CREATE INDEX | `KipData/KiteSQL` | 30% | Structural expression identity constrains validation, catalog persistence, key construction, DML/NULL maintenance, optimizer matching, range/equality scans, covering-index behavior, explain output, and reopen. |
| 5 | Use Parquet Map Leaf Metadata for Row-Group Pruning | `apache/datafusion` | 40% | Map key/value leaf selection, flattened statistics, null counts, Bloom filters, candidate quantification, AND/OR three-valued conservatism, SQL planning, and Parquet pruning agree without false-positive pruning. |
| 6 | Preserve Aggregate UDF Overrides Across FFI Boundaries | `apache/datafusion` | 20% | Producer-defined callbacks and metadata cross ABI representation, ownership/lifecycle, concrete-expression downcasting, error and absence handling, aggregate-returning hooks, ordering/reversal reconfiguration, codecs, loading, and execution without consumer access to private implementation. |
| 7 | Support Concrete Patterns Over Trait Objects | `dinfuehr/dora` | Not captured | Static compatibility and unique implementation selection cross trait arguments, associated bindings, generic specialization and ambiguity; lowering adds type-test-before-extraction; bytecode writer/reader/verifier/dumper, Cannon JIT/AOT, self-hosted Boots on x64/arm64, open-world exhaustiveness, identity, mutation visibility, and GC safety remain aligned. |

## Preserved evidence

- Calyx: `kh763xwhkq11gc38ata5g1rn358cgw9m`
- Ladybug: `kh7037hnydbvan6167ssq2cwrx8c7425`
- Lisette: `kh7ctmnq19q2qn7sn2sf5nektx8c63ks`
- KiteSQL: `kh76cw7dz3e4cm5wg4nwzdfjyh8bkwj7`
- DataFusion Map pruning: `kh7b3bb3afj470xz4vyyt1q2kn8b3zeq`
- DataFusion aggregate-UDF FFI: `kh7dzpzqdxx7wyg8zz12e9673s8atwq5`
- Dora: user-confirmed accepted on 2026-08-31 with preserved final approved artifact evidence; live challenge ID and displayed rate still require capture.

The full comparison rules, accepted floor, every-calibrator matrix, anti-mechanical rejection, and hardness kill sheet remain in `hardness-calibrators.md`.
