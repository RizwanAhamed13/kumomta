#!/usr/bin/env python3
"""Compute evidence-bound Olympus rollout gates from classified runs."""

from __future__ import annotations

import argparse
import json
import math
import statistics
from collections import Counter
from pathlib import Path
from typing import Any


VALID_STATUSES = {"pass", "fail"}


def median(values: list[float]) -> float | None:
    return statistics.median(values) if values else None


def label(ok: bool) -> str:
    return "PASS" if ok else "NOT MET"


def wilson_interval(successes: int, total: int, z: float = 1.96) -> tuple[float, float] | None:
    if total == 0:
        return None
    proportion = successes / total
    denominator = 1 + z * z / total
    center = (proportion + z * z / (2 * total)) / denominator
    margin = z * math.sqrt((proportion * (1 - proportion) + z * z / (4 * total)) / total) / denominator
    return max(0.0, center - margin), min(1.0, center + margin)


def numeric_median(runs: list[dict[str, Any]], key: str) -> float | None:
    return median([float(run[key]) for run in runs if run.get(key) is not None])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("runs", type=Path, help="JSON array of rollout objects")
    parser.add_argument("--min-runs", type=int, required=True)
    parser.add_argument("--max-pass-rate", type=float, required=True)
    parser.add_argument("--min-loc", type=float, required=True)
    parser.add_argument("--min-files", type=float, required=True)
    parser.add_argument("--min-messages", type=float, required=True)
    parser.add_argument("--max-cheat-rate", type=float, required=True)
    parser.add_argument("--fast-minutes", type=float, default=20.0)
    parser.add_argument("--json", action="store_true", help="emit JSON instead of text")
    args = parser.parse_args()

    runs = json.loads(args.runs.read_text(encoding="utf-8"))
    if not isinstance(runs, list):
        raise SystemExit("runs JSON must be an array")
    for index, run in enumerate(runs):
        if not isinstance(run, dict) or "status" not in run:
            raise SystemExit(f"run {index} must be an object with status")

    valid = [run for run in runs if run.get("status") in VALID_STATUSES]
    passing = [run for run in valid if run.get("status") == "pass"]
    durable = [run for run in passing if run.get("false_positive_passed") is True]
    cheating = [run for run in valid if run.get("cheating") is True]
    blockers = [run for run in runs if run.get("environment_blocker") is True]
    contested = [run for run in runs if run.get("status") == "contested"]
    platform_failures = [run for run in runs if run.get("status") == "platform_failure"]

    valid_count = len(valid)
    pass_count = len(passing)
    pass_rate = pass_count / valid_count if valid_count else None
    cheat_rate = len(cheating) / valid_count if valid_count else None
    interval = wilson_interval(pass_count, valid_count)
    median_loc = numeric_median(passing, "loc")
    median_files = numeric_median(passing, "files")
    median_messages = numeric_median(passing, "messages")
    fp_ok = bool(passing) and len(durable) == len(passing)

    fingerprints = Counter(
        str(run["architecture_fingerprint"])
        for run in passing if run.get("architecture_fingerprint")
    )
    fast_passes = [
        run for run in passing
        if run.get("elapsed_minutes") is not None and float(run["elapsed_minutes"]) <= args.fast_minutes
    ]
    fast_fingerprints = Counter(
        str(run["architecture_fingerprint"])
        for run in fast_passes if run.get("architecture_fingerprint")
    )
    converged_fast = [fingerprint for fingerprint, count in fast_fingerprints.items() if count >= 2]

    complete = (
        valid_count >= args.min_runs
        and bool(passing)
        and pass_rate is not None and pass_rate <= args.max_pass_rate
        and cheat_rate is not None and cheat_rate < args.max_cheat_rate
        and not blockers
        and median_loc is not None and median_loc >= args.min_loc
        and median_files is not None and median_files >= args.min_files
        and median_messages is not None and median_messages >= args.min_messages
        and fp_ok
    )

    remaining = max(0, args.min_runs - valid_count)
    max_total_passes = math.floor(args.max_pass_rate * args.min_runs + 1e-9)
    additional_allowed = max_total_passes - pass_count
    early_signals: list[str] = []
    if converged_fast:
        early_signals.append("two or more fast genuine passes share an architecture fingerprint; pause and audit mechanical convergence")
    if len(passing) >= 3 and len(passing) == valid_count:
        early_signals.append("all first valid runs passed; pause before expanding the cohort")
    if valid_count >= 3 and not passing:
        early_signals.append("no genuine solve in the observed cohort; audit solvability and fairness")
    if blockers:
        early_signals.append("environment blockers exist; stop rollout spend until classified")
    if any(run.get("unfair") is True for run in runs):
        early_signals.append("an unfairness signal exists; stop and reproduce it")

    report = {
        "valid_runs": valid_count,
        "required_runs": args.min_runs,
        "passing_runs": pass_count,
        "durable_passing_runs": len(durable),
        "pass_rate": pass_rate,
        "pass_rate_wilson_95": interval,
        "cheat_rate": cheat_rate,
        "environment_blockers": len(blockers),
        "contested_runs": len(contested),
        "platform_failures": len(platform_failures),
        "median_passing_loc": median_loc,
        "median_passing_files": median_files,
        "median_passing_messages": median_messages,
        "fingerprints": dict(fingerprints),
        "remaining_valid_runs": remaining,
        "additional_passes_allowed_at_minimum_cohort": max(0, additional_allowed),
        "early_stop_signals": early_signals,
        "complete": complete,
    }

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        rate_text = "n/a" if pass_rate is None else f"{pass_rate:.1%}"
        interval_text = "n/a" if interval is None else f"{interval[0]:.1%}–{interval[1]:.1%}"
        cheat_text = "n/a" if cheat_rate is None else f"{cheat_rate:.1%}"
        print(f"Valid runs: {valid_count}/{args.min_runs} [{label(valid_count >= args.min_runs)}]")
        print(f"Passing runs: {pass_count}; pass rate: {rate_text}; Wilson 95%: {interval_text} [{label(bool(passing) and pass_rate is not None and pass_rate <= args.max_pass_rate)}]")
        print(f"Durable passes after FP review: {len(durable)}/{pass_count} [{label(fp_ok)}]")
        print(f"Cheating rate: {cheat_text} [{label(cheat_rate is not None and cheat_rate < args.max_cheat_rate)}]")
        print(f"Environment blockers: {len(blockers)} [{label(not blockers)}]")
        print(f"Median passing LOC: {median_loc} [{label(median_loc is not None and median_loc >= args.min_loc)}]")
        print(f"Median passing files: {median_files} [{label(median_files is not None and median_files >= args.min_files)}]")
        print(f"Median passing messages: {median_messages} [{label(median_messages is not None and median_messages >= args.min_messages)}]")
        if remaining:
            print(f"Remaining valid runs: {remaining}; at most {max(0, additional_allowed)} additional passes at the minimum cohort")
        for signal in early_signals:
            print(f"PAUSE: {signal}")
        print(f"Overall rollout gates: {label(complete)}")
    return 0 if complete else 1


if __name__ == "__main__":
    raise SystemExit(main())
