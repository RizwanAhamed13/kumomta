#!/usr/bin/env python3
"""Deterministic fingerprints, conservative reuse advice, and usage checkpoints."""
import argparse
import datetime as dt
import hashlib
import json
import math
from pathlib import Path
import sys
import docker_contract

ARTIFACTS = ('problem.md', 'solution.patch', 'test.patch', 'Dockerfile')
DEPENDENCIES = {
    'alignment': {'problem', 'solution', 'test', 'repo'},
    'scope_semantics': {'problem', 'solution', 'scope_test', 'repo'},
    'patch_application': {'solution', 'test', 'repo'},
    'four_state_matrix': {'solution', 'test', 'docker', 'repo', 'environment', 'selection'},
    'flakiness': {'solution', 'test', 'docker', 'repo', 'environment', 'selection'},
    'test_quality': {'problem', 'solution', 'test', 'repo'},
    'solution_quality': {'problem', 'solution', 'test', 'docker', 'repo'},
    'rollout_replay': {'problem', 'solution', 'test', 'docker', 'repo', 'environment', 'selection'},
    'holistic_review': {'problem', 'solution', 'test', 'docker', 'scope_test', 'repo', 'environment', 'selection'},
    'freeze': {'problem', 'solution', 'test', 'docker', 'scope_test', 'repo', 'environment', 'selection'},
}

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def write(path, value):
    p = Path(path); p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, indent=2) + '\n')

def snapshot(directory, commit, environment, selection, scope_tests=None):
    root = Path(directory).resolve()
    if len(commit) != 40 or any(c not in '0123456789abcdefABCDEF' for c in commit):
        raise ValueError('Use the exact full 40-character repository commit.')
    env = json.loads(Path(environment).read_text())
    required = {'host', 'workdir', 'image_identity', 'toolchain', 'uid', 'build_flags'}
    if not isinstance(env, dict) or not required <= env.keys() or any(env[k] is None or env[k] == '' for k in required):
        raise ValueError('Environment must record: ' + ', '.join(sorted(required)))
    for name in ARTIFACTS:
        if not (root / name).is_file() or (root / name).is_symlink() or (root / name).stat().st_size == 0:
            raise ValueError('Missing, empty, or symlink artifact: ' + name)
    components = dict(zip(('problem', 'solution', 'test', 'docker'), [sha(root / n) for n in ARTIFACTS]))
    components.update(repo=commit.lower(), environment=hashlib.sha256(json.dumps(env, sort_keys=True).encode()).hexdigest(),
                      selection=sha(selection), scope_test=sha(scope_tests) if scope_tests else None)
    return {'schema': 1, 'captured_at': dt.datetime.now(dt.timezone.utc).isoformat(),
            'artifact_directory': str(root), 'components': components, 'environment': env,
            'note': 'Fingerprints only. This snapshot is not proof of passing any check.'}

def compare(before, after):
    a, b = before['components'], after['components']
    if not isinstance(a, dict) or not isinstance(b, dict):
        raise ValueError('Snapshot components must be objects.')
    def known(key, value):
        width = 40 if key == 'repo' else 64
        return isinstance(value, str) and len(value) == width and all(c in '0123456789abcdef' for c in value)
    changed = sorted(k for k in set(a) | set(b) if a.get(k) != b.get(k))
    unknown = {k for k in set().union(*DEPENDENCIES.values()) if not known(k, a.get(k)) or not known(k, b.get(k))}
    stale, reusable, unproven = {}, [], {}
    for gate, deps in DEPENDENCIES.items():
        hit = sorted(deps.intersection(changed))
        missing = sorted(deps.intersection(unknown))
        if hit:
            stale[gate] = hit
        elif missing:
            unproven[gate] = missing
        else:
            reusable.append(gate)
    return {'changed': changed, 'stale': stale, 'unknown': unproven,
            'eligible_for_evidence_reuse': reusable,
            'authority': 'Advice for saved local evidence only. Check its pass receipt, commands, completeness '
                         'and execution identity. The live Shipd panel controls paid-gate staleness. '
                         'Expanded test-only edits preserve scope semantics only when the reduced Scope '
                         'test bytes remain frozen and no behavior or reference change is concealed.'}

def unwrap(value):
    if not isinstance(value, dict):
        return {}
    if isinstance(value.get('content'), list):
        for item in value['content']:
            if not isinstance(item, dict):
                continue
            if item.get('type') == 'text':
                try:
                    obj = json.loads(item['text'])
                except (ValueError, KeyError):
                    continue
                if isinstance(obj, dict) and ('rateLimits' in obj or 'rateLimitsByLimitId' in obj):
                    return obj
    return value

