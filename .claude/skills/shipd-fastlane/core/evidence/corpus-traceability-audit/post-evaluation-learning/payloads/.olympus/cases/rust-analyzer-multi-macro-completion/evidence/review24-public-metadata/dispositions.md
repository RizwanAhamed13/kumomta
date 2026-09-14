# Review dispositions — 2026-08-24

Artifact set reviewed before repair: `2ef5979036b02e39e6ac01c051191996d7991ae2f1c8de97a166b0a8696812fc`.

| Finding | Classification | Disposition |
|---|---|---|
| Direct attribute macro fanout is untested | STALE / ALREADY COVERED | Current `test.patch` contains the `duplicate_attribute_sites` expander and `unions_sites_produced_directly_by_an_attribute_expansion`, which exercises fanout produced by the attribute branch itself. |
| `_`-suppressed sites must not consume the 64-site budget | STALE / CONTRADICTORY | The current prompt guarantees trigger continuation only within the first 64 mapped identifier sites and explicitly permits trigger-filtered contexts to consume that traversal bound. The retired cross-product is outside the current contract. |
| `(` non-visibility sites must not consume the 64-site budget | STALE / CONTRADICTORY | Same current trigger-boundary carve as the underscore finding. Standalone non-contributing-context continuation remains tested. |
| Same-label/same-kind items differing by documentation or deprecation collapse | PROMPT-STATED / REPRODUCED | Exact current reference failed the focused three-field probe with one item; Nova 7 passed with three; the reference fix preserves detail, documentation, deprecation, and trigger-call metadata in `CompletionIdentity`. Incorporated as A36/M27. |
| Attribute expansion plus >64 nested sites and ignored paths | ADVISORY COMBINATORIAL VARIANT | Direct attribute fanout, nested shared budgeting, and nested ignored-path accounting are independently covered. No demonstrated current mutant was supplied, and adding the cross-product would undo the deliberate bounded de-variation without new behavioral scope. Not added. |
| Additional punctuation/dot non-identifier regression | ADVISORY / NO DEMONSTRATED GAP | The current string-literal repeated-mapping test pins the stated legacy non-identifier boundary, and the ten-test base set covers neighboring macro completion. No exact candidate/reference discriminator was supplied. Not added. |

The older Test Fairness PASS and Verifier Completeness reports refer to 22/27/28-test artifact sets,
not the current bytes. They remain historical evidence and are not treated as current approvals.
