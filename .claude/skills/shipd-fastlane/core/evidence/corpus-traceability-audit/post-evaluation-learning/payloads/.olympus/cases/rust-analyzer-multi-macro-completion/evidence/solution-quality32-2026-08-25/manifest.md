# Solution Quality 32 evidence manifest

All repository compilation and execution was performed in Google Cloud Shell against
`rust-lang/rust-analyzer@d2e55da49132fa70a13dfbdc99122432b02cf464`. Local work was limited to
artifact, ledger, and evidence-file maintenance.

## Executed checks

- Clean patch application: `test.patch` alone, `solution.patch` alone, and both together.
- Static patch checks: `git diff --check`, `cargo fmt --all -- --check`, and `bash -n test.sh`.
- Isolated four-state wrapper matrix with separate worktrees and Cargo targets:
  unsolved base 10/10, unsolved new 0/24, solved base 10/10, solved new 24/24.
- Full reference regression: `RUSTFLAGS='-D warnings' cargo test --offline --locked -p ide-completion --lib`, 782/782 passed.
- Exact pre-fix discriminators: raw underscore suppression, relevance-only duplicate identity,
  and lifetime token-kind routing all fail on the old reference and pass on the fixed reference.
- Saved Nova 2 replay: suppression and relevance probes pass, lifetime routing fails; it is not a
  current independent solve.

## Evidence hashes

```text
f110b0b11b427fe897044165604061167ea02147cadceece844d7b0dbb74a656  cloud/candidate2-lifetime.log
08e51763554672bfc52d1513954d96cf71d651423d955607c9adf2aaec3a5288  cloud/candidate2-relevance.log
5104e70cfc5684fb5794008227b7bce3b3c687e7084530b65b677e5ca06f8ea0  cloud/candidate2-underscore.log
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  cloud/final-fmt.log
cc386dc5cdf4bf4e6d27c105700b7588898c0462433eb92e3bbed2d89db78f37  cloud/final-solved-base.log
20935fbcd81fee819e4a6c00cc9f745771e187ac83d4153572477ae400da3620  cloud/final-solved-base.xml
4d051ac80a70e6e37ad467cbc28c4215d17620cc2671a97f81236108618d1a2a  cloud/final-solved-new.log
1b828e6ad8f25f490bc4acc681a05f70cbec434f5f51acc6185416f1a868d91d  cloud/final-solved-new.xml
d5fd0db5a2406e0972fb8daf4c04c8fa0542f1e2f6b3538e8865da0781fe712c  cloud/final-unsolved-base.log
20935fbcd81fee819e4a6c00cc9f745771e187ac83d4153572477ae400da3620  cloud/final-unsolved-base.xml
4c32eccb3fd2dc1a9dd2de9ad7c799d2133ceb53b11860e56d622fb5b8ea9d51  cloud/final-unsolved-new.log
f03d819a27369c7acd331f8518f249719073f42f5e547f76aa943b404b1823f0  cloud/final-unsolved-new.xml
f8becc1f82dc48b8a2a2aabef18fbbfa50bfaa87e5d1e1ac2cd32c5d80eef331  cloud/oldref-lifetime.log
734655efbc9a8779a948d699199f568b2663b70c596cc7691c365a36f8092687  cloud/oldref-relevance.log
a8f9224192f05078460ccd2b7ae0ea216c17df0f7172771cd5ee69b8421b67f7  cloud/oldref-underscore.log
4a09bb4385ba9aedc681104c4f77dc9d37873c33fd2959bdf74e59d4cdfbe6a3  cloud/reference-base.log
20935fbcd81fee819e4a6c00cc9f745771e187ac83d4153572477ae400da3620  cloud/reference-base.xml
646e4650308dbd98ef6e244ddb49a22a2581bbbb628257b2513d8feda0bd5d7d  cloud/reference-full.log
6a9d9a19cf74bc30b8ec93dab8b09d2f1f31c9736bc739230dd2e81556853762  cloud/reference-new.log
1b828e6ad8f25f490bc4acc681a05f70cbec434f5f51acc6185416f1a868d91d  cloud/reference-new.xml
```

The empty formatter log is expected and records a successful no-output format check.
