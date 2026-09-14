# Final description–test map — 2026-08-29

The authoritative machine-readable map is `requirements.json` at SHA-256 `4207aea7dfa87bdec776b6296ddd804faf9a990c8e431cd8d97f6cfaccd34e16`.

- Compatibility and specialized bindings: positive class, inline struct, enum, primitive literal, generic class/struct/enum, and non-generic typed struct/enum runtime cases; 13 isolated compatibility or ambiguity rejection cases.
- Runtime shape before extraction: correct and wrong class/struct/enum nominals, zero-field mismatch, guard true/false/not-evaluated, next alternative, and next match arm.
- Pattern contexts: `match`, `is`, conditional chains, nested patterns, and alternatives.
- Open-world exhaustiveness: top-level and nested concrete-only rejection plus wildcard and variable fallbacks.
- Representations and lifetime: reference identity, mutation visibility, inline scalar and managed-reference extraction retained across forced collection, enums, integers, Boolean all-four cells, character, floats, and string.
- Backend parity: every successful hidden runtime file executes with Cannon and Boots.
- Regressions: 14 base groups cover casts, direct patterns, trait dispatch, bytecode, compiler/AOT closure, and failed-cast diagnostics.

There are 31 new groups: 16 successful runtime executions and 15 clean compile-time rejections. Every rejection requires status `1` but does not inspect diagnostic text.
