# Shipd Fastlane

A separate Codex plugin for faster Shipd artifact delivery with fewer avoidable review cycles. It complements the installed Olympus Forge phase skills and keeps the workspace's builder, fairness, authorization and evidence rules.

## Use it

In a fresh Codex task, invoke **$shipd-fastlane**:

> Use $shipd-fastlane for <case path>. Resume the first unproven stage, retrieve the relevant historical lessons, build the public contract map, and deliver the next proven artifact package with hashes and a handoff. Keep Codex account usage below 50%. Paid checks require my explicit authorization.

For a fresh historical reconstruction:

> Use $shipd-fastlane for a fresh reconstruction benchmark of <original prompt and pinned commit>. Use the prompt, pinned source and generic workflow only, record exposure, and withhold archived tests until the first-complete package passes the agreed own validation and its transferred hashes are verified. Preserve first results and repairs separately. Finish the authorized offline work; do not run paid checks.

This [route](skills/shipd-fastlane/references/fresh-reconstruction-benchmark.md) does not certify blindness or live submission readiness. Record the current task’s usage override when the user explicitly changes or removes the default cap.

For a runner optimization:

> Use $shipd-fastlane to optimize Verify Solution for <case path> on shipd-local. Measure the current runtime, remove repeated setup/build work, preserve full contract coverage, validate the complete four-state matrix, and report before/after timings and stale gates.

The default workflow stops at a completed stage boundary. Explicitly request continuation across stages when needed. Existing paid-gate authorization remains scoped to what the user approved.

## What changes the work

| Avoidable cost | Built-in response |
|---|---|
| Building weak or occupied candidates | Accepted architecture calibrators and rejection lessons before construction |
| Repeated omissions and review fixes | Independent public input inventory, requirement/test graph, adjacent-role audit and batched repairs |
| Rereading the whole project on every task | Searchable 195-lesson corpus and compact case handoff |
| Repeating checks or trusting stale results | Artifact, commit, environment and test-selection fingerprints with dependency-based reuse advice |
| Slow runner setup and duplicate compilation | Build-time hydration where permitted, safe caches, affected-component rebuilds, bounded jobs and measured remote validation |
| Confusing local success with acceptance | Separate local receipts, live gate results, Auto Review and manager acceptance |
| Uploading before a quality check was rehearsed | Mandatory local counterparts and evidence gate before every upload; missing, failed, unknown or stale results block |

## Tools

Python 3 standard library only. Commands below run from this plugin directory on `shipd-local`. They inspect metadata and delivered evidence; all source work and validation also stay on that designated builder. The Mac only orchestrates and inspects or transfers lightweight evidence.

```sh
python3 scripts/evidence_index.py query knowledge "reopen" --limit 6
python3 scripts/contract_check.py assets/contract.example.json
python3 scripts/test_result_gate.py --junit /path/to/evidence/combined.xml --inventory /path/to/evidence/discovery.json --events /path/to/evidence/combined.jsonl --event-classname ide_completion --exit-code 0 --expected pass --output /path/to/evidence/reconciliation.json
python3 scripts/partition_result_gate.py --inventory /path/to/evidence/complete-discovery.json --partitions /path/to/evidence/partitions.json --output /path/to/evidence/partition-reconciliation.json
python3 scripts/fastlane.py preflight /path/to/delivered-artifacts
python3 scripts/fastlane.py snapshot /path/to/delivered-artifacts --commit FULL_40_HEX_COMMIT --environment /path/to/environment.json --selection /path/to/exact-commands.txt --scope-tests /path/to/frozen-scope-test.patch --output /path/to/before.json
python3 scripts/fastlane.py compare /path/to/before.json /path/to/after.json
python3 scripts/fastlane.py budget /path/to/usage-tool-response.json
python3 scripts/quality_gate.py init --stage full --inputs /path/to/current-inputs.json --panel /path/to/panel-contract.json --output /path/to/evidence/local-quality.json
python3 scripts/quality_gate.py check /path/to/evidence/local-quality.json --artifacts /path/to/artifacts --commit FULL_40_HEX_COMMIT --environment /path/to/environment.json --selection /path/to/selection.txt --scope-tests /path/to/frozen-scope-test.patch
```

