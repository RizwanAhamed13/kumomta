#!/usr/bin/env python3
"""Validate triad alignment, dimension coverage, mutations, and grader records."""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from pathlib import Path
from typing import Any


MUTATION_CLASSES = {
    "omission", "boundary", "boolean-cell", "routing-shape", "persistence-order",
    "conversion-serialization", "error-contract", "hardcoding", "agent-derived", "other",
}
MUTATION_STATUSES = {"killed", "survived", "invalid", "deferred"}
ALIGNMENT_STATUSES = {"covered", "out-of-scope", "open"}
ORACLE_KINDS = {
    "semantic", "prompt-token", "repo-token", "exact-representation", "category", "rejection",
}


def load_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ValueError(f"missing file: {path}") from None
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in {path}: {exc}") from None
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def require_fields(item: dict[str, Any], fields: tuple[str, ...], label: str, errors: list[str]) -> None:
    for field in fields:
        if field not in item or item[field] in (None, ""):
            errors.append(f"{label}: missing {field}")


def validate_requirements(path: Path, errors: list[str]) -> tuple[set[str], dict[str, set[str]]]:
    data = load_object(path)
    requirements = data.get("requirements")
    assertions = data.get("assertions")
    if not isinstance(requirements, list) or not isinstance(assertions, list):
        errors.append("requirements.json must contain requirements[] and assertions[]")
        return set(), {}
    requirement_ids: set[str] = set()
    assertion_ids: set[str] = set()
    requirement_assertions: dict[str, set[str]] = {}
    for index, requirement in enumerate(requirements):
        label = f"requirement[{index}]"
        if not isinstance(requirement, dict):
            errors.append(f"{label}: must be an object")
            continue
        require_fields(requirement, ("id", "public_path", "input_classes", "oracle", "grounding", "assertion_ids"), label, errors)
        identifier = requirement.get("id")
        if not isinstance(identifier, str):
            continue
        if identifier in requirement_ids:
            errors.append(f"duplicate requirement id: {identifier}")
        requirement_ids.add(identifier)
        requirement_assertions[identifier] = set(requirement.get("assertion_ids", []))
        if not requirement.get("input_classes"):
            errors.append(f"{label}: input_classes must not be empty")
    assertion_requirements: dict[str, set[str]] = {}
    for index, assertion in enumerate(assertions):
        label = f"assertion[{index}]"
        if not isinstance(assertion, dict):
            errors.append(f"{label}: must be an object")
            continue
        require_fields(assertion, ("id", "location", "requirement_ids", "grounding"), label, errors)
        identifier = assertion.get("id")
        if not isinstance(identifier, str):
            continue
        if identifier in assertion_ids:
            errors.append(f"duplicate assertion id: {identifier}")
        assertion_ids.add(identifier)
        assertion_requirements[identifier] = set(assertion.get("requirement_ids", []))
    for requirement_id, mapped_assertions in requirement_assertions.items():
        if not mapped_assertions:
            errors.append(f"requirement has no assertion: {requirement_id}")
        for assertion_id in mapped_assertions:
            if assertion_id not in assertion_requirements:
                errors.append(f"requirement {requirement_id} references unknown assertion {assertion_id}")
            elif requirement_id not in assertion_requirements[assertion_id]:
                errors.append(f"asymmetric map: {requirement_id} -> {assertion_id}")
    for assertion_id, mapped_requirements in assertion_requirements.items():
        if not mapped_requirements:
            errors.append(f"assertion has no requirement: {assertion_id}")
        for requirement_id in mapped_requirements:
            if requirement_id not in requirement_assertions:
                errors.append(f"assertion {assertion_id} references unknown requirement {requirement_id}")
            elif assertion_id not in requirement_assertions[requirement_id]:
                errors.append(f"asymmetric map: {assertion_id} -> {requirement_id}")
    return requirement_ids, assertion_requirements


