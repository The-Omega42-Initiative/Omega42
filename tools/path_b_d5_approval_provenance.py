#!/usr/bin/env python3
"""Pure D5 approval-provenance envelope validator. NO signature verification.

A valid envelope is a well-formed *request for independent verification*, not
authenticated Originator consent, authorization or permission to execute.
"""
import datetime
import hashlib
import json
import re

HEX = re.compile(r"^[0-9a-f]{64}$")
UTC = re.compile(r"^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ$")
FIELDS = ("schema", "repository_commit", "certificate_sha256", "procedure_sha256",
          "input_manifest_sha256", "sandbox_profile_sha256", "nonce",
          "issued_utc", "expires_utc", "authority_id", "signature_ref")
SCHEMA = "omega42-d5-approval-envelope-v0-proposal"


def parse_utc(value):
    if not isinstance(value, str) or not UTC.fullmatch(value):
        return None
    try:
        return datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S%z")
    except ValueError:
        return None


def validate(envelope, now_utc):
    """Return (canonical_digest_or_None, issues); never validate signatures."""
    issues = []
    if not isinstance(envelope, dict):
        return None, ["envelope must be a mapping"]
    missing = set(FIELDS) - set(envelope)
    unknown = set(envelope) - set(FIELDS)
    if missing:
        issues.append("missing fields: " + ",".join(sorted(missing)))
    if unknown:
        issues.append("unexpected fields: " + ",".join(sorted(unknown)))
    if missing or unknown:
        return None, issues
    if envelope["schema"] != SCHEMA:
        issues.append("unsupported schema")
    for name in ("repository_commit", "certificate_sha256", "procedure_sha256",
                 "input_manifest_sha256", "sandbox_profile_sha256"):
        value = envelope[name]
        if not isinstance(value, str) or not HEX.fullmatch(value):
            issues.append("invalid " + name)
    for name in ("nonce", "authority_id", "signature_ref"):
        value = envelope[name]
        if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9._:/-]{8,256}", value):
            issues.append("invalid " + name)
    issued = parse_utc(envelope["issued_utc"])
    expires = parse_utc(envelope["expires_utc"])
    now = parse_utc(now_utc)
    if issued is None or expires is None or now is None:
        issues.append("invalid UTC timestamp")
    else:
        if issued > now:
            issues.append("approval issued in future")
        if expires <= now or expires <= issued:
            issues.append("approval expired or invalid interval")
        if expires - issued > datetime.timedelta(hours=24):
            issues.append("approval lifetime exceeds 24 hours")
    if issues:
        return None, issues
    canonical = json.dumps(envelope, sort_keys=True, separators=(",", ":"),
                           ensure_ascii=True, allow_nan=False).encode("ascii")
    return hashlib.sha256(canonical).hexdigest(), []


if __name__ == "__main__":
    raise SystemExit("Library only. Never authenticates approvals or executes procedures.")
