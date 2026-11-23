#!/usr/bin/env python3
"""Experimental Path B strict guard for static Omega42 certificate validation.

This guard never executes certificate PROCEDURE text. Canonical certify.py is
called only through check(); --verify remains a separate privileged profile.
"""
import os
import re
import sys
sys.path.insert(0, __import__("os").path.dirname(__file__))
import certify


def strict_findings(text):
    findings = []
    opening_count = text.count(certify.OPEN)
    closing_count = text.count(certify.END)
    blocks = re.findall(re.escape(certify.OPEN) + r"(.*?)" + re.escape(certify.END), text, re.S)
    if opening_count != 1 or closing_count != 1 or len(blocks) != 1:
        return ["exactly one balanced certificate block is required per certificate file (open=%d, close=%d, complete=%d)" %
                (opening_count, closing_count, len(blocks))]
    body = blocks[0]
    values = {}
    for field in certify.FIELDS:
        lines = [line for line in body.splitlines() if line.startswith(field)]
        if len(lines) != 1:
            findings.append("exactly one %s line is required" % field.rstrip(":"))
            continue
        values[field[:-1]] = lines[0][len(field):].strip()

    for key in ("CERTIFICATE", "KIND", "SUBJECT", "CRITERIA", "PROCEDURE",
                "CWD", "RESULT", "GRADE", "SCOPE", "STATUS", "STATEMENT"):
        if key in values and not values[key]:
            findings.append("%s must not be blank" % key)

    certificate_id = values.get("CERTIFICATE", "")
    if certificate_id and not re.fullmatch(r"CERT-\d{4}", certificate_id):
        findings.append("CERTIFICATE identifier must have the form CERT-####")

    cwd = values.get("CWD", "")
    normalized_cwd = cwd.replace("\\", "/")
    if cwd and (os.path.isabs(normalized_cwd) or re.match(r"^[A-Za-z]:", normalized_cwd)
                or ".." in normalized_cwd.split("/")):
        findings.append("CWD must be a relative path confined to the package (no absolute path or '..' segment)")

    status = values.get("STATUS", "")
    digest = values.get("RESULT SHA-256", "")
    if not status.startswith("REGISTERED") and not re.fullmatch(r"[0-9a-f]{64}", digest):
        findings.append("RESULT SHA-256 must be 64 lowercase hexadecimal characters unless REGISTERED")
    statement = values.get("STATEMENT", "")
    if statement.startswith("Ω42 certifies") and not statement[len("Ω42 certifies"):].strip():
        findings.append("STATEMENT must contain a finding after 'Ω42 certifies'")
    return findings


def check_file(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    canonical = certify.check(text)
    strict = strict_findings(text)
    problems = canonical + strict
    print("D3 STRICT CERTIFICATE: %s | %s" % (path, "PASS" if not problems else "FAIL"))
    for problem in problems:
        print("  - " + problem)
    return not problems


if __name__ == "__main__":
    paths = sys.argv[1:]
    if not paths:
        print("Usage: python tools/path_b_d3_certificate_guard.py FILE [...]")
        sys.exit(2)
    sys.exit(0 if all(check_file(p) for p in paths) else 1)
