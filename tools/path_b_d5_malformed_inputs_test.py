#!/usr/bin/env python3
"""Adversarial type controls for pure D5 gates. No subprocess execution."""
import hashlib
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(__file__))
from path_b_d5_execution_preflight import preflight
from path_b_d5_execution_contract import evaluate

NOW = "2026-11-23T12:00:00Z"


def main():
    failures = []
    with tempfile.TemporaryDirectory(prefix="o42-d5-types-") as root:
        base = {"STATUS": "CERTIFIED", "PROCEDURE": "python3 -V", "CWD": ".",
                "CERTIFICATE": "CERT-9999", "RESULT SHA-256": "a" * 64}
        approval = {"certificate_id": "CERT-9999",
                    "procedure_sha256": hashlib.sha256(b"python3 -V").hexdigest(),
                    "approved_argv": ["python3", "-V"], "cwd": ".",
                    "approved_by": "SYNTHETIC ONLY",
                    "approval_scope": "single-certificate-read-only-review",
                    "expires_utc": "2026-11-24T12:00:00Z"}
        cases = [
            ("fields None", None),
            ("fields list", []),
            ("status None", dict(base, STATUS=None)),
            ("status list", dict(base, STATUS=[])),
            ("procedure None", dict(base, PROCEDURE=None)),
            ("procedure list", dict(base, PROCEDURE=[])),
            ("CWD None", dict(base, CWD=None)),
            ("CWD number", dict(base, CWD=123)),
            ("expected digest None", dict(base, **{"RESULT SHA-256": None})),
            ("expected digest list", dict(base, **{"RESULT SHA-256": []})),
        ]
        for label, fields in cases:
            try:
                _, issues = preflight(fields, root)
                _, contract_issues = evaluate(fields, approval, root, NOW)
                ok = bool(issues) and bool(contract_issues)
            except Exception as exc:
                ok = False
                issues = ["unexpected exception: " + repr(exc)]
            print("%s %s" % ("PASS" if ok else "FAIL", label))
            if not ok:
                failures.append(label + ": " + repr(issues))
    for failure in failures:
        print("FAIL: " + failure)
    print("D5 MALFORMED INPUTS: %d/%d %s (pure validation)" %
          (len(cases)-len(failures), len(cases), "PASS" if not failures else "FAIL"))
    return int(bool(failures))


if __name__ == "__main__":
    sys.exit(main())
