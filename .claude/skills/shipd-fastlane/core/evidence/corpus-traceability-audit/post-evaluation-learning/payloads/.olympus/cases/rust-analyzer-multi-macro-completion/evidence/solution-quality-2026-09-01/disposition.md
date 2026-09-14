# Solution Quality disposition

Verdict: contest as a stale/static misread; no artifact change.

The reported unused import does not exist on the exact submitted bytes. `CompletionContext::new` is test-only, but `CompletionContext::new_all` is production code and calls `expand_and_analyze` in its `expand_all == false` single-site fallback. The same production function calls `expand_and_analyze_all` only for eligible multi-site requests. Consequently both imports are required in non-test builds.

Execution proof on `aswin` / `ladybug-olympus`, commit `d2e55da49132fa70a13dfbdc99122432b02cf464`:

`RUSTFLAGS="-D warnings -W unreachable-pub --cfg no_salsa_async_drops" cargo +stable check --locked -p ide-completion`

Exit code: 0. The exact log is `ci-check.log`; the recorded status is `ci-check.status`.

Gating `expand_and_analyze` or its import with `#[cfg(test)]` would be incorrect: it would remove the production fallback used by trigger-bearing, attribute-routed, keyword, tokenless, and otherwise non-multi-site completion requests.
