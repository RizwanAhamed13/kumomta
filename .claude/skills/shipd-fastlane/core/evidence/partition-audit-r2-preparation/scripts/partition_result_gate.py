#!/usr/bin/env python3
"""Reconcile split test runs against one independently discovered complete inventory.

CLI: partition_result_gate.py --inventory complete.json --partitions manifest.json
                             [--output receipt.json]

All paths in the partition manifest are relative to that manifest. Each partition:
  {"id": "base", "expected": "pass", "receipt": "base/gate.json",
   "receipt_sha256": "...", "junit": "base/junit.xml",
   "inventory": "base/inventory.json", "events": "base/events.jsonl",
   "identity": {"source_manifest": "source.json", "source_sha256": "...",
                "source_root": "../checkout", "binary": "../test-executable",
                "binary_sha256": "..."}}
source.json is {"files": {"relative/source.rs": "sha256", ...}}. Its exact bytes
identify the declared source snapshot; every listed source file and executable is
hashed again. The complete inventory is {"tests": ["classname::name", ...]} and
must have no exclusions.

An expected-fail partition also needs "triage" and "triage_sha256". The triage
file is {"raw_events_sha256": "...", "failures": [
  {"id": "classname::name", "classification": "behavioral",
   "grounding": "Prompt requirement", "diagnosis": "Observed assertion mismatch"}
]}. Every actual failing test must appear exactly once.

This checks consistency, not authenticity or completeness of declared source
snapshots, inventory discovery, process exits, or production execution.
"""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import sys
import xml.etree.ElementTree as ET

from test_result_gate import check as check_partition

LIMITATION = (
    "Reconciles supplied evidence, not actual production provenance. Source manifests "
    "must independently enumerate the complete relevant source snapshot, and the complete "
    "test inventory must come from real discovery. Hashes and raw-event consistency do "
    "not authenticate execution, process exits, or the truth of behavioral triage. "
    "This does not measure coverage or establish private Shipd checks."
)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON key: " + key)
        result[key] = value
    return result


def read_json(path):
    return json.loads(Path(path).read_text(), object_pairs_hook=_unique_object)


