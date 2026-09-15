# Case plan and evidence templates

## One-page plan
- Case/repository/full commit:
- Original prompt or current description SHA-256:
- Current stage and authorized completion boundary:
- Explicit paid authorizations:
- Usage policy and override expiry:
- Required remote host/workdir/filesystem:
- Current thermal controls and resource slot:
- Feasibility decisions and unresolved blockers:
- Frozen artifacts and runner hashes:
- Next commands and independently discovered test selections:
- Acceptance criteria:
- Current invalidated evidence:

## Requirement row
| ID | Prompt/compatibility grounding | Input family | Semantic role | Producer → consumer | Expected observable result | Test IDs | Existing regression IDs | Plausible mutant | Status |
|---|---|---|---|---|---|---|---|---|---|

## Execution receipt
Record full commit; source/test/runner/selection hashes; toolchain and executable identity; image identity; workspace and mount; CPU quota/affinity; command; start/end UTC; raw log; independently discovered IDs; start/terminal event files; exit status; JUnit; reconciliation result. Separate setup failure from executed assertions.

## Mutation receipt
Record requirement; wrong behavior; mutated paths/diff hash; passing reference receipt; rebuilt executable hash; exact test command; actual assertion witness; valid kill/survived/invalid classification; equivalence explanation if applicable; restored source hash and passing reference check.

## Coverage receipt
| Selection | Instrumentation/source identity | Changed executable denominator | Covered | Missed | Unmapped | Non-counter lines | Warnings |
|---|---|---|---|---|---|---|---|

## Quality receipt
For each applicable catalog/live-panel family: local counterpart; STRUCTURAL/EXECUTED/REVIEWED/HOSTED status; raw evidence paths/hashes; dependent inputs; current result; limitations; staleness reason; next action. Unknown private results remain UNPROVEN.

## Final handoff
- Canonical package and hashes:
- Completed stage:
- Required evidence and actual result:
- Unproven or stale gates:
- Current paid authorization:
- Exact next action:
- Failed attempts retained:
- Paused workloads and host-control blockers:
- Task-only override restoration:
