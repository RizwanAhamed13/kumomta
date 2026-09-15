# Verify Solution wrapper-classification repair

Hosted Verify Solution reported `before_extras_not_skipped` because the unsolved compile-failure fallback emitted `test-runner.cargo-test`, which was neither P2P nor F2P. The same run also reported permission errors creating `/app/target*`. The seven intended integration tests were otherwise correctly classified F2P, and the base regression was correctly classified P2P.

Repairs:

- The compile-failure fallback now emits the canonical base testcase identity in `base` mode and all seven canonical integration testcase identities in `new` mode. It emits no synthetic extra testcase.
- `CARGO_TARGET_DIR` is set to `${TMPDIR:-/tmp}/scylla-paging-affinity-${mode}-target`, keeping base and new builds isolated and writable outside `/app`.
- The argument parser continues to accept `./test.sh --output_path <path> base` and the reverse ordering.

Forced-failure parser probes produced valid XML with one base failure or seven integration failures and exited 101.

Aswin/LXC UID-1000 matrix at commit `611d43b595fb0ad7010f2bdbd887acae3d962d65`:

| State | Mode | Exit | JUnit |
|---|---|---:|---|
| test only | base | 0 | 1 case, 0 failures |
| test only | new | 101 | 7 canonical integration cases, 7 failures, no extras |
| test + solution | base | 0 | 1 case, 0 failures |
| test + solution | new | 0 | 7 canonical integration cases, 0 failures |

All four Cargo target directories were created under the state-specific `/tmp` directories and owned by UID 1000. No `/app/target*` permission failure occurred.

`validate_submission.py` and the temporary-index clean patch matrix passed on final bytes.