The [mandatory local quality workflow](skills/shipd-fastlane/references/local-quality-gate.md) supplies 20 counterparts: 12 apply before Scope upload, 18 before full-package upload, and all 20 after real rollouts for final review. Run the actual Forge validators and rubric reviews on `shipd-local`, attach hashed evidence, then require `LOCAL_EVIDENCE_GATE_PASS`. The metadata checker does not run candidate code or certify review truth. Private AI graders/similarity are approximations; live panel inventory and hosted results remain authoritative. No paid action is started by this plugin.

Use [execution integrity](skills/shipd-fastlane/references/execution-integrity.md) for independently discovered test inventories, JUnit reconciliation, behavioral failure classification, and measured changed-line coverage. The report gate rejects missing or duplicate selected tests, selected skips, incomplete event starts, inconsistent counters, harness errors and process/report disagreement. Require raw events as well as its status label; XML-only consistency remains provenance-unverified. The [partition gate](skills/shipd-fastlane/references/partition-result-gate.md) rechecks receipts and their source/binary hashes against complete discovery, resolves all exclusions and requires behavioral triage for expected failures. It does not certify assertion meaning, discovery completeness or the authenticity of supplied files.

The current Python gate/tool fixture suite passed **133/133** on `shipd-local`; the retained R2 receipt binds the tested source hashes. Earlier fixture failures and revisions remain in evidence. This is fixture validation, not production-run provenance or proof of hosted grader behavior. Documentation-only changes after that run do not imply a new execution result.

For test patch generation, use the [coverage workflow](skills/shipd-fastlane/references/test-coverage.md). The contract checker now enforces declared input/role cells, whole-scenario witnesses and boundary/error/compatibility/interaction reviews. `--stage scope` reports a reduced slice and deferred gaps; `--stage full` (default) rejects missing obligations. Existing contracts need the updated example schema. Contract checks validate declared coverage, not completeness or measured line/branch coverage. Fingerprints only identify whether a saved passing receipt may still apply; they never prove a check passed. Preflight is a limited static check. Unknown or malformed usage stops expensive work; the default checkpoint is 40%, reserving 10 percentage points below the 50% ceiling. An explicit task instruction can change the threshold or remove it with `--no-cap`; account service limits remain. Usage is account-wide and can lag; this tool is not a hard account quota.

For an explicitly requested full audit:

```sh
python3 scripts/evidence_index.py index /path/to/Shipd /path/to/audit-output
python3 scripts/evidence_index.py revisions /path/to/audit-output
python3 -m unittest discover -s tests -v
```

The revision catalog groups saved four-file sets by content and lists individual patches without treating copies as separate accepted iterations. ZIP inventories do not extract payloads.

## Included material and limits

Start with the [workflow](skills/shipd-fastlane/SKILL.md), [accepted patterns](skills/shipd-fastlane/references/accepted-patterns.md), [repair example](skills/shipd-fastlane/references/repair-case-study.md), and [provenance](skills/shipd-fastlane/references/provenance.md). Templates cover contracts, runtime environment, stage handoffs and metrics. Report local workflow completion, full compatibility evidence and platform upload readiness separately; missing hosted results remain unproven rather than being inferred from local success. The original Forge plugin is unchanged.

All nine accepted references now have live Accepted status in the September 13 header-confirmed dashboard receipt. Their accepted artifact byte identities remain null: current status does not bind any saved package to the accepted upload. The broader audit inventories 11,706 files and 42 cases, but it is not a semantic review of every source line, archived conversation or ZIP payload. The workflow's speed and acceptance gains still need prospective measurement. Detailed private workspace evidence remains in the local audit rather than this shareable package.
