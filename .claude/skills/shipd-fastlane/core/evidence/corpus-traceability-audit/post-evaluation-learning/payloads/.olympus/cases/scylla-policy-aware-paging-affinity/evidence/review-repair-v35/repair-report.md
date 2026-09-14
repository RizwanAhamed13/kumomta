# v35 Test Quality fairness repair

- Repository: `scylladb/scylla-rust-driver`
- Commit: `611d43b595fb0ad7010f2bdbd887acae3d962d65`
- Execution host: `codespaces-14482c`
- Artifact set: `306609ec869c9c97da6d5ce34f2e416cd07567116d4abc824d1f09f90302d9cd`

Only the opacity oracle inside `test.patch` changed. The problem, solution, Dockerfile, behavioral suite, 16 testcase identities, and solver-facing scope are unchanged.

## Blocking finding repaired

The checker no longer requires `PagingContinuation` to be a rustdoc-local plain or tuple struct. It still rejects locally inspectable structs with public fields or no private state, transparent primitive aliases, alias cycles, and missing/ambiguous public paths. It accepts external opaque carriers and non-struct local representations because ownership and concrete item kind are not part of the prompt contract.

A ten-case representation battery passed: private named struct, private tuple struct, local enum, local union, direct external carrier, and external alias were accepted; public-field struct, unit struct, primitive alias, and cyclic alias were rejected.

## Advisory dispositions

- Removed-target scenario: prompt-grounded coverage suggestion, but not a proven current-suite survivor. Existing stale/replaced identity coverage remains; deferred rather than adding speculative hardening.
- RetrySameTarget parity: prompt-grounded advisory, but no exact surviving implementation was supplied or reproduced. Deferred.
- Prepared/caching error parity: prompt-grounded advisory; existing unprepared error equivalence plus prepared/cached execution-path coverage remains. Deferred pending a concrete discriminator.
- Automatic prepared observability: prompt-grounded advisory; existing automatic prepared affinity and automatic unprepared observability tests remain. Deferred pending a concrete discriminator.

These advisories do not justify scope expansion under the bounded false-positive rule.

## Validation

- Four-state matrix: base 1/1 before and after; new 0/16 before and 16/16 after.
- Stability: 12/12 full solved wrappers, 16/16 each.
- Saved-agent replay: Nova 1 and 7 pass; the other eight fail on the same prior architectural gaps. Rate remains 2/10 (20%).
- Evidence archive SHA-256: `8fb7c0b87cf4128a55ac2dd87f7f53855d4c81122df6d3257401a43980ae6517`.

## Artifact hashes

- `problem.md`: `7cd6d8f7f070c6c98a5c1d5df2b41ddaff8c6b8cf654f20a6cbdd1f6d38d4d8b`
- `test.patch`: `2e97393aa04da418d1a8213a1712a1c8d743080a3dfb60d71c02af46def6f16a`
- `solution.patch`: `b3624a960d4d76fe4475d6e319f6987690c3c39c07f36cc3f65874e54d214b44`
- `Dockerfile`: `d935b06286b10be4b1f847993baeed8723c01da1a5654ae91adcddb759398d71`

Hosted test-dependent checks remain stale and must be rerun on v35.
