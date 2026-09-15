# Review dispositions — label detail and first-seen order

Source artifact set: `9467359ac793daccfe29fcd55b97d2622564063a5ef2165efc07f311a5b7d0b7`.

| Finding | Classification | Disposition |
|---|---|---|
| One-marker speculative-mapping wording is implementation-shaped | STALE / ALREADY FIXED | The current `problem.md` says to analyze viable identifier occurrences and treat them independently; it no longer mentions a one-marker mechanism. |
| Trigger-filtered contexts must consume a first-64-examined bound | STALE / CONTRADICTORY | The quoted interaction was removed after Description Quality rejected it as untested over-specification. Current wording independently preserves trigger continuation and the ordinary-request 64-site traversal budget. No trigger-boundary test or solution change was added. |
| Relevance-only items must remain distinct | STALE / CONTRADICTORY | The quoted relevance sentence was removed after Description Quality rejected it as untested over-specification. No relevance test or solution change was added. |
| Equivalent duplicates do not prove retention of the first stream position | PROMPT-STATED / REPRODUCED | Strengthened the existing solution-dependent dedup helper to emit `A, B, A` and require `A, B`. Reference and Nova 7 pass; a reverse-scan retain-last mutant fails exactly this assertion. |
| Full label-left disambiguation is missing from identity coverage | PROMPT-STATED / REPRODUCED | Added a helper for inherent and `(as Extra)` trait-method variants with the same primary label and public kind. It is called from the existing solution-dependent dedup test. Reference and Nova 7 pass; a primary-label-only identity mutant collapses two items to one. |
| Verifier Completeness proposed a standalone method-label test | ACCEPTED WITH EDITS | Exact Cloud replay showed that standalone test also passes on the clean base because one legacy site already exposes both method variants. Registering it as a separate new test would violate base/new sanity. Folding the assertions into the already fail-to-pass multi-site dedup test preserves the discriminator and keeps 24 named new tests. |

The attached Test Fairness PASS reviewed the older prompt and pre-edit test bytes. Its findings informed this repair, but it is not a current-byte hosted approval.

## Exact execution

- Clean base: 10/10 base pass; all 24 named new tests fail.
- Reference: 10/10 base and 24/24 new pass; full `ide-completion` library suite 771/771 passes.
- Preserved genuine solve Nova 7: 10/10 base and 24/24 new pass.
- Label-primary-only mutant: exact combined dedup test fails, returning one method variant instead of two.
- Reverse-scan retain-last mutant: exact combined dedup test fails with `record_field, local_value` instead of `local_value, record_field`.

Raw logs and JUnit are under `cloud/`.
