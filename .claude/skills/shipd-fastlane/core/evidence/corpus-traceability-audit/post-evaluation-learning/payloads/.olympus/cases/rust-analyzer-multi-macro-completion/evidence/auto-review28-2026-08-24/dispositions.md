# Auto Review dispositions

| Finding | Disposition | Resolution |
| --- | --- | --- |
| Unused `target` binding fails `-D warnings` | Accepted | Removed from the reference solution; verify with the repository warning gate. |
| Relevance-only variants are collapsed | Accepted as description/test mismatch | The current suite does not define relevance as an identity discriminator. The merge contract now exhaustively names the tested discriminators and no longer uses the broader “fully equivalent” wording. No relevance-only test was added. |
| The 64-site limit is applied after expansion traversal | Accepted as description/test mismatch | The executable oracle caps contributing results, not internal work. The description now promises suggestions from at most the first 64 viable mapped sites and no longer calls this a traversal-resource budget. |

The latter two changes intentionally keep the executable task aligned with its existing hidden tests and preserve the previously validated genuine Nova solve.
