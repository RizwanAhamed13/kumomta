#!/usr/bin/env python3
"""Fail closed while watching one explicitly owned Docker container."""
import argparse
import datetime
import json
import math
import pathlib
import re
import signal
import subprocess
import sys
import time


class Guard:
    def __init__(self, args):
        self.args = args
        self.log = pathlib.Path(args.log)
        self.log.parent.mkdir(parents=True, exist_ok=True)
        self.started = time.monotonic()
        self.identity = args.container if re.fullmatch(r"[0-9a-f]{64}", args.container) else None
        self.attached = False
        self.configured = False
        self.pause_started = None
        self.pause_seconds = 0.0
        self.closing = False

    def emit(self, action, **extra):
        record = dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                      container=self.identity or self.args.container, action=action, **extra)
        with self.log.open("a") as stream:
            stream.write(json.dumps(record) + "\n")

    def emergency_emit(self, action, **extra):
        try:
            self.emit(action, **extra)
        except Exception as error:
            print(json.dumps(dict(action=action, log_error=repr(error), **extra)),
                  file=sys.stderr, flush=True)

    def command(self, *args):
        return subprocess.run(args, capture_output=True, text=True, timeout=15)

    def inspect(self):
        result = self.command("docker", "inspect", self.identity or self.args.container)
        if result.returncode:
            raise RuntimeError("docker inspect failed: " + result.stderr.strip())
        info = json.loads(result.stdout)[0]
        if not isinstance(info["State"]["Running"], bool):
            raise RuntimeError("docker inspect returned an invalid Running state")
        if not re.fullmatch(r"[0-9a-f]{64}", info["Id"]):
            raise RuntimeError("docker inspect returned an invalid immutable ID")
        if self.identity is not None and info["Id"] != self.identity:
            raise RuntimeError("container identity changed")
        self.identity = info["Id"]
        return info

    def finish(self, reason):
        paused = self.pause_seconds
        if self.pause_started is not None:
            paused += time.monotonic() - self.pause_started
        wall = time.monotonic() - self.started
        self.emergency_emit("finished", reason=reason, wall_seconds=round(wall, 3),
                            thermal_pause_seconds=round(paused, 3),
                            active_elapsed_seconds=round(max(0, wall - paused), 3))

    def fail_closed(self, reason, code):
        if self.closing:
            return code
        self.closing = True
        self.emergency_emit("fail_closed", reason=reason)
        if self.identity is None:
            self.emergency_emit("fail_closed_no_resolved_identity")
        else:
            # Inspection failure never means completion. Attempt a pause on the
            # known immutable ID even when Docker cannot report its state.
            confirmed_stopped = False
            already_paused = False
            try:
                current = self.inspect()
                confirmed_stopped = not current["State"]["Running"]
                already_paused = current["State"].get("Paused", False)
            except Exception as error:
                self.emergency_emit("fail_closed_inspect_failed", diagnostic=repr(error))
            if confirmed_stopped:
                self.emergency_emit("fail_closed_confirmed_stopped")
            elif already_paused:
                self.emergency_emit("fail_closed_already_paused")
            else:
                try:
                    result = self.command("docker", "pause", self.identity)
                    self.emergency_emit("fail_closed_pause", returncode=result.returncode,
                                        diagnostic=result.stderr.strip())
                except Exception as error:
                    self.emergency_emit("fail_closed_pause_failed", diagnostic=repr(error))
        self.finish(reason)
        return code

    def interrupted(self, signum, _frame):
        self.emergency_emit("interrupted", signal=signum)
        raise SystemExit(self.fail_closed("guard_interrupted", 128 + signum))

    def temperature(self):
        result = self.command("sensors")
        if result.returncode:
            raise RuntimeError("sensors failed: " + result.stderr.strip())
        match = re.search(r"Package id 0:\s*\+([\d.]+)", result.stdout)
        if match is None:
            raise RuntimeError("CPU package temperature unavailable")
        value = float(match.group(1))
        if not math.isfinite(value):
            raise RuntimeError("CPU package temperature is not finite")
        return value

    def watch(self):
        while True:
            info = self.inspect()
            state = info["State"]
            if not self.attached:
                self.emit("attached", pre_existing_paused=state.get("Paused", False))
                self.attached = True
            if not state["Running"]:
                if state["Status"] == "created":
                    if time.monotonic() - self.started >= self.args.wait_start:
                        return self.fail_closed("start_timeout", 2)
                    time.sleep(self.args.interval)
                    continue
                self.finish("container_confirmed_stopped")
                return 0
            if not self.configured:
                flags = (["--cpus", str(self.args.cpus)]
                         if info["HostConfig"].get("NanoCpus", 0)
                         else ["--cpu-period", "100000", "--cpu-quota",
                               str(round(self.args.cpus * 100000))])
                result = self.command("docker", "update", *flags, self.identity)
                self.emit("quota_update", returncode=result.returncode,
                          cpus=self.args.cpus, diagnostic=result.stderr.strip())
                if result.returncode:
                    return self.fail_closed("quota_update_failed", 4)
                self.configured = True
            try:
                temp = self.temperature()
            except Exception as error:
                self.emergency_emit("sensor_read_failed", diagnostic=repr(error))
                return self.fail_closed("sensor_read_failed", 5)
            action = None
            if temp >= self.args.pause_at and not state.get("Paused", False):
                action = "pause"
            elif temp < self.args.resume_below and self.pause_started is not None:
                action = "unpause"
            if action is not None:
                result = self.command("docker", action, self.identity)
                self.emit(action, celsius=temp, returncode=result.returncode,
                          diagnostic=result.stderr.strip())
                if result.returncode:
                    return self.fail_closed(action + "_failed", 6)
                if action == "pause":
                    self.pause_started = time.monotonic()
                else:
                    elapsed = time.monotonic() - self.pause_started
                    self.pause_seconds += elapsed
                    self.pause_started = None
                    self.emit("thermal_wait", seconds=round(elapsed, 3))
            else:
                self.emit("sample", celsius=temp, paused=state.get("Paused", False))
            time.sleep(self.args.interval)

    def run(self):
        signal.signal(signal.SIGTERM, self.interrupted)
        signal.signal(signal.SIGINT, self.interrupted)
        try:
            return self.watch()
        except Exception as error:
            self.emergency_emit("watcher_error", diagnostic=repr(error))
            return self.fail_closed("watcher_error", 7)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--container", required=True)
    parser.add_argument("--log", required=True)
    parser.add_argument("--cpus", type=float, default=.5)
    parser.add_argument("--pause-at", type=float, default=75)
    parser.add_argument("--resume-below", type=float, default=65)
    parser.add_argument("--interval", type=float, default=3)
    parser.add_argument("--wait-start", type=float, default=300)
    args = parser.parse_args()
    numeric = [args.cpus, args.pause_at, args.resume_below, args.interval, args.wait_start]
    if (not all(math.isfinite(value) for value in numeric) or args.cpus <= 0 or
            args.interval <= 0 or args.wait_start < 0 or args.pause_at <= args.resume_below):
        parser.error("finite positive quota/interval and pause-at > resume-below are required")
    return Guard(args).run()


if __name__ == "__main__":
    sys.exit(main())
