# Description Quality review dispositions

| Comment | Disposition | Current-byte resolution |
| --- | --- | --- |
| `normal one-marker speculative mappings` | Stale | The canonical description already says “viable identifier occurrences produced by a macro expansion” and contains no one-marker mechanism. |
| `Keep mapper emission order for equal ranks` | Accepted | Removed because the suite proves ascending rank and depth-first order but has no dedicated equal-rank tie oracle. |
| `within the first 64 mapped identifier sites examined` | Stale | The canonical description already separates ordinary-request budgeting from trigger continuation and contains no trigger/budget cross-product. |
| `Relevance metadata may likewise distinguish items` | Stale | The canonical description already omits relevance and names only tested public distinctions. |

No test or reference-solution behavior changed. This is a description-only narrowing to the existing executable contract.
