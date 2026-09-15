# Thermal safety for remote execution

Use this reference before any compilation, test, image build, image export, or other material execution phase. User instructions override these defaults. This profile does not authorize host fallback, partitioning, formatting, mounting, hardware controls, or changes to unrelated services.

## Execution profile

Run on the authorized `shipd-local` host (`arch`) under `/home/admin/olympus-work`, after the execution preflight verifies workspace, pinned commit, input and artifact hashes, free space, Docker root, and destination filesystem provenance. Current observed `/home` is Btrfs on HDD; `/mnt/ssd/docker` also resolves to that HDD. Do not infer SSD storage from its pathname. Leave Windows and NVMe partitions untouched.

Set the quota and sampling interval for the authorized task and record them; the helper defaults are configurable, not a promise that a given quota is thermally safe. The September 12–13 dogfood uses one compile job and one-second sampling. Its current Parquet coverage worker was reduced from **0.25 to 0.1 CPU** after further overshoot; choose and record the conservative quota for the exact authorized workload. Neither quota guarantees a temperature ceiling. Reassess measured temperatures before changing this task profile. Apply limits only to the explicitly owned container. Sample the server's CPU package temperature using `sensors` before starting. Start only below 75°C; pause at or above 75°C; resume only below 65°C. Missing, invalid, or failed sensor reads prohibit execution. Coordinate the shared compute slot with other workflow owners; do source and evidence work while computation is held.

## Exact container ownership and supervision

The helper is [scripts/thermal_guard.py](../../../scripts/thermal_guard.py). Create the owned container first; pass its full immutable Docker container ID, not a discovery expression. Do not enumerate or alter unrelated containers. Start the helper, verify that it has attached and applied the quota, and verify its process is alive before launching material work.

```sh
python3 scripts/thermal_guard.py   --container "$OWNED_CONTAINER_ID"   --log "$THERMAL_LOG"   --cpus 0.1 --pause-at 75 --resume-below 65 --interval 1
```

The launcher must independently poll the guard while work is running. Any guard exit before the owned workload finishes—including a zero exit, sensor failure, inspect failure, Python exception, or watcher crash—must trigger an immediate pause of that exact immutable container ID, record the pause command's outcome, and stop dispatching work. Persist the first operation outcome before cleanup; a failed stop or guard wait must be recorded separately rather than erasing test evidence. A live watcher alone is insufficient: retain the attachment and quota events before dispatch. If the pause command itself fails, record the failure and halt the phase; never label the phase continuously guarded.

The helper handles quota, sensor, and pause/resume failures by attempting to pause the owned container before exiting. SIGTERM and SIGINT likewise attempt a fail-closed pause. It does not resume a pause that existed before attachment. Terminating a guard can therefore leave the owned container paused; a subsequent authorized phase must inspect its state and explicitly take ownership before resuming it. Never automatically resume a pre-existing pause.

The current candidate treats failed inspection and unexpected Python exceptions as watcher errors, attempts to pause the immutable owned ID, and exits nonzero. Inspection unavailability is never evidence of completion. Failed-inspection, malformed-inspection JSON, quota-failure, pause/resume, and pre-existing-pause paths passed isolated fault validation for the revised hash recorded below. Independent launcher supervision remains mandatory, including for termination that Python cannot catch.

## Timing and evidence

Preserve the raw JSONL events, command stdout/stderr and exit codes, original failures, guard source hash, configuration, container ID, CPU quota, sensor source, and launch/finish timestamps. Report total wall time, summed guard-owned thermal pause time, and active elapsed time (wall minus guard-owned pause) separately. Active elapsed time is not CPU time and may still include scheduling or I/O waits. Report image build, runtime rematerialization, tests, and image export separately. Do not overwrite an earlier unguarded result with a later guard validation.

## Observed sampling overshoot

Parent-reported Parquet coverage observations on 2026-09-12: the verified 0.25 CPU / one-second guard recorded 15 brief pauses and a peak of 84°C, with no competing compiler seen. The exact owned worker was reduced live to 0.1 CPU at 23:15:01 UTC; the following two minutes peaked at 74°C with no pauses. These are workload observations, not a controlled quota comparison or a guaranteed safe setting. Preserve the original overshoot, raw samples and quota-change timestamp; label timings that span different quotas and do not combine them into an unsupported speedup claim. This documentation update did not independently rerun the workload.

## Validation status

The current scripts/thermal_guard.py has SHA-256 `5dfb7caa5a919017104b73351cc5253c16308c67382050ea3f8bae2b44a70e21`. Its isolated five-case validation passed in 14.558 seconds at a starting package temperature of 60°C. The owned idle container `d948ad498aac14b10a8a71f85e10bb5de46ef3e0a8c6601bdfc9ca4ca5ff9ccf` was stopped afterward. Validation covered forced pause/resume plus SIGTERM, retention of pre-existing pause, inspect command failure, malformed inspect JSON, and quota failure. The revised sensor-error path was source-reviewed; only the prior version received sensor-error injection. The earlier validated snapshot is preserved at evidence/thermal-guard-v1/thermal_guard.py and is byte-identical to Calyx's helper:

- SHA-256: `7700182175e55385459e215779435f2cfa6fa124b9bdea4ffb5ac48fbe9cff04` (see machine-readable mapping for authoritative bytes).
- Validation source: `/home/admin/olympus-work/fastlane-dogfood-20260912/calyx/thermal-container-guard.py`.
- Validation receipt: `calyx/evidence/guard-validation.json`; raw logs: `guard-validation-cycle.jsonl`, `guard-validation-preexisting.jsonl`, and `guard-validation-sensor-failure.jsonl`.
- Owned idle container: `8701b9ad08d4273524b0d60fe5dc99f02aa16257dc10674f65fd2120e2be1e87`, stopped after the probe.
- Measured starting temperature: 43°C. Total probe wall time: 8.036 seconds.
- Verified NanoCpus = 500000000, forced pause/resume, retention of a pre-existing pause, sensor-error exit 5 with owned-container pause, and SIGTERM fail-closed pause.
- The forced cycle used test thresholds around the measured temperature; production defaults remain 75°C / 65°C. Quota failure and arbitrary watcher crashes were not injected in this validation.

The mapping in [thermal-guard-validation.json](thermal-guard-validation.json) binds the prior validated file, revised candidate, and raw receipts. Promotion and hardening were source-only; the five-case tiny probe ran later in an explicitly allocated slot. The prior pass does not certify additional paths of the revised helper.
