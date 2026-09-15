# Base-mode exclusion repair

Artifact set: `0f2bccd7bd1751384d07337247167d1280f8decbe022b1377e654f3c7374b5f6`

- Pinned commit: `dc060ecd16224ad01cdb8d7bafe89230e477446a`.
- `test.patch` applies cleanly to the pristine commit.
- `bash -n test.sh`: PASS.
- The exact base e2e selection with all 8 feature-test names excluded reports `running 0 tests`, `8 filtered out`, exit 0.
- The previous exact hosted baseline had 9,051 passes and only the two newly added e2e tests failing; both are now excluded.
- Test bodies are unchanged. The prior exact reference and Batch 92 Nova 1 each passed all 25 new tests; the prior test-only state failed all 25. Those execution results are stale by strict hash policy after this runner edit and may be replayed or refreshed by hosted Verify Solution.
- Dockerfile, problem.md, and solution.patch are unchanged.
