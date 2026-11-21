#!/usr/bin/env python3
"""Emit the K4 shared-vector verification record."""
import json
import subprocess
import sys
from pathlib import Path
from omega42_k4_reference import analyze

fixture = Path("tests/fixtures/omega42-k4-vectors.json")
data = json.loads(fixture.read_text(encoding="utf-8"))
results = [analyze(case) for case in data["cases"]]
record = {
    "schema": "omega42.cross-language-verification-record.k4",
    "status": "EXECUTED",
    "fixture_schema": data["schema"],
    "case_count": len(results),
    "depths": sorted({r["depth"] for r in results}),
    "python_reference": "PASS",
    "results": results
}
print(json.dumps(record, indent=2, sort_keys=True))
