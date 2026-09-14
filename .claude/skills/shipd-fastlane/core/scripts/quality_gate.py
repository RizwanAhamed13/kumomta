#!/usr/bin/env python3
"""Fail-closed audit of recorded local evidence; never runs candidate code or uploads."""
import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys
from urllib.parse import urlparse

import fastlane

CATALOG = Path(__file__).resolve().parents[1] / 'assets' / 'quality-checks.json'
STAGES = ('scope', 'full', 'final')


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def stamp(value):
    parsed = dt.datetime.fromisoformat(value.replace('Z', '+00:00'))
    if parsed.tzinfo is None:
        raise ValueError('Timestamps require timezone offsets.')
    return parsed


def evidence(root, entry):
    if not isinstance(entry, dict) or not nonempty(entry.get('path')):
        raise ValueError('Missing evidence file path.')
    path = Path(entry['path'])
    if path.is_absolute() or '..' in path.parts:
        raise ValueError('Evidence paths must stay relative to the bundle directory.')
    target = root / path
    if any(p.is_symlink() for p in [target, *target.parents] if p != root.parent):
        raise ValueError('Symlink evidence is not supported.')
    if not target.resolve().is_relative_to(root.resolve()):
        raise ValueError('Evidence escaped the bundle directory.')
    if not target.is_file() or target.stat().st_size == 0:
        raise ValueError('Missing or empty evidence: ' + str(path))
    if fastlane.sha(target) != entry.get('sha256'):
        raise ValueError('Evidence hash mismatch: ' + str(path))
    return target


def initialize(stage, inputs, panel, catalog):
    contract = digest(panel.get('contract'))
    return {
        'schema': 1, 'stage': stage, 'panel': panel,
        'note': 'PENDING template. Attach real evidence; this is not a passing result.',
        'checks': [{
            'id': row['id'], 'stage': stage, 'status': 'PENDING',
            'inputs': {key: inputs['components'].get(key) for key in row['dependencies']},
            'catalog_sha256': digest(catalog), 'contract_sha256': contract,
            'started_at': None, 'completed_at': None,
            'items': [{'id': item, 'status': 'PENDING', 'reason': '', 'evidence': []}
                      for item in row['items']],
            'evidence': [], 'required_evidence_roles': row['evidence_roles'],
            'findings': [], 'commands': [], 'execution': None, 'review': None,
            'replica_limit': row['limit']
        } for row in catalog['checks'] if stage in row['stages']]
    }


DEFAULT_EXECUTION_POLICY = {
    'ssh_alias': 'shipd-local', 'host': 'arch', 'ip': '100.105.254.33',
    'workspace_root': '/home/admin/olympus-work',
}



def allowed_recorded_storage_path(value):
    """Reject protected destinations lexically; no mount/device probing occurs here."""
    if not nonempty(value):
        return False
    path = PurePosixPath(value)
    return (path.is_absolute() and '..' not in path.parts
            and not path.is_relative_to(PurePosixPath('/mnt/windows')))


def protected_recorded_device(value):
    # findmnt can append Btrfs subvolume notation: /dev/nvme0n1p3[/@home].
    return bool(re.search(r'(?:^|/)nvme0n1p[1-4](?=$|[^0-9])', value))


def selected_commands(receipt, current, root, paths, identifier, stage, definitions):
    """Bind outcomes to a frozen command inventory, not arbitrary command prose."""
    execution = receipt.get('execution') or {}
    path = execution.get('selection_evidence')
    if path not in paths:
        raise ValueError('command selection requires a hashed selection_evidence attachment.')
    target = root / path
    if fastlane.sha(target) != current['components'].get('selection'):
        raise ValueError('command selection attachment does not match the frozen selection hash.')
    selection = json.loads(target.read_text())
    if (not isinstance(selection, dict) or selection.get('schema') != 1
            or not isinstance(selection.get('commands'), list) or not selection['commands']):
        raise ValueError('command selection requires schema 1 and a nonempty commands inventory.')
    ids, selected = set(), {}
    for command in selection['commands']:
        if not isinstance(command, dict):
            raise ValueError('command selection entries must be objects.')
        cid = command.get('id')
        stages = command.get('stages')
        if (not nonempty(cid) or cid in ids or not nonempty(command.get('check_id'))
                or not nonempty(command.get('command'))
                or type(command.get('expected_exit_code')) is not int
                or not isinstance(stages, list) or not stages
                or len(stages) != len(set(stages)) or any(s not in STAGES for s in stages)):
            raise ValueError('command selection has invalid or duplicate IDs, stages or outcomes.')
        definition = definitions.get(command['check_id'])
        if (definition is None or definition['kind'] not in ('executable', 'mixed')
                or not set(stages) <= set(definition['stages'])):
            raise ValueError('command selection names an unknown/nonexecutable check or unsupported stage.')
        ids.add(cid)
        if command['check_id'] == identifier and stage in stages:
            selected[cid] = command
    if not selected:
        raise ValueError('command selection has no commands for this check and stage.')
    return selected


