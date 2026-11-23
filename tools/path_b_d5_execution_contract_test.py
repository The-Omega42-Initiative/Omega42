#!/usr/bin/env python3
"""Synthetic D5 authorization-contract tests. No command execution."""
import hashlib
import os
import sys
import tempfile
sys.path.insert(0, os.path.dirname(__file__))
from path_b_d5_execution_contract import evaluate

NOW = "2026-11-23T12:00:00Z"


def main():
    failures = []
    with tempfile.TemporaryDirectory(prefix="o42-d5-contract-") as root:
        os.mkdir(os.path.join(root, "safe"))
        fields = {"CERTIFICATE": "CERT-9999", "STATUS": "CERTIFIED",
                  "PROCEDURE": "python3 -V", "CWD": "safe",
                  "RESULT SHA-256": "a" * 64}
        approval = {
            "certificate_id": "CERT-9999",
            "procedure_sha256": hashlib.sha256(b"python3 -V").hexdigest(),
            "cwd": "safe", "approved_argv": ["python3", "-V"],
            "approved_by": "SYNTHETIC TEST ONLY",
            "approval_scope": "single-certificate-read-only-review",
            "expires_utc": "2026-11-24T12:00:00Z",
        }
        cases = [
            ("complete synthetic contract", {}, {}, True),
            ("missing approval", {}, None, False),
            ("procedure changed", {"PROCEDURE": "python3 -VV"}, {}, False),
            ("CWD changed", {"CWD": "."}, {}, False),
            ("certificate changed", {"CERTIFICATE": "CERT-9998"}, {}, False),
            ("withdrawn", {"STATUS": "WITHDRAWN"}, {}, False),
            ("no output digest", {"RESULT SHA-256": ""}, {}, False),
            ("approval expired", {}, {"expires_utc": "2026-11-22T12:00:00Z"}, False),
            ("impossible expiry date", {}, {"expires_utc": "2026-02-30T12:00:00Z"}, False),
            ("impossible expiry hour", {}, {"expires_utc": "2026-11-24T25:00:00Z"}, False),
            ("expiry wrong type", {}, {"expires_utc": 12345}, False),
            ("approval wrong scope", {}, {"approval_scope": "all"}, False),
            ("approval wrong argv", {}, {"approved_argv": ["echo", "ok"]}, False),
            ("approval digest mismatch", {}, {"procedure_sha256": "0" * 64}, False),
            ("missing approver", {}, {"approved_by": ""}, False),
            ("argv wrong type", {}, {"approved_argv": "python3 -V"}, False),
        ]
        for name, changes, approval_changes, expected in cases:
            f = dict(fields, **changes)
            a = None if approval_changes is None else dict(approval, **approval_changes)
            ok, issues = evaluate(f, a, root, NOW)
            passed = ok == expected
            print("%s %s" % ("PASS" if passed else "FAIL", name))
            if not passed:
                failures.append(name + ": " + repr(issues))
        invalid_now, errors = evaluate(fields, approval, root, "not-a-time")
        if invalid_now or not any("current UTC time malformed" in x for x in errors):
            failures.append("malformed current UTC clock was not rejected")
        else:
            print("PASS malformed current UTC clock")
    for problem in failures:
        print("FAIL: " + problem)
    print("D5 AUTHORIZATION CONTRACT: %s (pure validation; no procedure execution)" %
          ("FAIL" if failures else "PASS"))
    return int(bool(failures))


if __name__ == "__main__":
    sys.exit(main())
