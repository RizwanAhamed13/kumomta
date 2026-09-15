# Auto Review / Solution Quality repair dispositions

Pinned commit: `d2e55da49132fa70a13dfbdc99122432b02cf464`

## Findings

- Post-analysis 64-site accounting — `REQUIRES CONTRACT EXPANSION`. The exact previous reference and preserved Nova solution both failed the proposed missing-`in` recovery probe. The prompt now explicitly bounds terminal expanded identifier occurrences, matching the implemented traversal boundary and existing 64-site tests.
- Nested and attribute edit targeting — `PROMPT-STATED`. Strengthened `applies_the_edit_to_the_original_invocation` with nested declarative and direct attribute-produced `check_edit` cases.
- Equal non-empty import deduplication — `STALE/CONTRADICTORY`. Current `problem.md` permits import-producing suggestions to retain single-context behavior.
- String non-fanout — `PROMPT-STATED`. Added two distinguishable viable format-string contexts and requires exactly one context to contribute.
- Opening-parenthesis expression noise — `PROMPT-STATED`. Added a unique expression local and requires it to remain absent while `super` survives.
- Macro-generated marker provenance — `PROMPT-STATED`, `FIXED`. A span-preserving fixture emits identical ordinary/speculative marker-shaped output. The old exact reference incorrectly returned `record_field`; the fixed reference and preserved Nova reject it.
- Repeated tree scans — `CODE-QUALITY`, `FIXED`. `isolate_completion_site` now indexes expansion token membership once per isolated site with `HashSet`, eliminating the nested whole-tree scan inside the mapped-token loop.

## Exact Cloud evidence

- Untouched: base `10/10`; new `0/21` with 21 assertion failures.
- Fixed reference: base `10/10`; new `21/21`; full `ide-completion --lib` `768/768`.
- Preserved Nova 1: base `10/10`; new `21/21`; full `ide-completion --lib` `773/773`.
- Prior exact reference plus generated-marker helper: failed with `record_field`, exit 101.
- Patch application, `git diff --check`, and `cargo fmt --all -- --check` passed in Google Cloud Shell with Rust 1.97.0.

Raw JUnit and logs are under `cloud/`.
