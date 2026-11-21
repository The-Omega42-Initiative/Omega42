#!/usr/bin/env python3
"""K5 proof-obligation register linter.

Checks schema, unique identifiers, known dependency references, and acyclicity.
It does NOT check proof validity, prove a theorem, or promote claim status.
"""
import json
import sys
from pathlib import Path

ALLOWED = {
    "reconstructed-proof", "deduced", "computed", "source-reported",
    "review-required", "open", "conjecture", "interpretation"
}

def audit(data):
    errors = []
    if not isinstance(data, dict):
        return {"valid": False, "errors": ["root must be an object"]}
    if data.get("schema") != "omega42.proof-obligations.k5":
        errors.append("unsupported schema")
    convention = data.get("convention")
    if not isinstance(convention, dict):
        errors.append("convention must be an object")
    else:
        if convention.get("relation") != "n=2d":
            errors.append("canonical depth relation must be n=2d")
        if convention.get("modulus") != "3^n=9^d":
            errors.append("modulus convention must be 3^n=9^d")
    items = data.get("obligations")
    if not isinstance(items, list):
        errors.append("obligations must be an array")
        items = []
    by_id = {}
    for i, item in enumerate(items):
        if not isinstance(item, dict):
            errors.append(f"obligation {i} must be an object")
            continue
        ident = item.get("id")
        if not isinstance(ident, str) or not ident.strip():
            errors.append(f"obligation {i} needs a non-empty id")
            continue
        if ident in by_id:
            errors.append(f"duplicate obligation id: {ident}")
        by_id[ident] = item
        if item.get("status") not in ALLOWED:
            errors.append(f"{ident}: invalid status")
        if not isinstance(item.get("title"), str) or not item["title"].strip():
            errors.append(f"{ident}: missing title")
        if not isinstance(item.get("claim"), str) or not item["claim"].strip():
            errors.append(f"{ident}: missing claim")
        deps = item.get("dependsOn")
        if not isinstance(deps, list) or any(not isinstance(x, str) for x in deps):
            errors.append(f"{ident}: dependsOn must be an array of ids")
    for ident, item in by_id.items():
        for dep in item.get("dependsOn", []):
            if dep not in by_id:
                errors.append(f"{ident}: unknown dependency {dep}")
    visiting, visited = set(), set()
    def visit(ident):
        if ident in visiting:
            return True
        if ident in visited:
            return False
        visiting.add(ident)
        for dep in by_id[ident].get("dependsOn", []):
            if dep in by_id and visit(dep):
                return True
        visiting.remove(ident)
        visited.add(ident)
        return False
    for ident in by_id:
        if visit(ident):
            errors.append("dependency cycle detected")
            break
    return {
        "schema": "omega42.proof-obligation-audit.k5",
        "valid": not errors,
        "obligationCount": len(items),
        "statusCounts": {
            status: sum(1 for x in items if isinstance(x, dict) and x.get("status") == status)
            for status in sorted(ALLOWED)
        },
        "proofValidityCertified": False,
        "errors": errors
    }

def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("tests/fixtures/omega42-k5-proof-obligations.json")
    data = json.loads(path.read_text(encoding="utf-8"))
    result = audit(data)
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["valid"] else 1)

if __name__ == "__main__":
    main()
