#!/usr/bin/env python3
"""Initialize, checkpoint, validate, and project Olympus case state."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ARTIFACTS = ("problem.md", "test.patch", "solution.patch", "Dockerfile")
MODES = {"REVIEW", "LIVE"}
VERDICTS = {"PASS", "REJECT", "CARVE", "BLOCKED", "IN_PROGRESS"}
STAGES = ("0", "1", "2", "3", "4", "5", "5b", "5c", "6", "7", "8", "9", "10", "11", "11b", "12", "13", "14", "14a", "14b", "14c", "14d", "14e", "15", "15b", "16", "17")
DEPENDENCY_DEFAULTS = {
    "problem.md": {"scope", "description", "alignment", "fairness", "graders", "rollouts", "holistic", "auto-review"},
    "test.patch": {"patch", "discovery", "matrix", "flakiness", "offline", "mutation", "fairness", "graders", "replay", "verify-tests", "verify-solution", "rollouts", "holistic", "auto-review"},
    "solution.patch": {"patch", "solved-matrix", "regression", "format", "lint", "mutation", "solution-quality", "verify-solution", "replay", "holistic", "auto-review"},
    "Dockerfile": {"image", "environment", "offline", "environment-quality", "verify-tests", "verify-solution", "holistic", "auto-review"},
}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def state_root(workspace: Path) -> Path:
    return workspace.resolve() / ".olympus"


def case_dir(workspace: Path, case_id: str) -> Path:
    return state_root(workspace) / "cases" / case_id


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"missing state file: {path}")
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {path}: {exc}")


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def artifact_snapshot(artifact_dir: Path) -> dict[str, dict[str, Any]]:
    snapshot: dict[str, dict[str, Any]] = {}
    for name in ARTIFACTS:
        path = artifact_dir / name
        if path.is_file():
            snapshot[name] = {"path": str(path.resolve()), "sha256": sha256(path), "size": path.stat().st_size}
    return snapshot


def artifact_set_id(snapshot: dict[str, dict[str, Any]]) -> str | None:
    if set(snapshot) != set(ARTIFACTS):
        return None
    material = "\n".join(f"{name}:{snapshot[name]['sha256']}" for name in ARTIFACTS)
    return hashlib.sha256(material.encode("ascii")).hexdigest()


def git_value(repo: Path, *args: str) -> str | None:
    result = subprocess.run(
        ("git", "-C", str(repo), *args), check=False, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
    )
    return result.stdout.strip() if result.returncode == 0 else None


def repository_snapshot(repo_path: str | None, expected_commit: str) -> dict[str, Any]:
    if not repo_path:
        return {"root": None, "head": None, "clean": None, "root_matches": None}
    requested = Path(repo_path).resolve()
    root_text = git_value(requested, "rev-parse", "--show-toplevel")
    if root_text is None:
        return {"root": None, "head": None, "clean": None, "root_matches": False}
    root = Path(root_text).resolve()
    head = git_value(root, "rev-parse", "HEAD")
    status = git_value(root, "status", "--porcelain")
    return {
        "root": str(root),
        "head": head,
        "clean": status == "" if status is not None else None,
        "root_matches": root == requested,
        "commit_matches": head == expected_commit,
    }


def append_event(path: Path, event: dict[str, Any]) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, sort_keys=True) + "\n")


def render_state(case_path: Path, state: dict[str, Any], items: list[dict[str, Any]]) -> None:
    lines = [
        f"# Case state — {state['case_id']}", "",
        f"- Schema: `{state['schema_version']}`",
        f"- Mode: `{state['mode']}`",
        f"- Stage: `{state['stage']}`",
        f"- Verdict: `{state['verdict']}`",
        f"- Next legal stage: `{state['next_legal_stage']}`",
        f"- Repository: {state['repository']['url']}",
        f"- Exact commit: `{state['repository']['commit']}`",
        f"- Repository root: `{state['repository'].get('root')}`",
        f"- Repository clean: `{state['repository'].get('clean')}`",
        f"- Artifact directory: `{state['artifact_dir']}`",
        f"- Artifact set: `{state.get('artifact_set_id')}`",
        f"- Token budget: `{state.get('budget', {}).get('spent', 0)}` spent / `{state.get('budget', {}).get('authorized')}` authorized",
        f"- Blocking open items: `{sum(1 for item in items if item.get('status') == 'open' and item.get('blocking', True))}`",
        f"- Updated: `{state['updated_at']}`", "", "## Artifacts", "",
    ]
    for name in ARTIFACTS:
        entry = state.get("artifacts", {}).get(name)
        lines.append(f"- `{name}`: `{entry['sha256']}`" if entry else f"- `{name}`: MISSING")
    lines.extend(["", "## Current proofs", ""])
    current = state.get("proofs", {}).get("current", {})
    lines.extend(f"- `{name}` — {record.get('evidence', 'no evidence path')}" for name, record in sorted(current.items()))
    if not current:
        lines.append("- none")
    lines.extend(["", "## Stale proofs", ""])
    stale = state.get("proofs", {}).get("stale", {})
    lines.extend(f"- `{name}` — {record.get('stale_reason', 'artifact drift')}" for name, record in sorted(stale.items()))
    if not stale:
        lines.append("- none")
    lines.extend(["", "## Open items", ""])
    open_items = [item for item in items if item.get("status") == "open"]
    lines.extend(f"- `{item['id']}` — {item['summary']}" for item in open_items)
    if not open_items:
        lines.append("- none")
    lines.append("")
    (case_path / "state.md").write_text("\n".join(lines), encoding="utf-8")


def load_case(args: argparse.Namespace) -> tuple[Path, dict[str, Any], list[dict[str, Any]]]:
    path = case_dir(args.workspace, args.case)
    state = read_json(path / "case.json")
    items = read_json(path / "open-items.json")
    if not isinstance(items, list):
        fail("open-items.json must contain an array")
    return path, state, items


def command_init(args: argparse.Namespace) -> int:
    path = case_dir(args.workspace, args.case)
    if (path / "case.json").exists():
        fail(f"case already exists: {args.case}")
    (path / "artifacts").mkdir(parents=True, exist_ok=True)
    (path / "evidence").mkdir(exist_ok=True)
    (path / "rollouts").mkdir(exist_ok=True)
    artifact_dir = Path(args.artifact_dir).resolve() if args.artifact_dir else path / "artifacts"
    snapshot = artifact_snapshot(artifact_dir)
    repo = repository_snapshot(args.repo_path, args.commit)
    repo.update({"url": args.repository, "commit": args.commit})
    timestamp = now()
    state = {
        "schema_version": 2,
        "case_id": args.case,
        "mode": "REVIEW",
        "stage": "0",
        "verdict": "IN_PROGRESS",
        "next_legal_stage": "1",
        "repository": repo,
        "artifact_dir": str(artifact_dir),
        "artifacts": snapshot,
        "artifact_set_id": artifact_set_id(snapshot),
        "proofs": {"current": {}, "stale": {}},
        "requirement_map": None,
        "live_panel_snapshot": None,
        "budget": {"authorized": None, "spent": 0.0, "entries": []},
        "last_blocker": None,
        "created_at": timestamp,
        "updated_at": timestamp,
    }
    write_json(path / "case.json", state)
    write_json(path / "open-items.json", [])
    append_event(path / "events.jsonl", {"at": timestamp, "type": "initialized", "artifact_set_id": state["artifact_set_id"]})
    root = state_root(args.workspace)
    root.mkdir(parents=True, exist_ok=True)
    (root / "active-case").write_text(args.case + "\n", encoding="utf-8")
    (root / "portfolio.md").touch(exist_ok=True)
    render_state(path, state, [])
    print(f"initialized {args.case} at {path}")
    return 0


def command_checkpoint(args: argparse.Namespace) -> int:
    path, state, items = load_case(args)
    if args.mode not in MODES or args.verdict not in VERDICTS:
        fail("invalid mode or verdict")
    artifact_dir = Path(args.artifact_dir or state["artifact_dir"]).resolve()
    old = state.get("artifacts", {})
    new = artifact_snapshot(artifact_dir)
    changed = {name for name in ARTIFACTS if old.get(name, {}).get("sha256") != new.get(name, {}).get("sha256")}
    current = state.setdefault("proofs", {}).setdefault("current", {})
    stale = state["proofs"].setdefault("stale", {})
    for name, record in list(current.items()):
        dependencies = set(record.get("depends_on", ARTIFACTS))
        if dependencies & changed:
            record["stale_reason"] = "artifact changed: " + ", ".join(sorted(dependencies & changed))
            stale[name] = record
            del current[name]
    state.update({
        "mode": args.mode,
        "stage": args.stage,
        "verdict": args.verdict,
        "next_legal_stage": args.next_stage,
        "artifact_dir": str(artifact_dir),
        "artifacts": new,
        "artifact_set_id": artifact_set_id(new),
        "updated_at": now(),
    })
    if args.repo_path:
        repo = repository_snapshot(args.repo_path, state["repository"]["commit"])
        state["repository"].update(repo)
    if args.last_blocker is not None:
        state["last_blocker"] = args.last_blocker or None
    if args.panel_snapshot is not None:
        state["live_panel_snapshot"] = args.panel_snapshot or None
    if args.requirement_map is not None:
        state["requirement_map"] = str(Path(args.requirement_map).resolve()) if args.requirement_map else None
    transition_errors = stage_guard_errors(state, items, args.stage)
    if transition_errors:
        fail("illegal stage checkpoint: " + "; ".join(transition_errors))
    write_json(path / "case.json", state)
    append_event(path / "events.jsonl", {
        "at": state["updated_at"], "type": "checkpoint", "stage": args.stage,
        "mode": args.mode, "verdict": args.verdict, "artifact_set_id": state["artifact_set_id"],
        "changed_artifacts": sorted(changed),
    })
    render_state(path, state, items)
    print(f"checkpointed {args.case}; changed={','.join(sorted(changed)) or 'none'}")
    return 0


def command_record_proof(args: argparse.Namespace) -> int:
    path, state, items = load_case(args)
    depends = args.depends_on or list(ARTIFACTS)
    unknown = set(depends) - set(ARTIFACTS)
    if unknown:
        fail(f"unknown artifact dependencies: {sorted(unknown)}")
    record = {
        "name": args.name, "command": args.command, "exit_code": args.exit_code,
        "evidence": args.evidence, "environment": args.environment,
        "depends_on": depends, "artifact_set_id": state.get("artifact_set_id"), "recorded_at": now(),
    }
    state.setdefault("proofs", {}).setdefault("current", {})[args.name] = record
    state["proofs"].setdefault("stale", {}).pop(args.name, None)
    state["updated_at"] = now()
    write_json(path / "case.json", state)
    append_event(path / "events.jsonl", {"at": state["updated_at"], "type": "proof", **record})
    render_state(path, state, items)
    print(f"recorded proof {args.name}")
    return 0


def command_record_scope_override(args: argparse.Namespace) -> int:
    path, state, items = load_case(args)
    if state.get("mode") != "REVIEW":
        fail("scope-gate override must be recorded in REVIEW mode")
    if state.get("stage") not in {"5b", "5c"}:
        fail("scope-gate override may be recorded only after stage 5b and before stage 6")
    instruction = args.user_instruction.strip()
    if not instruction:
        fail("scope-gate override requires the explicit user instruction")
    state_errors = validate_state(state, items, require_artifacts=True, require_clear=False, for_stage="5c")
    if state_errors:
        fail("cannot record scope-gate override: " + "; ".join(state_errors))
    record = {
        "name": "scope-gate-override",
        "authorization_kind": "explicit-user-scope-gate-override",
        "user_instruction": instruction,
        "evidence": args.evidence,
        "environment": "user-authorized workflow bypass; Scope Gate not run",
        "depends_on": ["problem.md", "solution.patch"],
        "artifact_set_id": state.get("artifact_set_id"),
        "recorded_at": now(),
    }
    state.setdefault("proofs", {}).setdefault("current", {})[record["name"]] = record
    state["proofs"].setdefault("stale", {}).pop(record["name"], None)
    state["updated_at"] = now()
    write_json(path / "case.json", state)
    append_event(path / "events.jsonl", {"at": state["updated_at"], "type": "scope-gate-override", **record})
    render_state(path, state, items)
    print("recorded explicit scope-gate override; Scope Gate remains NOT RUN")
    return 0


def command_item(args: argparse.Namespace) -> int:
    path, state, items = load_case(args)
    existing = next((item for item in items if item.get("id") == args.id), None)
    timestamp = now()
    if args.action == "add":
        if existing and existing.get("status") == "open":
            fail(f"open item already exists: {args.id}")
        item = {"id": args.id, "summary": args.summary, "blocking": not args.advisory, "status": "open", "opened_at": timestamp}
        if existing:
            items[items.index(existing)] = item
        else:
            items.append(item)
    else:
        if not existing or existing.get("status") != "open":
            fail(f"open item not found: {args.id}")
        existing.update({"status": "closed", "closed_at": timestamp, "resolution": args.resolution})
    write_json(path / "open-items.json", items)
    append_event(path / "events.jsonl", {"at": timestamp, "type": f"item-{args.action}", "id": args.id})
    render_state(path, state, items)
    print(f"{args.action} item {args.id}")
    return 0


def command_budget(args: argparse.Namespace) -> int:
    path, state, items = load_case(args)
    budget = state.setdefault("budget", {"authorized": None, "spent": 0.0, "entries": []})
    timestamp = now()
    if args.action == "set":
        if args.authorized is None or args.authorized < 0:
            fail("budget set requires a nonnegative --authorized value")
        if args.authorized < float(budget.get("spent", 0.0)):
            fail("authorized budget cannot be below recorded spend")
        budget["authorized"] = args.authorized
        event = {"at": timestamp, "type": "budget-set", "authorized": args.authorized, "panel_snapshot": args.panel_snapshot}
    else:
        if args.cost is None or args.cost < 0 or not args.name or not args.result_id:
            fail("budget spend requires nonnegative --cost, --name, and --result-id")
        authorized = budget.get("authorized")
        projected = float(budget.get("spent", 0.0)) + args.cost
        if authorized is None:
            fail("record an authorized budget before spend")
        if projected > float(authorized) + 1e-9:
            fail(f"spend would exceed authorized budget: {projected} > {authorized}")
        entry = {
            "at": timestamp, "name": args.name, "cost": args.cost,
            "result_id": args.result_id, "panel_snapshot": args.panel_snapshot,
            "artifact_set_id": state.get("artifact_set_id"),
        }
        budget.setdefault("entries", []).append(entry)
        budget["spent"] = projected
        event = {"type": "budget-spend", **entry}
    state["updated_at"] = timestamp
    write_json(path / "case.json", state)
    append_event(path / "events.jsonl", event)
    render_state(path, state, items)
    print(f"budget {args.action} recorded")
    return 0


def stage_guard_errors(state: dict[str, Any], items: list[dict[str, Any]], target_stage: str | None) -> list[str]:
    if target_stage is None:
        return []
    errors: list[str] = []
    artifacts = state.get("artifacts", {})
    current_proofs = state.get("proofs", {}).get("current", {})
    if target_stage in STAGES[STAGES.index("5b"):]:
        if set(artifacts) != set(ARTIFACTS) or not state.get("artifact_set_id"):
            errors.append(f"stage {target_stage} requires all four hashed artifacts")
        for proof_name in ("full-reference", "hardness-proof"):
            proof = current_proofs.get(proof_name)
            dependencies = set(proof.get("depends_on", [])) if proof else set()
            if (
                not proof
                or proof.get("exit_code") != 0
                or dependencies != {"problem.md", "solution.patch"}
            ):
                errors.append(
                    f"stage {target_stage} requires current {proof_name} proof "
                    "depending only on problem.md and solution.patch"
                )
    if target_stage == "5c":
        prechecks = current_proofs.get("scope-gate-prechecks")
        if not prechecks or prechecks.get("exit_code") != 0:
            errors.append("stage 5c requires current scope-gate-prechecks proof")
    if target_stage == "6":
        scope = current_proofs.get("scope-gate")
        override = current_proofs.get("scope-gate-override")
        gate_passed = bool(
            scope
            and scope.get("exit_code") == 0
            and set(scope.get("depends_on", [])) == {"problem.md", "solution.patch"}
        )
        explicitly_overridden = bool(
            override
            and override.get("authorization_kind") == "explicit-user-scope-gate-override"
            and override.get("user_instruction")
            and set(override.get("depends_on", [])) == {"problem.md", "solution.patch"}
        )
        if not gate_passed and not explicitly_overridden:
            errors.append(f"stage {target_stage} requires a current scope-gate PASS or non-stale explicit user override")
    elif target_stage in STAGES[STAGES.index("7"):]:
        scope = current_proofs.get("scope-gate")
        override = current_proofs.get("scope-gate-override")
        gate_passed = bool(
            scope
            and scope.get("exit_code") == 0
            and set(scope.get("depends_on", [])) == {"problem.md", "solution.patch"}
        )
        explicitly_overridden = bool(
            override
            and override.get("authorization_kind") == "explicit-user-scope-gate-override"
            and override.get("user_instruction")
            and set(override.get("depends_on", [])) == {"problem.md", "solution.patch"}
        )
        if not gate_passed and not explicitly_overridden:
            errors.append(f"stage {target_stage} requires a non-stale scope-gate PASS or explicit user override")
    if target_stage == "17":
        for proof_name in ("duplicate-final", "rollout-gates", "auto-review"):
            proof = current_proofs.get(proof_name)
            if not proof or proof.get("exit_code") != 0 or proof.get("artifact_set_id") != state.get("artifact_set_id"):
                errors.append(f"stage 17 requires current proof: {proof_name}")
        blocking = [item for item in items if item.get("status") == "open" and item.get("blocking", True)]
        if blocking:
            errors.append("stage 17 requires zero blocking open items")
    if target_stage in {"15", "15b", "17"}:
        for proof_name in ("local-validation", "requirement-map", "mutation-inventory", "grader-loop"):
            proof = current_proofs.get(proof_name)
            if not proof or proof.get("exit_code") != 0:
                errors.append(f"stage {target_stage} requires current proof: {proof_name}")
        requirement_map = state.get("requirement_map")
        if not requirement_map or not Path(requirement_map).is_file():
            errors.append(f"stage {target_stage} requires an existing requirement-map file")
        blocking = [item for item in items if item.get("status") == "open" and item.get("blocking", True)]
        if blocking:
            errors.append(f"stage {target_stage} requires zero blocking open items")
    return errors


def validate_state(state: dict[str, Any], items: list[dict[str, Any]], require_artifacts: bool, require_clear: bool, for_stage: str | None) -> list[str]:
    errors: list[str] = []
    for key in ("schema_version", "case_id", "mode", "stage", "verdict", "next_legal_stage", "repository", "artifact_dir", "proofs"):
        if key not in state:
            errors.append(f"missing key: {key}")
    if state.get("mode") not in MODES:
        errors.append("mode must be REVIEW or LIVE")
    if state.get("verdict") not in VERDICTS:
        errors.append("invalid verdict")
    repo = state.get("repository", {})
    if not repo.get("url") or not repo.get("commit"):
        errors.append("repository URL and exact commit are required")
    if repo.get("root") and repo.get("root_matches") is not True:
        errors.append("recorded repository path is not the Git toplevel")
    if repo.get("head") and repo.get("commit_matches") is not True:
        errors.append("repository HEAD does not match pinned commit")
    artifact_dir = Path(state.get("artifact_dir", "."))
    current = artifact_snapshot(artifact_dir) if artifact_dir.is_dir() else {}
    if current != state.get("artifacts", {}):
        errors.append("artifact hashes drifted since last checkpoint")
    if require_artifacts and set(current) != set(ARTIFACTS):
        errors.append("all four canonical artifacts are required")
    blocking = [item for item in items if item.get("status") == "open" and item.get("blocking", True)]
    if require_clear and blocking:
        errors.append(f"blocking open items remain: {[item.get('id') for item in blocking]}")
    errors.extend(stage_guard_errors(state, items, for_stage))
    return errors


def command_validate(args: argparse.Namespace) -> int:
    path, state, items = load_case(args)
    errors = validate_state(state, items, args.require_artifacts, args.require_no_open_items, args.for_stage)
    render_state(path, state, items)
    if args.json:
        print(json.dumps({"case": args.case, "ok": not errors, "errors": errors}, indent=2))
    else:
        print(f"case={args.case} status={'PASS' if not errors else 'FAIL'}")
        for error in errors:
            print(f"ERROR: {error}")
    return 0 if not errors else 1


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    sub = result.add_subparsers(dest="subcommand", required=True)

    init = sub.add_parser("init")
    init.add_argument("--workspace", type=Path, required=True)
    init.add_argument("--case", required=True)
    init.add_argument("--repository", required=True)
    init.add_argument("--commit", required=True)
    init.add_argument("--repo-path")
    init.add_argument("--artifact-dir")
    init.set_defaults(func=command_init)

    checkpoint = sub.add_parser("checkpoint")
    checkpoint.add_argument("--workspace", type=Path, required=True)
    checkpoint.add_argument("--case", required=True)
    checkpoint.add_argument("--mode", choices=sorted(MODES), required=True)
    checkpoint.add_argument("--stage", choices=STAGES, required=True)
    checkpoint.add_argument("--verdict", choices=sorted(VERDICTS), required=True)
    checkpoint.add_argument("--next-stage", required=True)
    checkpoint.add_argument("--artifact-dir")
    checkpoint.add_argument("--repo-path")
    checkpoint.add_argument("--last-blocker")
    checkpoint.add_argument("--panel-snapshot")
    checkpoint.add_argument("--requirement-map")
    checkpoint.set_defaults(func=command_checkpoint)

    proof = sub.add_parser("record-proof")
    proof.add_argument("--workspace", type=Path, required=True)
    proof.add_argument("--case", required=True)
    proof.add_argument("--name", required=True)
    proof.add_argument("--command", required=True)
    proof.add_argument("--exit-code", type=int, required=True)
    proof.add_argument("--evidence", required=True)
    proof.add_argument("--environment", required=True)
    proof.add_argument("--depends-on", action="append", choices=ARTIFACTS)
    proof.set_defaults(func=command_record_proof)

    override = sub.add_parser("record-scope-override")
    override.add_argument("--workspace", type=Path, required=True)
    override.add_argument("--case", required=True)
    override.add_argument("--user-instruction", required=True)
    override.add_argument("--evidence", required=True)
    override.set_defaults(func=command_record_scope_override)

    item = sub.add_parser("item")
    item.add_argument("--workspace", type=Path, required=True)
    item.add_argument("--case", required=True)
    item.add_argument("action", choices=("add", "close"))
    item.add_argument("--id", required=True)
    item.add_argument("--summary")
    item.add_argument("--advisory", action="store_true")
    item.add_argument("--resolution")
    item.set_defaults(func=command_item)

    budget = sub.add_parser("budget")
    budget.add_argument("--workspace", type=Path, required=True)
    budget.add_argument("--case", required=True)
    budget.add_argument("action", choices=("set", "spend"))
    budget.add_argument("--authorized", type=float)
    budget.add_argument("--cost", type=float)
    budget.add_argument("--name")
    budget.add_argument("--result-id")
    budget.add_argument("--panel-snapshot")
    budget.set_defaults(func=command_budget)

    validate = sub.add_parser("validate")
    validate.add_argument("--workspace", type=Path, required=True)
    validate.add_argument("--case", required=True)
    validate.add_argument("--require-artifacts", action="store_true")
    validate.add_argument("--require-no-open-items", action="store_true")
    validate.add_argument("--for-stage", choices=STAGES)
    validate.add_argument("--json", action="store_true")
    validate.set_defaults(func=command_validate)
    return result


def main() -> int:
    args = parser().parse_args()
    if args.subcommand == "item":
        if args.action == "add" and not args.summary:
            fail("item add requires --summary")
        if args.action == "close" and not args.resolution:
            fail("item close requires --resolution")
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
