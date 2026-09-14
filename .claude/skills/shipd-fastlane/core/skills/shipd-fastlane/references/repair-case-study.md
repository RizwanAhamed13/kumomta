# A storage repair that created another review cycle

The Ladybug relationship ART index case illustrates three distinct causes that should be considered together before a repair. Sources are local September 3 feedback files under `.olympus/cases/ladybug-rel-art-index-feature-pioneer/`.

1. `solution-quality-feedback-2026-09-03.txt` reported persistence rows for unpopulated index shards and appended metadata without a compatible storage format upgrade.
2. `solution-quality-feedback-round2-2026-09-03.txt` reported a repair that changed the header to version 47 only when an index existed, while serialization appended the new fields unconditionally. An ordinary unindexed table could then checkpoint with header 46 and reopen incorrectly. It also reported that early lookup failure bypassed the existing `DROP INDEX IF EXISTS` behavior.
3. `test-quality-feedback-2026-09-03.txt` reported an unfair assertion requiring exactly version 47. The grounded behavior was compatible persisted layout, not a particular implementation's new version integer.

The preventive contract is public: populated and empty shards; indexed and unindexed tables; supported preexisting and new data; checkpoint and reopen; missing index with and without the existing conflict option. Derive expected outcomes from the pinned repository and stated requirements. Test observable persistence compatibility and retained error-handling behavior. Do not prescribe a private version choice where another conforming implementation is possible.

Before repairing one version predicate, inspect every writer, header decision, reader and record boundary affected by it. Reproduce the original failure and adjacent feature-absent path, then validate the batch. A patch that addresses only the first failing review sentence can introduce the next defect; a test that pins the reference's internal fix can unfairly reject a correct alternative.

These are attributed historical feedback findings, not new reproductions or current acceptance claims. Read the original receipts before using them to change that case.
