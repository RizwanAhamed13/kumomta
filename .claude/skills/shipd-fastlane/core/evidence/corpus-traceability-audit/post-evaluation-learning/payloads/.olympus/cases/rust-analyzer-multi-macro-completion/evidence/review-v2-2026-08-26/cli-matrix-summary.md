# Review v2 CLI matrix

Date: 2026-08-26
Pinned commit: `d2e55da49132fa70a13dfbdc99122432b02cf464`
Execution: Google Cloud Shell through `gcloud cloud-shell ssh`

Exact artifacts:

- `test.patch`: `d1a697b423f2477e3571827f1d68041fb90950de6a4cccdcea69f15fa1c9c1a5`
- `solution.patch`: `9e0e6339880be12af8f0cab785a7a45aa5cfecf9ea5c2ce1fca829a47abb36f3`

Results:

- Reference + tests, new: 29 passed, 0 failed, exit 0.
- Reference + tests, full base: 747 passed, 0 failed, exit 0.
- Untouched + tests, new: 0 passed, 29 failed, exit 101.
- Untouched + tests, full base: 747 passed, 0 failed, exit 0.
- Saved Nova10 (`a8734f97...`), new: 27 passed, 2 failed. Failures: token/raw identifier boundary edit coverage and unsupported-context rejection.
- Latest prior legitimate pass (`agent-runs-2026-08-26T174502-107/Nova_Nova`), new: 28 passed, 1 failed. Failure: unsupported-context rejection.
- Saved filtered Orion3, new: 24 passed, 5 failed.

Decision: do not upload. The verifier and golden are aligned, but no independent saved solver passes the current exact artifact set. A fresh rollout must produce at least one conforming solve before upload.