def nonempty(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(label + " must be a nonempty string.")
    return value


def canonical_ids(values, label, allow_empty=False):
    if not isinstance(values, list) or (not values and not allow_empty):
        raise ValueError(label + " must be a nonempty list.")
    for value in values:
        nonempty(value, label + " ID")
        if "::" not in value or not all(value.split("::", 1)):
            raise ValueError(label + " ID must be classname::name: " + value)
    if len(set(values)) != len(values):
        raise ValueError("Duplicate " + label + " IDs.")
    return set(values)


def resolve(base, value, label):
    return (base / nonempty(value, label)).resolve()


def verified_path(base, record, key, hash_key):
    path = resolve(base, record.get(key), key)
    expected = nonempty(record.get(hash_key), hash_key)
    if digest(path) != expected:
        raise ValueError("Hash mismatch for " + key + ": " + str(path))
    return path


def verify_identity(base, obj):
    if not isinstance(obj, dict):
        raise ValueError("Each partition requires a source and binary identity.")
    manifest = verified_path(base, obj, "source_manifest", "source_sha256")
    source_root = resolve(base, obj.get("source_root"), "source_root")
    files = read_json(manifest).get("files")
    if not isinstance(files, dict) or not files:
        raise ValueError("Source manifest requires a nonempty files mapping.")
    for name, expected in files.items():
        nonempty(name, "Source filename")
        logical = PurePosixPath(name)
        if logical.is_absolute() or ".." in logical.parts or logical.as_posix() != name or name == ".":
            raise ValueError("Source filename must be a normalized relative path: " + name)
        path = (source_root / name).resolve()
        if not path.is_relative_to(source_root):
            raise ValueError("Source file escapes source_root: " + name)
        if digest(path) != nonempty(expected, "Source SHA-256"):
            raise ValueError("Source file hash mismatch: " + name)
    verified_path(base, obj, "binary", "binary_sha256")
    return (obj["source_sha256"], obj["binary_sha256"])


def verify_triage(base, partition, events_sha, failures):
    path = verified_path(base, partition, "triage", "triage_sha256")
    obj = read_json(path)
    if obj.get("raw_events_sha256") != events_sha:
        raise ValueError("Behavioral triage does not match raw events.")
    entries = obj.get("failures")
    if not isinstance(entries, list):
        raise ValueError("Behavioral triage failures must be a list.")
    ids = []
    for item in entries:
        if not isinstance(item, dict) or item.get("classification") != "behavioral":
            raise ValueError("Every failure needs behavioral classification.")
        ids.append(nonempty(item.get("id"), "Triage ID"))
        nonempty(item.get("grounding"), "Triage grounding")
        nonempty(item.get("diagnosis"), "Triage diagnosis")
    if canonical_ids(ids, "triage") != failures:
        raise ValueError("Behavioral triage must cover exactly the failed tests.")


def check(inventory, partitions):
    inventory, partitions = Path(inventory).resolve(), Path(partitions).resolve()
    base = partitions.parent
    complete = read_json(inventory)
    expected_ids = canonical_ids(complete.get("tests"), "complete inventory")
    if complete.get("excluded", []):
        raise ValueError("The complete inventory must not have exclusions.")
    manifest = read_json(partitions)
    specs = manifest.get("partitions")
    if not isinstance(specs, list) or not specs:
        raise ValueError("Partition manifest requires a nonempty partitions list.")
    issues, checked, owners, seen_partition_ids = [], [], {}, set()
    for spec in specs:
        if not isinstance(spec, dict):
            raise ValueError("Each partition must be an object.")
        part_id = nonempty(spec.get("id"), "Partition ID")
        if part_id in seen_partition_ids:
            raise ValueError("Duplicate partition ID: " + part_id)
        seen_partition_ids.add(part_id)
        receipt_path = verified_path(base, spec, "receipt", "receipt_sha256")
        saved = read_json(receipt_path)
        if saved.get("status") != "EXECUTION_RECONCILED":
            raise ValueError(part_id + ": partition receipt is not EXECUTION_RECONCILED.")
        expected = spec.get("expected")
        if expected not in ("pass", "fail") or expected != saved.get("expected"):
            raise ValueError(part_id + ": expected outcome differs from receipt.")
        raw = saved.get("raw_event_evidence")
        if not isinstance(raw, dict) or not raw.get("classname"):
            raise ValueError(part_id + ": raw execution evidence is required.")
        exit_code = saved.get("process_exit_code")
        if type(exit_code) is not int:
            raise ValueError(part_id + ": integer process exit code required.")
        junit = resolve(base, spec.get("junit"), "junit")
        discovered = resolve(base, spec.get("inventory"), "inventory")
        events = resolve(base, spec.get("events"), "events")
        current = check_partition(junit, discovered, exit_code, expected, events, raw["classname"])
        for field in ("status", "counts", "selected", "executed", "missing", "unexpected",
                      "issues", "unverified_exclusions", "process_exit_code", "expected",
                      "junit_sha256", "inventory_sha256", "raw_event_evidence"):
            if saved.get(field) != current.get(field):
                raise ValueError(part_id + ": stale or inconsistent receipt field " + field)
        if current["status"] != "EXECUTION_RECONCILED":
            raise ValueError(part_id + ": current evidence no longer reconciles.")
        discovery = read_json(discovered)
        selected = canonical_ids(discovery.get("tests"), part_id + " inventory")
        identity = verify_identity(base, spec.get("identity"))
        failures = {
            case.get("classname", "") + "::" + case.get("name")
            for case in ET.parse(junit).getroot().iter("testcase")
            if case.find("failure") is not None
        }
        if expected == "fail":
            verify_triage(base, spec, raw["sha256"], failures)
        for test_id in sorted(selected):
            if test_id in owners:
                issues.append("Overlapping executed ID: " + test_id)
            else:
                owners[test_id] = (part_id, identity)
        checked.append({
            "id": part_id, "identity": identity, "selected": sorted(selected),
            "excluded": current["unverified_exclusions"], "counts": current["counts"],
            "expected": expected, "receipt_sha256": digest(receipt_path),
        })
    missing, excess = sorted(expected_ids - owners.keys()), sorted(owners.keys() - expected_ids)
    if missing:
        issues.append("Complete inventory has tests that no partition executed.")
    if excess:
        issues.append("Partitions executed tests outside the complete inventory.")
    resolved = []
    for part in checked:
        for exclusion in part["excluded"]:
            test_id = exclusion["id"]
            target = owners.get(test_id)
            if test_id not in expected_ids:
                issues.append(part["id"] + ": exclusion absent from complete inventory: " + test_id)
            elif target is None:
                issues.append(part["id"] + ": exclusion was not executed: " + test_id)
            elif target[0] == part["id"]:
                issues.append(part["id"] + ": exclusion executed by its own partition: " + test_id)
            elif target[1] != part["identity"]:
                issues.append(part["id"] + ": excluded test has different source/binary identity: " + test_id)
            else:
                resolved.append({"id": test_id, "excluded_by": part["id"], "executed_by": target[0]})
    counts = {kind: sum(p["counts"][kind] for p in checked)
              for kind in ("pass", "failure", "error", "skipped")}
    return {
        "status": "FAIL" if issues else "PARTITIONS_RECONCILED",
        "expected_tests": len(expected_ids), "executed_unique": len(owners),
        "counts": counts, "missing": missing, "unexpected": excess, "issues": issues,
        "partitions": checked, "resolved_exclusions": resolved,
        "inventory_sha256": digest(inventory), "manifest_sha256": digest(partitions),
        "production_provenance": "unverified", "limitation": LIMITATION,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--inventory", required=True)
    parser.add_argument("--partitions", required=True)
    parser.add_argument("--output")
    args = parser.parse_args(argv)
    try:
        result = check(args.inventory, args.partitions)
    except (OSError, ValueError, TypeError, AttributeError, KeyError, ET.ParseError) as error:
        result = {"status": "FAIL", "issues": [str(error)],
                  "production_provenance": "unverified", "limitation": LIMITATION}
    rendered = json.dumps(result, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(rendered)
    print(rendered, end="")
    return 0 if result["status"] == "PARTITIONS_RECONCILED" else 2


if __name__ == "__main__":
    sys.exit(main())
