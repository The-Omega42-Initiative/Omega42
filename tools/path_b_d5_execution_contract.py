#!/usr/bin/env python3
"""Proposal-only D5 execution authorization contract (pure validation, no execution).

An explicit approval record is required even after the command preflight.
This module NEVER calls subprocess or certificate verify. A passing contract
does NOT guarantee an executable's safety; isolation is a separate requirement.
"""
import datetime
import hashlib
import re

from path_b_d5_execution_preflight import preflight

HEX = re.compile(r"^[0-9a-f]{64}$")
REQUIRED_APPROVAL = ("certificate_id", "procedure_sha256", "cwd", "approved_argv",
                     "approved_by", "approval_scope", "expires_utc")


def evaluate(fields, approval, root, now_utc):
    """Return (approved, issues) without executing or modifying anything.

    The approval must be supplied independently by an authorized reviewer;
    this function does NOT authenticate identities or approval signatures.
    """
    argv, issues = preflight(fields, root=root)
    issues = list(issues)
    if not isinstance(approval, dict):
        return False, issues + ["approval record missing or invalid"]
    for key in REQUIRED_APPROVAL:
        if key not in approval:
            issues.append("approval missing " + key)
    if issues:
        return False, issues
    if not isinstance(fields.get("PROCEDURE"), str):
        return False, issues + ["procedure must be text"]
    procedure = fields["PROCEDURE"]
    digest = hashlib.sha256(procedure.encode("utf-8")).hexdigest()
    if approval["procedure_sha256"] != digest:
        issues.append("approved procedure digest mismatch")
    if approval["approved_argv"] != argv:
        issues.append("approved argv mismatch")
    if approval["cwd"] != fields.get("CWD", "."):
        issues.append("approved CWD mismatch")
    if approval["certificate_id"] != fields.get("CERTIFICATE"):
        issues.append("approved certificate ID mismatch")
    if approval["approval_scope"] != "single-certificate-read-only-review":
        issues.append("approval scope not restricted to single-certificate review")
    if not isinstance(approval["approved_by"], str) or not approval["approved_by"].strip():
        issues.append("approver identity absent")
    def parse_utc(value):
        if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ", value):
            return None
        try:
            return datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S%z")
        except ValueError:
            return None
    expiry = parse_utc(approval["expires_utc"])
    now = parse_utc(now_utc)
    if expiry is None:
        issues.append("approval expiry malformed or impossible date")
    if now is None:
        issues.append("current UTC time malformed or impossible date")
    if expiry is not None and now is not None and expiry <= now:
        issues.append("approval expired")
    expected = fields.get("RESULT SHA-256", "")
    if not isinstance(expected, str) or not HEX.fullmatch(expected):
        issues.append("expected output digest missing or invalid")
    # This is a request-review gate only. No executable allowlist, sandbox,
    # network isolation, resource limits, or cryptographic approval validation.
    return not issues, issues


if __name__ == "__main__":
    raise SystemExit("Library only. No certificate execution is implemented.")
