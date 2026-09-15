"""Synthetic fixtures for evidence consistency; these do not assert production provenance."""
import contextlib
import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import partition_result_gate as gate
import test_result_gate as individual


class PartitionGateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "source").mkdir()
        (self.root / "source/lib.rs").write_text("fn fixture() {}\n")
        (self.root / "binary").write_bytes(b"fixture executable identity")
        self.write("source.json", {"files": {"lib.rs": gate.digest(self.root / "source/lib.rs")}})
        self.identity = {
            "source_manifest": "source.json", "source_sha256": gate.digest(self.root / "source.json"),
            "source_root": "source", "binary": "binary", "binary_sha256": gate.digest(self.root / "binary")
        }
        self.complete = self.write("complete.json", {"tests": ["suite::a", "suite::b"]})
        self.manifest = self.root / "partitions.json"
        self.specs = []

    def write(self, name, value):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, indent=2) + "\n")
        return path

    def add(self, name, selected, excluded=(), failed=(), identity=None):
        folder = self.root / name
        folder.mkdir()
        inventory = {"tests": ["suite::" + n for n in selected],
                     "excluded": [{"id": "suite::" + n, "reason": "Separate partition",
                                   "grounding": "Complete suite partition"} for n in excluded]}
        self.write(name + "/inventory.json", inventory)
        xml = ET.Element("testsuite", tests=str(len(selected)), failures=str(len(failed)), errors="0")
        events = []
        for n in selected:
            case = ET.SubElement(xml, "testcase", classname="suite", name=n)
            if n in failed:
                ET.SubElement(case, "failure").text = "assertion mismatch"
            events.extend([{"type": "test", "event": "started", "name": n},
                           {"type": "test", "event": "failed" if n in failed else "ok", "name": n}])
        ET.ElementTree(xml).write(folder / "junit.xml")
        (folder / "events.jsonl").write_text("".join(json.dumps(e) + "\n" for e in events))
        expected = "fail" if failed else "pass"
        receipt = individual.check(folder / "junit.xml", folder / "inventory.json",
                                   101 if failed else 0, expected, folder / "events.jsonl", "suite")
        self.write(name + "/receipt.json", receipt)
        spec = {
            "id": name, "expected": expected, "receipt": name + "/receipt.json",
            "receipt_sha256": gate.digest(folder / "receipt.json"),
            "junit": name + "/junit.xml", "inventory": name + "/inventory.json",
            "events": name + "/events.jsonl", "identity": dict(identity or self.identity)
        }
        if failed:
            self.write(name + "/triage.json", {
                "raw_events_sha256": gate.digest(folder / "events.jsonl"),
                "failures": [{"id": "suite::" + n, "classification": "behavioral",
                              "grounding": "Feature requirement", "diagnosis": "Expected assertion mismatch"}
                             for n in failed]
            })
            spec.update(triage=name + "/triage.json", triage_sha256=gate.digest(folder / "triage.json"))
        self.specs.append(spec)
        return spec

    def result(self):
        self.write("partitions.json", {"partitions": self.specs})
        return gate.check(self.complete, self.manifest)

    def assertRejected(self, text=None):
        try:
            result = self.result()
        except (ValueError, OSError, TypeError, AttributeError, KeyError, ET.ParseError) as error:
            if text:
                self.assertIn(text, str(error))
        else:
            self.assertEqual("FAIL", result["status"])
            if text:
                self.assertIn(text, " ".join(result["issues"]))

    def refresh_receipt_hash(self, spec):
        spec["receipt_sha256"] = gate.digest(self.root / spec["receipt"])

    def edit_json(self, path, change):
        value = gate.read_json(self.root / path)
        change(value)
        self.write(path, value)

    def test_complementary_passing_partitions(self):
        self.add("base", ["a"], ["b"])
        self.add("fresh", ["b"], ["a"])
        result = self.result()
        self.assertEqual("PARTITIONS_RECONCILED", result["status"])
        self.assertEqual(2, result["executed_unique"])
        self.assertEqual(2, len(result["resolved_exclusions"]))
        self.assertEqual("unverified", result["production_provenance"])

    def test_expected_behavioral_failure_can_complete_baseline(self):
        self.add("base", ["a"], ["b"])
        self.add("feature", ["b"], ["a"], failed=["b"])
        result = self.result()
        self.assertEqual("PARTITIONS_RECONCILED", result["status"])
        self.assertEqual({"pass": 1, "failure": 1, "error": 0, "skipped": 0}, result["counts"])

    def test_disjoint_partitions_need_not_declare_complement(self):
        self.add("base", ["a"])
        self.add("fresh", ["b"])
        self.assertEqual("PARTITIONS_RECONCILED", self.result()["status"])

    def test_different_binaries_allowed_only_without_cross_identity_exclusion(self):
        self.add("base", ["a"])
        (self.root / "other").write_bytes(b"other fixture binary")
        identity = dict(self.identity, binary="other", binary_sha256=gate.digest(self.root / "other"))
        self.add("integration", ["b"], identity=identity)
        self.assertEqual("PARTITIONS_RECONCILED", self.result()["status"])

    def test_disjoint_partitions_cannot_combine_source_revisions(self):
        self.add("base", ["a"])
        (self.root / "other-source").mkdir()
        (self.root / "other-source/lib.rs").write_text("fn fixture_changed() {}")
        self.write("other-source.json", {"files": {
            "lib.rs": gate.digest(self.root / "other-source/lib.rs")}})
        identity = dict(self.identity, source_root="other-source", source_manifest="other-source.json",
                        source_sha256=gate.digest(self.root / "other-source.json"))
        self.add("fresh", ["b"], identity=identity)
        self.assertRejected("different source snapshots")

    def forged_reconciled_receipt(self, spec):
        folder = self.root / spec["id"]
        receipt = individual.check(folder / "junit.xml", folder / "inventory.json",
                                   101 if spec["expected"] == "fail" else 0,
                                   spec["expected"], folder / "events.jsonl", "suite")
        receipt.update(status="EXECUTION_RECONCILED", issues=[])
        self.write(spec["receipt"], receipt)
        self.refresh_receipt_hash(spec)

    def test_unmatched_start_cannot_hide_behind_refrozen_receipt(self):
        spec = self.add("one", ["a", "b"])
        path = self.root / "one/events.jsonl"
        with path.open("a") as stream:
            stream.write(json.dumps({"type": "test", "event": "started", "name": "hidden"}) + "\n")
        self.forged_reconciled_receipt(spec)
        self.assertRejected("inconsistent receipt field status")

    def test_terminal_without_start_cannot_hide_behind_refrozen_receipt(self):
        spec = self.add("one", ["a", "b"])
        path = self.root / "one/events.jsonl"
        path.write_text("".join(line + "\n" for line in path.read_text().splitlines()
                                if json.loads(line)["event"] != "started"))
        self.forged_reconciled_receipt(spec)
        self.assertRejected("inconsistent receipt field status")

    def test_zero_events_cannot_hide_behind_refrozen_receipt(self):
        spec = self.add("one", ["a", "b"])
        (self.root / "one/events.jsonl").write_text("")
        self.forged_reconciled_receipt(spec)
        self.assertRejected("inconsistent receipt field status")

    def test_duplicate_behavioral_triage_ids_are_rejected(self):
        spec = self.add("one", ["a", "b"], failed=["b"])
        self.edit_json("one/triage.json", lambda x: x["failures"].append(dict(x["failures"][0])))
        spec["triage_sha256"] = gate.digest(self.root / "one/triage.json")
        self.assertRejected("Duplicate triage")

    def test_partial_green_suite_is_rejected(self):
        self.add("base", ["a"], ["b"])
        self.assertRejected("no partition executed")

    def test_partial_suite_without_exclusion_is_still_rejected(self):
        self.add("base", ["a"])
        self.assertRejected("no partition executed")

    def test_overlapping_execution_is_rejected(self):
        self.add("one", ["a", "b"])
        self.add("two", ["b"])
        self.assertRejected("Overlapping executed ID")

    def test_unexpected_execution_is_rejected(self):
        self.add("one", ["a", "b", "c"])
        self.assertRejected("outside the complete inventory")

    def test_duplicate_complete_inventory_ids_are_rejected(self):
        self.write("complete.json", {"tests": ["suite::a", "suite::a"]})
        self.add("one", ["a"])
        self.assertRejected("Duplicate complete inventory")

    def test_complete_inventory_cannot_hide_exclusions(self):
        self.write("complete.json", {"tests": ["suite::a"], "excluded": [{"id": "suite::b"}]})
        self.add("one", ["a"])
        self.assertRejected("must not have exclusions")

    def test_empty_complete_inventory_is_rejected(self):
        self.write("complete.json", {"tests": []})
        self.assertRejected("nonempty")

    def test_noncanonical_complete_inventory_id_is_rejected(self):
        self.write("complete.json", {"tests": ["name"]})
        self.assertRejected("classname::name")

    def test_duplicate_partition_names_are_rejected(self):
        self.add("one", ["a", "b"])
        self.specs.append(dict(self.specs[0]))
        self.assertRejected("Duplicate partition ID")

    def test_receipt_tampering_is_rejected(self):
        self.add("one", ["a", "b"])
        self.edit_json("one/receipt.json", lambda x: x.update(executed=100))
        self.assertRejected("Hash mismatch for receipt")

    def test_refrozen_fabricated_receipt_is_rejected(self):
        spec = self.add("one", ["a", "b"])
        self.edit_json("one/receipt.json", lambda x: x.update(executed=100))
        self.refresh_receipt_hash(spec)
        self.assertRejected("inconsistent receipt field executed")

    def test_altered_junit_is_rejected(self):
        self.add("one", ["a", "b"])
        path = self.root / "one/junit.xml"
        path.write_text(path.read_text() + "\n")
        self.assertRejected("junit_sha256")

    def test_altered_inventory_is_rejected(self):
        self.add("one", ["a", "b"])
        self.edit_json("one/inventory.json", lambda x: x.update(note="changed"))
        self.assertRejected("inventory_sha256")

    def test_altered_events_are_rejected(self):
        self.add("one", ["a", "b"])
        path = self.root / "one/events.jsonl"
        path.write_text(path.read_text() + "\n")
        self.assertRejected("raw_event_evidence")

    def test_xml_only_receipt_is_rejected(self):
        spec = self.add("one", ["a", "b"])
        self.edit_json("one/receipt.json", lambda x: x.update(raw_event_evidence=None))
        self.refresh_receipt_hash(spec)
        self.assertRejected("raw execution evidence")

    def test_nonreconciled_receipt_is_rejected(self):
        spec = self.add("one", ["a", "b"])
        self.edit_json("one/receipt.json", lambda x: x.update(status="FAIL"))
        self.refresh_receipt_hash(spec)
        self.assertRejected("not EXECUTION_RECONCILED")

    def test_changed_source_is_rejected(self):
        self.add("one", ["a", "b"])
        (self.root / "source/lib.rs").write_text("changed\n")
        self.assertRejected("Source file hash mismatch")

    def test_changed_source_manifest_is_rejected(self):
        self.add("one", ["a", "b"])
        self.edit_json("source.json", lambda x: x.update(note="changed"))
        self.assertRejected("Hash mismatch for source_manifest")

    def test_changed_binary_is_rejected(self):
        self.add("one", ["a", "b"])
        (self.root / "binary").write_bytes(b"new executable")
        self.assertRejected("Hash mismatch for binary")

    def test_exclusion_cannot_be_satisfied_by_another_binary(self):
        self.add("base", ["a"], ["b"])
        (self.root / "other").write_bytes(b"other executable")
        identity = dict(self.identity, binary="other", binary_sha256=gate.digest(self.root / "other"))
        self.add("fresh", ["b"], identity=identity)
        self.assertRejected("different source/binary identity")

    def test_exclusion_cannot_be_satisfied_by_another_source(self):
        self.add("base", ["a"], ["b"])
        self.write("other-source.json", {"files": {"lib.rs": gate.digest(self.root / "source/lib.rs")}, "revision": 2})
        identity = dict(self.identity, source_manifest="other-source.json",
                        source_sha256=gate.digest(self.root / "other-source.json"))
        self.add("fresh", ["b"], identity=identity)
        self.assertRejected("different source/binary identity")

    def test_unknown_exclusion_is_rejected(self):
        self.add("base", ["a", "b"], ["unlisted"])
        self.assertRejected("exclusion absent from complete inventory")

    def test_expected_failure_needs_triage(self):
        spec = self.add("one", ["a", "b"], failed=["b"])
        spec.pop("triage")
        self.assertRejected("triage")

    def test_triage_must_cover_all_failed_ids(self):
        spec = self.add("one", ["a", "b"], failed=["a", "b"])
        self.edit_json("one/triage.json", lambda x: x["failures"].pop())
        spec["triage_sha256"] = gate.digest(self.root / "one/triage.json")
        self.assertRejected("exactly the failed tests")

    def test_triage_cannot_label_harness_error_behavioral(self):
        spec = self.add("one", ["a", "b"], failed=["b"])
        self.edit_json("one/triage.json", lambda x: x["failures"][0].update(classification="compiler"))
        spec["triage_sha256"] = gate.digest(self.root / "one/triage.json")
        self.assertRejected("behavioral classification")

    def test_triage_requires_prompt_grounding(self):
        spec = self.add("one", ["a", "b"], failed=["b"])
        self.edit_json("one/triage.json", lambda x: x["failures"][0].update(grounding=""))
        spec["triage_sha256"] = gate.digest(self.root / "one/triage.json")
        self.assertRejected("Triage grounding")

    def test_triage_must_match_actual_event_hash(self):
        spec = self.add("one", ["a", "b"], failed=["b"])
        self.edit_json("one/triage.json", lambda x: x.update(raw_events_sha256="0" * 64))
        spec["triage_sha256"] = gate.digest(self.root / "one/triage.json")
        self.assertRejected("does not match raw events")

    def test_expected_outcome_cannot_change_from_receipt(self):
        spec = self.add("one", ["a", "b"])
        spec["expected"] = "fail"
        self.assertRejected("expected outcome differs")

    def test_source_manifest_cannot_escape_root(self):
        self.write("source.json", {"files": {"../binary": gate.digest(self.root / "binary")}})
        self.identity["source_sha256"] = gate.digest(self.root / "source.json")
        self.add("one", ["a", "b"])
        self.assertRejected("normalized relative path")

    def test_duplicate_json_keys_are_rejected(self):
        self.add("one", ["a", "b"])
        self.complete.write_text('{"tests":["suite::a"],"tests":["suite::a","suite::b"]}')
        self.assertRejected("Duplicate JSON key")

    def test_cli_missing_report_writes_failed_receipt(self):
        self.add("one", ["a", "b"])
        self.specs[0]["junit"] = "missing.xml"
        self.write("partitions.json", {"partitions": self.specs})
        output = self.root / "result.json"
        with contextlib.redirect_stdout(io.StringIO()):
            code = gate.main(["--inventory", str(self.complete), "--partitions", str(self.manifest),
                              "--output", str(output)])
        self.assertEqual(2, code)
        self.assertEqual("FAIL", gate.read_json(output)["status"])


if __name__ == "__main__":
    unittest.main()