def validate_independent_inventory(
    path: Path, requirement_ids: set[str], errors: list[str]
) -> dict[tuple[str, str], dict[str, tuple[str, ...]]]:
    data = load_object(path)
    if data.get("schema_version") != 2:
        errors.append("independent-inventory.json must use schema_version 2")
    items = data.get("requirements")
    if not isinstance(items, list):
        errors.append("independent-inventory.json must contain requirements[]")
        return {}
    expected: dict[tuple[str, str], dict[str, tuple[str, ...]]] = {}
    for index, item in enumerate(items):
        label = f"independent requirement[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{label}: must be an object")
            continue
        require_fields(item, ("requirement_id", "roles", "dimensions", "grounding"), label, errors)
        requirement_id = item.get("requirement_id")
        if requirement_id not in requirement_ids:
            errors.append(f"{label}: unknown requirement {requirement_id!r}")
            continue
        roles = item.get("roles")
        dimensions = item.get("dimensions")
        if not isinstance(roles, list) or not roles:
            errors.append(f"{label}: roles must be a non-empty array")
            continue
        if not isinstance(dimensions, list):
            errors.append(f"{label}: dimensions must be an array")
            continue
        parsed_dimensions: dict[str, tuple[str, ...]] = {}
        for dim_index, dimension in enumerate(dimensions):
            dim_label = f"{label} dimension[{dim_index}]"
            if not isinstance(dimension, dict):
                errors.append(f"{dim_label}: must be an object")
                continue
            require_fields(dimension, ("name", "values", "grounding"), dim_label, errors)
            name = dimension.get("name")
            values = dimension.get("values")
            if not isinstance(name, str) or not isinstance(values, list) or not values:
                errors.append(f"{dim_label}: name and non-empty values[] are required")
                continue
            normalized = tuple(str(value) for value in values)
            if len(set(normalized)) != len(normalized):
                errors.append(f"{dim_label}: duplicate dimension values")
            if name in parsed_dimensions:
                errors.append(f"{dim_label}: duplicate dimension name {name!r}")
            parsed_dimensions[name] = normalized
        for role in roles:
            if not isinstance(role, str) or not role:
                errors.append(f"{label}: every role must be a non-empty string")
                continue
            key = (requirement_id, role)
            if key in expected:
                errors.append(f"{label}: duplicate requirement/role {key}")
            expected[key] = parsed_dimensions
    return expected


