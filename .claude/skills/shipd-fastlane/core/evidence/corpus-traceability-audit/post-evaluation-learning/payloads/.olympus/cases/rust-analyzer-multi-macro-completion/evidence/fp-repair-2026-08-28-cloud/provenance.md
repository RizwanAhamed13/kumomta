# False-positive repair replay

- Repository commit: `d2e55da49132fa70a13dfbdc99122432b02cf464`
- Artifact set: `ac6fb68411938c8a8c50c905b40ba95ea1e39b65aac480930ae97a99133cb6f1`
- Execution: Google Cloud Shell CLI, Rust `1.97.0-x86_64-unknown-linux-gnu`
- Isolation: each state used a distinct `CARGO_TARGET_DIR`; the earlier shared-target run was discarded as contaminated.
- Reference new: 29 passed, 0 failed.
- Exact known-genuine Nova 2 new: 29 passed, 0 failed.
- Exact qualified-path FP Nova 4 new: 28 passed, 1 failed (`unions_different_syntactic_contexts`).
- Exact field-access FP Nova 5 new: 28 passed, 1 failed (`unions_different_syntactic_contexts`).
- Untouched plus test patch new: 0 passed, 29 failed.
- Reference base: 747 passed, 0 failed.
- Exact known-genuine Nova 2 base: 753 passed, 0 failed.

The repaired patch retains the same 29 test IDs. It strengthens existing scope cells for qualified ordinary path expressions, distinct-receiver field access, and supported record-field siblings following ignored pattern/binding occurrences.
