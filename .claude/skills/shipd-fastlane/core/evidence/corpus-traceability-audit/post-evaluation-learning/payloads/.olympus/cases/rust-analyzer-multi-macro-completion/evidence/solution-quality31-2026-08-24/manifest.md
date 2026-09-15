# Evidence manifest

Producer environment: Google Cloud Shell, pinned rust-analyzer commit `d2e55da49132fa70a13dfbdc99122432b02cf464`, Rust `1.97.0-x86_64-unknown-linux-gnu`.

| File | SHA-256 | Purpose |
| --- | --- | --- |
| `cloud/base-probe.log` | `c67b0462b1bf19cbf4adc62b619489ce7c6049d901cb17d2543157f01396917c` | Clean pinned behavior for corrected non-identifier probe |
| `cloud/current-probe.log` | `d9fdea99dd01e32f7607c088fbcee1bd37824e97585314f85ee9228c042bdd36` | Old reference failure |
| `cloud/nova-probe.log` | `fcf623eed38f2c3ce6813ab0904de6bb62e2eba2370a1d786b31741e58a9b142` | Previously preserved Nova 7 failure |
| `cloud/current-fixed-probe.log` | `16fcedf9c986720c0fcab9fd1b1f18bbe6d50f5bf562fd49ec3fd59ef86fa3de` | Initial focused reference fix passes |
| `cloud/unsolved-base.xml` | `20935fbcd81fee819e4a6c00cc9f745771e187ac83d4153572477ae400da3620` | Unsolved baseline, 10/10 |
| `cloud/unsolved-new.xml` | `1a1bcf8c30f324ca037a8164eedc6d862b53d6013264c6a52c7e107b7a917000` | Unsolved hidden suite, 0/24 |
| `cloud/nova7fixed-base.xml` | `20935fbcd81fee819e4a6c00cc9f745771e187ac83d4153572477ae400da3620` | Solved baseline, 10/10 |
| `cloud/nova7fixed-new.xml` | `1b828e6ad8f25f490bc4acc681a05f70cbec434f5f51acc6185416f1a868d91d` | Solved hidden suite, 24/24 |
| `cloud/nova7fixed-full.log` | `26fe02348c8191493e6e8aec689d350d4ba0e3b2ae5ab0cc4e3349037afc55cc` | Full warnings-denied library suite, 782/782 |
| `cloud/nova7fixed-fmt.log` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `cargo fmt --all -- --check`, exit 0 |
| `cloud/candidate2-base.xml` | `20935fbcd81fee819e4a6c00cc9f745771e187ac83d4153572477ae400da3620` | Saved independent Nova 2 baseline replay, 10/10 |
| `cloud/candidate2-new.xml` | `1b828e6ad8f25f490bc4acc681a05f70cbec434f5f51acc6185416f1a868d91d` | Saved independent Nova 2 corrected hidden-suite replay, 24/24 |
| `cloud/candidate2-full.log` | `9c5f4f5bcc5e41549a164f9b498a64c26e54d9a09e5808166e098e022d4f0841` | Saved independent Nova 2 full library replay, 778/778 |

The corresponding `.log` files for every matrix mode are retained beside the JUnit documents. Patch application alone/together, `git diff --check`, and `bash -n test.sh` all exited 0 in the same Cloud verification session.
