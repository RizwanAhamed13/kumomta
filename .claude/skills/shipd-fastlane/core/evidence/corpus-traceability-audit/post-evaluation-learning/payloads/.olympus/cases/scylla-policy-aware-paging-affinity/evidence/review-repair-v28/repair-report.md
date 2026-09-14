# Review 28 flakiness repair

- Execution host: `codespaces-14482c`
- Repository commit: `611d43b595fb0ad7010f2bdbd887acae3d962d65`
- Reference worktree: `/workspaces/olympus-scylla-v28-solved3`
- Test-only worktree: `/workspaces/olympus-scylla-v28b-testonly`
- Artifact set: `ad0a7481488b40fd22e0c720b214e39d093f77bb5a2cee814a26745e840ea069`
- Test patch SHA-256: `7266b7d4477e99c4174d9b422306b65b533d26ed133fb1a2af5012542717da60`

Root cause: the v27 speculative oracle dropped a fixed proxy node and used a zero retry interval. On resumed pages the immediate primary response could complete before the speculative fiber was recorded, making the exact attempt and history-fiber assertions scheduling-dependent.

Repair: the fixture now exposes the two proxy addresses, maps the policy's actual primary node to its proxy, and drops that primary. After the first page returns, the proxy rules are reconfigured to drop the returned coordinator for the resumed page. The alternate target is therefore required to answer both pages; the test does not depend on a response-delay race.

Evidence:

- Unsolved base: 1/1 pass.
- Unsolved new: 0/13 pass; 13 expected failures.
- Solved base: 1/1 pass.
- Solved new: seven consecutive runs, each 13/13 pass with no failures, errors, or skips.
- Exact test patch applies after the reference and saved Nova patches 2, 4, 6, 8, and 9.
- Full saved-agent wrappers: Nova 2, 4, and 8 pass. Nova 6 and 9 fail the pre-existing same-DC/other-rack eligibility assertion that was already present before this flake repair; their prior genuine labels require reconciliation and were not used to weaken that requirement.

Hosted Verify Solution, Verify Flakiness, quality/fairness/FP checks, Auto Review, and rollout evaluation tied to earlier test bytes are stale.
