#!/usr/bin/env python3
"""Validate Olympus artifacts, repository identity, and clean patch application."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


ARTIFACTS = ("problem.md", "test.patch", "solution.patch", "Dockerfile")
BANNED = re.compile(r"\b(?:challenge|quest|olympus|shipd|mars|datacurve)\b", re.IGNORECASE)
CODE_SUFFIXES = {".c", ".cc", ".cpp", ".cxx", ".go", ".h", ".hpp", ".java", ".js", ".jsx", ".py", ".rs", ".ts", ".tsx"}
REVIEW_ROWS = {
    "category_fit",
    "plagiarism_screen",
    "problem_test_quality",
    "description_necessity",
    "problem_test_alignment",
    "test_filename_collision",
    "docker_guidelines",
}


def run(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_lf(path: Path) -> None:
    data = path.read_bytes()
    if b"\r\n" in data or b"\r" in data:
        fail(f"artifact is not LF-only: {path.name}")


def changed_paths(patch: Path) -> list[str]:
    paths: list[str] = []
    for line in patch.read_text(encoding="utf-8").splitlines():
        match = re.match(r"diff --git a/(.+) b/(.+)$", line)
        if match:
            paths.append(match.group(2))
    return paths


def is_test_path(path: str) -> bool:
    lower = path.lower()
    name = Path(lower).name
    segments = Path(lower).parts
    return (
        path == "test.sh"
        or any(segment in {"test", "tests", "testing", "__tests__"} for segment in segments)
        or name.startswith("test_") or name.endswith("_test.go") or ".test." in name or ".spec." in name
        or name.endswith("test.java") or name.endswith("tests.java")
    )


def effective_added_loc(patch: Path) -> int:
    current_path: str | None = None
    count = 0
    generated = False
    for line in patch.read_text(encoding="utf-8").splitlines():
        match = re.match(r"diff --git a/(.+) b/(.+)$", line)
        if match:
            current_path = match.group(2)
            generated = False
            continue
        if current_path is None or is_test_path(current_path):
            continue
        if line.startswith("+") and not line.startswith("+++"):
            code = line[1:].strip()
            if "generated" in code.lower() and ("do not edit" in code.lower() or "codegen" in code.lower()):
                generated = True
            if not code or generated or code.startswith(("//", "#", "/*", "*", "*/", "<!--")):
                continue
            count += 1
    return count


def docker_instructions(text: str) -> list[str]:
    instructions: list[str] = []
    current = ""
    for raw in text.splitlines():
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        current = f"{current} {stripped}".strip()
        if current.endswith("\\"):
            current = current[:-1].rstrip()
            continue
        instructions.append(current)
        current = ""
    if current:
        instructions.append(current)
    return instructions


def validate_description(text: str, warnings: list[str], *, pre_scope: bool, allow_url: bool) -> int:
    words = re.findall(r"\b\w+(?:[-']\w+)*\b", text)
    if len(text.strip()) < 50:
        fail("problem.md must contain at least 50 characters")
    if len(words) > 1000:
        fail(f"description is {len(words)} words; re-check the live panel limit")
    if not 100 <= len(words) <= 200:
        warnings.append(f"description is {len(words)} words; target 100-200 (500 remains a nonblocking ceiling)")
    if 500 < len(words) <= 1000:
        warnings.append(f"description is {len(words)} words; strong warning above 500")
    for index, char in enumerate(text):
        if ord(char) > 127 or (ord(char) < 32 and char not in "\n\t"):
            fail(f"description contains non-ASCII/control character at index {index}: {char!r}")
    if re.search(r"https?://|www\.", text, re.IGNORECASE):
        if pre_scope and not allow_url:
            fail("description contains a URL that solver agents cannot fetch")
        warnings.append("description contains a URL; preserve only when URL handling is itself the contract")
    return len(words)


def validate_unified_diff(path: Path) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not any(line.startswith("diff --git a/") for line in lines):
        fail(f"{path.name} has no diff --git file header")
    if not any(line.startswith("--- ") for line in lines) or not any(line.startswith("+++ ") for line in lines):
        fail(f"{path.name} has incomplete unified-diff file headers")
    hunk_indexes = [index for index, line in enumerate(lines) if line.startswith("@@ ")]
    if not hunk_indexes:
        fail(f"{path.name} has no unified-diff hunk header")
    in_hunk = False
    for index, line in enumerate(lines, start=1):
        if line.startswith("diff --git "):
            in_hunk = False
        elif line.startswith("@@ "):
            in_hunk = True
        elif in_hunk and not line.startswith((" ", "+", "-", "\\")):
            fail(f"{path.name} has invalid hunk line {index}: {line[:120]!r}")


def validate_dockerfile(text: str, allowed_prefixes: list[str], warnings: list[str]) -> str:
    instructions = docker_instructions(text)
    from_lines = [line for line in instructions if line.upper().startswith("FROM ")]
    if not from_lines:
        fail("Dockerfile has no FROM instruction")
    base = from_lines[0].split()[1]
    base_name, separator, _digest = base.partition("@")
    if allowed_prefixes and not any(base_name.startswith(prefix) for prefix in allowed_prefixes):
        fail(f"Dockerfile base is outside the current allowed prefixes: {base}")
    if separator:
        fail(f"Dockerfile FROM must use the allowed :latest tag without an @sha256 digest: {base}")
    if not base_name.endswith(":latest"):
        fail(f"Dockerfile base must retain the required :latest tag: {base}")
    if not any(line.upper() == "WORKDIR /APP" for line in instructions):
        fail("Dockerfile must set WORKDIR /app")
    if not re.search(r'^CMD\s*\[\s*"/bin/bash"\s*\]\s*$', text, re.MULTILINE | re.IGNORECASE):
        fail('Dockerfile must end with CMD ["/bin/bash"]')
    test_pattern = re.compile(r"(?:^|\s)(?:pytest|go\s+test|cargo\s+test|npm\s+(?:run\s+)?test|mvn(?:\s+\S+)*\s+test|gradle(?:w)?\s+test|ctest|\./test\.sh)(?:\s|$)", re.IGNORECASE)
    for instruction in instructions:
        if instruction.upper().startswith("RUN ") and test_pattern.search(instruction):
            fail(f"Dockerfile runs tests during build: {instruction}")
    if not any(line.upper().startswith("COPY ") for line in instructions):
        fail("Dockerfile does not copy repository sources")
    if not any(re.match(r"USER\s+\S+", line, re.IGNORECASE) for line in instructions):
        warnings.append("Dockerfile has no explicit runtime USER; reproduce the evaluator's unprivileged user")
    return base


def load_json(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        fail(f"invalid {label} JSON at {path}: {error}")
    if not isinstance(value, dict):
        fail(f"{label} must be a JSON object")
    return value


def validate_compliance(path: Path) -> dict[str, Any]:
    report = load_json(path, "compliance")
    required = {
        "github_url", "resolved_commit", "stars", "primary_language", "language_supported",
        "license", "license_permissive", "commit_age_days", "checked_at", "evidence_urls",
    }
    missing = sorted(required - report.keys())
    if missing:
        fail(f"compliance report is missing fields: {missing}")
    if not re.fullmatch(r"https://github\.com/[^/]+/[^/]+/?", str(report["github_url"])):
        fail(f"repository is not a canonical GitHub URL: {report['github_url']}")
    if not re.fullmatch(r"[0-9a-fA-F]{40}", str(report["resolved_commit"])):
        fail("compliance resolved_commit is not a full Git commit hash")
    if int(report["stars"]) < 500:
        fail(f"repository has {report['stars']} stars; minimum is 500")
    if report["language_supported"] is not True:
        fail(f"unsupported primary language: {report['primary_language']}")
    if report["license_permissive"] is not True:
        fail(f"license is not confirmed permissive/currently allowed: {report['license']}")
    if int(report["commit_age_days"]) > 365:
        fail(f"pinned commit is {report['commit_age_days']} days old; maximum is 365")
    if not isinstance(report["evidence_urls"], list) or not report["evidence_urls"]:
        fail("compliance report must preserve at least one evidence URL")
    try:
        dt.datetime.fromisoformat(str(report["checked_at"]).replace("Z", "+00:00"))
    except ValueError:
        fail("compliance checked_at must be an ISO-8601 timestamp")
    return report


def validate_local_review(path: Path) -> dict[str, Any]:
    report = load_json(path, "local review")
    rows = report.get("rows")
    if not isinstance(rows, dict):
        fail("local review must contain a rows object")
    missing = sorted(REVIEW_ROWS - rows.keys())
    if missing:
        fail(f"local review is missing rows: {missing}")
    for name in sorted(REVIEW_ROWS):
        row = rows[name]
        if not isinstance(row, dict) or row.get("status") not in {"PASS", "WARN", "FAIL"}:
            fail(f"local review row {name} needs PASS|WARN|FAIL status")
        if not str(row.get("evidence", "")).strip():
            fail(f"local review row {name} needs cited evidence")
        if row["status"] == "FAIL":
            fail(f"local review row failed: {name}: {row['evidence']}")
        if row["status"] == "WARN" and not str(row.get("disposition", "")).strip():
            fail(f"local review warning lacks accepted disposition: {name}")
    return report


def validate_hardness_proof(path: Path, problem_hash: str, solution_hash: str) -> dict[str, Any]:
    report = load_json(path, "hardness proof")
    if report.get("verdict") != "PASS" or report.get("full_reference_complete") is not True:
        fail("hardness proof must PASS with full_reference_complete=true")
    loc = report.get("effective_production_loc")
    if not isinstance(loc, int) or isinstance(loc, bool) or loc <= 0:
        fail("hardness proof needs positive measured effective_production_loc")
    files = report.get("production_files")
    if not isinstance(files, int) or isinstance(files, bool) or files <= 0:
        fail("hardness proof needs positive measured production_files")
    if report.get("problem_sha256") != problem_hash or report.get("solution_sha256") != solution_hash:
        fail("hardness proof hashes do not match the frozen problem.md and solution.patch")
    evidence = report.get("executable_evidence")
    if not isinstance(evidence, list) or not evidence or not all(str(value).strip() for value in evidence):
        fail("hardness proof needs nonempty executable_evidence")
    wrong = report.get("wrong_architectures")
    if not isinstance(wrong, list) or len(wrong) < 3:
        fail("hardness proof needs at least three executed wrong architectures or mutations")
    for index, row in enumerate(wrong):
        if not isinstance(row, dict) or not str(row.get("implementation", "")).strip() or not str(row.get("evidence", "")).strip():
            fail(f"hardness wrong architecture {index} needs implementation and evidence")
        if row.get("result") not in {"KILLED", "WRONG"}:
            fail(f"hardness wrong architecture {index} must have result KILLED or WRONG")
    matrix = report.get("calibrator_matrix")
    if not isinstance(matrix, list) or len(matrix) < 7:
        fail("hardness proof must compare every accepted calibrator")
    calibrator_names = [str(row.get("calibrator", "")).strip() for row in matrix if isinstance(row, dict)]
    if len(calibrator_names) != len(matrix) or any(not name for name in calibrator_names):
        fail("every hardness calibrator row needs a calibrator name")
    normalized_calibrators = "\n".join(calibrator_names).lower()
    accepted_markers = {
        "Calyx inlining": "inlining",
        "Ladybug composite primary keys": "composite primary",
        "Lisette ownership-safe defaults": "ownership-safe defaults",
        "KiteSQL CREATE INDEX expressions": "create index",
        "DataFusion Parquet Map pruning": "parquet map",
        "DataFusion FFI overrides": "ffi",
        "Dora concrete trait-object patterns": "trait objects",
    }
    missing_calibrators = [name for name, marker in accepted_markers.items() if marker not in normalized_calibrators]
    if missing_calibrators:
        fail(f"hardness calibrator matrix is missing accepted tasks: {missing_calibrators}")
    closest = report.get("closest_analogues")
    if not isinstance(closest, list) or len(closest) != 2 or not all(str(value).strip() for value in closest):
        fail("hardness proof needs exactly two closest accepted analogues")
    if any(name not in calibrator_names for name in closest):
        fail("closest_analogues must exactly name rows in calibrator_matrix")
    scored_dimensions = (
        "semantic_coupling", "state_order_interaction", "repository_discovery",
        "wrong_architectures", "deterministic_feedback",
    )
    by_name = {str(row["calibrator"]): row for row in matrix}
    for name, row in by_name.items():
        if not str(row.get("evidence", "")).strip():
            fail(f"hardness calibrator {name} needs evidence")
        scores = row.get("scored_dimensions")
        if not isinstance(scores, dict) or set(scores) != set(scored_dimensions):
            fail(f"hardness calibrator {name} needs all five scored_dimensions")
        if any(value not in {"weaker", "match", "stronger"} for value in scores.values()):
            fail(f"hardness calibrator {name} has an invalid scored comparison")
    for name in closest:
        scores = by_name[name]["scored_dimensions"]
        non_weaker = sum(value in {"match", "stronger"} for value in scores.values())
        if non_weaker < 4 or scores["semantic_coupling"] == "weaker" or scores["repository_discovery"] == "weaker":
            fail(f"candidate is not comparable to closest accepted analogue: {name}")
    kill_sheet = report.get("kill_sheet")
    if not isinstance(kill_sheet, dict):
        fail("hardness proof needs a kill_sheet object")
    dimensions = ("semantic_coupling", "state_order_interaction", "repository_discovery", "wrong_architectures", "deterministic_feedback")
    scores = [kill_sheet.get(name) for name in dimensions]
    if any(not isinstance(score, int) or isinstance(score, bool) or score < 0 or score > 2 for score in scores):
        fail("hardness kill_sheet dimensions must be integer scores from 0 to 2")
    if sum(scores) < 8 or any(score == 0 for score in scores[:4]):
        fail("hardness kill_sheet must score at least 8/10 with no zero in the first four dimensions")
    return report


def validate_gate_map(path: Path, problem_hash: str, solution_hash: str) -> dict[str, Any]:
    report = load_json(path, "scope-gate map")
    if (
        report.get("full_scope_frozen") is not True
        or report.get("full_solution_complete") is not True
        or report.get("calibrator_verdict") != "PASS"
    ):
        fail("scope-gate map must freeze full scope and solution with calibrator_verdict PASS")
    if report.get("problem_sha256") != problem_hash or report.get("solution_sha256") != solution_hash:
        fail("scope-gate map hashes do not match the frozen problem.md and solution.patch")
    if report.get("requirements_complete") is not True:
        fail("scope-gate map must assert requirements_complete=true")
    if report.get("omitted_requirements") != []:
        fail("scope-gate map must contain omitted_requirements=[]")
    rows = report.get("requirements")
    if not isinstance(rows, list) or not rows:
        fail("scope-gate map needs at least one requirement row")
    subsystems: set[str] = set()
    barriers: set[str] = set()
    requirement_ids: set[str] = set()
    has_fail_to_pass = False
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            fail(f"scope-gate requirement {index} is not an object")
        for field in ("id", "requirement", "oracle", "evidence"):
            if not str(row.get(field, "")).strip():
                fail(f"scope-gate requirement {index} is missing {field}")
        requirement_id = str(row["id"])
        if requirement_id in requirement_ids:
            fail(f"scope-gate requirement ID is duplicated: {requirement_id}")
        requirement_ids.add(requirement_id)
        for field in ("production_paths", "subsystems", "semantic_barriers"):
            values = row.get(field)
            if not isinstance(values, list) or not values or not all(str(value).strip() for value in values):
                fail(f"scope-gate requirement {requirement_id} needs a nonempty {field} list")
        if row.get("solution_review_status") != "PASS":
            fail(f"scope-gate requirement {requirement_id} needs solution_review_status PASS")
        status = row.get("coverage_status")
        if status not in {"GATE_COVERED", "POST_GATE_TEST_EXPANSION"}:
            fail(f"scope-gate requirement {requirement_id} has invalid coverage_status")
        if status == "POST_GATE_TEST_EXPANSION":
            if not str(row.get("expansion_plan", "")).strip():
                fail(f"scope-gate requirement {requirement_id} needs a post-gate expansion_plan")
            continue
        for field in ("gate_scenario", "test_ids"):
            value = row.get(field)
            if field == "test_ids":
                valid = isinstance(value, list) and value and all(str(item).strip() for item in value)
            else:
                valid = bool(str(value or "").strip())
            if not valid:
                fail(f"scope-gate requirement {requirement_id} needs {field}")
        if row.get("execution_status") != "PASS":
            fail(f"scope-gate requirement {requirement_id} is unexecuted")
        transition = row.get("expected_transition")
        if transition not in {"FAIL_TO_PASS", "PASS_TO_PASS"}:
            fail(f"scope-gate requirement {requirement_id} needs FAIL_TO_PASS or PASS_TO_PASS expected_transition")
        if transition == "FAIL_TO_PASS":
            has_fail_to_pass = True
            if row.get("test_only_result") != "FAIL" or row.get("full_solution_result") != "PASS":
                fail(f"scope-gate requirement {requirement_id} lacks its executed FAIL_TO_PASS transition")
        elif row.get("test_only_result") != "PASS" or row.get("full_solution_result") != "PASS":
            fail(f"scope-gate compatibility requirement {requirement_id} lacks its executed PASS_TO_PASS transition")
        subsystems.update(str(value) for value in row["subsystems"])
        barriers.update(str(value) for value in row["semantic_barriers"])
    if not has_fail_to_pass:
        fail("scope-gate map has no executed missing-capability FAIL_TO_PASS row")
    if len(subsystems) < 3:
        fail(f"gate-covered rows reach only {len(subsystems)} named subsystems; required minimum is 3")
    if len(barriers) < 2:
        fail(f"gate-covered rows name only {len(barriers)} interacting semantic barriers; required minimum is 2")
    return report


def validate_python_install(
    checkout: Path,
    docker_text: str,
    description: str,
    primary_language: str | None = None,
) -> None:
    # A repository may keep a docs/tooling-only Python project at its root. When
    # pre-Scope compliance has already established another primary language, do
    # not impose Python packaging requirements on that repository's evaluator.
    if primary_language and primary_language.casefold() != "python":
        return
    python_project = any((checkout / name).exists() for name in ("pyproject.toml", "setup.py", "setup.cfg"))
    if not python_project:
        return
    editable = re.search(r"(?:pip3?|uv\s+pip)\s+install\s+[^\n]*\s(?:-e|--editable)(?:\s|=)", docker_text, re.IGNORECASE)
    noneditable = re.search(r"(?:pip3?|uv\s+pip)\s+install\s+(?:\.|[^\n]*--no-editable)|uv\s+sync\s+[^\n]*--no-editable", docker_text, re.IGNORECASE)
    documented = re.search(r"(?:python\s+-m\s+pytest|pytest|tox|nox|unittest)", description, re.IGNORECASE)
    if not editable and (noneditable or not re.search(r"(?:pip3?|uv\s+pip)\s+install|uv\s+sync", docker_text, re.IGNORECASE)) and not documented:
        fail("Python project is not installed editably; problem.md must document the repository-native test invocation")


def clone_at(repo: str, commit: str, destination: Path) -> None:
    result = run("git", "clone", "--no-hardlinks", repo, str(destination))
    if result.returncode:
        fail(f"git clone failed:\n{result.stdout}")
    result = run("git", "checkout", "--detach", commit, cwd=destination)
    if result.returncode:
        fail(f"exact commit checkout failed:\n{result.stdout}")
    root = run("git", "rev-parse", "--show-toplevel", cwd=destination)
    if root.returncode or Path(root.stdout.strip()).resolve() != destination.resolve():
        fail("checkout path is not the Git toplevel")
    head = run("git", "rev-parse", "HEAD", cwd=destination)
    if head.returncode or head.stdout.strip() != commit:
        fail("checkout HEAD does not equal the pinned commit")


def apply_patch(checkout: Path, patch: Path) -> None:
    result = run("git", "apply", "--check", str(patch), cwd=checkout)
    if result.returncode:
        fail(f"{patch.name} does not apply cleanly:\n{result.stdout}")
    result = run("git", "apply", str(patch), cwd=checkout)
    if result.returncode:
        fail(f"failed to apply {patch.name}:\n{result.stdout}")


def validate_test_script(checkout: Path) -> None:
    script = checkout / "test.sh"
    if not script.is_file():
        fail("test.patch does not create test.sh")
    if not script.stat().st_mode & 0o111:
        fail("test.sh is not executable")
    text = script.read_text(encoding="utf-8")
    for token in ("base", "new", "--output_path"):
        if token not in text:
            fail(f"test.sh does not expose required token: {token}")
    install = re.compile(r"\b(?:apt(?:-get)?\s+install|pip3?\s+install|npm\s+install|pnpm\s+install|yarn\s+install|go\s+get|cargo\s+install|mvn\s+dependency:get)\b", re.IGNORECASE)
    if install.search(text):
        fail("test.sh installs packages; dependencies belong in the image build")
    destructive = re.compile(r"\b(?:rm\s+-rf|mkfs(?:\.|\s)|dd\s+if=|shutdown|reboot|kill\s+-9\s+1|curl\s+[^|]*\|\s*(?:sh|bash)|wget\s+[^|]*\|\s*(?:sh|bash))\b", re.IGNORECASE)
    if destructive.search(text):
        fail("test.sh contains a destructive or remote-execution command")
    if re.search(r"--fail-?fast|\s-x(?:\s|$)|-failfast", text):
        fail("test.sh uses a fail-fast option")
    syntax = run("bash", "-n", str(script), cwd=checkout)
    if syntax.returncode:
        fail(f"test.sh fails bash syntax check:\n{syntax.stdout}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, help="Git repository path or URL")
    parser.add_argument("--commit", required=True)
    parser.add_argument("--artifacts", required=True, type=Path)
    parser.add_argument("--allowed-base-prefix", action="append", default=[])
    parser.add_argument("--pre-scope", action="store_true")
    parser.add_argument("--compliance-json", type=Path)
    parser.add_argument("--local-review-json", type=Path)
    parser.add_argument("--gate-map-json", type=Path)
    parser.add_argument("--hardness-proof-json", type=Path)
    parser.add_argument("--predicted-test-path", action="append", default=[])
    parser.add_argument("--allow-description-url", action="store_true")
    parser.add_argument("--min-solution-loc", type=int, default=0)
    parser.add_argument("--min-solution-files", type=int, default=0)
    parser.add_argument("--docker-build", action="store_true")
    parser.add_argument("--docker-tag", default="olympus-artifact-check")
    parser.add_argument("--json-output", type=Path)
    args = parser.parse_args()

    warnings: list[str] = []
    artifacts = args.artifacts.resolve()
    for name in ARTIFACTS:
        path = artifacts / name
        if not path.is_file() or path.stat().st_size == 0:
            fail(f"missing or empty artifact: {name}")
        require_lf(path)

    description = (artifacts / "problem.md").read_text(encoding="utf-8")
    description_words = validate_description(description, warnings, pre_scope=args.pre_scope, allow_url=args.allow_description_url)
    docker_text = (artifacts / "Dockerfile").read_text(encoding="utf-8")
    base = validate_dockerfile(docker_text, args.allowed_base_prefix, warnings)
    test_patch = artifacts / "test.patch"
    solution_patch = artifacts / "solution.patch"
    test_paths = changed_paths(test_patch)
    solution_paths = changed_paths(solution_patch)
    if not test_paths or not solution_paths:
        fail("both patches must contain file changes")
    validate_unified_diff(test_patch)
    validate_unified_diff(solution_patch)
    for patch in (test_patch, solution_patch):
        match = BANNED.search(patch.read_text(encoding="utf-8"))
        if match:
            fail(f"{patch.name} leaks banned platform marker: {match.group(0)}")
    suspicious_test_paths = [path for path in test_paths if Path(path).suffix.lower() in CODE_SUFFIXES and not is_test_path(path)]
    if suspicious_test_paths:
        fail(f"test.patch appears to modify production code: {suspicious_test_paths}")
    solution_tests = [path for path in solution_paths if is_test_path(path)]
    if solution_tests:
        fail(f"solution.patch modifies test paths: {solution_tests}")
    leaked_path = next((path for path in test_paths if BANNED.search(path)), None)
    if leaked_path:
        fail(f"test filename leaks a banned platform marker: {leaked_path}")
    predicted = {path.removeprefix("./") for path in args.predicted_test_path}
    collisions = sorted(predicted.intersection(path.removeprefix("./") for path in test_paths))
    if collisions:
        fail(f"hidden test paths collide with blind predicted defaults: {collisions}")

    compliance: dict[str, Any] | None = None
    local_review: dict[str, Any] | None = None
    gate_map: dict[str, Any] | None = None
    hardness_proof: dict[str, Any] | None = None
    if args.pre_scope:
        if not args.compliance_json or not args.local_review_json or not args.gate_map_json or not args.hardness_proof_json:
            fail("--pre-scope requires --compliance-json, --local-review-json, --gate-map-json, and --hardness-proof-json")
        if not predicted:
            fail("--pre-scope requires at least one blind --predicted-test-path")
        compliance = validate_compliance(args.compliance_json)
        if compliance["resolved_commit"].lower() != args.commit.lower():
            fail("compliance commit does not match --commit")
        local_review = validate_local_review(args.local_review_json)
        problem_hash = sha256(artifacts / "problem.md")
        solution_hash = sha256(artifacts / "solution.patch")
        gate_map = validate_gate_map(args.gate_map_json, problem_hash, solution_hash)
        hardness_proof = validate_hardness_proof(args.hardness_proof_json, problem_hash, solution_hash)
    estimated_loc = effective_added_loc(solution_patch)
    production_files = len([path for path in solution_paths if not is_test_path(path)])
    if hardness_proof and hardness_proof["effective_production_loc"] != estimated_loc:
        fail("hardness proof effective_production_loc does not match solution.patch")
    if hardness_proof and hardness_proof["production_files"] != production_files:
        fail("hardness proof production_files does not match solution.patch")
    if estimated_loc < args.min_solution_loc:
        fail(f"estimated effective added LOC is {estimated_loc}; required estimate is {args.min_solution_loc}")
    if production_files < args.min_solution_files:
        fail(f"estimated production files is {production_files}; required estimate is {args.min_solution_files}")

    with tempfile.TemporaryDirectory(prefix="olympus-validate-") as temporary:
        temp = Path(temporary)
        untouched = temp / "untouched"
        test_only = temp / "test-only"
        solution_only = temp / "solution-only"
        together = temp / "together"
        for checkout in (untouched, test_only, solution_only, together):
            clone_at(args.repo, args.commit, checkout)
            shutil.copy2(artifacts / "Dockerfile", checkout / "Dockerfile")
        primary_language = str(compliance["primary_language"]) if compliance else None
        validate_python_install(untouched, docker_text, description, primary_language)
        apply_patch(test_only, test_patch)
        validate_test_script(test_only)
        apply_patch(solution_only, solution_patch)
        apply_patch(together, test_patch)
        apply_patch(together, solution_patch)
        validate_test_script(together)
        for checkout in (test_only, solution_only, together):
            diff_check = run("git", "diff", "--check", args.commit, cwd=checkout)
            if diff_check.returncode:
                fail(f"applied state contains whitespace errors:\n{diff_check.stdout}")
        if args.docker_build:
            build = run("docker", "build", "-t", args.docker_tag, ".", cwd=untouched)
            if build.returncode:
                fail(f"Dockerfile does not build on untouched source plus the submitted Dockerfile:\n{build.stdout}")

    report: dict[str, Any] = {
        "status": "PASS", "repository": args.repo, "commit": args.commit, "base_image": base,
        "profile": "pre-scope" if args.pre_scope else "structural",
        "description_words": description_words,
        "artifact_hashes": {name: sha256(artifacts / name) for name in ARTIFACTS},
        "test_patch_files": len(test_paths), "solution_patch_files": len(solution_paths),
        "estimated_effective_added_production_loc": estimated_loc,
        "estimated_production_files": production_files, "warnings": warnings,
        "compliance": compliance,
        "local_review": local_review,
        "gate_map": gate_map,
        "hardness_proof": hardness_proof,
        "unproven": ["hosted plagiarism/similarity", "hosted AI checks", "Scope Gate", "four-state execution", "offline runtime", "flakiness", "later platform checks and rollouts"],
    }
    if args.json_output:
        args.json_output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("OK: structural, repository-root, LF, shell, and clean-application checks pass")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
