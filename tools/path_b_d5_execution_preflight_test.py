#!/usr/bin/env python3
"""Synthetic negative/positive controls for D5 preflight. No subprocess calls."""
import os
import sys
import tempfile
sys.path.insert(0, os.path.dirname(__file__))
from path_b_d5_execution_preflight import preflight


def main():
    failures = []
    with tempfile.TemporaryDirectory(prefix="o42-d5-preflight-") as root:
        os.mkdir(os.path.join(root, "safe"))
        cases = [
            ("safe argv", {"STATUS": "CERTIFIED", "PROCEDURE": "python3 -V", "CWD": "safe"}, True),
            ("shell chaining", {"STATUS": "CERTIFIED", "PROCEDURE": "echo ok; echo bad", "CWD": "safe"}, False),
            ("shell substitution", {"STATUS": "CERTIFIED", "PROCEDURE": "echo $(id)", "CWD": "safe"}, False),
            ("shell redirection", {"STATUS": "CERTIFIED", "PROCEDURE": "echo ok > file", "CWD": "safe"}, False),
            ("CWD traversal", {"STATUS": "CERTIFIED", "PROCEDURE": "python3 -V", "CWD": "../"}, False),
            ("absolute CWD", {"STATUS": "CERTIFIED", "PROCEDURE": "python3 -V", "CWD": root}, False),
            ("missing CWD", {"STATUS": "CERTIFIED", "PROCEDURE": "python3 -V", "CWD": "missing"}, False),
            ("registered not executable", {"STATUS": "REGISTERED", "PROCEDURE": "python3 -V", "CWD": "safe"}, False),
            ("withdrawn not executable", {"STATUS": "WITHDRAWN", "PROCEDURE": "python3 -V", "CWD": "safe"}, False),
            ("unknown status", {"STATUS": "CERTIFIED-ish", "PROCEDURE": "python3 -V", "CWD": "safe"}, False),
            ("unclosed quote", {"STATUS": "CERTIFIED", "PROCEDURE": "python3 '", "CWD": "safe"}, False),
        ]
        try:
            os.symlink(os.path.dirname(root), os.path.join(root, "escape"))
            cases.append(("symlink CWD escape", {"STATUS": "CERTIFIED", "PROCEDURE": "python3 -V", "CWD": "escape"}, False))
        except OSError:
            print("SKIP symlink escape control: symlink unavailable")
        for label, fields, expected in cases:
            argv, problems = preflight(fields, root=root)
            actual = not problems
            ok = actual == expected and (not expected or argv == ["python3", "-V"])
            print("%s %s" % ("PASS" if ok else "FAIL", label))
            if not ok:
                failures.append(label + " " + repr(problems))
    for f in failures:
        print("FAIL: " + f)
    print("D5 PREFLIGHT: %s (synthetic, no execution, not sandboxing)" %
          ("FAIL" if failures else "PASS"))
    return int(bool(failures))


if __name__ == "__main__":
    sys.exit(main())