def execution_matches(execution, env, commit, paths):
    """Audit recorded routing/preflight provenance, without probing any host."""
    policy = env.get('execution_policy', DEFAULT_EXECUTION_POLICY)
    if not isinstance(policy, dict) or not all(nonempty(policy.get(k)) for k in DEFAULT_EXECUTION_POLICY):
        return False
    if policy != DEFAULT_EXECUTION_POLICY and execution.get('authorization_evidence') not in paths:
        return False
    workdir = PurePosixPath(str(env.get('workdir', '')))
    workspace = PurePosixPath(policy['workspace_root'])
    if (not workdir.is_absolute() or not workspace.is_absolute()
            or '..' in workdir.parts or '..' in workspace.parts
            or workdir == workspace or not workdir.is_relative_to(workspace)
            or not allowed_recorded_storage_path(str(workdir))
            or not allowed_recorded_storage_path(str(workspace))):
        return False
    if (any(execution.get(k) != policy[k] for k in ('ssh_alias', 'host', 'ip'))
            or execution.get('host') != env.get('host')
            or execution.get('workdir') != env.get('workdir')
            or execution.get('commit') != commit
            or any(execution.get(k) not in paths for k in
                   ('identity_evidence', 'transfer_hash_evidence', 'preflight_evidence'))):
        return False
    preflight = env.get('preflight')
    if not isinstance(preflight, dict) or execution.get('preflight') != preflight:
        return False
    if (preflight.get('docker_available') is not True
            or not nonempty(preflight.get('docker_server_version'))
            or not nonempty(preflight.get('phase_id'))
            or execution.get('phase_id') != preflight['phase_id']
            or preflight.get('workdir_realpath') != str(workdir)
            or not allowed_recorded_storage_path(preflight.get('docker_root_dir'))
            or type(preflight.get('free_bytes')) is not int or preflight['free_bytes'] <= 0):
        return False
    try:
        stamp(preflight['captured_at'])
    except (KeyError, TypeError, ValueError, AttributeError):
        return False
    for key in ('workspace_filesystem', 'docker_filesystem'):
        fs = preflight.get(key)
        if (not isinstance(fs, dict) or not all(nonempty(fs.get(k)) for k in
                ('source', 'target', 'fstype', 'physical_device'))
                or type(fs.get('rotational')) is not bool
                or not allowed_recorded_storage_path(fs.get('target'))
                or protected_recorded_device(fs['source'])
                or protected_recorded_device(fs['physical_device'])
                or (fs['source'].startswith('/mnt/windows')
                    and not allowed_recorded_storage_path(fs['source']))):
            return False
    return True


