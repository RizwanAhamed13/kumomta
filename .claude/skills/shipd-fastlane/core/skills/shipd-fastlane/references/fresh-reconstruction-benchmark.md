# Fresh reconstruction benchmark

Use this route when the user asks for a new implementation of an existing historical problem to measure the workflow. It is an offline benchmark, not a new live submission. Apply the Forge artifact-builder and offline-validator procedures relevant to local construction and validation; do not represent an unrun Scope Gate or other hosted lifecycle gate as satisfied.

## Establish the evidence boundary

Record the original problem hash, exact repository commit, validated denylist receipt, permitted inputs, exposure history and prohibited sources before source work. Read the original prompt, pinned source and generic workflow instructions. Do not read archived case patches, case-specific repair lessons, upstream solutions or historical evaluator payloads before the declared boundary. A coordinator may supply identity metadata without supplying implementation details; record that exposure.

Withholding named files does not certify blindness. Metadata, task descriptions, generic examples and prior conversational exposure can carry information. Describe what was actually available and read; avoid an unsupported “fully blind” claim.

Use `shipd-local` for all source work, builds, tests and plugin validation. Keep exact source hashes, compiler version, image identity and a preflight for each material phase. Follow [thermal-safety.md](thermal-safety.md) and the current shared compute-slot allocation. Honor the user's current usage policy and its stated duration without changing global settings.

## Build coverage before the implementation

1. Independently inventory the prompt's public input forms, semantic roles, errors, boundary cases, compatibility requirements and whole-scenario interactions. Create the requirement map before choosing implementation details. Use [test-coverage.md](test-coverage.md).
2. Inspect targeted pinned-source consumers and fixture conventions. Run the smallest real baseline/toolchain smoke. Apply the new test patch to the untouched base early; detect missing dependency features, unsupported APIs and fixture assumptions before an expensive image build.
3. Implement the complete stated behavior and meaningful feature tests plus adjacent regression tests. Keep feature discrimination and compatibility selections explicit: a compatibility case that already passes baseline is not a fail-to-pass witness.
4. Preserve every first test result before repairs. Count production, test/fixture, harness, environment and packaging revisions separately. Group confirmed related defects into one repair, then run the required affected validation. Do not overwrite a failed receipt with a later pass.

## Validate the package efficiently

Run every locally reproducible quality family relevant to the contract using the [local quality workflow](local-quality-gate.md): artifact/description alignment, test and solution quality, fairness, false-positive discrimination, image/runtime behavior, flakiness and the applicable review rubrics. Record exact commands or rubric evidence and each limitation. The historical catalog is a checklist of counterparts, not knowledge of private hosted implementations. Do not invent a panel capture or a private grader result to populate a local benchmark receipt.

Run a clean four-state matrix at the pinned commit. Discover canonical selected test IDs independently of JUnit, retain raw native test events, and reconcile actual process exits with [execution-integrity.md](execution-integrity.md). For split selections, use the [partition gate](partition-result-gate.md) with a complete independent inventory. Every excluded ID must resolve through execution in another reconciled partition with the same source and executable identity. Report missing services, unsupported suites and other unresolved exclusions explicitly; they prevent a claim of complete compatibility.

Measure changed executable-line coverage separately under existing, fresh feature and fresh adjacent tests, plus their union. Retain raw profiles, source hashes, covered/mapped counts, added lines without instrumentation and unsupported branch coverage. Do not replace missing measurements with a contract-map percentage.

Use prompt-grounded semantic mutants. A valid kill needs an executed assertion witness and behavioral triage; a compiler error, signal, setup crash or untriaged panic does not count. Restore exact source hashes, refresh build inputs and retain rebuild/binary evidence between mutants. Investigate meaningful survivors before freezing, while preserving the initial mutation result.

Reuse unchanged, correctly bound evidence. Keep dependency hydration in permitted image-build layers and rematerialize every component affected by runtime patches. A development-container pass is not a runnable delivery-image pass. Record dependency build, image export/unpack, runtime compilation, test execution, queue delay and thermal pause durations separately.

## Freeze, then evaluate the holdout

Freeze immutable first-complete problem, solution patch, test patch, Dockerfile, runner and requirement-map bytes after the agreed own matrix, coverage, mutation and runnable-image checks. A prior provisional hash freeze or first passing feature suite is a separate milestone. Write a hash manifest and verify the checksummed transfer before exposing an archived evaluator. If a required check is infeasible, preserve the exact blocker and label the package incomplete instead of claiming the first-complete boundary.

When auditing older runs, preserve the original snapshot label, timestamp and receipt even if it was called first-complete before validation finished. Record the later validation-completion receipt separately; do not relabel the historical bytes or manufacture a post-validation freeze. If an exact event receipt is absent, leave its time unknown. A retrospective results summary or file modification time does not establish when validation completed.

Record archive exposure separately from archive execution. An explicit first-read receipt can support an exact read time; a transfer, preflight, native-identity inspection or first outcome supports only its own event and any justified exposure bound. Keep each timestamp tied to its evidence source. A late archive-run timestamp must not be substituted for an earlier unknown first read.

Only then read the authorized archived test patch or native runner. Run it unchanged against the frozen first solution in a clean isolated pinned base. Preserve the first native outcome, including reporting failures. Reconcile unchanged raw evidence separately if reporting failed; do not rerun passing tests merely to erase that error. Never read a historical solution unless separately authorized.

A justified post-holdout repair becomes a new revision. Keep the original result, scope classification and frozen bytes. If an archived assertion is outside the original contract, preserve its native failure and provide a concrete prompt/source-grounded control; do not silently remove it or report the native suite as green.

## Report three distinct states

- **Workflow completion:** whether the agreed local reconstruction, validation, freeze and optional holdout work is complete, with any negotiated limits.
- **Compatibility coverage:** which independently discovered suites executed, whether all required exclusions reconciled, and what remains untested.
- **Platform upload readiness:** separate from local completion; current live-panel mapping, all applicable upload evidence and separately authorized hosted actions remain unproven until performed.

Use `NOT_RUN` for unexecuted hosted checks and `UNPROVEN` for unknown private behavior or missing evidence. No paid gate is required solely to complete this offline route. Preserve unknown historical accepted-artifact byte identity explicitly. Report first outcomes, revisions, elapsed phases, test/LOC counts, measured coverage and limitations through the metrics template and handoff.
