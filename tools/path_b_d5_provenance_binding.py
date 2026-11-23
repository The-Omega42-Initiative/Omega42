#!/usr/bin/env python3
"""Pure D5 provenance cross-binding: no signature verification or execution.

An envelope match is only a structural consistency check. It cannot establish
authority, replay safety, filesystem isolation, or permission to execute.
"""
import hashlib
import re

from path_b_d5_approval_provenance import validate

HEX = re.compile(r"^[0-9a-f]{64}$")


def bind(fields, envelope, evidence, now_utc):
    """Return (envelope_digest_or_None, issues), never an execution permit.

    evidence must come from an independently established immutable checkout
    and certificate-byte source. This function cannot attest its provenance.
    """
    digest, issues = validate(envelope, now_utc)
    if issues:
        return None, issues
    if not isinstance(fields, dict) or not isinstance(evidence, dict):
        return None, ["certificate fields and evidence must be mappings"]
    expected_keys = ("repository_commit", "certificate_sha256",
                     "input_manifest_sha256", "sandbox_profile_sha256")
    for key in expected_keys:
        value = evidence.get(key)
        if not isinstance(value, str) or not HEX.fullmatch(value):
            issues.append("invalid evidence " + key)
        elif value != envelope[key]:
            issues.append("evidence mismatch " + key)
    procedure = fields.get("PROCEDURE")
    if not isinstance(procedure, str):
        issues.append("procedure must be text")
    elif hashlib.sha256(procedure.encode("utf-8")).hexdigest() != envelope["procedure_sha256"]:
        issues.append("procedure mismatch")
    if issues:
        return None, issues
    return digest, []


if __name__ == "__main__":
    raise SystemExit("Pure validation only; never authorizes or executes.")
