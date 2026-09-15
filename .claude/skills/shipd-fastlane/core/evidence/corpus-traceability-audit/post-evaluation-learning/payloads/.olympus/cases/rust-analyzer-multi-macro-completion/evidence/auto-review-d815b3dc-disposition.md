# Auto Review disposition — d815b3dc — 2026-08-27

- T4 no-parentheses field access: `REQUIRES CONTRACT EXPANSION`. The bounded `left.$field; right.$field;` probe failed both the canonical reference and the preserved Nova 8 solution. The public contract is narrowed to distinct-receiver method-call positions; no assertion was added.
- S1 markerless mapping multiplicity: `PROMPT GAP / GOLDEN MISMATCH`, resolved by clarifying that multi-site classification concerns cursor-bearing mapped occurrences. Markerless changed-text outputs remain non-contributors and must not hide a later exact cursor-bearing occurrence, which the current suite retains.
- Stale rollout discussion: `STALE`. It cites token-start requirements and a ten-run cohort; current scope excludes token-start positions and the preserved latest cohort contains seventeen runs.
- Pass-floor decision: no tests were removed in response to this Auto Review. The earlier token-start carve retains one execution-proven Nova pass. No claim of three platform passes is made without a new hosted cohort.

Execution evidence:

- Preserved Nova 8 plus no-parentheses field probe: 28/29; `same_label_items_with_different_public_kinds_are_preserved` failed with an empty field-item list (`/tmp/n8-field-probe.xml`, Google Cloud Shell).
- Canonical reference plus the same probe: failed the same new logical test (`/tmp/ref-field-probe.xml`, Google Cloud Shell).
- Exact reduced canonical suite before this description-only clarification: Nova 8 29/29 and reference 29/29 in `evidence/zero-pass-carve-2026-08-27/`.
