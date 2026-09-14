# Shipd Fastlane portable core

Read [PORTABILITY.md](PORTABILITY.md), then [WORKFLOW.md](WORKFLOW.md) and the [Fastlane procedure](skills/shipd-fastlane/PROCEDURE.md). Native app entrypoints sit outside this directory.

- `scripts/`: unchanged Fastlane validators and bookkeeping tools; Python standard library.
- `assets/`: plans, checklists, gate catalog and evidence schemas.
- `knowledge/` and `evidence/`: preserved historical corpus and receipts.
- `vendor/olympus-forge/skills/`: bundled phase procedures and supporting tools.
- `vendor/eligibility/`: repository denylist checker and dated list.
- `provenance/`: source identities and original plugin metadata.

Run tools only on the authorized server. The legacy budget subcommand understands Codex usage JSON only. Neither original receipts nor structural tests of this package prove hosted acceptance.
