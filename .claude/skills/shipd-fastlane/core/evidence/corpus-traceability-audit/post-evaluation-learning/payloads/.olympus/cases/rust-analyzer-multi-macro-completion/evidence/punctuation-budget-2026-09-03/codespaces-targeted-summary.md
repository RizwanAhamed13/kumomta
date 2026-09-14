# Codespaces targeted replay

- Codespace: `ra-punctuation-replay-v6gwrpjqjw67cp7qr`
- Hostname: `codespaces-14482c`
- Repository: `rust-lang/rust-analyzer`
- Commit: `d2e55da49132fa70a13dfbdc99122432b02cf464`
- Toolchain: Rust `1.97.0`
- Strengthened test SHA-256: `3acdec9d9d80f22ba7e5b6fa2b0a68d2710cc912207e5d3def349a563ff5edbc`
- Reference solution SHA-256: `490181546a007d7909fd8761ce9309e2c594c83cf2970790944410c01525341f`
- Nova 1 SHA-256: `fa818ee71043ebda58558aedf9a59f1b4fdf65609c018e28cf5b0042041a921b`
- Nova 2 SHA-256: `7bb96ee6839db9f0f4112f58c5d4f7b0ab2f5cff03fc41d3e82e22c3a43161d5`

Targeted command in four isolated worktrees and target directories:

`cargo +1.97.0 test --locked -p ide-completion --lib tests::macro_multi_completion::ignored_paths_do_not_consume_the_viable_site_budget -- --exact --nocapture`

Results:

- Reference: exit `0`, 1 passed.
- Historical genuine Nova 1: exit `101`; the existing same-expansion literal-before-record assertion failed with no `beta_field` completion.
- Historical genuine Nova 2: exit `101`; the same test failed.
- Untouched base: exit `101`; the earlier ignored-path assertion failed as expected.

The punctuation-only addition was not promoted. Canonical `test.patch` was restored byte-for-byte to the prior literal-regression artifact, SHA-256 `8570793202f720d9a0f86493ac00f01b467f2332ef226d4f4764155d03ef46ff`.

The remote raw logs remain in `/workspaces/ra-punctuation/evidence/` inside the Codespace.
