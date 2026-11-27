"""Build a public audit index from explicitly human-approved receipts only.

Input receipts remain private. Output contains no auditor identity, command,
environment, raw output or free-text submission. Approval is a trusted local
review input, not a field supplied by the contributor.
"""
import argparse
import json
from pathlib import Path
from validate_audit_receipts import validate

def build_index(rows, receipts, approvals, revision):
    validate(receipts, rows, revision)
    by_id = {r["audit_id"]: r for r in receipts}
    seen = set()
    result = {r["id"]: {"inherited_status": r["status"], "audits": []} for r in rows}
    for approval in approvals:
        ident = approval["audit_id"]
        if ident in seen or ident not in by_id:
            raise ValueError("Duplicate or unknown approval")
        seen.add(ident)
        receipt = by_id[ident]
        if approval.get("revision") != revision or approval.get("verdict") != receipt["verdict"]:
            raise ValueError("Approval does not match receipt")
        if approval.get("public_consent") is not True or approval.get("review_status") != "HUMAN_APPROVED":
            raise ValueError("Publication requires consent and human approval")
        result[receipt["record_id"]]["audits"].append({
            "verdict": receipt["verdict"],
            "review_status": "HUMAN_APPROVED",
            "evidence_status": "REVIEWED_RECEIPT_NOT_LOCAL_EXECUTION"
        })
    return {"revision": revision, "records": result}

def main():
    p = argparse.ArgumentParser(description=__doc__)
    for name in ("register", "receipts", "approvals", "output"):
        p.add_argument(name, type=Path)
    p.add_argument("revision")
    a = p.parse_args()
    def read(path):
        return json.loads(path.read_text(encoding="utf-8"))
    index = build_index(read(a.register)["results"], read(a.receipts), read(a.approvals), a.revision)
    a.output.write_text(json.dumps(index, ensure_ascii=False, sort_keys=True, indent=2)+"\n", encoding="utf-8")
if __name__ == "__main__":
    main()
