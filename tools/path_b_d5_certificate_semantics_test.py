#!/usr/bin/env python3
"""Safe D5 boundary characterization. Never executes certificate PROCEDURE text.

This test monkeypatches certify.run_procedure before calling verify(). It
characterizes current semantics only; it is not a D5 execution test.
"""
import hashlib
import inspect
import os
import re
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import certify


def filled_certificate(status, digest):
    text = certify.skeleton("D5 safe boundary characterization")
    text = text.replace("[FILL: four digits]", "9997")
    text = text.replace("[FILL: " + " / ".join(certify.KINDS) + "]", "COMPUTATIONAL")
    text = text.replace("[FILL: the command anyone can run]", "THIS_COMMAND_MUST_NEVER_RUN")
    text = text.replace("[FILL: the folder it runs in, or .]", ".")
    text = text.replace("[FILL: SHA-256 of the procedure's output]", digest)
    text = text.replace("[FILL: " + " / ".join(certify.STATUSES) + "]", status)
    return re.sub(r"\\[FILL: [^\\]]*\\]", "x", text)


def main():
    failures = []
    expected = hashlib.sha256(b"expected stdout\\n").hexdigest()
    original = certify.run_procedure
    with tempfile.TemporaryDirectory(prefix="omega42-d5-safe-boundary-") as d:
        path = os.path.join(d, "synthetic-certificate.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write(filled_certificate("CERTIFIED", expected))

        calls = []
        certify.run_procedure = lambda fields: (expected, 17)
        ok, message = certify.verify(path)
        nonzero_ignored = ok and "REPRODUCED" in message
        print("Matching stdout digest with exit code 17 reported reproduced: %s" %
              ("KNOWN DEFECT REPRODUCED" if nonzero_ignored else "NOT REPRODUCED"))
        if not nonzero_ignored:
            failures.append("nonzero exit-code behavior changed; review audit")

        def forbidden(fields):
            calls.append(fields)
            raise AssertionError("procedure execution must not occur in this test")

        certify.run_procedure = forbidden
        for status in ("REGISTERED", "WITHDRAWN"):
            with open(path, "w", encoding="utf-8") as f:
                f.write(filled_certificate(status, expected))
            ok, message = certify.verify(path)
            lifecycle_ok = ok and "not rerun" in message and not calls
            print("%s status returns lifecycle success without running procedure: %s" %
                  (status, "CONFIRMED" if lifecycle_ok else "UNEXPECTED"))
            if not lifecycle_ok:
                failures.append(status + " lifecycle behavior changed or executed")

    certify.run_procedure = original
    source = inspect.getsource(certify.run_procedure)
    shell = "shell=True" in source
    timeout = "timeout=" in source
    cwd_join = "os.path.join(ROOT, f.get('CWD', '.'))" in source
    print("Procedure runner uses shell=True: %s" % ("CONFIRMED" if shell else "NOT FOUND"))
    print("Procedure runner sets timeout: %s" % ("PRESENT" if timeout else "ABSENT"))
    print("Procedure runner joins CWD to repository root without visible resolved-path containment: %s" %
          ("CONFIRMED" if cwd_join else "NOT REPRODUCED"))
    if not shell or timeout or not cwd_join:
        failures.append("static execution-boundary source shape changed; audit required")

    print("D5 SAFE BOUNDARY CHARACTERIZATION: %s" %
          ("PASS — known boundary defects reproduced; no procedure executed" if not failures else "FAIL"))
    for failure in failures:
        print(" - " + failure)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
