---
name: shipd-fastlane
description: Build, validate and improve Shipd/Olympus challenge artifacts with accepted-case lessons, contract and execution coverage, local quality gates, exact-byte evidence and server-only computation. Use to resume a case, reduce review iterations, strengthen tests, optimize Verify Solution runtime or run an authorized fresh reconstruction.
---

# Shipd Fastlane

This skill includes the complete workflow, validators, reference corpus, Olympus phase procedures and repository eligibility checker. Resources are in [core](core/README.md), relative to this SKILL.md.

1. Read [the portable execution policy](core/PORTABILITY.md) before acting. It defines client capabilities, usage handling and mandatory `shipd-local` routing. Do not assume Codex-specific tools exist.
2. Read [the complete Fastlane procedure](core/skills/shipd-fastlane/PROCEDURE.md) and [delivery workflow](core/WORKFLOW.md). Resolve the selected case and first unproven stage; avoid a broad rescan.
3. Read the selected phase in `core/vendor/olympus-forge/skills/<phase>/PROCEDURE.md` and its referenced laws. Those phase names identify bundled procedures, not separately installed plugins.
4. Copy the complete core to the authorized server with checksummed transfer before running any scripts. Use its server path as `<core-root>` and `<plugin-root>`.
5. Produce exact artifacts, current local evidence and a handoff distinguishing passed, stale, blocked and unrun checks.

A removed 50% cap stays removed. No global settings edits, automatic credit resets or paid Shipd checks. Specific paid gates require explicit user authorization. Existing host pauses stay owned by their original tasks. Local validation does not guarantee a hosted pass.

For fresh reconstruction, follow `core/skills/shipd-fastlane/references/fresh-reconstruction-benchmark.md` before reading case-specific knowledge. Preserve its evidence-withholding boundary.
