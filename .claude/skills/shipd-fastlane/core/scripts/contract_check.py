#!/usr/bin/env python3
"""Validate declared coverage cells and scenario witnesses, never execution coverage."""
import argparse
import json
from pathlib import Path
import sys


def strings(value):
    return (isinstance(value, list) and bool(value)
            and all(isinstance(x, str) and x.strip() for x in value)
            and len(value) == len(set(value)))


def text(value):
    return isinstance(value, str) and bool(value.strip())


def grounded(value):
    return (isinstance(value, dict) and value.get('kind') in ('prompt', 'pinned-repository')
            and text(value.get('source')))


def check(document, stage='full'):
    errors, gaps = [], []
    if stage not in ('full', 'scope') or not isinstance(document, dict):
        return {'status': 'FAIL', 'errors': ['Expected a contract object and full or scope stage.']}
    requirements, tests = document.get('requirements', []), document.get('tests', [])
    if (not isinstance(requirements, list) or not isinstance(tests, list)
            or any(not isinstance(r, dict) for r in requirements + tests)):
        return {'status': 'FAIL', 'errors': ['Requirements and tests must be lists of objects.']}
    if not requirements or not tests:
        errors.append('Requirements and tests must both be nonempty.')
    if not strings(document.get('inventory_sources')):
        gaps.append('Missing independent public inventory_sources (prompt and pinned public forms).')
    reqs, required_cells, excluded_cells = {}, set(), set()
    for r in requirements:
        rid = r.get('id')
        if not text(rid) or rid in reqs:
            errors.append('Missing or duplicate requirement ID.')
            continue
        reqs[rid] = r
        for field in ('statement', 'public_boundary'):
            if not text(r.get(field)):
                errors.append(f'{rid}: missing {field}')
        if not grounded(r.get('grounding')):
            errors.append(f'{rid}: grounding must cite prompt or pinned repository evidence')
        if not strings(r.get('input_classes')) or not strings(r.get('roles')):
            errors.append(f'{rid}: input_classes and roles must be nonempty unique strings')
            continue
        required_cells.update((rid, i, role) for i in r['input_classes'] for role in r['roles'])
        excluded = r.get('excluded_cells', [])
        if not isinstance(excluded, list):
            errors.append(f'{rid}: excluded_cells must be a list')
            continue
        for c in excluded:
            if not isinstance(c, dict) or not text(c.get('input_class')) or not text(c.get('role')):
                errors.append(f'{rid}: malformed excluded cell')
                continue
            cell = (rid, c['input_class'], c['role'])
            if cell not in required_cells or cell in excluded_cells:
                errors.append(f'{rid}: unknown or duplicate excluded cell')
            if not text(c.get('reason')) or not grounded(c.get('grounding')):
                errors.append(f'{rid}: exclusion needs an applicability reason and grounding')
            excluded_cells.add(cell)
    applicable = required_cells - excluded_cells

    def cells_for(covers, label):
        cells = set()
        if not isinstance(covers, list) or not covers:
            errors.append(f'{label}: covers must be a nonempty list')
            return cells
        for c in covers:
            if not isinstance(c, dict):
                errors.append(f'{label}: malformed coverage')
                continue
            rid = c.get('requirement')
            if not text(rid) or rid not in reqs:
                errors.append(f'{label}: orphaned requirement')
                continue
            if not strings(c.get('roles')) or not strings(c.get('input_classes')):
                errors.append(f'{label}: coverage roles and input_classes must be nonempty unique strings')
                continue
            declared = {(rid, i, role) for i in c['input_classes'] for role in c['roles']}
            if declared - required_cells:
                errors.append(f'{label}: coverage invents an undeclared role or input for {rid}')
            if declared & excluded_cells:
                errors.append(f'{label}: coverage contradicts an excluded cell for {rid}')
            cells.update(declared & applicable)
        return cells

    test_cells, covered = {}, set()
    for t in tests:
        tid = t.get('id')
        if not text(tid) or tid in test_cells:
            errors.append('Missing or duplicate test ID.')
            continue
        if t.get('mode') not in ('base', 'new'):
            errors.append(f'{tid}: mode must be base or new')
        if not isinstance(t.get('baseline_valid'), bool):
            errors.append(f'{tid}: baseline_valid must be a boolean')
        if t.get('mode') == 'new' and not text(t.get('solution_dependent_prerequisite')):
            errors.append(f'{tid}: new-mode test lacks a solution-dependent public prerequisite')
        if t.get('baseline_valid') is True and t.get('mode') == 'new':
            errors.append(f'{tid}: baseline-valid tests belong in base')
        for field in ('observable', 'assertion_location'):
            if not text(t.get(field)):
                errors.append(f'{tid}: missing {field}')
        if t.get('oracle') not in ('behavior', 'public-schema', 'pinned-regression'):
            errors.append(f'{tid}: unsupported oracle; private structure/prose layouts are not fair defaults')
        test_cells[tid] = cells_for(t.get('covers'), tid)
        covered.update(test_cells[tid])
    missing_cells = sorted(applicable - covered)
    for rid, family, role in missing_cells:
        gaps.append(f'{rid}: uncovered cell {family} / {role}')

    scenarios = document.get('scenarios', [])
    if not isinstance(scenarios, list):
        errors.append('scenarios must be a list')
        scenarios = []
    scenario_ids, witnessed = set(), set()
    for s in scenarios:
        if not isinstance(s, dict) or not text(s.get('id')) or s['id'] in scenario_ids:
            errors.append('Malformed scenario or missing/duplicate scenario ID.')
            continue
        sid = s['id']; scenario_ids.add(sid)
        if not strings(s.get('steps')) or len(s['steps']) < 2:
            errors.append(f'{sid}: describe at least a setup/action and an observation step')
        if not text(s.get('observable')) or not grounded(s.get('grounding')):
            errors.append(f'{sid}: scenario needs a public observable and grounding')
        expected = cells_for(s.get('covers'), sid)
        tid = s.get('test_id')
        if tid is not None and not text(tid):
            errors.append(f'{sid}: test_id must be a string or null while deferred')
            continue
        if tid not in test_cells:
            gaps.append(f'{sid}: needs one concrete test_id executing the whole scenario')
        elif expected - test_cells[tid]:
            gaps.append(f'{sid}: witness {tid} misses scenario cells; separate tests cannot substitute')
        else:
            witnessed.add(sid)

    reviews = document.get('risk_review', {})
    if not isinstance(reviews, dict):
        errors.append('risk_review must be an object')
        reviews = {}
    for kind in ('boundary', 'error', 'compatibility', 'interaction'):
        review = reviews.get(kind)
        if not isinstance(review, dict):
            gaps.append(f'{kind}: missing risk review')
            continue
        ids, na = review.get('scenario_ids'), review.get('not_applicable')
        if ids is not None and na is not None:
            errors.append(f'{kind}: use scenario_ids or a grounded not_applicable decision, not both')
        elif strings(ids):
            for sid in ids:
                if sid not in scenario_ids:
                    errors.append(f'{kind}: unknown scenario {sid}')
        elif isinstance(na, dict) and text(na.get('reason')) and grounded(na.get('grounding')):
            pass
        else:
            gaps.append(f'{kind}: name required scenarios or justify inapplicability with grounding')
    if stage == 'full':
        errors.extend(gaps)
    return {
        'status': 'FAIL' if errors else ('DECLARED_COVERAGE_PASS' if stage == 'full' else 'DECLARED_SCOPE_SLICE_PASS'),
        'stage': stage, 'errors': errors, 'deferred_to_full': gaps if stage == 'scope' else [],
        'requirements': len(requirements), 'tests': len(tests),
        'declared_cells': {'applicable': len(applicable), 'covered': len(covered),
                           'excluded': len(excluded_cells), 'missing': [list(c) for c in missing_cells]},
        'declared_scenarios': {'required': len(scenario_ids), 'witnessed': len(witnessed),
                               'missing': sorted(scenario_ids - witnessed)},
        'limitation': 'Self-declared graph validation only, not measured line/branch coverage or execution proof. '
                      'Independently inventory public forms, inspect witnesses and exclusions, and execute '
                      'the exact four-state matrix. A complete graph can still omit a whole public input family. '
                      'Scope status never satisfies the full-suite gate.'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('contract')
    p.add_argument('--stage', choices=('full', 'scope'), default='full')
    a = p.parse_args()
    try:
        result = check(json.loads(Path(a.contract).read_text()), a.stage)
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as e:
        result = {'status': 'FAIL', 'errors': [str(e)]}
    print(json.dumps(result, indent=2))
    return 2 if result['status'] == 'FAIL' else 0


if __name__ == '__main__':
    sys.exit(main())
