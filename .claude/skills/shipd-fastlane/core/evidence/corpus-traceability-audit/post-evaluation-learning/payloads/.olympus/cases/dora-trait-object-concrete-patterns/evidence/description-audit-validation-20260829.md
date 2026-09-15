# Description alignment validation — 2026-08-29

Current artifact hashes:

- `problem.md`: `28b7f49b0d5bd0035c4c7b2689756c783df155ab5208d54a158bb4d4ea64d940`
- `test.patch`: `0dc56061792b916b326944519c247aafbf2bc86710e70070935da2750717172a`
- `solution.patch`: `760f7aed22213a3c9dc6cbc0388a1a774cddf9b3f1d77b3512e4a5fe5fe8a4d4`
- `Dockerfile`: `d12f2fcad89966994e61fe2ef00b68dcc80d0f36c3756e50930312d7acfe2801`

The clause-by-clause map is in `description-test-map-20260829.md`. The audit
expanded `test.patch` to 586 inserted lines across 15 randomized files.

Strengthening added independent literal trait-argument and associated-binding
rejections, partially constrained generic ambiguity, generic patterns in `is`,
all primitive literal representations in `match` and `is`, a zero-field
wrong-shape object, both guard outcomes plus guard non-evaluation, a managed
reference inside an inline implementation across mutation and collection, and
direct class/struct/enum/literal regressions under both backends.

Aswin source matrix in LXC `podspub27`:

- untouched production: base `14/14`; new `8/20` (`12` failures)
- reference production: base `14/14`; new `20/20`
- exact current applied patch tree and passing remote tree:
  `40bc56f549b67628f1c6c8b8ff298b68f046143a`

The non-root evaluator image ran with UID/GID 1000 and no Docker network. Six
consecutive repetitions each returned `BASE=0 NEW=0`, with 14 base and 20 new
groups discovered every time.

Mutation `M11_LITERAL_COMPATIBILITY_BYPASS` accepted every literal without
checking trait arguments or associated bindings. The prior 15-group suite
passed it; the current suite failed exactly the two new literal rejection
groups. The reference passes both.

Local structural validation passed diff syntax, shell syntax, clean application,
repository identity, LF rules, randomized paths, production-size thresholds,
and Docker static checks. No paid or live check was run. The earlier Scope Gate
and every older test-dependent proof are stale for the new test-patch hash.
