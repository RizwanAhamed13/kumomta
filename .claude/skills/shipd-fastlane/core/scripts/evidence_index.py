#!/usr/bin/env python3
"""Read-only Shipd evidence inventory. Never execute or extract candidate code."""
import argparse
import collections
import hashlib
import json
import os
from pathlib import Path
import re
import zipfile

PRUNE = {'.git', 'node_modules', 'target', 'build', '_build', 'dist', '.venv', 'venv',
         '__pycache__', '.cache', '.pytest_cache', '.ruff_cache', 'vendor', '.next'}
TEXT = {'.md', '.txt', '.json', '.jsonl', '.yaml', '.yml', '.toml', '.csv', '.log'}
ARTIFACT = {'.patch', '.diff', '.zip', '.tar', '.gz', '.tgz', '.pdf'}
PRIVATE = re.compile(r'(^|[._-])(secret|credential|password|cookie|token|private.key)([._-]|$)', re.I)
TAGS = {
    'contract': r'prompt|contract|description|fairness|over.?spec|unfair|representation',
    'discrimination': r'false.positive|mutant|discriminat|mask|baseline|fail.to.pass',
    'environment': r'docker|permission|ownership|toolchain|offline|platform|runner|junit',
    'runtime': r'cache|runtime|compile|build|seconds|minutes|sleep|flaki|race|timing',
    'hardness': r'hardness|scope|semantic|natural|LOC|too.easy|genuine|retire|rollout',
    'packaging': r'patch|untracked|collision|filename|artifact|hash|stale|snapshot',
    'state': r'lifecycle|state|identity|reopen|continuation|recovery|order|transaction',
}

def digest(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1024 * 1024), b''):
            h.update(b)
    return h.hexdigest()

def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')

def tags(text):
    return [k for k, pattern in TAGS.items() if re.search(pattern, text, re.I)]

def index(root, output):
    root, output = Path(root).resolve(), Path(output).resolve()
    files, skipped, errors, cases, lessons, archives = [], [], [], [], [], []
    source_roots = set()
    for base, dirs, names in os.walk(root, followlinks=False,
            onerror=lambda e: errors.append({'path': str(e.filename), 'error': str(e)})):
        folder = Path(base)
        keep = []
        for name in sorted(dirs):
            p = folder / name
            rel = p.relative_to(root).as_posix()
            reason = ('generated-output' if p.resolve() == output else
                      'symlink' if p.is_symlink() else
                      'build/dependency/VCS' if name in PRUNE else
                      'source-checkout-store' if rel in {'.olympus/repos', '.olympus/worktrees',
                         '.olympus/tmp', '.olympus/scratch', '.tmp-kumo-fix', '.kumo-gap-fix'} else None)
            # Inspect checkout-root delivery files while omitting implementation subtrees.
            if not reason and folder in source_roots and name not in {'artifacts', 'evidence', 'deliverables', 'delivery', '.olympus'}:
                reason = 'source-subtree'
            if not reason and (p / '.git').exists():
                source_roots.add(p)
            if reason:
                skipped.append({'path': rel, 'reason': reason})
            else:
                keep.append(name)
        dirs[:] = keep
        for name in sorted(names):
            p = folder / name
            rel = p.relative_to(root).as_posix()
            if p.is_symlink() or name.startswith('.env') or PRIVATE.search(name) or p.suffix in {'.pem', '.key'}:
                skipped.append({'path': rel, 'reason': 'symlink-or-private-name'})
                continue
            relevant = p.suffix.lower() in TEXT | ARTIFACT or name in {'Dockerfile', 'case.json', 'AGENTS.md'} or name.endswith('.sh')
            if not relevant:
                continue
            try:
                st = p.stat()
                item = {'path': rel, 'bytes': st.st_size, 'mtime_ns': st.st_mtime_ns,
                        'kind': 'artifact' if p.suffix in ARTIFACT or name == 'Dockerfile' else 'record'}
                if st.st_size <= 64 * 1024 * 1024:
                    item['sha256'] = digest(p)
                else:
                    item['hash_status'] = 'metadata-only: exceeds 64 MiB'
                files.append(item)
                if name == 'case.json':
                    obj = json.loads(p.read_text())
                    cases.append({'path': rel, 'record': obj})
                if name == 'lessons.md':
                    for line_no, line in enumerate(p.read_text(errors='replace').splitlines(), 1):
                        if re.match(r'^20\d\d-\d\d-\d\d\s*\|', line):
                            fields = [x.strip() for x in line.split('|', 4)]
                            lessons.append({'source': rel, 'line': line_no, 'date': fields[0],
                                'case': fields[1], 'text': line, 'tags': tags(line)})
                if p.suffix.lower() == '.zip':
                    with zipfile.ZipFile(p) as z:
                        entries = [{'path': e.filename, 'bytes': e.file_size,
                                    'compressed_bytes': e.compress_size, 'crc32': f'{e.CRC:08x}'}
                                   for e in z.infolist() if not e.is_dir()]
                        archives.append({'path': rel, 'entries': entries,
                            'note': 'Central directory only; CRC is not a cryptographic content hash. Not extracted.'})
            except (OSError, ValueError, zipfile.BadZipFile) as e:
                errors.append({'path': rel, 'error': type(e).__name__ + ': ' + str(e)})
    by_hash = collections.defaultdict(list)
    for f in files:
        if 'sha256' in f:
            by_hash[f['sha256']].append(f['path'])
    unique_lessons = {}
    for row in lessons:
        key = hashlib.sha256(row['text'].encode()).hexdigest()
        kept = unique_lessons.setdefault(key, {**row, 'provenance': []})
        kept['provenance'].append({'source': row['source'], 'line': row['line']})
    summary = {'root': str(root), 'files_indexed': len(files), 'bytes_indexed': sum(x['bytes'] for x in files),
        'artifact_files': sum(x['kind'] == 'artifact' for x in files), 'case_records': len(cases),
        'lesson_rows': len(lessons), 'unique_lesson_rows': len(unique_lessons),
        'archives': len(archives), 'archive_entries': sum(len(x['entries']) for x in archives),
        'duplicate_content_groups': sum(len(v) > 1 for v in by_hash.values()),
        'skipped_paths': len(skipped), 'errors': len(errors),
        'coverage': 'Artifact/record inventory, structured case records and full lesson rows. '
                    'Source checkouts, build/dependency trees, private-name files and symlinks excluded. '
                    'Archive payloads not extracted. Metadata inventory is not a semantic review of every file.'}
    for name, data in [('inventory', files), ('cases', cases), ('lessons', list(unique_lessons.values())),
                       ('archives', archives), ('skipped', skipped), ('errors', errors), ('summary', summary),
                       ('duplicates', {k: v for k, v in by_hash.items() if len(v) > 1})]:
        dump(output / (name + '.json'), data)
    return summary