def validate_alignment(
    path: Path,
    expected: dict[tuple[str, str], dict[str, tuple[str, ...]]],
    assertion_requirements: dict[str, set[str]],
    errors: list[str],
) -> None:
    data = load_object(path)
    if data.get("schema_version") != 3:
        errors.append("alignment-audit.json must use schema_version 3")
    rows = data.get("rows")
    if not isinstance(rows, list):
        errors.append("alignment-audit.json must contain rows[]")
        return
    seen: set[tuple[str, str]] = set()
    routing_needed = False
    numeric_domain_needed = False
    semantic_documentation_requirements: set[str] = set()
    for index, row in enumerate(rows):
        label = f"alignment row[{index}]"
        if not isinstance(row, dict):
            errors.append(f"{label}: must be an object")
            continue
        require_fields(
            row,
            (
                "requirement_id", "role", "input_classes", "assertion_ids", "solution_paths",
                "execution_paths", "evidence", "status", "oracle_contract", "dimensions", "cells",
            ),
            label,
            errors,
        )
        key = (row.get("requirement_id"), row.get("role"))
        if key in seen:
            errors.append(f"{label}: duplicate requirement/role {key}")
        seen.add(key)
        if key not in expected:
            errors.append(f"{label}: absent from independent inventory: {key}")
            continue
        if row.get("status") != "covered":
            errors.append(f"{label}: unresolved row status {row.get('status')!r}")
        execution_paths = row.get("execution_paths")
        if not isinstance(execution_paths, list) or not execution_paths:
            errors.append(f"{label}: execution_paths must be a non-empty array")
        else:
            for path_index, execution_path in enumerate(execution_paths):
                path_label = f"{label} execution_path[{path_index}]"
                if not isinstance(execution_path, dict):
                    errors.append(f"{path_label}: must be an object")
                    continue
                require_fields(
                    execution_path,
                    ("entry", "decision", "observable", "graph_evidence"),
                    path_label,
                    errors,
                )
        row_assertions = row.get("assertion_ids")
        if not isinstance(row_assertions, list) or not row_assertions:
            errors.append(f"{label}: assertion_ids must be a non-empty array")
            row_assertions = []
        for assertion_id in row_assertions:
            if assertion_id not in assertion_requirements:
                errors.append(f"{label}: unknown assertion {assertion_id}")
            elif row.get("requirement_id") not in assertion_requirements[assertion_id]:
                errors.append(f"{label}: assertion {assertion_id} maps to another requirement")

        contract = row.get("oracle_contract")
        if not isinstance(contract, dict):
            errors.append(f"{label}: oracle_contract must be an object")
        else:
            require_fields(
                contract,
                (
                    "kind", "grounding", "layout_independent", "presentation_constraints",
                    "conformant_alternatives",
                ),
                f"{label} oracle_contract",
                errors,
            )
            kind = contract.get("kind")
            if kind not in ORACLE_KINDS:
                errors.append(f"{label}: invalid oracle kind {kind!r}")
            constraints = contract.get("presentation_constraints")
            if not isinstance(constraints, list):
                errors.append(f"{label}: presentation_constraints must be an array")
            else:
                for constraint_index, constraint in enumerate(constraints):
                    if not isinstance(constraint, dict) or not constraint.get("mandated_by"):
                        errors.append(
                            f"{label}: presentation constraint[{constraint_index}] lacks mandated_by"
                        )
            if contract.get("layout_independent") is not True and kind != "exact-representation":
                errors.append(f"{label}: non-exact oracle must be layout_independent")
            alternatives = contract.get("conformant_alternatives")
            if (
                kind in {"semantic", "category", "rejection"}
                and (not isinstance(alternatives, list) or not alternatives)
            ):
                errors.append(f"{label}: semantic oracle must name a conformant alternative")

        dimensions = row.get("dimensions")
        actual_dimensions: dict[str, tuple[str, ...]] = {}
        if not isinstance(dimensions, list):
            errors.append(f"{label}: dimensions must be an array")
            dimensions = []
        for dim_index, dimension in enumerate(dimensions):
            if not isinstance(dimension, dict):
                errors.append(f"{label} dimension[{dim_index}]: must be an object")
                continue
            name = dimension.get("name")
            values = dimension.get("values")
            if isinstance(name, str) and isinstance(values, list):
                actual_dimensions[name] = tuple(str(value) for value in values)
        routing_needed = routing_needed or "target-source" in actual_dimensions
        grounding_text = " ".join(
            str(value)
            for value in (
                row.get("evidence", ""),
                (row.get("oracle_contract") or {}).get("grounding", "")
                if isinstance(row.get("oracle_contract"), dict)
                else "",
            )
        ).lower()
        numeric_domain_needed = numeric_domain_needed or any(
            marker in grounding_text
            for marker in ("json integer", "non-negative integer", "positive observation")
        ) or "observation-count" in actual_dimensions
        if (
            isinstance(row.get("oracle_contract"), dict)
            and row["oracle_contract"].get("kind") == "semantic"
            and any(str(solution_path).startswith("docs/") for solution_path in row.get("solution_paths", []))
        ):
            semantic_documentation_requirements.add(str(row.get("requirement_id")))
        if actual_dimensions != expected[key]:
            errors.append(
                f"{label}: dimensions differ from independent inventory: "
                f"{actual_dimensions!r} != {expected[key]!r}"
            )

        expected_cells: set[tuple[tuple[str, str], ...]]
        if actual_dimensions:
            names = list(actual_dimensions)
            expected_cells = {
                tuple(zip(names, values))
                for values in itertools.product(*(actual_dimensions[name] for name in names))
            }
        else:
            expected_cells = {()}
        actual_cells: set[tuple[tuple[str, str], ...]] = set()
        cells = row.get("cells")
        if not isinstance(cells, list):
            errors.append(f"{label}: cells must be an array")
            cells = []
        for cell_index, cell in enumerate(cells):
            cell_label = f"{label} cell[{cell_index}]"
            if not isinstance(cell, dict):
                errors.append(f"{cell_label}: must be an object")
                continue
            require_fields(cell, ("coordinates", "status", "grounding"), cell_label, errors)
            coordinates = cell.get("coordinates")
            if not isinstance(coordinates, dict):
                errors.append(f"{cell_label}: coordinates must be an object")
                continue
            coordinate_key = tuple((name, str(coordinates.get(name))) for name in actual_dimensions)
            if set(coordinates) != set(actual_dimensions):
                errors.append(f"{cell_label}: coordinates do not match dimensions")
            if coordinate_key in actual_cells:
                errors.append(f"{cell_label}: duplicate coordinates")
            actual_cells.add(coordinate_key)
            status = cell.get("status")
            if status not in ALIGNMENT_STATUSES:
                errors.append(f"{cell_label}: invalid status {status!r}")
            elif status == "open":
                errors.append(f"{cell_label}: open coverage cell")
            elif status == "covered":
                cell_assertions = cell.get("assertion_ids")
                if not isinstance(cell_assertions, list) or not cell_assertions or not cell.get("evidence"):
                    errors.append(f"{cell_label}: covered requires assertion_ids and evidence")
                else:
                    for assertion_id in cell_assertions:
                        if assertion_id not in row_assertions:
                            errors.append(
                                f"{cell_label}: assertion {assertion_id!r} is absent from its row"
                            )
            elif status == "out-of-scope" and not cell.get("out_of_scope_reason"):
                errors.append(f"{cell_label}: out-of-scope requires out_of_scope_reason")
        missing = expected_cells - actual_cells
        extra = actual_cells - expected_cells
        if missing:
            errors.append(f"{label}: missing Cartesian cells {sorted(missing)!r}")
        if extra:
            errors.append(f"{label}: unexpected Cartesian cells {sorted(extra)!r}")
    missing_rows = set(expected) - seen
    if missing_rows:
        errors.append(f"alignment rows missing independent roles: {sorted(missing_rows)!r}")

    routing_audits = data.get("routing_audits")
    if not isinstance(routing_audits, list):
        errors.append("alignment-audit.json must contain routing_audits[]")
        routing_audits = []
    if routing_needed and not routing_audits:
        errors.append("resolved-target dimensions require a routing audit")
    for audit_index, audit in enumerate(routing_audits):
        label = f"routing audit[{audit_index}]"
        if not isinstance(audit, dict):
            errors.append(f"{label}: must be an object")
            continue
        require_fields(
            audit,
            (
                "id", "status", "input_sources", "outcomes", "environment_dimensions",
                "entry", "decision", "observable", "graph_evidence", "cells", "evidence",
            ),
            label,
            errors,
        )
        if audit.get("status") != "covered":
            errors.append(f"{label}: unresolved status {audit.get('status')!r}")
        sources = tuple(str(value) for value in audit.get("input_sources", []))
        outcomes = tuple(str(value) for value in audit.get("outcomes", []))
        if set(sources) != {"explicit", "default"}:
            errors.append(f"{label}: input_sources must cover explicit and default")
        if set(outcomes) != {"accept", "reject"}:
            errors.append(f"{label}: outcomes must cover accept and reject")
        expected_route_cells = {(source, outcome) for source in sources for outcome in outcomes}
        actual_route_cells: set[tuple[str, str]] = set()
        for cell_index, cell in enumerate(audit.get("cells", [])):
            cell_label = f"{label} cell[{cell_index}]"
            if not isinstance(cell, dict):
                errors.append(f"{cell_label}: must be an object")
                continue
            coordinate = (str(cell.get("input_source")), str(cell.get("outcome")))
            actual_route_cells.add(coordinate)
            status = cell.get("status")
            if status == "covered" and not str(cell.get("evidence", "")).strip():
                errors.append(f"{cell_label}: covered route needs evidence")
            elif status == "out-of-scope" and not str(cell.get("reason", "")).strip():
                errors.append(f"{cell_label}: out-of-scope route needs a reason")
            elif status not in {"covered", "out-of-scope"}:
                errors.append(f"{cell_label}: invalid status {status!r}")
        if actual_route_cells != expected_route_cells:
            errors.append(
                f"{label}: routing cells differ from explicit/default x accept/reject: "
                f"{sorted(actual_route_cells)!r} != {sorted(expected_route_cells)!r}"
            )

    numeric_audits = data.get("numeric_domain_audits")
    if not isinstance(numeric_audits, list):
        errors.append("alignment-audit.json must contain numeric_domain_audits[]")
        numeric_audits = []
    if numeric_domain_needed and not numeric_audits:
        errors.append("public JSON-integer domains require a numeric-domain audit")
    for audit_index, audit in enumerate(numeric_audits):
        label = f"numeric domain audit[{audit_index}]"
        if not isinstance(audit, dict):
            errors.append(f"{label}: must be an object")
            continue
        require_fields(
            audit,
            (
                "id", "requirement_ids", "status", "public_domain", "host_word_widths",
                "representation_path", "representation_type", "boundary_cases",
                "assertion_ids", "evidence",
            ),
            label,
            errors,
        )
        if audit.get("status") != "covered":
            errors.append(f"{label}: unresolved status {audit.get('status')!r}")
        if set(audit.get("host_word_widths", [])) != {32, 64}:
            errors.append(f"{label}: must cover 32- and 64-bit hosts")
        if str(audit.get("representation_type", "")).lower() in {"usize", "isize"}:
            errors.append(f"{label}: public JSON integer domain cannot use pointer-width storage")
        boundaries = audit.get("boundary_cases", [])
        if not isinstance(boundaries, list) or not any(
            isinstance(value, int) and value > 2**32 - 1 for value in boundaries
        ):
            errors.append(f"{label}: must include a positive boundary above u32::MAX")

    variant_audits = data.get("oracle_variant_audits")
    if not isinstance(variant_audits, list):
        errors.append("alignment-audit.json must contain oracle_variant_audits[]")
        variant_audits = []
    covered_variant_requirements = {
        str(requirement_id)
        for audit in variant_audits
        if isinstance(audit, dict) and audit.get("status") == "covered"
        for requirement_id in audit.get("requirement_ids", [])
    }
    missing_variant_requirements = semantic_documentation_requirements - covered_variant_requirements
    if missing_variant_requirements:
        errors.append(
            "semantic documentation oracles lack conformant-variant execution: "
            f"{sorted(missing_variant_requirements)!r}"
        )
    for audit_index, audit in enumerate(variant_audits):
        label = f"oracle variant audit[{audit_index}]"
        if not isinstance(audit, dict):
            errors.append(f"{label}: must be an object")
            continue
        require_fields(
            audit,
            ("id", "requirement_ids", "status", "oracle", "fixtures", "evidence"),
            label,
            errors,
        )
        fixtures = audit.get("fixtures")
        if not isinstance(fixtures, list) or len(fixtures) < 2:
            errors.append(f"{label}: requires at least two conformant alternative fixtures")
            continue
        distinctions: set[str] = set()
        for fixture_index, fixture in enumerate(fixtures):
            fixture_label = f"{label} fixture[{fixture_index}]"
            if not isinstance(fixture, dict):
                errors.append(f"{fixture_label}: must be an object")
                continue
            require_fields(fixture, ("id", "path", "status", "distinction"), fixture_label, errors)
            distinction = str(fixture.get("distinction", "")).strip()
            distinctions.add(distinction)
            if fixture.get("status") != "passed":
                errors.append(f"{fixture_label}: oracle did not pass")
            fixture_path = path.parent / str(fixture.get("path", ""))
            if not fixture_path.is_file():
                errors.append(f"{fixture_label}: missing fixture {fixture_path}")
        if len(distinctions) < 2:
            errors.append(f"{label}: fixtures do not demonstrate distinct conformant forms")


