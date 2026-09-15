#!/usr/bin/env python3
"""Bounded Dockerfile checks from current general docs; never builds an image."""
import json
import re
import shlex

BASE = re.compile(r"public\.ecr\.aws/d3j8x8q7/olympus-base-[a-z0-9][a-z0-9-]*:latest\Z")
# This is a visible-command screen, not a shell evaluator or script call-graph audit.
TEST_COMMAND = re.compile(
    r"(?:^|[\s;&|])(?:cargo\s+(?:test\b|nextest\s+run\b)|"
    r"go\s+test\b|(?:python[0-9.]*\s+-m\s+)?pytest\b|"
    r"python[0-9.]*\s+-m\s+unittest\b|ctest\b|"
    r"(?:npm|pnpm|yarn)\s+(?:run\s+)?test\b|dotnet\s+test\b|"
    r"(?:mvn|gradle|gradlew|./gradlew)\s+(?:[^\s;&|]+\s+)*test\b|"
    r"(?:bundle\s+exec\s+)?rspec\b|(?:bash\s+|sh\s+)?(?:\./)?test\.sh\b)"
)

def check(text):
    issues, instructions = [], []
    pending, start = "", 0
    for number, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if stripped.lower().startswith("# escape=") and stripped.split("=", 1)[1] != "\\":
            issues.append("Non-default Docker escape directive needs a separate parser review.")
        if not stripped or stripped.startswith("#"):
            continue
        if not pending:
            start = number
        pending += stripped[:-1] + " " if stripped.endswith("\\") else stripped
        if stripped.endswith("\\"):
            continue
        match = re.match(r"([A-Za-z]+)\s+(.*)\Z", pending)
        if not match:
            issues.append(f"Line {start}: Docker instruction could not be statically parsed.")
        else:
            instructions.append((start, match[1].upper(), match[2]))
        pending = ""
    if pending:
        issues.append("Unterminated Docker continuation.")
    stages, current, from_count = {}, None, 0
    for line, op, body in instructions:
        if op == "FROM":
            from_count += 1
            try:
                args = shlex.split(body)
            except ValueError:
                args = []
            if args and args[0].startswith("--platform="):
                args = args[1:]
            if not args:
                issues.append(f"Line {line}: missing literal FROM image.")
                current = {"workdir": None, "cmd": None}
                continue
            base = args[0]
            if base in stages:
                current = dict(stages[base])
            else:
                current = {"workdir": None, "cmd": None}
                if not BASE.fullmatch(base):
                    issues.append(f"Line {line}: FROM must resolve literally to the required language-specific public.ecr.aws/d3j8x8q7/olympus-base-<language>:latest; no digest or other registry.")
            if len(args) == 3 and args[1].upper() == "AS":
                stages[args[2]] = current
            elif len(args) != 1:
                issues.append(f"Line {line}: unrecognized FROM options.")
        elif op in ("WORKDIR", "CMD"):
            if current is None:
                issues.append(f"Line {line}: {op} precedes FROM.")
            else:
                current[op.lower()] = body
        elif op == "RUN":
            if "<<" in body:
                issues.append(f"Line {line}: RUN heredoc requires manual command inspection; this parser cannot certify it.")
            visible = body
            if body.startswith("["):
                try:
                    args = json.loads(body)
                    if not isinstance(args, list) or not all(isinstance(x, str) for x in args):
                        raise ValueError("not a string array")
                    visible = " ".join(args)
                except ValueError:
                    issues.append(f"Line {line}: invalid RUN exec-form JSON.")
            if TEST_COMMAND.search(visible):
                issues.append(f"Line {line}: test commands in RUN are prohibited, including cargo test --no-run; compile with cargo build --tests when suitable.")
    if not from_count:
        issues.append("Missing FROM.")
    if current is None or current["workdir"] != "/app":
        issues.append("Final stage must use literal WORKDIR /app.")
    cmd = current.get("cmd") if current else None
    if cmd != "/bin/bash":
        try:
            valid = json.loads(cmd) == ["/bin/bash"] if cmd is not None else False
        except (ValueError, TypeError):
            valid = False
        if not valid:
            issues.append('Final CMD must be /bin/bash or ["/bin/bash"].')
    return {
        "status": "FAIL" if issues else "STATIC_DOCKER_CHECKS_PASS",
        "issues": issues,
        "checked": ["literal language-base latest tag", "final WORKDIR /app", "final CMD /bin/bash", "visible test commands in RUN"],
        "limitation": "General-doc static screen only. Verify the language against the current panel. This is not a complete Docker/shell parser, does not inspect invoked scripts or prove dependency hydration, clean unpatched build, runtime rematerialization, offline execution, or platform approval. Unsupported syntax must be reviewed before building."
    }
