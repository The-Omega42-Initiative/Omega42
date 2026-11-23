#!/usr/bin/env python3
"""D5 raw-byte result classification controls; never runs subprocesses."""
import hashlib
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
from path_b_d5_result_semantics import classify


def main():
    good = hashlib.sha256(b"42\n").hexdigest()
    obs = {"exit_code": 0, "stdout": b"42\n", "timed_out": False, "truncated": False}
    cases = [
        ("exact successful reproduction", "CERTIFIED", good, obs, "VERIFIED"),
        ("not certified cannot upgrade", "NOT CERTIFIED", good, obs, "NOT_CERTIFIED"),
        ("registered never rerun", "REGISTERED", good, obs, "SKIPPED"),
        ("withdrawn never rerun", "WITHDRAWN", good, obs, "SKIPPED"),
        ("no observation", "CERTIFIED", good, None, "NOT_RUN"),
        ("nonzero exit even matching stdout", "CERTIFIED", good, dict(obs, exit_code=1), "FAILED"),
        ("bool exit code rejected", "CERTIFIED", good, dict(obs, exit_code=False), "FAILED"),
        ("timeout rejected", "CERTIFIED", good, dict(obs, timed_out=True), "FAILED"),
        ("missing timeout metadata rejected", "CERTIFIED", good,
         {"exit_code": 0, "stdout": b"42\n", "truncated": False}, "FAILED"),
        ("truncated output rejected", "CERTIFIED", good, dict(obs, truncated=True), "FAILED"),
        ("missing truncation metadata rejected", "CERTIFIED", good,
         {"exit_code": 0, "stdout": b"42\n", "timed_out": False}, "FAILED"),
        ("digest mismatch", "CERTIFIED", good, dict(obs, stdout=b"41\n"), "MISMATCH"),
        ("newline difference", "CERTIFIED", good, dict(obs, stdout=b"42"), "MISMATCH"),
        ("unicode bytes differ", "CERTIFIED", good, dict(obs, stdout="42\n"), "INVALID"),
        ("missing expected digest", "CERTIFIED", "", obs, "INVALID"),
        ("invalid lifecycle", "OTHER", good, obs, "INVALID"),
        ("invalid observation", "CERTIFIED", good, [], "INVALID"),
    ]
    failures = []
    for name, status, digest, observation, expected in cases:
        actual, reason = classify(status, digest, observation)
        ok = actual == expected
        print("%s %-46s %s" % ("PASS" if ok else "FAIL", name, actual))
        if not ok:
            failures.append("%s: expected %s, got %s (%s)" % (name, expected, actual, reason))
    for problem in failures:
        print("FAIL: " + problem)
    print("D5 RESULT SEMANTICS: %d/%d %s (no procedure execution)" %
          (len(cases) - len(failures), len(cases), "PASS" if not failures else "FAIL"))
    return int(bool(failures))


if __name__ == "__main__":
    sys.exit(main())
