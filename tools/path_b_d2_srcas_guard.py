#!/usr/bin/env python3
"""Experimental Path B strict guard for SR-CAS/SNCA assessment packages.

Canonical tools/srcas_check.py remains unchanged. This wrapper adds package-level
consistency checks for fields the canonical parser currently treats permissively.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(__file__))
import srcas_check


def _count_line(body, label):
    return len(re.findall(r"(?mi)^\s*" + re.escape(label) + r"\s*", body))


def strict_findings(text):
    findings = []
    enforced = srcas_check.dated_from(text)
    if not enforced:
        return findings

    sr_rx = re.compile(
        r"======= SR-CAS ASSESSMENT REPORT =======(.*?)======= END SR-CAS ASSESSMENT REPORT =======",
        re.S,
    )
    for number, match in enumerate(sr_rx.finditer(text), 1):
        body = match.group(1)
        before = text[:match.start()]
        prefix = "SR-CAS report %d" % number
        verifications = srcas_check.blocks(before, "PRE-SR-CAS VERBATIM VERIFICATION")
        if not verifications:
            continue  # canonical checker reports the missing block
        verification = verifications[-1]
        matches = re.findall(r"\bMATCH:\s*(YES|NO)\b", verification)
        verdicts = re.findall(r"\bVERDICT:\s*(PROCEED|HALT)\b([^\n]*)", verification)
        if len(matches) != 1:
            findings.append(prefix + ": verification block must contain exactly one MATCH: YES/NO line")
        if len(verdicts) != 1:
            findings.append(prefix + ": verification block must contain exactly one VERDICT line")
        if len(matches) == 1 and len(verdicts) == 1:
            match_value = matches[0]
            verdict, tail = verdicts[0]
            if match_value == "YES" and verdict != "PROCEED":
                findings.append(prefix + ": MATCH: YES requires VERDICT: PROCEED")
            if match_value == "NO" and not (verdict == "HALT" and "VERBATIM MISMATCH" in tail):
                findings.append(prefix + ": MATCH: NO requires HALT -- VERBATIM MISMATCH")

        halted = bool(re.search(r"HALT\s*[-—]+\s*VERBATIM MISMATCH", verification + body))
        if halted:
            for label in ("DOMAIN:", "ARCHITECTURES COMPARED", "PER-RUN VERDICT", "MANDATORY CORRECTIONS:"):
                if _count_line(body, label) != 1:
                    findings.append(prefix + ": halted report requires exactly one %s line" % label.rstrip(":"))
            continue

        for label in ("Base Score:", "Comparison-class weight", "Weighted index"):
            if len(re.findall(re.escape(label), body)) != 1:
                findings.append(prefix + ": exactly one %s field is required" % label.rstrip(":"))

        weight_tail = body[body.find("Comparison-class weight"):] if "Comparison-class weight" in body else ""
        weight_match = re.search(r"(?:x|×)\s*(\d+(?:\.\d+)?)", weight_tail)
        base = srcas_check.first(body, "Base Score:")
        weighted = srcas_check.first(body, "Weighted index")
        if weight_match is None:
            findings.append(prefix + ": comparison-class weight must contain a numeric multiplier")
        if weighted is None:
            findings.append(prefix + ": weighted index must contain a numeric value")
        if base is not None and weight_match is not None and weighted is not None:
            multiplier = float(weight_match.group(1))
            expected = min(1.0, base * multiplier)
            if abs(expected - weighted) > 0.01:
                findings.append(prefix + ": weighted index does not recompute from Base Score and comparison-class weight")

    sn_rx = re.compile(
        r"======= SNCA ASSESSMENT REPORT =======(.*?)======= END SNCA ASSESSMENT REPORT =======",
        re.S,
    )
    for number, match in enumerate(sn_rx.finditer(text), 1):
        body = match.group(1)
        prefix = "SNCA report %d" % number
        for label in ("Base Score:", "STATUS (two axes"):
            if _count_line(body, label) != 1:
                findings.append(prefix + ": exactly one %s line is required" % label.rstrip(":"))
    return findings


def check_file(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    canonical = []
    for kind, name, problems in srcas_check.check(text):
        canonical.extend("%s %s: %s" % (kind, name, p) for p in problems)
    strict = strict_findings(text)
    problems = canonical + strict
    print("D2 STRICT SR-CAS/SNCA: %s | %s" % (path, "PASS" if not problems else "FAIL"))
    for problem in problems:
        print("  - " + problem)
    return not problems


if __name__ == "__main__":
    paths = sys.argv[1:]
    if not paths:
        print("Usage: python tools/path_b_d2_srcas_guard.py FILE [...]")
        sys.exit(2)
    sys.exit(0 if all(check_file(p) for p in paths) else 1)