def validate_mutations(path: Path, requirement_ids: set[str], errors: list[str]) -> None:
    data = load_object(path)
    mutations = data.get("mutations")
    if not isinstance(mutations, list):
        errors.append("mutation-inventory.json must contain mutations[]")
        return
    identifiers: set[str] = set()
    for index, mutation in enumerate(mutations):
        label = f"mutation[{index}]"
        if not isinstance(mutation, dict):
            errors.append(f"{label}: must be an object")
            continue
        require_fields(mutation, ("id", "requirement_ids", "class", "exact_change", "status", "evidence"), label, errors)
        identifier = mutation.get("id")
        if isinstance(identifier, str):
            if identifier in identifiers:
                errors.append(f"duplicate mutation id: {identifier}")
            identifiers.add(identifier)
        unknown = set(mutation.get("requirement_ids", [])) - requirement_ids
        if not mutation.get("requirement_ids"):
            errors.append(f"{label}: requirement_ids must not be empty")
        if not mutation.get("evidence"):
            errors.append(f"{label}: evidence must not be empty")
        if unknown:
            errors.append(f"{label}: unknown requirements {sorted(unknown)}")
        mutation_class = mutation.get("class")
        if mutation_class not in MUTATION_CLASSES:
            errors.append(f"{label}: invalid mutation class {mutation_class!r}")
        status = mutation.get("status")
        if status not in MUTATION_STATUSES:
            errors.append(f"{label}: invalid status {status!r}")
        if status in {"survived", "deferred"}:
            errors.append(f"{label}: unresolved mutation status {status}")
        if status == "killed":
            if mutation.get("reference_passed") is not True or mutation.get("mutant_failed") is not True:
                errors.append(f"{label}: killed requires reference_passed=true and mutant_failed=true")
        if status == "invalid" and not mutation.get("invalid_reason"):
            errors.append(f"{label}: invalid requires invalid_reason")


