# Review repair v36

- Repository: `scylladb/scylla-rust-driver`
- Commit: `611d43b595fb0ad7010f2bdbd887acae3d962d65`
- Execution: Codespace `codespaces-14482c`, `/workspaces/scylla-runs38-audit/v36`
- Artifact set: `76828d87177757eb880b16ffd52ffd35ba164076651ed490caf2c40f35ac0833`

## Dispositions

- Platform-leaking test identifier: **fixed**. Renamed `default_policy_rejects_each_prompt_invalid_target_category` to `default_policy_rejects_each_invalid_target_category` in the Rust test and both runner inventories. No behavior changed.
- Public enum/union opacity escape: **fixed**. The Rustdoc oracle still accepts external opaque carriers, private named structs, private tuple structs, and private-field unions. It now rejects public enums, public-field unions, stateless structs, primitive aliases, and alias cycles. The 11-shape battery passed 11/11.
- Prepared/caching retry winner: **covered** by extending the existing retry scenario. Both prepared Session and CachingSession now fail the first EXECUTE attempt, succeed on another coordinator, resume, and assert that the successful coordinator is the policy preference. No new requirement or public API was introduced.
- Test Quality's five remaining suggestions: **advisory/nonblocking**. They did not affect its PASS verdict. This batch consumed the three-probe cap on the two Auto Review blockers plus the prepared/caching gap; speculative topology/error/input expansion was not added without a current-suite survivor.

## Exact validation

- Patch application: test patch applies alone and after the reference solution.
- Patch contents: three test-only files; no `scylla/src/*` hunks.
- Four-state JUnit: base `1/1` before and after; new `0/16` before and `16/16` after.
- Stability: 12 sequential solved-new runs, all `16/16`, zero failures/errors/skips.
- Saved-agent replay: unchanged `2/10` pass profile. Nova 1 and 7 pass `16/16`; Nova 2–6 and 8–10 fail on the same pre-existing semantic cases as v35.
- Opacity alternatives: `11/11` expected outcomes.

## Artifact hashes

- `problem.md`: `7cd6d8f7f070c6c98a5c1d5df2b41ddaff8c6b8cf654f20a6cbdd1f6d38d4d8b`
- `test.patch`: `cb715d7f2b1832154c4aa947ad5ef72359ad1b546d1d8684b5a22179f5652f98`
- `solution.patch`: `b3624a960d4d76fe4475d6e319f6987690c3c39c07f36cc3f65874e54d214b44`
- `Dockerfile`: `d935b06286b10be4b1f847993baeed8723c01da1a5654ae91adcddb759398d71`

Hosted Verify Solution, Verify Flakiness, Test Quality/Fairness, false-positive review, Holistic, Auto Review, and rollout results that depend on `test.patch` are stale and must be rerun against v36 before readiness.
