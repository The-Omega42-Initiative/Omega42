#!/usr/bin/env python3
"""Synthetic D5 provenance schema controls. No signatures or procedures."""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
from path_b_d5_approval_provenance import validate, SCHEMA

NOW = "2026-11-23T12:00:00Z"


def main():
    e = {"schema": SCHEMA, "repository_commit": "a"*64,
         "certificate_sha256": "b"*64, "procedure_sha256": "c"*64,
         "input_manifest_sha256": "d"*64, "sandbox_profile_sha256": "e"*64,
         "nonce": "nonce-unique-0001", "issued_utc": "2026-11-23T11:00:00Z",
         "expires_utc": "2026-11-23T13:00:00Z",
         "authority_id": "originator-id-placeholder",
         "signature_ref": "signature-not-verified-placeholder"}
    cases = [
        ("syntactically valid unverified envelope", {}, True),
        ("unknown field", {"extra": 1}, False),
        ("wrong commit digest", {"repository_commit": "a"*63}, False),
        ("wrong certificate digest", {"certificate_sha256": None}, False),
        ("missing sandbox profile", {"sandbox_profile_sha256": ""}, False),
        ("empty nonce", {"nonce": ""}, False),
        ("future issue", {"issued_utc": "2026-11-24T11:00:00Z"}, False),
        ("expired", {"expires_utc": "2026-11-23T11:30:00Z"}, False),
        ("overlong approval", {"expires_utc": "2026-11-25T13:00:00Z"}, False),
        ("impossible issue date", {"issued_utc": "2026-02-30T11:00:00Z"}, False),
        ("malformed authority", {"authority_id": "bad authority"}, False),
        ("malformed signature ref", {"signature_ref": 123}, False),
        ("wrong schema", {"schema": "unknown"}, False),
    ]
    failures = []
    for name, changes, should_pass in cases:
        candidate = dict(e, **changes)
        digest, issues = validate(candidate, NOW)
        ok = (digest is not None and not issues) == should_pass
        print("%s %s" % ("PASS" if ok else "FAIL", name))
        if not ok:
            failures.append(name + ": " + repr(issues))
    digest, issues = validate(None, NOW)
    if digest is not None or not issues:
        failures.append("non-mapping envelope accepted")
    else:
        print("PASS non-mapping envelope")
    digest, issues = validate({k:v for k,v in e.items() if k != "nonce"}, NOW)
    if digest is not None or not issues:
        failures.append("missing field accepted")
    else:
        print("PASS missing field")
    digest, issues = validate(e, "not-a-time")
    if digest is not None or not issues:
        failures.append("invalid clock accepted")
    else:
        print("PASS invalid clock")
    digest, issues = validate(e, NOW)
    reverse_digest, reverse_issues = validate(dict(reversed(list(e.items()))), NOW)
    if digest is None or digest != reverse_digest or issues or reverse_issues:
        failures.append("canonical digest order dependent")
    else:
        print("PASS canonical digest independent of field order")
    for problem in failures:
        print("FAIL: " + problem)
    print("D5 PROVENANCE SCHEMA: %s (NOT approval authentication)" %
          ("FAIL" if failures else "PASS"))
    return int(bool(failures))


if __name__ == "__main__":
    sys.exit(main())
