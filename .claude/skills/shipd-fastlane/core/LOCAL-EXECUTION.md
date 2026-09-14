# Local execution override: sandboxed remote container

This override applies whenever Fastlane runs inside this repository's
Claude Code remote execution container (or an equivalent ephemeral,
already-sandboxed CI/cloud container) instead of on the physical
`shipd-local` / `arch` workstation described in `PORTABILITY.md` and
`WORKFLOW.md` section 16. It replaces the SSH-to-`shipd-local` routing;
it does not waive any eligibility, quality, evidence or paid-operation
gate defined elsewhere in this skill.

## When this override applies

- No `shipd-local` SSH target is reachable, configured or authorized
  from this session, and the user has not asked for it.
- The current container already has a working local Docker daemon
  (verify with `docker info`; start one with `dockerd &` if the CLI is
  present but no daemon is running).
- The user has explicitly asked to keep all computation inside this
  container rather than touching the external Arch host.

When these hold, treat this container as `<core-root>`'s compute target
directly. Do not attempt the `ssh -o BatchMode=yes ... shipd-local`
step; do not transfer the core to a remote workspace first.

## Workspace

Use a scratch workspace under this session's scratchpad directory
(never the repository working tree itself) for candidate checkouts,
Docker builds and test runs, e.g. `<scratchpad>/fastlane-work/<case-id>/`.
Record its path in the case plan in place of `/home/admin/olympus-work`.

## What is dropped from the Arch-specific policy

The following sections of `WORKFLOW.md` #16 and `PORTABILITY.md`
describe controls specific to the physical shared Arch workstation and
do not apply to an ephemeral, already-isolated cloud container:

- Hostname/IP checks requiring `arch`, and mount/filesystem identity
  checks for `/mnt/ssd/docker` vs Windows partitions — this container
  has no such shared or dual-boot storage to protect.
- CPU temperature sampling, the 65°C/75°C thermal thresholds, CPU
  affinity 16-31 and the 0.25 CPU quota — those exist to protect a
  physical machine shared with other workloads; this container's own
  platform-level resource limits already bound it.
- The requirement for an independent thermal/SIGKILL watcher process.
- Coordinating pauses of other users' workloads on the shared host.

## What still fully applies

- Everything in `WORKFLOW.md` #1-#15 and #17-#18: source of truth,
  denylist checks, feasibility proof, test inventory, the full
  reference solution, Scope Gate authorization, the four-state matrix,
  coverage, mutation testing, the offline Docker package, the 20
  quality families, repair discipline, exact-byte release and the
  lessons ledger.
- One material build/test job at a time in this container; do not
  launch competing parallel Docker builds against the same case.
- Record actual resource use (wall time, `docker stats` CPU/memory)
  in evidence in place of the Arch thermal/affinity log — label it
  "container-local, no thermal policy" rather than inventing a
  temperature reading.
- All paid/hosted Shipd gates still require explicit user
  authorization per gate; local execution here never substitutes for
  a hosted receipt.
- Never point Docker at anything outside the scratch workspace; never
  touch this repository's own git history or unrelated running
  containers.

## Preflight (replaces the Arch preflight in WORKFLOW.md #16)

Before each computational phase, record:

- Confirmation `docker info` succeeds (daemon reachable).
- Real working directory (the scratch workspace path above).
- Full source commit and input SHA-256 hashes.
- Free disk in the container (`df -h` on the scratch workspace mount).
- That no other Fastlane build/test job is currently running here.

Stop and report rather than silently falling back if Docker cannot be
reached after starting `dockerd`, or if disk space is insufficient.
