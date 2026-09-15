Verify Flakiness — VERDICT FAIL

Two flaky tests were detected across six runs per state:

- `integration::affinity_preserves_metrics_tracing_history_speculation_and_errors`
- `integration::prepared_and_cached_manual_apis_carry_opaque_continuations`

The same hosted artifact set also failed Verify Solution because `integration::prepared_and_cached_manual_apis_carry_opaque_continuations` failed in the solved `new` suite (12 passed, 1 failed).

Classification: test/harness race in the speculative-execution oracle. The zero-interval speculative fiber could lose to an immediate primary response on a resumed page, making exact attempt and history-fiber counts scheduling-dependent.
