#!/usr/bin/env python3
"""Validate independent audit receipts; never execute untrusted commands."""
import argparse
import json
import re
from pathlib import Path

VERDICTS = {"PASS", "FAIL", "INCONCLUSIVE", "NOT_EXECUTED", "SOURCE_REPORTED"}
SHA = re.compile(r"[0-9a-f]{40}")
DIGEST = re.compile(r"[0-9a-f]{64}")

def validate(receipts, rows, revision):
    if not SHA.fullmatch(revision):
        raise ValueError("Immutable revision required")
    index = {r["id"]: r for r in rows}
    seen = set()
    for receipt in receipts:
        ident = receipt["record_id"]
        if ident not in index or receipt["revision"] != revision:
            raise ValueError("Unknown record or mismatched revision")
        if receipt["certificate"] != index[ident]["tool"]:
            raise ValueError("Certificate mismatch")
        audit_id = receipt["audit_id"]
        if not isinstance(audit_id, str) or not audit_id.strip() or audit_id in seen:
            raise ValueError("Invalid or duplicate audit ID")
        seen.add(audit_id)
        verdict = receipt["verdict"]
        if verdict not in VERDICTS:
            raise ValueError("Unknown verdict")
        if verdict in {"PASS", "FAIL", "INCONCLUSIVE"}:
            for field in ("auditor", "environment", "command", "executed_at"):
                if not isinstance(receipt.get(field), str) or not receipt[field].strip():
                    raise ValueError("Missing execution provenance: " + field)
            if not DIGEST.fullmatch(receipt.get("output_sha256", "")):
                raise ValueError("Execution output digest required")
            if type(receipt.get("exit_code")) is not int:
                raise ValueError("Exit code required")
            if verdict == "PASS" and (receipt["exit_code"] != 0 or receipt.get("expected_marker_observed") is not True):
                raise ValueError("PASS requires successful exit and observed marker")
        elif receipt.get("exit_code") is not None or receipt.get("expected_marker_observed") is not None:
            raise ValueError("Non-execution receipt cannot assert execution results")
    return len(seen)

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("register", type=Path)
    p.add_argument("receipts", type=Path)
    p.add_argument("revision")
    a = p.parse_args()
    rows = json.loads(a.register.read_text(encoding="utf-8"))["results"]
    receipts = json.loads(a.receipts.read_text(encoding="utf-8"))
    print(f"Validated {validate(receipts, rows, a.revision)} receipt structures; no certificate executed or verdict authenticated.")
if __name__ == "__main__":
    main()
