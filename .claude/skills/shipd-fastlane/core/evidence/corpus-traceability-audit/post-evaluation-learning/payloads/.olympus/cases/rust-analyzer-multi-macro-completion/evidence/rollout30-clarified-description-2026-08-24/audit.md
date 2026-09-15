# Rollout audit and description clarification

- Source ZIP: `agent-runs - 2026-08-24T214736.319.zip`
- Source SHA-256: `2b4025b9f57d41e71ba6d283c4d3fcb4e1e93f0a5543090c975c2b45969b6688`
- Cohort: 22 Nova patches
- Hosted result: 0/22 passed the current 24-test suite
- Permanent extraction: `rollouts/agent-runs-2026-08-24T214736-319/`

## Exact hosted outcomes

| Candidate | Base | New | Main failure cluster |
| --- | ---: | ---: | --- |
| Nova 1 | 10/10 | 21/24 | nested shared cap; non-identifier compatibility |
| Nova 2 | 10/10 | 19/24 | nested cap; imports; isolation; mixed contexts |
| Nova 3 | 0/10 | 0/24 | build/execution failure |
| Nova 4 | 10/10 | 5/24 | first-site/partial traversal architecture |
| Nova 5 | 0/10 | 0/24 | build/execution failure |
| Nova 6 | 0/10 | 0/24 | build/execution failure |
| Nova 7 | 10/10 | 5/24 | first-site/partial traversal architecture |
| Nova 8 | 10/10 | 19/24 | nested cap; trigger continuation; isolation; mixed contexts |
| Nova 9 | 10/10 | 19/24 | nested cap; imports; isolation; mixed contexts |
| Nova 10 | 10/10 | 22/24 | non-identifier compatibility; unsafe mixed-context offset |
| Nova 11 | 9/10 | 18/24 | base regression plus nested cap/import/isolation gaps |
| Nova 12 | 10/10 | 5/24 | first-site/partial traversal architecture |
| Nova 13 | 10/10 | 21/24 | imports; non-identifier compatibility; mixed contexts |
| Nova 14 | 9/10 | 18/24 | base regression plus nested cap/import/isolation gaps |
| Nova 15 | 0/10 | 0/24 | build/execution failure |
| Nova 16 | 10/10 | 21/24 | ignored paths; non-identifier compatibility |
| Nova 17 | 10/10 | 5/24 | first-site/partial traversal architecture |
| Nova 18 | 0/10 | 0/24 | build/execution failure |
| Nova 19 | 10/10 | 20/24 | nested cap; imports; isolation |
| Nova 20 | 10/10 | 5/24 | first-site/partial traversal architecture |
| Nova 21 | 10/10 | 5/24 | first-site/partial traversal architecture |
| Nova 22 | 10/10 | 21/24 | imports; non-identifier compatibility; mixed contexts |

## Decision

No current candidate is a fair one-clause rescue. The closest patch, Nova 10, changes legacy
non-identifier completion and panics while traversing the required mixed type/expression/path/pattern
contexts. Both are central observable defects, not auxiliary implementation preferences. Removing
their tests would create a verifier false positive.

Instead, the description was reorganized without changing the contract or tests. It now states in
one place that aggregation is identifier-only, explicitly lists module/type/pattern path contexts,
explains that the 64-site cap is shared rather than reset recursively, and states the pinned
single-site result for non-identifiers. These are the exact behaviors missed by the closest cluster.
The clarification should improve future solver discovery while preserving all false-positive
discriminators. The previously preserved Nova 7 solution from the earlier cohort remains an exact
10/10 base, 24/24 new, and 782/782 full-suite genuine solve on the unchanged executable bytes.

