# v32 Auto Review coverage repair

Repository: `scylladb/scylla-rust-driver`  
Commit: `611d43b595fb0ad7010f2bdbd887acae3d962d65`  
Execution host: `codespaces-14482c`  
Reference worktree: `/workspaces/olympus-scylla-v32-solved`

## Classification

The Auto Review findings were prompt-stated test gaps. No problem or solution scope changed. The source-free test-patch constraint remains intact.

## Test-only changes

- Added `default_policy_rejects_each_prompt_invalid_target_category`, covering a valid routed replica plus remote, non-replica, replaced, host-filtered/disabled, and disconnected targets through public topology metadata and connection behavior.
- Added `automatic_paging_revalidates_against_refreshed_cluster_state`, which replaces a node under the same host ID during the first-page response and proves page two observes the refreshed `ClusterState`.
- Added `automatic_affinity_preserves_tracing_metrics_history_and_speculation`, which forces a preferred-attempt failure under automatic paging and checks trace IDs, exact automatic request metrics, request history, and speculative fibers.
- Updated `test.sh` expected and synthetic JUnit inventories from 12 to 15 cases.

`test.patch` still changes only:

- `scylla/tests/check_paging_continuation_opacity.py`
- `scylla/tests/paging_affinity_1d7881.rs`
- `test.sh`

No `scylla/src/*`, problem, solution, or Dockerfile bytes changed.

## Exact artifacts

- problem: `7cd6d8f7f070c6c98a5c1d5df2b41ddaff8c6b8cf654f20a6cbdd1f6d38d4d8b`
- test: `46287c03cead059377c85e7e618007d442dd22da1557a1ae9e3e3200fbc98302`
- solution: `b3624a960d4d76fe4475d6e319f6987690c3c39c07f36cc3f65874e54d214b44`
- Dockerfile: `d935b06286b10be4b1f847993baeed8723c01da1a5654ae91adcddb759398d71`
- artifact set: `15dba95417cd94a874f47c43f523ddd988f233228ed5ea2595cf972dc337fd7a`

## Verification

- Solved base: 1/1 pass.
- Unsolved base: 1/1 pass.
- Solved new: 15/15 pass.
- Unsolved new: 0/15 pass; all 15 named cases are reported as failures.
- Stability: six consecutive solved-new wrapper runs, all 15/15 with no failures, errors, or skips.
- Targeted policy matrix: 10/10 consecutive passes after replacing the nondeterministic fixed-token owner assumption with the public locator's actual replica.
- Saved agents: Nova 1 and 7 pass 15/15; Nova 2, 3, 4, 5, 6, 8, 9, and 10 remain failures. Pass rate remains 2/10 (20%).
- Patch application: all ten agent patches plus final `test.patch` applied cleanly; zero environment blockers.

Replay matrix: `v32-final-full-replay.tsv`.

## Staleness

Hosted Verify Solution, Verify Flakiness, Test Quality/Fairness, false-positive review, and Auto Review must be rerun on the v32 test hash. Earlier hosted results remain stale.
