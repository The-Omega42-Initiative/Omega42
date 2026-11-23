#!/usr/bin/env python3
"""Synthetic D5 envelope/evidence cross-binding; no command execution."""
import hashlib
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
from path_b_d5_approval_provenance import SCHEMA
from path_b_d5_provenance_binding import bind

NOW = "2026-11-23T12:00:00Z"


def main():
    procedure = "python3 -V"
    envelope = {"schema": SCHEMA, "repository_commit": "a"*64,
                "certificate_sha256": "b"*64,
                "procedure_sha256": hashlib.sha256(procedure.encode()).hexdigest(),
                "input_manifest_sha256": "c"*64,
                "sandbox_profile_sha256": "d"*64,
                "nonce": "synthetic-nonce-0001",
                "issued_utc": "2026-11-23T11:00:00Z",
                "expires_utc": "2026-11-23T13:00:00Z",
                "authority_id": "untrusted-authority-placeholder",
                "signature_ref": "unverified-signature-reference"}
    evidence = {k: envelope[k] for k in
                ("repository_commit", "certificate_sha256",
                 "input_manifest_sha256", "sandbox_profile_sha256")}
    cases = [
        ("matching synthetic evidence", {"PROCEDURE": procedure}, evidence, True),
        ("altered procedure", {"PROCEDURE": "python3 -VV"}, evidence, False),
        ("non-string procedure", {"PROCEDURE": None}, evidence, False),
        ("missing procedure", {}, evidence, False),
        ("changed repository", {"PROCEDURE": procedure},
         dict(evidence, repository_commit="e"*64), False),
        ("changed certificate", {"PROCEDURE": procedure},
         dict(evidence, certificate_sha256="e"*64), False),
        ("changed input manifest", {"PROCEDURE": procedure},
         dict(evidence, input_manifest_sha256="e"*64), False),
        ("changed sandbox profile", {"PROCEDURE": procedure},
         dict(evidence, sandbox_profile_sha256="e"*64), False),
        ("missing evidence", {"PROCEDURE": procedure}, {}, False),
        ("invalid evidence", {"PROCEDURE": procedure},
         dict(evidence, certificate_sha256=None), False),
        ("non-mapping evidence", {"PROCEDURE": procedure}, None, False),
        ("non-mapping fields", None, evidence, False),
    ]
    failures = []
    for name, fields, supplied, should_match in cases:
        digest, issues = bind(fields, envelope, supplied, NOW)
        actual = digest is not None and not issues
        ok = actual == should_match
        print("%s %s" % ("PASS" if ok else "FAIL", name))
        if not ok:
            failures.append(name + ": " + repr(issues))
    altered = dict(envelope, procedure_sha256="0"*64)
    digest, issues = bind({"PROCEDURE": procedure}, altered, evidence, NOW)
    if digest is not None or not issues:
        failures.append("tampered envelope accepted")
    else:
        print("PASS tampered envelope")
    for problem in failures:
        print("FAIL: " + problem)
    print("D5 CROSS-BINDING: %s (no authenticated approval)" %
          ("FAIL" if failures else "PASS"))
    return int(bool(failures))


if __name__ == "__main__":
    sys.exit(main())
