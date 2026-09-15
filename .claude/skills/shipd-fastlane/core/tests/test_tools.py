"""Plugin bookkeeping tests only; never clone, compile or run candidate code."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile

PLUGIN = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PLUGIN / 'scripts'))
import fastlane
import contract_check
import evidence_index


class BudgetTests(unittest.TestCase):
    def usage(self, used=1):
        return {'rateLimitsByLimitId': {'codex': {'limitId': 'codex', 'primary': {'usedPercent': used}, 'secondary': None}}}

    def test_below_checkpoint(self):
        self.assertEqual(fastlane.budget(self.usage())['decision'], 'CONTINUE')

    def test_reserve_stops_before_cap(self):
        self.assertEqual(fastlane.budget(self.usage(40))['decision'], 'STOP')

    def test_secondary_window_controls(self):
        value = self.usage(); value['rateLimitsByLimitId']['codex']['secondary'] = {'usedPercent': 45}
        self.assertEqual(fastlane.budget(value)['decision'], 'STOP')

    def test_missing_and_invalid_fail_closed(self):
        for value in ({}, [], None, {'rateLimitsByLimitId': []}, self.usage(None), self.usage(True), self.usage(float('nan')), self.usage(-1), self.usage(101)):
            with self.subTest(value=value):
                self.assertEqual(fastlane.budget(value)['decision'], 'STOP')

    def test_malformed_window_and_wrong_legacy(self):
        self.assertEqual(fastlane.budget({'rateLimits': {'primary': []}})['decision'], 'STOP')
        self.assertEqual(fastlane.budget({'rateLimits': {'limitId': 'codex_bengalfox', 'primary': {'usedPercent': 0}}})['decision'], 'STOP')

    def test_app_tool_wrapper(self):
        result = fastlane.budget({'content': [{'type': 'text', 'text': json.dumps(self.usage(3))}]})
        self.assertEqual(result['windows'][0]['used_percent'], 3)

    def test_spend_block(self):
        value = self.usage(); value['rateLimitsByLimitId']['codex']['spendControlReached'] = True
        self.assertEqual(fastlane.budget(value)['decision'], 'STOP')

    def test_invalid_cap(self):
        for maximum, reserve in [(101, 10), (0, 0), (50, -1), (50, 50), (float('nan'), 1), (50, float('nan'))]:
            with self.assertRaises(ValueError):
                fastlane.budget(self.usage(), maximum, reserve)


    def test_explicit_custom_cap(self):
        self.assertEqual(fastlane.budget(self.usage(50), 75, 5)['decision'], 'CONTINUE')
        self.assertEqual(fastlane.budget(self.usage(70), 75, 5)['decision'], 'STOP')
        self.assertEqual(fastlane.budget(self.usage(99), 100, 0)['decision'], 'CONTINUE')

    def test_explicit_no_cap_preserves_account_block(self):
        result = fastlane.budget(self.usage(99), None)
        self.assertEqual(result['decision'], 'CONTINUE')
        self.assertIsNone(result['maximum_percent'])
        self.assertIsNone(result['stop_at_used_percent'])
        value = self.usage(99)
        value['rateLimitsByLimitId']['codex']['spendControlReached'] = True
        self.assertEqual(fastlane.budget(value, None)['decision'], 'STOP')


class FingerprintTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.root = Path(self.tmp.name)
        for name in fastlane.ARTIFACTS:
            (self.root / name).write_text('FROM public.ecr.aws/d3j8x8q7/olympus-base-rust:latest\nWORKDIR /app\nCMD [\"/bin/bash\"]\n' if name == 'Dockerfile' else 'diff --git a/example b/example\n')
        self.env = self.root / 'environment.json'
        self.env.write_text(json.dumps({'host': 'builder', 'workdir': '/case', 'image_identity': 'digest', 'toolchain': 'v1', 'uid': 1000, 'build_flags': {'jobs': 5}}))
        self.selection = self.root / 'selection.txt'; self.selection.write_text('base and new')
        self.scope = self.root / 'scope.patch'; self.scope.write_text('frozen reduced tests')

    def tearDown(self):
        self.tmp.cleanup()

    def snap(self, scope=True):
        return fastlane.snapshot(self.root, 'a' * 40, self.env, self.selection, self.scope if scope else None)

    def test_identical_not_a_passing_receipt(self):
        result = fastlane.compare(self.snap(), self.snap())
        self.assertEqual(result['stale'], {})
        self.assertIn('four_state_matrix', result['eligible_for_evidence_reuse'])
        self.assertIn('not proof', self.snap()['note'])

    def test_test_expansion_keeps_scope_semantics_only(self):
        before = self.snap(); (self.root / 'test.patch').write_text('changed test')
        result = fastlane.compare(before, self.snap())
        self.assertIn('scope_semantics', result['eligible_for_evidence_reuse'])
        for gate in ['four_state_matrix', 'rollout_replay', 'holistic_review', 'freeze']:
            self.assertIn(gate, result['stale'])

    def test_solution_and_prompt_reopen_scope(self):
        for filename in ['solution.patch', 'problem.md']:
            before = self.snap(); (self.root / filename).write_text(filename + ' changed')
            self.assertIn('scope_semantics', fastlane.compare(before, self.snap())['stale'])

    def test_missing_scope_is_unknown(self):
        self.assertIn('scope_semantics', fastlane.compare(self.snap(False), self.snap(False))['unknown'])

    def test_matching_invalid_fingerprints_cannot_enable_reuse(self):
        broken = self.snap(); broken['components']['solution'] = 'placeholder'
        result = fastlane.compare(broken, broken)
        self.assertIn('scope_semantics', result['unknown'])
        self.assertNotIn('four_state_matrix', result['eligible_for_evidence_reuse'])
        with self.assertRaises(ValueError):
            fastlane.compare({'components': []}, broken)

    def test_environment_and_selection_invalidate_runtime(self):
        before = self.snap(); self.selection.write_text('new command')
        self.assertIn('four_state_matrix', fastlane.compare(before, self.snap())['stale'])
        before = self.snap(); env = json.loads(self.env.read_text()); env['toolchain'] = 'v2'; self.env.write_text(json.dumps(env))
        self.assertIn('four_state_matrix', fastlane.compare(before, self.snap())['stale'])

    def test_invalid_or_missing_inputs(self):
        with self.assertRaises(ValueError):
            fastlane.snapshot(self.root, 'abc', self.env, self.selection)
        (self.root / 'test.patch').unlink()
        with self.assertRaises(ValueError):
            self.snap()

    def test_preflight_has_explicit_limits_and_rejects_digest(self):
        self.assertEqual(fastlane.preflight(self.root)['status'], 'STATIC_CHECKS_PASS')
        (self.root / 'Dockerfile').write_text('FROM allowed:latest@sha256:abcd\n')
        self.assertEqual(fastlane.preflight(self.root)['status'], 'FAIL')


class ContractTests(unittest.TestCase):
    def setUp(self):
        self.doc = json.loads((PLUGIN / 'assets/contract.example.json').read_text())

    def test_example_declared_coverage_only(self):
        result = contract_check.check(self.doc)
        self.assertEqual(result['status'], 'DECLARED_COVERAGE_PASS')
        self.assertIn('omit a whole public input family', result['limitation'])

    def test_missing_input_family_is_caught(self):
        self.doc['tests'].pop()
        self.assertEqual(contract_check.check(self.doc)['status'], 'FAIL')

    def test_baseline_valid_new_is_rejected(self):
        self.doc['tests'][0]['baseline_valid'] = True
        self.assertEqual(contract_check.check(self.doc)['status'], 'FAIL')

    def test_missing_feature_prerequisite_is_rejected(self):
        self.doc['tests'][0].pop('solution_dependent_prerequisite')
        self.assertEqual(contract_check.check(self.doc)['status'], 'FAIL')

    def test_ungrounded_and_private_oracles_rejected(self):
        self.doc['requirements'][0]['grounding'] = {'kind': 'implementation', 'source': 'private layout'}
        self.doc['tests'][0]['oracle'] = 'private-structure'
        self.assertEqual(contract_check.check(self.doc)['status'], 'FAIL')

    def test_duplicate_and_orphan_ids(self):
        self.doc['tests'].append(copy.deepcopy(self.doc['tests'][0]))
        self.doc['tests'][0]['covers'][0]['requirement'] = 'unknown'
        self.assertEqual(contract_check.check(self.doc)['status'], 'FAIL')

    def test_malformed_documents_fail(self):
        for value in [None, [], {}, {'requirements': ['bad'], 'tests': []}]:
            self.assertEqual(contract_check.check(value)['status'], 'FAIL')

    def test_independent_dimension_totals_do_not_cover_cross_product(self):
        # Both input families and all roles occur, but each misses two roles.
        self.doc['tests'][0]['covers'][0]['roles'] = ['write', 'commit']
        self.doc['tests'][1]['covers'][0]['roles'] = ['reopen', 'read']
        result = contract_check.check(self.doc)
        self.assertEqual(result['status'], 'FAIL')
        self.assertIn(['R1', 'scalar', 'reopen'], result['declared_cells']['missing'])
        self.assertIn(['R1', 'composite', 'write'], result['declared_cells']['missing'])

    def test_complete_cells_still_need_one_interaction_witness(self):
        split = copy.deepcopy(self.doc['tests'][1])
        split['id'] += '.reader'
        split['covers'][0]['roles'] = ['reopen', 'read']
        self.doc['tests'][1]['covers'][0]['roles'] = ['write', 'commit']
        self.doc['tests'].append(split)
        result = contract_check.check(self.doc)
        self.assertEqual(result['declared_cells']['missing'], [])
        self.assertEqual(result['status'], 'FAIL')
        self.assertIn('S.interaction', result['declared_scenarios']['missing'])

    def test_scope_can_defer_but_cannot_claim_full_coverage(self):
        self.doc['tests'] = self.doc['tests'][:1]
        scope = contract_check.check(self.doc, 'scope')
        self.assertEqual(scope['status'], 'DECLARED_SCOPE_SLICE_PASS')
        self.assertTrue(scope['deferred_to_full'])
        self.assertEqual(contract_check.check(self.doc)['status'], 'FAIL')
        self.doc['tests'][0]['oracle'] = 'private-structure'
        self.assertEqual(contract_check.check(self.doc, 'scope')['status'], 'FAIL')

    def test_legacy_contract_needs_inventory_and_risk_review_for_full_gate(self):
        for key in ('inventory_sources', 'scenarios', 'risk_review'):
            self.doc.pop(key)
        self.assertEqual(contract_check.check(self.doc)['status'], 'FAIL')

    def test_each_risk_family_needs_a_review(self):
        for kind in ('boundary', 'error', 'compatibility', 'interaction'):
            d = copy.deepcopy(self.doc); d['risk_review'].pop(kind)
            self.assertEqual(contract_check.check(d)['status'], 'FAIL')

    def test_inapplicability_needs_reason_and_public_source(self):
        self.doc['risk_review']['error'] = {'not_applicable': {'reason': 'No new error behavior'}}
        self.assertEqual(contract_check.check(self.doc)['status'], 'FAIL')
        self.doc['risk_review']['error']['not_applicable']['grounding'] = self.doc['requirements'][0]['grounding']
        # Checks evidence shape; a human must still judge whether this rationale is true.
        self.assertEqual(contract_check.check(self.doc)['status'], 'DECLARED_COVERAGE_PASS')

    def test_missing_or_malformed_scenario_cannot_pass(self):
        for change in ({'test_id': 'missing'}, {'test_id': []}, {'steps': ['only setup']}, {'covers': []}):
            d = copy.deepcopy(self.doc); d['scenarios'][0].update(change)
            self.assertEqual(contract_check.check(d)['status'], 'FAIL')
        self.doc['risk_review']['boundary']['scenario_ids'] = ['unknown']
        self.assertEqual(contract_check.check(self.doc)['status'], 'FAIL')

    def test_excluded_cell_requires_grounding_and_cannot_also_be_covered(self):
        exclusion = {'input_class': 'composite', 'role': 'commit', 'reason': 'Example applicability exception'}
        self.doc['requirements'][0]['excluded_cells'] = [exclusion]
        self.doc['tests'][1]['covers'][0]['roles'].remove('commit')
        self.doc['scenarios'][1]['covers'][0]['roles'].remove('commit')
        self.assertEqual(contract_check.check(self.doc)['status'], 'FAIL')
        exclusion['grounding'] = self.doc['requirements'][0]['grounding']
        self.assertEqual(contract_check.check(self.doc)['status'], 'DECLARED_COVERAGE_PASS')
        self.doc['tests'][1]['covers'][0]['roles'].append('commit')
        self.assertEqual(contract_check.check(self.doc)['status'], 'FAIL')

    def test_empty_dimensions_or_unknown_stage_fail_closed(self):
        for value in ([], None, [''], ['scalar', 'scalar']):
            d = copy.deepcopy(self.doc); d['requirements'][0]['input_classes'] = value
            self.assertEqual(contract_check.check(d)['status'], 'FAIL')
        self.assertEqual(contract_check.check(self.doc, 'paid')['status'], 'FAIL')


class InventoryTests(unittest.TestCase):
    def test_provenance_duplicates_archive_errors_and_source_roots(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'project'; root.mkdir(); out = root / 'output'
            lesson = '2026-09-12 | example | baseline mask | public prerequisite | evidence\n'
            (root / 'lessons.md').write_text(lesson)
            (root / 'copy').mkdir(); (root / 'copy/lessons.md').write_text(lesson)
            (root / '.env').write_text('private'); (root / 'secret.json').write_text('private')
            (root / 'link.md').symlink_to(root / 'lessons.md')
            (root / 'bad.zip').write_bytes(b'not a zip')
            with zipfile.ZipFile(root / 'good.zip', 'w') as z:
                z.writestr('solution.patch', 'not executed')
            repo = root / 'repo'; (repo / '.git').mkdir(parents=True); (repo / 'src').mkdir()
            (repo / 'src/source.json').write_text('{}'); (repo / 'solution.patch').write_text('root delivery')
            result = evidence_index.index(root, out)
            self.assertEqual(result['unique_lesson_rows'], 1)
            self.assertEqual(result['errors'], 1)
            self.assertEqual(result['archive_entries'], 1)
            inventory = json.loads((out / 'inventory.json').read_text())
            paths = {x['path'] for x in inventory}
            self.assertIn('bad.zip', paths); self.assertIn('repo/solution.patch', paths)
            self.assertNotIn('repo/src/source.json', paths); self.assertNotIn('secret.json', paths)
            lessons = json.loads((out / 'lessons.json').read_text())
            self.assertEqual(len(lessons[0]['provenance']), 2)
            self.assertEqual(evidence_index.query(out, 'baseline', 1)['shown'], 1)
            self.assertEqual(evidence_index.index(root, out)['files_indexed'], result['files_indexed'])

    def test_bundled_lessons_search_without_inventory(self):
        self.assertGreater(evidence_index.query(PLUGIN / 'knowledge', 'reopen', 2)['matches'], 0)

    def test_revision_copies_are_not_counted_as_distinct_content(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d)
            rows = [{'path': folder + '/' + name, 'sha256': name, 'bytes': 1}
                    for folder in ('canonical', 'copy') for name in fastlane.ARTIFACTS]
            rows.append({'path': 'partial/solution.patch', 'sha256': 'different', 'bytes': 1})
            evidence_index.dump(out / 'inventory.json', rows)
            summary = evidence_index.revisions(out)
            self.assertEqual(summary['complete_four_file_directories'], 2)
            self.assertEqual(summary['distinct_complete_content_sets'], 1)
            result = json.loads((out / 'revisions.json').read_text())
            self.assertIsNone(result['artifact_sets'][-1]['four_file_content_id'])

    def test_revision_metadata_without_hash_cannot_identify_complete_bytes(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d)
            rows = [{'path': 'case/' + name, 'bytes': 100} for name in fastlane.ARTIFACTS]
            evidence_index.dump(out / 'inventory.json', rows)
            self.assertEqual(evidence_index.revisions(out)['distinct_complete_content_sets'], 0)


if __name__ == '__main__':
    unittest.main()