def query(directory, term, limit):
    output = Path(directory)
    hits = []
    for name, field in [('lessons', 'text'), ('inventory', 'path')]:
        if not (output / (name + '.json')).exists():
            continue
        for row in json.loads((output / (name + '.json')).read_text()):
            if term.casefold() in row[field].casefold():
                hits.append({'type': name, **row})
    return {'matches': len(hits), 'shown': min(limit, len(hits)), 'results': hits[:limit]}

def revisions(directory):
    """Group stored delivery metadata; copies and mtimes do not prove iteration order."""
    output = Path(directory)
    inventory = json.loads((output / 'inventory.json').read_text())
    names = {'problem.md', 'solution.patch', 'test.patch', 'Dockerfile'}
    groups = collections.defaultdict(dict)
    patches = []
    for row in inventory:
        path = Path(row['path'])
        if path.name in names:
            groups[path.parent.as_posix()][path.name] = row
        if path.suffix.lower() in {'.patch', '.diff'}:
            patches.append(row)
    sets = []
    for directory, members in sorted(groups.items()):
        # Ignore lone documentation or build files unrelated to a saved patch.
        if not {'solution.patch', 'test.patch'}.intersection(members):
            continue
        missing = sorted(names - members.keys())
        hashes = {n: members[n].get('sha256') for n in sorted(members)}
        complete = not missing and all(hashes.values())
        identity = hashlib.sha256(json.dumps(hashes, sort_keys=True).encode()).hexdigest() if complete else None
        sets.append({'directory': directory, 'artifacts': members, 'missing': missing,
                     'four_file_content_id': identity,
                     'context': 'solver-or-rollout' if any(x in Path(directory).parts for x in ('rollouts', 'agents')) else 'unclassified-delivery'})
    result = {'artifact_sets': sets, 'patch_files': patches,
              'summary': {'saved_directories': len(sets), 'complete_four_file_directories': sum(x['four_file_content_id'] is not None for x in sets),
                          'distinct_complete_content_sets': len({x['four_file_content_id'] for x in sets if x['four_file_content_id']}),
                          'patch_files': len(patches), 'distinct_patch_hashes': len({x['sha256'] for x in patches if x.get('sha256')})},
              'limitations': 'Saved directories and distinct bytes, not verified chronological iterations, canonical reference identity or accepted submissions. Mtime is filesystem metadata. Archives are inventoried separately and not extracted.'}
    dump(output / 'revisions.json', result)
    return result['summary']

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest='cmd', required=True)
    p = subs.add_parser('index'); p.add_argument('root'); p.add_argument('output')
    p = subs.add_parser('query'); p.add_argument('directory'); p.add_argument('term'); p.add_argument('--limit', type=int, default=12)
    p = subs.add_parser('revisions'); p.add_argument('directory')
    a = parser.parse_args()
    if a.cmd == 'index':
        result = index(a.root, a.output)
    elif a.cmd == 'revisions':
        result = revisions(a.directory)
    else:
        result = query(a.directory, a.term, max(0, a.limit))
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
