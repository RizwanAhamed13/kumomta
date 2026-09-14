#!/usr/bin/env python3
"""Reconcile executed JUnit cases with an independently recorded discovery inventory."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def check(junit, inventory, exit_code, expected='pass', events=None, event_classname=None):
    issues = []
    obj = json.loads(Path(inventory).read_text())
    entries = obj.get('tests', [])
    exclusions = obj.get('excluded', [])
    if not isinstance(entries, list) or not entries or any(not isinstance(i, str) or not i for i in entries):
        raise ValueError('Discovery tests must be a nonempty list of canonical classname::name IDs.')
    if len(entries) != len(set(entries)):
        issues.append('Duplicate discovery IDs.')
    excluded = []
    if not isinstance(exclusions, list):
        raise ValueError('Excluded tests must be a list.')
    for item in exclusions:
        if not isinstance(item, dict) or any(not isinstance(item.get(k), str) or not item[k].strip() for k in ('id', 'reason', 'grounding')):
            raise ValueError('Each exclusion requires id, reason and grounding; exclusions remain unverified.')
        excluded.append(item['id'])
    if len(excluded) != len(set(excluded)) or set(excluded) & set(entries):
        issues.append('Duplicate or selected exclusion IDs.')
    root = ET.parse(junit).getroot()
    if root.tag not in ('testsuite', 'testsuites'):
        raise ValueError('Expected testsuite or testsuites root.')
    cases = list(root.iter('testcase'))
    outcomes = {}
    for case in cases:
        name, classname = case.get('name'), case.get('classname', '')
        if not name:
            issues.append('Testcase missing name.')
            continue
        key = classname + '::' + name
        if key in outcomes:
            issues.append('Duplicate executed ID: ' + key)
        kinds = [tag for tag in ('failure', 'error', 'skipped') if case.find(tag) is not None]
        if len(kinds) > 1:
            issues.append('Conflicting outcomes: ' + key)
        outcomes[key] = kinds[0] if kinds else 'pass'
    for suite in root.iter():
        if suite.tag not in ('testsuite', 'testsuites'):
            continue
        descendants = list(suite.iter('testcase'))
        actual = {'tests': len(descendants)}
        actual.update({plural: sum(c.find(single) is not None for c in descendants)
                       for plural, single in [('failures', 'failure'), ('errors', 'error'), ('skipped', 'skipped')]})
        for key, value in actual.items():
            if suite.get(key) is not None:
                try:
                    valid = int(suite.get(key)) == value
                except ValueError:
                    valid = False
                if not valid:
                    issues.append('Inconsistent %s counter in %s.' % (key, suite.get('name', suite.tag)))
    event_evidence = None
    if (events is None) != (event_classname is None):
        raise ValueError('Raw events and their canonical classname must be supplied together.')
    if events is not None:
        if not isinstance(event_classname, str) or not event_classname:
            raise ValueError('A nonempty event classname is required.')
        started, terminal = set(), {}
        for line in Path(events).read_text().splitlines():
            try:
                event = json.loads(line)
            except ValueError:
                if line.lstrip().startswith('{'):
                    issues.append('Malformed raw JSON event.')
                continue
            if not isinstance(event, dict) or event.get('type') != 'test':
                continue
            name = event.get('name')
            if not isinstance(name, str) or not name:
                issues.append('Raw test event missing name.')
                continue
            key = event_classname + '::' + name
            kind = event.get('event')
            if kind == 'started':
                if key in started:
                    issues.append('Duplicate raw start event: ' + key)
                started.add(key)
            elif kind in ('ok', 'failed', 'ignored'):
                if key in terminal:
                    issues.append('Duplicate raw terminal event: ' + key)
                if kind != 'ignored' and key not in started:
                    issues.append('Raw terminal event has no preceding start: ' + key)
                terminal[key] = {'ok': 'pass', 'failed': 'failure', 'ignored': 'skipped'}[kind]
        for key in sorted(started - terminal.keys()):
            issues.append('Raw start event has no terminal outcome: ' + key)
        if terminal != outcomes:
            issues.append('JUnit outcomes differ from raw terminal events.')
        if not terminal:
            issues.append('No raw terminal events.')
        event_evidence = {'sha256': digest(events), 'terminal_count': len(terminal),
                          'format': 'rust-libtest-json', 'classname': event_classname}
    missing, unexpected = sorted(set(entries) - outcomes.keys()), sorted(outcomes.keys() - set(entries))
    if missing:
        issues.append('Discovered tests were not executed.')
    if unexpected:
        issues.append('Executed tests absent from discovery inventory.')
    counts = {kind: sum(v == kind for v in outcomes.values()) for kind in ('pass', 'failure', 'error', 'skipped')}
    if not cases:
        issues.append('No executed tests.')
    if counts['error']:
        issues.append('Infrastructure/test errors are not behavioral discrimination.')
    if counts['skipped']:
        issues.append('Selected tests were skipped.')
    if expected == 'pass':
        if exit_code != 0 or counts['failure']:
            issues.append('Expected successful process and passing cases.')
    elif expected == 'fail':
        if exit_code == 0 or not counts['failure']:
            issues.append('Expected nonzero process and at least one assertion failure.')
    else:
        raise ValueError('Expected must be pass or fail.')
    return {'status': 'FAIL' if issues else 'EXECUTION_RECONCILED', 'counts': counts,
            'selected': len(entries), 'executed': len(cases), 'missing': missing, 'unexpected': unexpected,
            'issues': issues, 'unverified_exclusions': exclusions, 'process_exit_code': exit_code,
            'expected': expected, 'junit_sha256': digest(junit), 'inventory_sha256': digest(inventory),
            'raw_event_evidence': event_evidence,
            'execution_provenance': 'raw events reconciled' if event_evidence else 'unverified: XML and inventory only',
            'limitation': 'Checks consistency of supplied reports, not their authenticity. Without raw execution evidence, '
                          'XML alone cannot establish that a reported failure executed. Inventory must come from actual '
                          'test discovery, not this JUnit. Assertion failures still need behavioral triage. '
                          'This does not measure coverage or prove private Shipd quality checks.'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--junit', required=True); p.add_argument('--inventory', required=True)
    p.add_argument('--exit-code', type=int, required=True)
    p.add_argument('--expected', choices=['pass', 'fail'], default='pass')
    p.add_argument('--output')
    p.add_argument('--events', help='Raw Rust libtest JSON stream, captured directly from the executable')
    p.add_argument('--event-classname', help='Canonical JUnit classname for raw libtest names')
    a = p.parse_args()
    try:
        result = check(a.junit, a.inventory, a.exit_code, a.expected, a.events, a.event_classname)
    except (OSError, ValueError, TypeError, AttributeError, ET.ParseError) as error:
        result = {'status': 'FAIL', 'issues': [str(error)]}
    value = json.dumps(result, indent=2) + '\n'
    if a.output:
        Path(a.output).write_text(value)
    print(value, end='')
    return 0 if result['status'] == 'EXECUTION_RECONCILED' else 2


if __name__ == '__main__':
    sys.exit(main())
