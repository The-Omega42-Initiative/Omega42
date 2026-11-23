#!/usr/bin/env python3
"""Fail-closed AST guard for proposal-only D5 pure validation modules.

Rejects direct execution APIs, dynamic imports, eval/exec and filesystem writes
in the designated D5 pure modules. Static guard only: not a sandbox, not proof
of absence of all side effects or safe execution.
"""
import ast
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PURE = (
    "tools/path_b_d5_execution_preflight.py",
    "tools/path_b_d5_execution_contract.py",
    "tools/path_b_d5_result_semantics.py",
)
BLOCKED_MODULES = {"subprocess", "socket", "requests", "urllib", "ctypes",
                   "multiprocessing", "importlib", "runpy", "asyncio"}
BLOCKED_CALLS = {"eval", "exec", "compile", "__import__", "open", "setattr",
                 "delattr", "getattr", "globals", "locals", "vars"}
BLOCKED_ATTRIBUTES = {"system", "popen", "spawn", "fork", "execv", "execve",
                      "remove", "unlink", "rmdir", "rename", "replace",
                      "write_text", "write_bytes", "mkdir", "makedirs",
                      "chmod", "chown", "run", "Popen", "check_call",
                      "check_output", "call"}


def violations(source):
    tree = ast.parse(source)
    errors = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.split(".")[0] in BLOCKED_MODULES:
                    errors.append("blocked import: " + alias.name)
        if isinstance(node, ast.ImportFrom) and node.module:
            if node.module.split(".")[0] in BLOCKED_MODULES:
                errors.append("blocked from-import: " + node.module)
        if isinstance(node, ast.Call):
            f = node.func
            if isinstance(f, ast.Name) and f.id in BLOCKED_CALLS:
                errors.append("blocked call: " + f.id)
            if isinstance(f, ast.Attribute) and f.attr in BLOCKED_ATTRIBUTES:
                errors.append("blocked attribute call: " + f.attr)
    return errors


def main():
    failures = []
    for path in PURE:
        with open(os.path.join(ROOT, path), encoding="utf-8") as handle:
            errors = violations(handle.read())
        print("%s %s" % ("PASS" if not errors else "FAIL", path))
        failures.extend(path + ": " + e for e in errors)
    adversarial = (
        ("subprocess import", "import subprocess\n", True),
        ("from subprocess", "from subprocess import run\n", True),
        ("dynamic import", "__import__('subprocess')\n", True),
        ("shell execution", "import os\nos.system('echo no')\n", True),
        ("file write", "open('x','w')\n", True),
        ("attribute subprocess", "runner.run(['echo'])\n", True),
        ("safe hashing", "import hashlib\nhashlib.sha256(b'abc')\n", False),
    )
    for label, code, should_reject in adversarial:
        actual = bool(violations(code))
        ok = actual == should_reject
        print("%s guard fixture: %s" % ("PASS" if ok else "FAIL", label))
        if not ok:
            failures.append("guard fixture failed: " + label)
    for issue in failures:
        print("FAIL: " + issue)
    print("D5 STATIC NO-EXECUTION GUARD: %s (AST only; not a sandbox)" %
          ("FAIL" if failures else "PASS"))
    return int(bool(failures))


if __name__ == "__main__":
    sys.exit(main())
