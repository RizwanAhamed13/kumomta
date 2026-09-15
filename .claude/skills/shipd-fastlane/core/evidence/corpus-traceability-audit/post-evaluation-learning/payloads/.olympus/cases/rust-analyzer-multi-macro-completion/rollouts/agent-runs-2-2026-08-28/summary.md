# Rollout audit — agent-runs-2.zip

- ZIP SHA-256: `68ace5a024634f8127fa8eb44a523bd7c5e4d029b525f860482f90bfba4a8ed6`
- Artifact set: `ac6fb68411938c8a8c50c905b40ba95ea1e39b65aac480930ae97a99133cb6f1`
- Valid runs: 10
- Baseline: every run passed 747/747
- New-suite passes: 0/10
- Environment failures: 0

| Run | New result | Decisive missing behavior |
|---|---:|---|
| Nova 1 | 26/29 | ignored-path budget, expression-role coverage, unsupported-role safety |
| Nova 2 | 28/29 | rowan bad-offset panic on pattern/binding sibling |
| Nova 3 | 28/29 | type-only suggestions leak after an empty sibling |
| Nova 4 | 5/29 | broad incomplete implementation |
| Nova 5 | 28/29 | type-only suggestions leak after an empty sibling |
| Nova 6 | 27/29 | expression-role coverage and unsupported-role safety |
| Nova 7 | 27/29 | expression-role coverage and unsupported-role safety |
| Nova 8 | 27/29 | ignored-path budget and unsupported-role safety |
| Nova 9 | 28/29 | rowan bad-offset panic on pattern/binding sibling |
| Nova 10 | 27/29 | expression-role coverage and unsupported-role safety |

The dominant difficulty driver is safely rejecting unsupported mapped roles after per-site expansion without leaking their suggestions or applying compensated offsets outside the analyzed syntax tree. Removing this assertion would recreate the previously adjudicated false-positive class, so this batch does not justify an artifact edit.
