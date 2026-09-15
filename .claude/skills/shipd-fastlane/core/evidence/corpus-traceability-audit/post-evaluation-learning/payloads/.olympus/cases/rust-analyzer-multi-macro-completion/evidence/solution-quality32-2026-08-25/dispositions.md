# Solution Quality 32 dispositions

| Finding | Classification | Resolution |
| --- | --- | --- |
| Sole bare-underscore suppression returns `Some([])` instead of `None` | Accepted: pinned single-site regression | Completion dispatch now records whether any context contributed. A request whose only context is suppressed returns `None`; multi-site `_` requests still continue to later contributing contexts. |
| Relevance differences prevent repeated public items from collapsing | Accepted: prompt-stated dedup defect | Cross-context identity now uses the stated public fields and excludes internal relevance. First-seen payload/order is retained. |
| Lifetime macro completion is fanned out | Accepted: identifier-only contract defect | Multi-site expansion is limited to identifier tokens plus the explicitly supported `_` and `(` trigger paths. `LIFETIME_IDENT` uses the pinned single-site traversal. |
| Global linear dedup makes ordinary accumulation quadratic | Accepted: code-quality defect | Ordinary `Completions::add`, `add_many`, and `add_opt` are restored to direct vector accumulation. A separate `CompletionMerger` deduplicates only between analysis contexts and uses a `BTreeMap` keyed by full displayed label and public kind to avoid scanning the complete output. No timing assertion was added. |

Three preservation assertions were added as helpers inside existing fail-to-pass tests because the clean pinned implementation already satisfies them. They cover raw `Option` suppression, relevance-only duplicate collapse, and lifetime single-site routing without changing the 24 named-test runner contract.

Exact Google Cloud discrimination:

- Pre-fix reference fails all three behavioral probes.
- Fixed reference passes all 24 named tests and the complete warnings-denied library suite, 782/782.
- Saved Nova 2 passes the suppression and relevance probes but fails the lifetime single-site probe; its prior passing classification is therefore stale on these bytes.
- Final isolated matrix: unsolved base 10/10, unsolved new 0/24, solved base 10/10, solved new 24/24.
- Test and solution patches apply cleanly alone and together; `git diff --check`, `cargo fmt --all -- --check`, and `bash -n test.sh` pass.

The package remains locally solvable by the reference, but there is currently no preserved independent candidate that passes the exact corrected suite. A fresh rollout and false-positive review are required before any difficulty or durable-pass claim.
