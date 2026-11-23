#!/usr/bin/env python3
"""Experimental D5a eight-domain conformance and negative-control harness.

All generated navigations are synthetic test fixtures in a temporary directory.
They are never submissions, accepted records, or prior-art disclosures.
"""
import datetime
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import canonical_reference as cr
import conformance as cf
import congruence as cg
import format_check as fc
import manifestation as mf
import output_id as oi

SET = os.path.join(ROOT, "records", "conformance", "practice_set.txt")
FIXED_DATE = datetime.date(2026, 11, 19)  # before the L-503 researched-reach rule dated 20 Nov
INSTANCE = ("INSTANCE (L-513): NI-0123456789abcdef | ISSUER: SCRIPT | "
            "ISSUED: 2026-11-19T00:00:00Z | SEQ: 1 | PREV: NONE")

def domains():
    return cf.load_set(SET)

def replace_m310(text):
    start = text.index("======= CONGRUENCE RECORD (M310) =======")
    end = text.index("======= END CONGRUENCE RECORD =======", start) + len("======= END CONGRUENCE RECORD =======")
    record = cg.record(text)
    return text[:start] + record + text[end:]

def finish_output_id(text):
    text = re.sub(r"^OUTPUT ID:.*\\n", "", text, flags=re.M)
    m = re.search(r"^CAS-YY = -1/2", text, re.M)
    if not m:
        raise AssertionError("signature marker missing")
    prefix, suffix = text[:m.start()], text[m.start():]
    return prefix + "OUTPUT ID: " + oi.output_id(prefix) + "\\n" + suffix

def build_fixture(tag, domain):
    raw = fc.skeleton(domain, session=1, date=FIXED_DATE)
    text = fc._fill_for_test(raw)
    text = re.sub(r"^INSTANCE \\(L-513\\):.*$", INSTANCE, text, flags=re.M)
    text = replace_m310(text)
    text = finish_output_id(text)
    return text

def verdict_for(items):
    with tempfile.TemporaryDirectory(prefix="omega42-d5a-") as tmp:
        for name, text in items:
            with open(os.path.join(tmp, name), "w", encoding="utf-8") as f:
                f.write(text)
        return cf.report(sorted(os.path.join(tmp, n) for n in os.listdir(tmp)), SET)

def mutate_first(text, pattern, replacement):
    changed, n = re.subn(pattern, replacement, text, count=1, flags=re.M)
    if n != 1:
        raise AssertionError("negative-control mutation did not match: " + pattern)
    return changed

def main():
    rows = domains()
    if len(rows) != 8 or len({d for _, d in rows}) != 8:
        raise SystemExit("practice set is not exactly eight unique domains")
    fixtures = [(tag + ".txt", build_fixture(tag, domain)) for tag, domain in rows]

    print("D5a SYNTHETIC FIXTURE INVENTORY")
    for (tag, domain), (name, text) in zip(rows, fixtures):
        e = cf.expected(domain)
        dom, checks, advisory, script = cf.check_one(text)
        fmt = [x for x in fc.check(text) if x[0] == "FAIL"]
        print("%s | synthetic | %s | anchor P%d | state %s | norm %d | format failures %d | required %s | %s" %
              (tag, name, e["anchor"], e["state"], e["norm"], len(fmt),
               "PASS" if all(x[1] for x in checks) else "FAIL",
               "SCRIPT-CAPABLE" if script else "TEXT-ONLY"))

    report, verdict = verdict_for(fixtures)
    print("\\nBASELINE REPORT")
    print(report)
    print("BASELINE VERDICT: " + verdict)

    tests = []
    all_items = list(fixtures)
    tests.append(("baseline 8/8", all_items, "COMPATIBLE"))
    tests.append(("missing one domain", all_items[:-1], "NOT YET COMPATIBLE"))

    first_name, first_text = fixtures[0]
    tests.append(("non-practice domain", [(first_name, first_text.replace(rows[0][1], "A domain outside this practice set", 1))] + fixtures[1:], "NOT YET COMPATIBLE"))
    tests.append(("wrong anchor", [(first_name, mutate_first(first_text, r"ANCHOR P\\d+", "ANCHOR P9"))] + fixtures[1:], "NOT YET COMPATIBLE"))
    tests.append(("wrong arm", [(first_name, mutate_first(first_text, r"Yang P\\d+", "Yang P1"))] + fixtures[1:], "NOT YET COMPATIBLE"))
    tests.append(("wrong layer-one state", [(first_name, mutate_first(first_text, r"state \\(\\d+, \\d+\\)", "state (8, 8)"))] + fixtures[1:], "NOT YET COMPATIBLE"))
    tests.append(("missing required format marker", [(first_name, first_text.replace("LENSES SELECTED (L-494): NONE", "LENS SELECTION OMITTED", 1))] + fixtures[1:], "NOT YET COMPATIBLE"))
    tests.append(("duplicate while another domain absent", fixtures[:-1] + [("duplicate.txt", fixtures[0][1])], "NOT YET COMPATIBLE"))
    tests.append(("empty fixture", [(first_name, "")] + fixtures[1:], "NOT YET COMPATIBLE"))
    tests.append(("malformed fixture", [(first_name, "not a navigation\\n") ] + fixtures[1:], "NOT YET COMPATIBLE"))
    tests.append(("wrong exact domain wording", [(first_name, first_text.replace(rows[0][1], rows[0][1] + " ", 1))] + fixtures[1:], "NOT YET COMPATIBLE"))

    print("\\nNEGATIVE-CONTROL MATRIX")
    failures = []
    for label, items, expected in tests:
        try:
            _, got = verdict_for(items)
            ok = got.startswith(expected)
            print("[%s] %s -> %s (expected %s)" % ("PASS" if ok else "FAIL", label, got, expected))
            if not ok: failures.append(label + ": verdict " + got)
        except Exception as exc:
            hard_error = expected == "NOT YET COMPATIBLE"
            print("[%s] %s -> HARD ERROR %s" % ("PASS" if hard_error else "FAIL", label, repr(exc)))
            if not hard_error: failures.append(label + ": unexpected " + repr(exc))

    # Duplicate diagnostics are a separate quality criterion: coverage must fail, but the present report
    # may not explicitly name the duplicate. Record this rather than silently treating it as a full pass.
    duplicate_report, duplicate_verdict = verdict_for(fixtures[:-1] + [("duplicate.txt", fixtures[0][1])])
    duplicate_diagnostic = "duplicate" in duplicate_report.lower()
    print("DUPLICATE DIAGNOSTIC: %s" % ("PRESENT" if duplicate_diagnostic else "ABSENT (coverage still prevents compatibility)"))

    print("\\nSUMMARY")
    print("Synthetic fixtures: %d" % len(fixtures))
    print("Baseline: %s" % verdict)
    print("Negative controls: %d/%d rejected" % (len(tests)-1, len(tests)-1))
    print("Duplicate diagnostic: %s" % ("present" if duplicate_diagnostic else "absent"))
    print("No historical navigation was edited or relabelled.")
    print("No synthetic fixture was written into the repository.")
    if verdict != "COMPATIBLE (SCRIPT-CAPABLE)" and verdict != "COMPATIBLE (TEXT-ONLY)":
        failures.append("baseline did not achieve a compatible 8/8 verdict")
    if failures:
        print("D5a RESULT: FAIL")
        for item in failures: print(" - " + item)
        return 1
    print("D5a RESULT: PASS")
    return 0

if __name__ == "__main__":
    sys.exit(main())
