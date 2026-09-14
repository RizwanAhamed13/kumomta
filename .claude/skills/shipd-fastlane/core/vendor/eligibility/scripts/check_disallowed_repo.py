#!/usr/bin/env python3
"""Fail closed when a GitHub repository is present in the Olympus denylist."""

from __future__ import annotations

import argparse
import csv
import hashlib
import re
import sys
from pathlib import Path


DEFAULT_LIST = Path(__file__).resolve().parent.parent / "references" / "disallowed_repos.csv"


def normalize(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"^(?:https?://)?github\.com/", "", value)
    value = value.rstrip("/")
    if value.endswith(".git"):
        value = value[:-4]
    parts = [part for part in value.split("/") if part]
    if len(parts) != 2:
        raise ValueError(f"expected GitHub owner/repo, got {value!r}")
    return "/".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True, help="GitHub owner/repo or repository URL")
    parser.add_argument("--list", type=Path, default=DEFAULT_LIST)
    args = parser.parse_args()

    try:
        raw = args.list.read_bytes()
        target = normalize(args.repo)
        entries: set[str] = set()
        for row in csv.reader(raw.decode("utf-8-sig").splitlines()):
            for cell in row:
                if cell.strip():
                    entries.add(normalize(cell))
    except (OSError, UnicodeError, csv.Error, ValueError) as error:
        print(f"REVIEW: denylist could not be validated: {error}", file=sys.stderr)
        return 2

    digest = hashlib.sha256(raw).hexdigest()
    if target in entries:
        print(f"DISALLOWED {target} list_sha256={digest}")
        return 3
    print(f"ALLOWED {target} list_sha256={digest} entries={len(entries)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
