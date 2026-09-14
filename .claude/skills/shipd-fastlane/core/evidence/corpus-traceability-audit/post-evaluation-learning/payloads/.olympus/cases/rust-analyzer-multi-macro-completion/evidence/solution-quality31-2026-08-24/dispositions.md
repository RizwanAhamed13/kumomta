# Solution Quality dispositions

| Finding | Disposition | Resolution plan |
| --- | --- | --- |
| Leading ignored non-identifier mapping hides a later viable pinned site | Accepted and fixed | The existing compatibility helper now covers ignored `env!` and empty `discard!` mappings before a viable `format_args!` site. The reference scans until the first viable non-identifier site instead of truncating candidates before viability. |
| The 64-site cap does not bound internal expansion work | Accepted and fixed as a code-quality improvement, not a new public oracle | The reference now carries one request-wide expansion state and stops materializing later branches after the viable-site limit is reached. No timing or internal-instrumentation assertion was added. |

The first assertion is prompt-grounded by ignored-path continuation plus pinned non-identifier behavior. Exact probing also showed that the prior helper incorrectly expected the first ranked mapping even when it expanded to nothing. That assertion is corrected to the pinned first-successful-site result. It intentionally remains a helper because the clean pinned implementation satisfies it; making it a standalone new test would violate the base/new fail-to-pass contract.

Google Cloud verification on the corrected bytes:

- Clean pinned base: base mode 10/10; new mode 0/24, with all 24 expected failures.
- Fixed reference: base mode 10/10; new mode 24/24.
- Full `ide-completion --lib` regression under `RUSTFLAGS=-D warnings`: 782/782.
- Patch application alone/together, `git diff --check`, `cargo fmt --all -- --check`, and `bash -n test.sh`: pass.

The previously preserved Nova 7 result is no longer a durable genuine solve for the corrected artifact bytes: its exact pre-fix traversal fails the pinned non-identifier discriminator. A separate saved Nova 2 implementation was replayed on the corrected bytes and passes base 10/10, new 24/24, and the full library suite 778/778. This is current local solvability evidence, while its formal hosted false-positive disposition still needs refreshing. Hosted rollout, Solution Quality, Verify Solution, fairness, mutation, and downstream review results that depend on `test.patch` or `solution.patch` are stale.