def budget(value, maximum=50.0, reserve=10.0):
    if maximum is not None and (not math.isfinite(maximum) or not 0 < maximum <= 100 or not math.isfinite(reserve) or not 0 <= reserve < maximum):
        raise ValueError('Maximum must be in (0, 100]; reserve must be nonnegative and below maximum.')
    obj = unwrap(value)
    buckets = obj.get('rateLimitsByLimitId') or {}
    if not isinstance(buckets, dict):
        return {'decision': 'STOP', 'reason': 'Malformed usage buckets.'}
    main = buckets.get('codex') or obj.get('rateLimits')
    if not isinstance(main, dict):
        return {'decision': 'STOP', 'reason': 'Main Codex usage unavailable.'}
    if main.get('limitId') not in (None, 'codex'):
        return {'decision': 'STOP', 'reason': 'Available legacy bucket is not main Codex usage.'}
    windows = []
    for name in ('primary', 'secondary'):
        window = main.get(name)
        if window is None:
            continue
        if not isinstance(window, dict):
            return {'decision': 'STOP', 'reason': 'Malformed usage window.'}
        used = window.get('usedPercent')
        if isinstance(used, bool) or not isinstance(used, (int, float)) or not math.isfinite(used) or not 0 <= used <= 100:
            return {'decision': 'STOP', 'reason': 'A present usage window has invalid or unknown usage.'}
        windows.append({'window': name, 'used_percent': used, 'resets_at': window.get('resetsAt')})
    if not windows:
        return {'decision': 'STOP', 'reason': 'No measured main Codex usage windows.'}
    threshold = None if maximum is None else maximum - reserve
    blocked = main.get('spendControlReached') is True or main.get('rateLimitReachedType') is not None
    return {'decision': 'STOP' if blocked or (threshold is not None and max(w['used_percent'] for w in windows) >= threshold) else 'CONTINUE',
            'stop_at_used_percent': threshold, 'maximum_percent': maximum, 'windows': windows,
            'limitation': 'Account-wide checkpoint, not a task quota or hard enforcement. Reports may lag. '
                          'Check before expensive phases and after bounded work; never redeem a reset automatically.'}

def preflight(directory):
    root = Path(directory)
    issues = []
    for name in ARTIFACTS:
        p = root / name
        if not p.is_file() or p.is_symlink() or p.stat().st_size == 0:
            issues.append('Missing, empty, or symlink artifact: ' + name)
    for name in ('solution.patch', 'test.patch'):
        p = root / name
        if not p.is_file():
            continue
        headers = [s for s in p.read_text(errors='replace').splitlines() if s.startswith('diff --git ')]
        if not headers:
            issues.append(name + ': no git patch headers')
        if any(not s.startswith('diff --git a/') or ' b/' not in s for s in headers):
            issues.append(name + ': nonstandard diff prefixes')
    p = root / 'Dockerfile'
    docker = docker_contract.check(p.read_text()) if p.is_file() else None
    if docker:
        issues.extend(docker['issues'])
    return {'status': 'FAIL' if issues else 'STATIC_CHECKS_PASS', 'issues': issues,
            'docker_contract': docker,
            'remaining': 'Remote clean application, intended-file inventory, exact runner CLI, allowed '
                         'language image, role split, four-state matrix, alignment and required live gates.'}

def main():
    p = argparse.ArgumentParser(description=__doc__)
    s = p.add_subparsers(dest='cmd', required=True)
    q = s.add_parser('snapshot'); q.add_argument('directory'); q.add_argument('--commit', required=True)
    q.add_argument('--environment', required=True); q.add_argument('--selection', required=True)
    q.add_argument('--scope-tests'); q.add_argument('--output', required=True)
    q = s.add_parser('compare'); q.add_argument('before'); q.add_argument('after')
    q = s.add_parser('budget'); q.add_argument('usage_json')
    cap = q.add_mutually_exclusive_group()
    cap.add_argument('--maximum', type=float, default=50)
    cap.add_argument('--no-cap', action='store_true', help='Explicit user override: no workflow usage threshold; account limits still apply.')
    q.add_argument('--reserve', type=float, default=10)
    q = s.add_parser('preflight'); q.add_argument('directory')
    a = p.parse_args()
    try:
        if a.cmd == 'snapshot':
            result = snapshot(a.directory, a.commit, a.environment, a.selection, a.scope_tests)
            write(a.output, result)
        elif a.cmd == 'compare':
            result = compare(json.loads(Path(a.before).read_text()), json.loads(Path(a.after).read_text()))
        elif a.cmd == 'budget':
            result = budget(json.loads(Path(a.usage_json).read_text()), None if a.no_cap else a.maximum, a.reserve)
        else:
            result = preflight(a.directory)
        print(json.dumps(result, indent=2))
        if result.get('decision') == 'STOP' or result.get('status') == 'FAIL':
            return 2
    except (OSError, ValueError, KeyError, TypeError) as e:
        print(json.dumps({'error': str(e)}), file=sys.stderr)
        return 2
    return 0

if __name__ == '__main__':
    sys.exit(main())