def check(bundle, current, root, catalog, now=None):
    """Validate evidence bindings/completeness, not the truth of arbitrary grader prose."""
    errors = []
    now = now or dt.datetime.now(dt.timezone.utc)
    root = Path(root).resolve()
    stage = bundle.get('stage')
    if stage not in STAGES or bundle.get('schema') != 1:
        raise ValueError('Use schema 1 and stage scope, full or final.')
    if stage == 'scope' and current['components'].get('test') != current['components'].get('scope_test'):
        errors.append('Scope submission test.patch must match the frozen Scope test fingerprint.')
    definitions = {row['id']: row for row in catalog['checks']}
    required = {key: row for key, row in definitions.items() if stage in row['stages']}
    panel = bundle.get('panel')
    if not isinstance(panel, dict):
        raise ValueError('Missing live panel contract.')
    contract = panel.get('contract')
    try:
        age = (now - stamp(panel['captured_at'])).total_seconds()
        if not 0 <= age <= 86400:
            errors.append('Live panel capture is future-dated or older than the local 24-hour maximum.')
        if panel.get('complete') is not True or urlparse(panel.get('url', '')).scheme != 'https':
            errors.append('An explicitly complete HTTPS live panel capture is required.')
        capture_text = evidence(root, panel.get('capture')).read_text()
        if not isinstance(contract, dict) or not nonempty(contract.get('case_id')) or not contract.get('rules'):
            raise ValueError('Record the case id and live panel rules.')
        if not isinstance(contract['rules'], dict):
            raise ValueError('Panel rules must be an object.')
        mappings = contract.get('checks')
        if not isinstance(mappings, list) or not mappings:
            raise ValueError('The complete panel check inventory is missing.')
        seen_labels = set()
        for mapping in mappings:
            label, ids, stages = mapping.get('label'), mapping.get('local_ids'), mapping.get('stages')
            if not nonempty(label) or label in seen_labels or label not in capture_text:
                errors.append('Panel label missing, duplicated or absent from captured text: ' + str(label))
            seen_labels.add(label)
            if not isinstance(ids, list) or not ids or any(i not in definitions for i in ids):
                errors.append('Unmapped/unknown live check: ' + str(label))
            elif not isinstance(stages, list) or not stages or any(s not in STAGES for s in stages):
                errors.append('Missing/invalid live check stages: ' + str(label))
            elif stage in stages and not all(i in required for i in ids):
                errors.append('No local counterpart available at this stage: ' + str(label))
            if not nonempty(mapping.get('rationale')):
                errors.append('Explain the semantic mapping for live check: ' + str(label))
    except (KeyError, TypeError, ValueError, OSError, AttributeError) as exc:
        errors.append('Panel evidence: ' + str(exc))

    receipts = bundle.get('checks')
    if not isinstance(receipts, list) or not all(isinstance(r, dict) for r in receipts):
        raise ValueError('Checks must be a list of receipt objects.')
    indexed = {}
    for receipt in receipts:
        identifier = receipt.get('id')
        if not isinstance(identifier, str) or identifier not in required or identifier in indexed:
            errors.append('Unknown, duplicate or out-of-stage receipt: ' + str(identifier))
            continue
        indexed[identifier] = receipt
    for identifier, row in required.items():
        receipt = indexed.get(identifier)
        if receipt is None:
            errors.append(identifier + ': missing local counterpart receipt.')
            continue
        prefix = identifier + ': '
        try:
            if receipt.get('status') != 'PASS' or receipt.get('stage') != stage:
                errors.append(prefix + 'requires an explicit current-stage PASS; PENDING/SKIP/WARN do not pass.')
            if receipt.get('catalog_sha256') != digest(catalog) or receipt.get('contract_sha256') != digest(contract):
                errors.append(prefix + 'stale catalog or live contract binding.')
            expected = {key: current['components'].get(key) for key in row['dependencies']}
            for key, value in expected.items():
                width = 40 if key == 'repo' else 64
                if not isinstance(value, str) or not re.fullmatch('[0-9a-f]{' + str(width) + '}', value):
                    errors.append(prefix + 'missing/invalid current fingerprint: ' + key)
            if receipt.get('inputs') != expected:
                errors.append(prefix + 'stale artifact, commit, environment or command selection.')
            start, end = stamp(receipt['started_at']), stamp(receipt['completed_at'])
            if not start <= end <= now:
                errors.append(prefix + 'invalid receipt time range.')
            if identifier in ('eligibility', 'originality', 'final_state') and (now - end).total_seconds() > 86400:
                errors.append(prefix + 'dynamic external evidence is older than the local 24-hour maximum.')
            attachments = receipt.get('evidence')
            if not isinstance(attachments, list) or not attachments:
                raise ValueError('Missing evidence attachments.')
            paths, roles = set(), set()
            for attachment in attachments:
                evidence(root, attachment)
                paths.add(attachment['path']); roles.add(attachment.get('role'))
            if not set(row['evidence_roles']) <= roles:
                errors.append(prefix + 'missing evidence roles: ' + ', '.join(sorted(set(row['evidence_roles']) - roles)))
            items = receipt.get('items')
            if not isinstance(items, list) or not all(isinstance(item, dict) for item in items):
                raise ValueError('Invalid rubric items.')
            if sorted(item.get('id', '') for item in items) != sorted(row['items']):
                errors.append(prefix + 'rubric items missing, duplicated or unknown.')
            for item in items:
                refs = item.get('evidence')
                if item.get('status') != 'PASS' or not nonempty(item.get('reason')) or not isinstance(refs, list) or not refs or not set(refs) <= paths:
                    errors.append(prefix + 'rubric item needs a reasoned PASS tied to hashed evidence: ' + str(item.get('id')))
            findings = receipt.get('findings')
            if not isinstance(findings, list):
                raise ValueError('An explicit findings list is required.')
            finding_ids = set()
            for finding in findings:
                fid = finding.get('id')
                if not nonempty(fid) or fid in finding_ids or finding.get('status') not in ('fixed', 'rejected_with_evidence') or not nonempty(finding.get('disposition')) or finding.get('evidence') not in paths:
                    errors.append(prefix + 'unresolved or unsupported finding disposition.')
                finding_ids.add(fid)
            if row['kind'] in ('executable', 'mixed'):
                execution = receipt.get('execution') or {}
                env = current['environment']
                if not execution_matches(execution, env, current['components']['repo'], paths):
                    errors.append(prefix + 'missing/mismatched designated-builder, preflight and transfer evidence.')
                commands = receipt.get('commands')
                if not isinstance(commands, list) or not commands:
                    raise ValueError('Executable counterpart requires actual command outcomes.')
                selected = selected_commands(receipt, current, root, paths, identifier, stage, definitions)
                actual_ids = [c.get('id') for c in commands if isinstance(c, dict)]
                if (len(actual_ids) != len(commands) or len(actual_ids) != len(set(actual_ids))
                        or set(actual_ids) != set(selected)):
                    errors.append(prefix + 'command selection has missing, extra or duplicate outcomes.')
                for command in commands:
                    if not isinstance(command, dict):
                        raise ValueError('Command outcomes must be objects.')
                    planned = selected.get(command.get('id'))
                    if (planned is None or command.get('command') != planned['command']
                            or command.get('expected_exit_code') != planned['expected_exit_code']):
                        errors.append(prefix + 'command outcome does not match its frozen selection entry.')
                    if (not nonempty(command.get('command')) or type(command.get('exit_code')) is not int
                            or type(command.get('expected_exit_code')) is not int
                            or command['exit_code'] != command['expected_exit_code']
                            or command.get('evidence') not in paths):
                        errors.append(prefix + 'missing or unexpected command outcome.')
                    try:
                        command_start = stamp(command['started_at'])
                        command_end = stamp(command['completed_at'])
                        preflight = execution['preflight']
                        if (not start <= command_start <= command_end <= end
                                or stamp(preflight['captured_at']) > command_start
                                or command.get('phase_id') != preflight.get('phase_id')
                                or not nonempty(command.get('phase_id'))):
                            raise ValueError('phase or timestamp mismatch')
                    except (KeyError, TypeError, ValueError, AttributeError) as exc:
                        errors.append(prefix + 'command/preflight phase binding: ' + str(exc))
            if row['kind'] in ('review', 'mixed'):
                review = receipt.get('review') or {}
                if (not all(nonempty(review.get(key)) for key in ('reviewer', 'model_version', 'rubric_version', 'context', 'limitations'))
                        or review.get('raw_output') not in paths or not review.get('citations')
                        or not isinstance(review['citations'], list)
                        or not all(nonempty(citation) for citation in review['citations'])):
                    errors.append(prefix + 'review needs identity, rubric, raw output, citations and limitations.')
            if not nonempty(receipt.get('replica_limit')):
                errors.append(prefix + 'local-versus-hosted limitation must be recorded.')
        except (KeyError, TypeError, ValueError, OSError, AttributeError) as exc:
            errors.append(prefix + str(exc))
    return {
        'status': 'LOCAL_EVIDENCE_GATE_PASS' if not errors else 'BLOCK_UPLOAD',
        'stage': stage, 'required_checks': len(required), 'errors': errors,
        'deferred_checks': sorted(set(definitions) - set(required)),
        'authority': 'Audits recorded evidence completeness and hashes; does not independently prove report truth, '
                     'run candidate checks, reproduce private graders, approve paid gates, or submit. '
                     'Recheck the live panel and artifact bytes immediately before any separately authorized action.'
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='action', required=True)
    init = commands.add_parser('init')
    init.add_argument('--stage', choices=STAGES, required=True)
    init.add_argument('--inputs', type=Path, required=True)
    init.add_argument('--panel', type=Path, required=True)
    init.add_argument('--output', type=Path, required=True)
    verify = commands.add_parser('check')
    verify.add_argument('bundle', type=Path)
    for name in ('artifacts', 'environment', 'selection', 'scope-tests'):
        verify.add_argument('--' + name, type=Path, required=True)
    verify.add_argument('--commit', required=True)
    verify.add_argument('--output', type=Path)
    args = parser.parse_args()
    try:
        catalog = json.loads(CATALOG.read_text())
        if args.action == 'init':
            if args.output.exists():
                raise ValueError('Refusing to overwrite an existing evidence bundle.')
            value = initialize(args.stage, json.loads(args.inputs.read_text()), json.loads(args.panel.read_text()), catalog)
            fastlane.write(args.output, value)
            print(json.dumps({'status': 'PENDING_TEMPLATE_CREATED', 'checks': len(value['checks']), 'output': str(args.output)}))
            return 0
        current = fastlane.snapshot(args.artifacts, args.commit, args.environment, args.selection, args.scope_tests)
        result = check(json.loads(args.bundle.read_text()), current, args.bundle.parent, catalog)
        if args.output:
            if args.output.resolve() == args.bundle.resolve():
                raise ValueError('Result output must not overwrite the evidence bundle.')
            fastlane.write(args.output, result)
        print(json.dumps(result, indent=2))
        return 0 if result['status'] == 'LOCAL_EVIDENCE_GATE_PASS' else 1
    except (ValueError, KeyError, TypeError, OSError, AttributeError) as exc:
        print(json.dumps({'status': 'BLOCK_UPLOAD', 'errors': [str(exc)]}))
        return 1


if __name__ == '__main__':
    sys.exit(main())