def validate_graders(directory: Path, artifact_set_id: str, errors: list[str]) -> None:
    files = sorted(directory.glob("*.json")) if directory.is_dir() else []
    if not files:
        errors.append(f"no grader JSON files found in {directory}")
        return
    for path in files:
        data = load_object(path)
        label = f"grader {path.name}"
        require_fields(data, ("grader", "prompt_version", "artifact_set_id", "started_at", "completed_at", "verdict", "findings", "raw_output"), label, errors)
        if data.get("artifact_set_id") != artifact_set_id:
            errors.append(f"{label}: stale artifact_set_id")
        raw_output = Path(str(data.get("raw_output", "")))
        if not raw_output.is_absolute():
            raw_output = path.parent / raw_output
        if not raw_output.is_file():
            errors.append(f"{label}: raw output does not exist: {raw_output}")
        findings = data.get("findings", [])
        if not isinstance(findings, list):
            errors.append(f"{label}: findings must be an array")
            continue
        seen: set[str] = set()
        for index, finding in enumerate(findings):
            finding_label = f"{label} finding[{index}]"
            if not isinstance(finding, dict):
                errors.append(f"{finding_label}: must be an object")
                continue
            require_fields(finding, ("id", "severity", "category", "status", "disposition"), finding_label, errors)
            identifier = finding.get("id")
            if isinstance(identifier, str):
                if identifier in seen:
                    errors.append(f"{label}: duplicate finding id {identifier}")
                seen.add(identifier)
            if finding.get("status") == "open" and finding.get("severity") in {"HIGH", "ERROR", "BLOCKER"}:
                errors.append(f"{finding_label}: blocking finding remains open")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--requirements", type=Path, required=True)
    parser.add_argument("--independent", type=Path, required=True)
    parser.add_argument("--alignment", type=Path, required=True)
    parser.add_argument("--mutations", type=Path, required=True)
    parser.add_argument("--grader-dir", type=Path, required=True)
    parser.add_argument("--artifact-set-id", required=True)
    args = parser.parse_args()
    errors: list[str] = []
    try:
        requirement_ids, assertion_requirements = validate_requirements(args.requirements, errors)
        expected = validate_independent_inventory(args.independent, requirement_ids, errors)
        validate_alignment(args.alignment, expected, assertion_requirements, errors)
        validate_mutations(args.mutations, requirement_ids, errors)
        validate_graders(args.grader_dir, args.artifact_set_id, errors)
    except ValueError as exc:
        errors.append(str(exc))
    print(f"evidence_validation={'PASS' if not errors else 'FAIL'}")
    for error in errors:
        print(f"ERROR: {error}")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
