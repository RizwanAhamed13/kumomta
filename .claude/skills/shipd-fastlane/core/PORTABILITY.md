# Portable execution policy

These OpenCode, Antigravity and Claude Code distributions use the same Fastlane engine, evidence corpus and bundled Olympus Forge procedures. This file adapts host integration; it does not waive eligibility, quality, paid-operation, routing or thermal gates.

## Resolve paths and capabilities

`<core-root>` is the directory containing this file. The full Fastlane entrypoint is `skills/shipd-fastlane/PROCEDURE.md`. Every `<plugin-root>` in the core workflow means this core directory. Olympus phase procedures are bundled in `vendor/olympus-forge/skills/<phase>/PROCEDURE.md`; read the chosen file and its relative references. A `$olympus-*` label in those documents names a phase procedure; it is not a promise that another app registered a slash command. Forge's `scripts/` means the scripts adjacent to `vendor/olympus-forge/skills/olympus-workflow/PROCEDURE.md`. No separately installed Codex or Forge plugin is required.

Use this client's available shell, file, browser and connector capabilities. Do not invoke Codex-specific tool names, thread automation or screenshot APIs that the client does not expose. Prefer a connected code graph for source discovery; if unavailable, use bounded repository searches on the server. Read the live panel through an authenticated browser capability when needed. If that capability or authentication is missing, persist the local result and identify the affected live step as blocked. Do not invent panel fields, usage measurements, tool calls or hosted results.

## Usage and task preferences

No workflow percentage cap is imposed by this distribution. Honor any cap, reserve, currency budget and duration the user explicitly sets for the current task. Use an actual client/provider usage measurement only when available; record unavailable measurements as unknown. Unknown usage alone is not a blocker when no user cap applies. If a requested cap cannot be measured reliably, stop the spend-dependent phase and ask for a usable measurement or an explicit policy change. A local workflow cannot enforce account-wide usage or exclude concurrent tasks.

`fastlane.py budget` remains an unchanged legacy parser for Codex usage JSON. It is not an OpenCode, Antigravity or Claude quota adapter. Never feed it invented or relabeled provider data. Account limits still apply. Do not change global model settings, purchase credits, redeem resets or add background tasks. Record temporary task preferences and their authorized expiry, restore only preferences this task changed, and do not reintroduce a removed cap.

## Remote execution and existing pauses

Use `ssh -o BatchMode=yes -o ConnectTimeout=10 shipd-local`; hostname must be `arch`, user `admin`, workspace `/home/admin/olympus-work`. All repository work, code generation, validators, packaging, builds, tests and material computation run there. The client machine orchestrates, reads lightweight metadata and transfers evidence. Preflight before each phase: verify hostname, workspace, exact source commit (or label a non-Git snapshot honestly), input SHA-256 hashes, available disk, Docker availability and destination mount/physical filesystem. Preserve the record. Stop if the host or required dependency is unavailable; no silent fallback.

**Exception — sandboxed remote container:** when running inside this repository's own already-isolated Claude Code remote execution container (or an equivalent ephemeral CI/cloud sandbox) with no `shipd-local` target authorized for this session, read `LOCAL-EXECUTION.md` instead and use this container as the compute target. That file defines the replacement workspace, preflight and which Arch-specific (thermal/affinity/shared-host) controls are dropped as inapplicable versus which gates still fully apply. Never use this exception to reach the physical Arch host from inside a session that has not been given SSH access to it.

Place a checksummed copy of this entire core under the authorized remote workspace before invoking its scripts. Use the matching remote core path in commands. Verify transfer hashes in both directions. Do not point remote Python at a client path.

Leave Windows partitions, `/mnt/windows`, storage layout and mounts untouched. An SSD-looking pathname is not proof of SSD backing. Follow `skills/shipd-fastlane/references/execution.md` and `skills/shipd-fastlane/references/thermal-safety.md`, maintain ownership of workload pauses and use a supervised compute slot. Do not automatically resume previously paused work. Missing/invalid sensors or supervision blocks computation. Stop dispatching at high temperature and preserve evidence; coordinate only identified, authorized workloads rather than killing unrelated processes. One agent is the default; additional agents require user authorization.

## Stage and evidence boundaries

Before candidate ranking or construction, run `python3 <core-root>/vendor/eligibility/scripts/check_disallowed_repo.py --repo <owner/name>` on the server. The bundled list is a dated snapshot, not an automatically current feed. Validate the checker/list, retain normalized repository, date, list hash, entry count and output, and repeat immediately before Scope. A denied repository is rejected; unreadable or unvalidated inputs remain REVIEW. Refresh from an authoritative supplied list when necessary, with provenance.

Read `WORKFLOW.md`, the full Fastlane entrypoint, and the selected bundled Forge phase. Keep reference implementation, prompt, tests, runner and Dockerfile aligned. Require applicable local evidence gates before any upload. No paid Shipd gate, rollout or extra platform batch without explicit authorization for that specific gate. Local replicas cannot certify private graders, hosted acceptance or future first-pass success.

For fresh reconstruction, read only the generic route and allowed inputs until its freeze boundary. Bundled case knowledge and historic implementations are available but are not automatically allowed benchmark inputs. Do not relabel historical validation or accepted status as a test of this port.

`provenance/` and `knowledge/` preserve historical records, including original Codex paths and old host observations. They are evidence, not installation instructions. Current user instructions take precedence over all packaged defaults.
