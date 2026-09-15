# FP master-prompt rerun

## Status

- Reported public-constant false-positive family: **PASS / closed**.
- Overall package acceptance: **not claimed**; fresh rollouts and hosted FP review remain required.

## Contract atom and fairness

Problem line 9 explicitly states that foreign autofill preserves declaration ownership for public bare constants, payload-less enum values, and enum constructor function values. This is observable behavior and does not prescribe inlining, qualification, AST representation, cache encoding, or emitter architecture.

## Coverage map

The existing `mica_q7m_preserves_values_across_owners_and_cache` scenario covers:

- same-file public bare constant `SAME_FILE_PUBLIC`;
- sibling public bare constant `SIBLING_PUBLIC`;
- sibling public alias of an imported nonliteral constant `IMPORTED_PUBLIC_ALIAS`;
- foreign direct struct construction;
- foreign nested generic construction;
- foreign enum-record construction;
- declaration-owned payload-less enum values and function-valued enum constructors;
- cold and warm generated-Go compilation and exact runtime parity.

## Executable discriminator

- Broken mutation: return a public declaration constant identifier unchanged during field-default materialization while retaining private-constant materialization.
- Mutant result: focused `mica` exits `101`; generated `main.go` reports undefined `SIBLING_PUBLIC`, `IMPORTED_PUBLIC_ALIAS`, and `SAME_FILE_PUBLIC` across direct, nested, and enum-record uses.
- Reference result: the identical focused test exits `0`, including cold/warm generated-Go execution.

The suite therefore rejects the exact panel candidate and broader equivalent variants, rather than only the literal `VALUE = 23` example.

## Historical passing-agent replay

There are two unique historical passing architectures repeated across batches:

1. The `default_references` architecture was already rejected by the repaired imported-enum/constructor domain.
2. The `construction_default` architecture was replayed against the current suite and exits `101`; foreign generated Go contains undefined `MakeChoiceFull`, `MakePhaseHot`, and `MakeChoiceEmpty`.

All historical patches that already failed remain failures because `test.patch` was strengthened and never relaxed. Thus the current-suite replay prediction for historical code is **0 durable passes**.

## Fresh-agent pass-rate prediction

Historical code replay is not the expected rate for fresh agents because those agents did not see the clarified prompt. From the batch-79 blind clusters, four implementations were near-complete and failed mainly at interactions now stated explicitly, while broad/regression implementations remain unlikely to recover. The defensible forecast for a fresh ten-run cohort is **2–4 genuine passes, centered at 3/10**. This is a prediction, not a measured platform rate.

## Remaining risk

No behavior, assertion, or test was relaxed by the description edit, so it cannot newly admit a broken solution. It improves solver discoverability only. No finite audit proves that an unrelated future implementation defect is impossible; every fresh passing agent still requires panel FP review.
