#!/usr/bin/env python3
"""Proposal-only D5 certificate execution preflight; NEVER runs a procedure.

Conservative preliminary policy, not canonical L-550 verification. Requires
review and approval before adoption. Rejects shell metacharacters and unsafe
working directories; does not claim to sandbox executable side effects.
"""
import os
import re
import shlex

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHELL_TOKENS = re.compile(r"[;&|<>\x60$\n\r]")
LIFECYCLE = ("CERTIFIED", "NOT CERTIFIED", "REGISTERED", "WITHDRAWN")


def preflight(fields, root=ROOT):
    issues = []
    if not isinstance(fields, dict):
        return [], ["certificate fields must be a mapping"]
    status_value = fields.get("STATUS", "")
    status = status_value.strip() if isinstance(status_value, str) else ""
    if status not in LIFECYCLE:
        issues.append("status must be exactly one recognized lifecycle value")
    elif status in ("REGISTERED", "WITHDRAWN"):
        issues.append("status %s is non-executable and cannot prove reproduction" % status)
    procedure = fields.get("PROCEDURE", "")
    if not isinstance(procedure, str) or not procedure.strip():
        issues.append("empty procedure")
        argv = []
    elif SHELL_TOKENS.search(procedure):
        issues.append("shell metacharacters or expansion forbidden")
        argv = []
    else:
        try:
            argv = shlex.split(procedure, posix=True)
        except ValueError:
            argv = []
            issues.append("malformed command quoting")
        if not argv:
            issues.append("procedure has no executable")
    cwd = fields.get("CWD", ".")
    if not isinstance(cwd, str) or not cwd or os.path.isabs(cwd):
        issues.append("CWD must be nonempty and relative to repository root")
    elif ".." in cwd.replace("\\", "/").split("/"):
        issues.append("CWD traversal forbidden")
    else:
        if not isinstance(root, (str, os.PathLike)):
            return argv, issues + ["repository root must be a path"]
        base = os.path.realpath(root)
        candidate = os.path.realpath(os.path.join(base, cwd))
        if os.path.commonpath((base, candidate)) != base:
            issues.append("CWD escapes repository root (including symlink resolution)")
        elif not os.path.isdir(candidate):
            issues.append("CWD does not exist")
    return argv, issues


if __name__ == "__main__":
    raise SystemExit("Library only: import preflight; never execute a certificate procedure")
