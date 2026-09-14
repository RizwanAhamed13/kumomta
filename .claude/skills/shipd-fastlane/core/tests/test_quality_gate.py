"""Synthetic receipt tests only. No candidate code, remote jobs or paid checks."""
import copy
import datetime as dt
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

PLUGIN = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PLUGIN / 'scripts'))
import fastlane
import quality_gate as gate


class QualityGateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name).resolve()
        self.now = dt.datetime(2026, 9, 12, 12, tzinfo=dt.timezone.utc)
        self.time = self.now.isoformat()
        self.catalog = json.loads(gate.CATALOG.read_text())
        self.log = self.root / 'synthetic.log'
        self.log.write_text('Synthetic unit-test fixture only: Verify Tests\n')
        self.ref = {'path': self.log.name, 'sha256': fastlane.sha(self.log)}
        self.current = {
            'components': {key: 'a' * 64 for key in ('problem', 'solution', 'test', 'docker', 'environment', 'selection', 'scope_test')},
            'environment': {'host': 'arch', 'workdir': '/home/admin/olympus-work/synthetic'}
        }
        self.current['environment']['preflight'] = {
            'phase_id': 'synthetic-phase', 'captured_at': self.time,
            'docker_available': True, 'docker_server_version': 'synthetic-version',
            'workdir_realpath': self.current['environment']['workdir'], 'free_bytes': 1024,
            'docker_root_dir': '/mnt/ssd/docker',
            'workspace_filesystem': dict(source='/dev/mapper/omarchy_root', target='/home', fstype='btrfs', physical_device='/dev/sda', rotational=True),
            'docker_filesystem': dict(source='/dev/mapper/omarchy_root', target='/', fstype='btrfs', physical_device='/dev/sda', rotational=True),
        }
        self.current['components']['repo'] = 'b' * 40
        self.selection = {'schema': 1, 'commands': [
            {'id': row['id'] + '.fixture', 'check_id': row['id'], 'stages': row['stages'],
             'command': 'synthetic test command', 'expected_exit_code': 0}
            for row in self.catalog['checks'] if row['kind'] in ('executable', 'mixed')
        ]}
        self.selection_path = self.root / 'selection.json'
        self.selection_path.write_text(json.dumps(self.selection))
        self.selection_ref = {'path': self.selection_path.name, 'sha256': fastlane.sha(self.selection_path)}
        self.current['components']['selection'] = self.selection_ref['sha256']
        self.panel = {
            'url': 'https://example.invalid/synthetic-case', 'captured_at': self.time,
            'complete': True, 'capture': self.ref,
            'contract': {'case_id': 'synthetic', 'rules': {'test_rule': 'fixture'}, 'checks': [
                {'label': 'Verify Tests', 'local_ids': ['verify_tests'], 'stages': list(gate.STAGES), 'rationale': 'Synthetic mapping fixture.'}
            ]}
        }
        self.bundle = self.passing('full')

    def tearDown(self):
        self.tmp.cleanup()

    def passing(self, stage):
        bundle = gate.initialize(stage, self.current, copy.deepcopy(self.panel), self.catalog)
        for receipt in bundle['checks']:
            receipt.update(status='PASS', started_at=self.time, completed_at=self.time)
            receipt['evidence'] = [dict(self.ref, role=role) for role in receipt['required_evidence_roles']]
            receipt['evidence'].append(dict(self.selection_ref, role='command_selection'))
            for item in receipt['items']:
                item.update(status='PASS', reason='Synthetic bookkeeping test; no real candidate claim.', evidence=[self.log.name])
            receipt['commands'] = [{'id': receipt['id'] + '.fixture', 'command': 'synthetic test command', 'exit_code': 0, 'expected_exit_code': 0, 'evidence': self.log.name,
                                    'phase_id': 'synthetic-phase', 'started_at': self.time, 'completed_at': self.time}]
            receipt['execution'] = dict(copy.deepcopy(self.current['environment']), phase_id='synthetic-phase', ssh_alias='shipd-local', ip='100.105.254.33',
                                        commit=self.current['components']['repo'], identity_evidence=self.log.name, transfer_hash_evidence=self.log.name, preflight_evidence=self.log.name, selection_evidence=self.selection_path.name)
            receipt['review'] = {'reviewer': 'synthetic', 'model_version': 'synthetic', 'rubric_version': 'synthetic',
                                 'context': 'single-agent correlated fixture', 'limitations': 'Synthetic test only.',
                                 'raw_output': self.log.name, 'citations': ['synthetic.patch:1']}
        return bundle

    def run_gate(self, bundle=None, current=None):
        return gate.check(bundle or self.bundle, current or self.current, self.root, self.catalog, self.now)

    def blocked(self, fragment):
        result = self.run_gate()
        self.assertEqual(result['status'], 'BLOCK_UPLOAD', result)
        self.assertIn(fragment, '\n'.join(result['errors']))

    def row(self, name='verify_tests'):
        return next(row for row in self.bundle['checks'] if row['id'] == name)

    def test_complete_stage_receipts_pass_without_hosted_claim(self):
        for stage, count in [('scope', 12), ('full', 18), ('final', 20)]:
            result = self.run_gate(self.passing(stage))
            self.assertEqual(result['status'], 'LOCAL_EVIDENCE_GATE_PASS', result)
            self.assertEqual(result['required_checks'], count)
            self.assertIn('does not independently prove', result['authority'])

    def test_missing_or_mismatched_preflight_blocks(self):
        del self.row()['execution']['preflight']['docker_filesystem']
        self.blocked('preflight')

    def test_incomplete_observed_storage_cannot_pass_even_when_receipt_matches(self):
        for section, key in [('workspace_filesystem', 'physical_device'), ('docker_filesystem', 'rotational')]:
            with self.subTest(section=section, key=key):
                observed = copy.deepcopy(self.current['environment']['preflight'])
                del self.current['environment']['preflight'][section][key]
                self.bundle = self.passing('full')
                self.blocked('preflight')
                self.current['environment']['preflight'] = observed

    def test_protected_windows_destinations_block(self):
        for path in ('/mnt/windows', '/mnt/windows/docker', '/mnt/windows/../safe', '/safe/../mnt/windows'):
            self.current['environment']['preflight']['docker_root_dir'] = path
            self.bundle = self.passing('full')
            self.blocked('preflight')

    def test_protected_mount_and_device_records_block(self):
        original = copy.deepcopy(self.current['environment']['preflight'])
        cases = [('target', '/mnt/windows/cache'), ('source', '/mnt/windows/bind'),
                 ('source', '/dev/nvme0n1p1'), ('source', '/dev/nvme0n1p2'),
                 ('source', '/dev/nvme0n1p3[/@home]'), ('source', '/dev/nvme0n1p4'),
                 ('physical_device', '/dev/nvme0n1p3')]
        for fs in ('workspace_filesystem', 'docker_filesystem'):
            for key, value in cases:
                with self.subTest(fs=fs, key=key, value=value):
                    self.current['environment']['preflight'] = copy.deepcopy(original)
                    self.current['environment']['preflight'][fs][key] = value
                    self.bundle = self.passing('full')
                    self.blocked('preflight')

    def test_future_linux_partition_is_not_blanket_rejected(self):
        # Synthetic metadata only: an actual new mount still needs user authorization
        # and physical preflight evidence; this is not permission to create one.
        for device in ('/dev/nvme0n1p5', '/dev/nvme0n1p14'):
            self.current['environment']['preflight']['docker_filesystem']['source'] = device
            self.current['environment']['preflight']['docker_filesystem']['physical_device'] = '/dev/nvme0n1'
            self.current['environment']['preflight']['docker_root_dir'] = '/mnt/linux/docker'
            self.bundle = self.passing('full')
            self.assertEqual(self.run_gate()['status'], 'LOCAL_EVIDENCE_GATE_PASS')

    def test_authorized_routing_override_cannot_use_protected_windows_workspace(self):
        env = self.current['environment']
        env.update(workdir='/mnt/windows/work/case', execution_policy=dict(gate.DEFAULT_EXECUTION_POLICY, workspace_root='/mnt/windows/work'))
        env['preflight']['workdir_realpath'] = env['workdir']
        self.bundle = self.passing('full')
        for row in self.bundle['checks']:
            row['execution']['authorization_evidence'] = self.log.name
        self.blocked('preflight')

    def test_selection_attachment_must_match_frozen_hash(self):
        self.current['components']['selection'] = 'c' * 64
        self.bundle = self.passing('full')
        self.blocked('does not match the frozen selection hash')

    def test_selection_attachment_is_required(self):
        self.row()['execution'].pop('selection_evidence')
        self.blocked('selection_evidence')

    def test_arbitrary_command_text_or_exit_cannot_replace_selected_command(self):
        for key, value in [('command', 'unrelated passing command'), ('expected_exit_code', 1), ('id', 'another-check.fixture')]:
            self.bundle = self.passing('full')
            self.row()['commands'][0][key] = value
            self.blocked('frozen selection entry')

    def test_selection_cannot_omit_or_duplicate_command_outcomes(self):
        command = dict(self.row()['commands'][0])
        self.row()['commands'].append(command)
        self.blocked('duplicate outcomes')
        self.bundle = self.passing('full')
        self.selection['commands'].append(dict(self.selection['commands'][0], id='extra-planned', check_id='verify_tests', stages=['full']))
        self.refresh_selection()
        self.blocked('missing, extra or duplicate outcomes')

    def refresh_selection(self):
        self.selection_path.write_text(json.dumps(self.selection))
        self.selection_ref['sha256'] = fastlane.sha(self.selection_path)
        self.current['components']['selection'] = self.selection_ref['sha256']
        self.bundle = self.passing('full')

    def test_selection_rejects_duplicate_ids_and_wrong_stage(self):
        original = copy.deepcopy(self.selection)
        self.selection['commands'].append(dict(self.selection['commands'][0]))
        self.refresh_selection()
        self.blocked('invalid or duplicate')
        self.selection = original
        for command in self.selection['commands']:
            if command['check_id'] == 'verify_tests':
                command['stages'] = ['scope']
        self.refresh_selection()
        self.blocked('no commands for this check and stage')

    def test_unstructured_selection_prose_cannot_pass(self):
        self.selection_path.write_text('Run the relevant tests and report PASS.')
        self.selection_ref['sha256'] = fastlane.sha(self.selection_path)
        self.current['components']['selection'] = self.selection_ref['sha256']
        self.bundle = self.passing('full')
        self.assertEqual(self.run_gate()['status'], 'BLOCK_UPLOAD')

    def test_unknown_or_exhausted_capacity_blocks(self):
        for capacity in (None, 0, -1, True):
            self.current['environment']['preflight']['free_bytes'] = capacity
            self.bundle = self.passing('full')
            self.blocked('preflight')

    def test_docker_unavailable_or_unknown_blocks_even_when_receipt_matches(self):
        for available in (False, None, 0, 1, 'true'):
            with self.subTest(available=available):
                self.current['environment']['preflight']['docker_available'] = available
                self.bundle = self.passing('full')
                self.blocked('preflight')

    def test_docker_version_and_phase_observation_are_required(self):
        for key in ('docker_server_version', 'captured_at', 'phase_id'):
            with self.subTest(key=key):
                observed = copy.deepcopy(self.current['environment']['preflight'])
                del self.current['environment']['preflight'][key]
                self.bundle = self.passing('full')
                self.blocked('preflight')
                self.current['environment']['preflight'] = observed

    def test_preflight_timestamp_must_have_timezone(self):
        for value in ('yesterday', '2026-09-12T12:00:00', None):
            self.current['environment']['preflight']['captured_at'] = value
            self.bundle = self.passing('full')
            self.blocked('preflight')

    def test_command_cannot_precede_preflight(self):
        self.current['environment']['preflight']['captured_at'] = (self.now + dt.timedelta(seconds=1)).isoformat()
        self.bundle = self.passing('full')
        self.blocked('command/preflight phase binding')

    def test_execution_and_command_must_share_observed_phase(self):
        self.row()['execution']['phase_id'] = 'another-phase'
        self.blocked('preflight')
        self.row()['execution']['phase_id'] = 'synthetic-phase'
        self.row()['commands'][0]['phase_id'] = 'another-phase'
        self.blocked('command/preflight phase binding')

    def test_missing_command_timestamps_block(self):
        for key in ('started_at', 'completed_at'):
            self.bundle = self.passing('full')
            del self.row()['commands'][0][key]
            self.blocked('command/preflight phase binding')

    def test_command_must_stay_within_receipt_interval(self):
        for key, seconds in (('started_at', -1), ('completed_at', 1)):
            self.bundle = self.passing('full')
            self.row()['commands'][0][key] = (self.now + dt.timedelta(seconds=seconds)).isoformat()
            self.blocked('command/preflight phase binding')

    def test_preserved_old_command_and_preflight_remain_eligible(self):
        old = (self.now - dt.timedelta(days=2)).isoformat()
        self.current['environment']['preflight']['captured_at'] = old
        self.bundle = self.passing('full')
        row = self.row()
        row['started_at'] = row['completed_at'] = old
        row['commands'][0]['started_at'] = row['commands'][0]['completed_at'] = old
        self.assertEqual(self.run_gate()['status'], 'LOCAL_EVIDENCE_GATE_PASS')

    def test_missing_preflight_attachment_blocks(self):
        self.row()['execution']['preflight_evidence'] = 'missing.log'
        self.blocked('preflight')

    def test_workdir_traversal_blocks(self):
        self.current['environment']['workdir'] = '/home/admin/olympus-work/../escape'
        self.row()['execution']['workdir'] = self.current['environment']['workdir']
        self.blocked('designated-builder')

    def test_old_builder_receipt_blocks(self):
        self.row()['execution']['ssh_alias'] = 'retired-builder'
        self.blocked('designated-builder')

    def test_user_override_requires_attached_authorization(self):
        policy = dict(gate.DEFAULT_EXECUTION_POLICY, host='authorized-host')
        self.current['environment']['execution_policy'] = policy
        self.current['environment']['host'] = 'authorized-host'
        self.bundle = self.passing('full')
        self.blocked('designated-builder')
        for receipt in self.bundle['checks']:
            receipt['execution']['authorization_evidence'] = self.log.name
        self.assertEqual(self.run_gate()['status'], 'LOCAL_EVIDENCE_GATE_PASS')

    def test_pending_template_cannot_pass(self):
        self.bundle = gate.initialize('full', self.current, self.panel, self.catalog)
        self.blocked('PENDING/SKIP/WARN')

    def test_missing_counterpart_blocks_even_if_panel_omits_it(self):
        self.bundle['checks'].pop()
        self.blocked('missing local counterpart')

    def test_warning_or_skip_cannot_pass(self):
        for status in ('WARN', 'SKIP', 'FAIL', None):
            self.row()['status'] = status
            self.blocked('explicit current-stage PASS')

    def test_changed_artifact_invalidates_dependent_proof(self):
        self.current['components']['test'] = 'c' * 64
        self.blocked('stale artifact')

    def test_prompt_edit_keeps_execution_receipt_eligible(self):
        self.current['components']['problem'] = 'c' * 64
        errors = self.run_gate()['errors']
        self.assertTrue(any('fairness: stale artifact' in e for e in errors))
        self.assertFalse(any(e.startswith('verify_tests:') for e in errors))

    def test_missing_scope_hash_blocks(self):
        self.current['components']['scope_test'] = None
        self.blocked('missing/invalid current fingerprint: scope_test')

    def test_scope_submission_must_match_frozen_scope_tests(self):
        self.current['components']['test'] = 'c' * 64
        self.bundle = self.passing('scope')
        self.blocked('must match the frozen Scope test fingerprint')

    def test_review_citations_must_be_nonempty_strings(self):
        for citations in ([None], [''], ['   '], [42]):
            self.row('fairness')['review']['citations'] = citations
            self.blocked('review needs identity')

    def test_tampered_or_missing_evidence_blocks(self):
        self.log.write_text('modified')
        self.blocked('Evidence hash mismatch')
        self.log.unlink()
        self.blocked('Missing or empty evidence')

    def test_path_traversal_and_symlinks_block(self):
        self.row()['evidence'][0]['path'] = '../outside'
        self.blocked('Evidence paths must stay relative')
        self.row()['evidence'][0]['path'] = 'link.log'
        (self.root / 'link.log').symlink_to(self.log)
        self.blocked('Symlink evidence')

    def test_stale_or_incomplete_panel_blocks(self):
        self.bundle['panel']['captured_at'] = (self.now - dt.timedelta(days=2)).isoformat()
        self.blocked('24-hour maximum')
        self.bundle['panel']['captured_at'] = self.time
        self.bundle['panel']['complete'] = False
        self.blocked('explicitly complete')

    def test_unknown_live_check_blocks(self):
        self.bundle['panel']['contract']['checks'][0]['local_ids'] = ['future_check']
        self.blocked('Unmapped/unknown live check')

    def test_new_contract_invalidates_old_reviews(self):
        self.bundle['panel']['contract']['rules']['changed'] = True
        self.blocked('stale catalog or live contract')

    def test_mapping_requires_explanation_and_stage(self):
        mapping = self.bundle['panel']['contract']['checks'][0]
        mapping['rationale'] = ''
        self.blocked('Explain the semantic mapping')
        mapping['local_ids'] = ['verify_tests', 'rollout_audit']
        self.blocked('No local counterpart available at this stage')

    def test_duplicate_receipts_and_items_block(self):
        self.bundle['checks'].append(copy.deepcopy(self.row()))
        self.blocked('duplicate or out-of-stage')
        self.bundle['checks'].pop()
        self.row()['items'].append(copy.deepcopy(self.row()['items'][0]))
        self.blocked('rubric items missing, duplicated')

    def test_evidence_role_and_item_citation_required(self):
        self.row()['evidence'] = [a for a in self.row()['evidence'] if a['role'] != 'junit']
        self.blocked('missing evidence roles: junit')
        self.row()['items'][0]['evidence'] = ['not-attached.log']
        self.blocked('reasoned PASS tied to hashed evidence')

    def test_command_failure_or_no_execution_blocks(self):
        self.row()['commands'][0]['exit_code'] = 2
        self.blocked('unexpected command outcome')
        self.row()['commands'] = []
        self.blocked('actual command outcomes')

    def test_expected_baseline_failure_is_allowed(self):
        for command in self.selection['commands']:
            if command['check_id'] == 'verify_tests':
                command['expected_exit_code'] = 1
        self.refresh_selection()
        self.row()['commands'][0].update(exit_code=1, expected_exit_code=1)
        self.assertEqual(self.run_gate()['status'], 'LOCAL_EVIDENCE_GATE_PASS')

    def test_boolean_exit_code_not_accepted(self):
        self.row()['commands'][0].update(exit_code=False)
        self.blocked('unexpected command outcome')

    def test_wrong_builder_or_missing_transfer_receipt_blocks(self):
        self.row()['execution']['ssh_alias'] = 'local'
        self.blocked('designated-builder')
        self.row()['execution']['ssh_alias'] = 'shipd-local'
        self.row()['execution']['transfer_hash_evidence'] = None
        self.blocked('designated-builder')

    def test_review_without_raw_output_or_limitations_blocks(self):
        self.row('fairness')['review']['raw_output'] = None
        self.blocked('review needs identity')
        self.row('fairness')['replica_limit'] = ''
        self.blocked('local-versus-hosted limitation')

    def test_open_finding_blocks(self):
        self.row('fairness')['findings'] = [{'id': 'F1', 'status': 'open', 'disposition': '', 'evidence': self.log.name}]
        self.blocked('unresolved or unsupported finding')

    def test_dynamic_evidence_expires_but_static_evidence_does_not(self):
        self.row('eligibility')['started_at'] = self.row('eligibility')['completed_at'] = (self.now - dt.timedelta(days=2)).isoformat()
        self.blocked('dynamic external evidence')
        self.row('eligibility')['started_at'] = self.row('eligibility')['completed_at'] = self.time
        old = (self.now - dt.timedelta(days=2)).isoformat()
        self.current['environment']['preflight']['captured_at'] = old
        self.bundle = self.passing('full')
        self.row()['started_at'] = self.row()['completed_at'] = old
        self.row()['commands'][0]['started_at'] = self.row()['commands'][0]['completed_at'] = old
        self.assertEqual(self.run_gate()['status'], 'LOCAL_EVIDENCE_GATE_PASS')

    def test_cli_recomputes_artifact_fingerprints(self):
        for name in fastlane.ARTIFACTS:
            (self.root / name).write_text('synthetic artifact\n')
        env = self.root / 'environment.json'
        env.write_text(json.dumps(dict(self.current['environment'], image_identity='synthetic', toolchain='synthetic', uid=1000, build_flags={'jobs': 5})))
        selection = self.root / 'selection.txt'; selection.write_text('synthetic command')
        scope = self.root / 'scope.patch'; scope.write_text('synthetic scope')
        bundle = self.root / 'bundle.json'; bundle.write_text(json.dumps(self.bundle))
        result = subprocess.run([sys.executable, str(PLUGIN / 'scripts/quality_gate.py'), 'check', str(bundle),
                                 '--artifacts', str(self.root), '--commit', 'b' * 40, '--environment', str(env),
                                 '--selection', str(selection), '--scope-tests', str(scope)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(result.stdout)['status'], 'BLOCK_UPLOAD')
        self.assertIn('stale artifact', result.stdout)


if __name__ == '__main__':
    unittest.main()
