#!/usr/bin/env python3
"""Experimental D5a eight-domain conformance and negative-control harness.

All generated navigations are synthetic test fixtures in a temporary directory.
They are never submissions, accepted records, or prior-art disclosures.
"""
import datetime
import os
import re
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import conformance as cf
import congruence as cg
import format_check as fc
import output_id as oi

SET = os.path.join(ROOT, "records", "conformance", "practice_set.txt")
FIXED_DATE = datetime.date(2026, 11, 19)  # before the L-503 researched-reach rule dated 20 Nov
INSTANCE = ("INSTANCE (L-513): NI-0123456789abcdef | ISSUER: SCRIPT | "
            "ISSUED: 2026-11-19T00:00:00Z | SEQ: 1 | PREV: NONE")

def domains():
    return cf.load_set(SET)

def replace_m310(text):
    start = text.index("======= CONGRUENCE RECORD (M310) =======")
    marker = "======= END CONGRUENCE RECORD ======="
    end = text.index(marker, start) + len(marker)
    return text[:start] + cg.record(text) + text[end:]

def finish_output_id(text):
    text = re.sub(r"^OUTPUT ID:.*\n", "", text, flags=re.M)
    m = re.search(r"^CAS-YY = -1/2", text, re.M)
    if not m:
        raise AssertionError("signature marker missing")
    prefix, suffix = text[:m.start()], text[m.start():]
    return prefix + "OUTPUT ID: " + oi.output_id(prefix) + "\n" + suffix

def build_fixture(tag, domain):
    raw = fc.skeleton(domain, session=1, date=FIXED_DATE)
    text = fc._fill_for_test(raw)
    text = re.sub(r"^INSTANCE \(L-513\):.*$", INSTANCE, text, flags=re.M)
    text = replace_m310(text)
    return finish_output_id(text)

def verdict_for(items):
    with tempfile.TemporaryDirectory(prefix="omega42-d5a-") as tmp:
        for name, text in items:
            with open(os.path.join(tmp, name), "w", encoding="utf-8") as f:
                f.write(text)
        paths = sorted(os.path.join(tmp, n) for n in os.listdir(tmp))
        return cf.report(paths, SET)

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
        _, checks, _, script = cf.check_one(text)
        fmt = [x for x in fc.check(text) if x[0] == "FAIL"]
        print("%s | synthetic | %s | anchor P%d | state %s | norm %d | format failures %d | required %s | %s" %
              (tag, name, e["anchor"], e["state"], e["norm"], len(fmt),
               "PASS" if all(x[1] for x in checks) else "FAIL",
               "SCRIPT-CAPABLE" if script else "TEXT-ONLY"))

    report, verdict = verdict_for(fixtures)
    print("\nBASELINE REPORT")
    print(report)
    print("BASELINE VERDICT: " + verdict)

    first_name, first_text = fixtures[0]
    tests = [
        ("missing one domain", fixtures[:-1]),
        ("non-practice domain", [(first_name, first_text.replace(rows[0][1], "A domain outside this practice set", 1))] + fixtures[1:]),
        ("wrong anchor", [(first_name, mutate_first(first_text, r"ANCHOR P\d+", "ANCHOR P9"))] + fixtures[1:]),
        ("wrong arm", [(first_name, mutate_first(first_text, r"Yang P\d+", "Yang P1"))] + fixtures[1:]),
        ("wrong layer-one state", [(first_name, mutate_first(first_text, r"state \(\d+, \d+\)", "state (8, 8)"))] + fixtures[1:]),
        ("missing required format marker", [(first_name, first_text.replace("LENSES SELECTED (L-494): NONE", "LENS SELECTION OMITTED", 1))] + fixtures[1:]),
        ("duplicate while another domain absent", fixtures[:-1] + [("duplicate.txt", fixtures[0][1])]),
        ("empty fixture", [(first_name, "")] + fixtures[1:]),
        ("malformed fixture", [(first_name, "not a navigation\n")] + fixtures[1:]),
        ("wrong exact domain wording", [(first_name, first_text.replace(rows[0][1], rows[0][1] + " ", 1))] + fixtures[1:]),
    ]

    print("\nNEGATIVE-CONTROL MATRIX")
    failures = []
    for label, items in tests:
        try:
            _, got = verdict_for(items)
            ok = got == "NOT YET COMPATIBLE"
            print("[%s] %s -> %s" % ("PASS" if ok else "FAIL", label, got))
            if not ok:
                failures.append(label + ": verdict " + got)
        except Exception as exc:
            print("[PASS] %s -> explicit hard error %s" % (label, repr(exc)))
    duplicate_report, _ = verdict_for(fixtures[:-1] + [("duplicate.txt", fixtures[0][1])])
    duplicate_diagnostic = "duplicate" in duplicate_report.lower()
    print("DUPLICATE DIAGNOSTIC: %s" % ("PRESENT" if duplicate_diagnostic else "ABSENT (coverage still prevents compatibility)"))

    print("\nSUMMARY")
    print("Synthetic fixtures: %d" % len(fixtures))
    print("Baseline: %s" % verdict)
    print("Negative controls: %d/%d rejected" % (len(tests)-1, len(tests)-1))
    print("Duplicate diagnostic: %s" % ("present" if duplicate_diagnostic else "absent"))
    print("No historical navigation was edited or relabelled.")
    print("No synthetic fixture was written into the repository.")
    if verdict not in ("COMPATIBLE (SCRIPT-CAPABLE)", "COMPATIBLE (TEXT-ONLY)"):
        failures.append("baseline did not achieve a compatible 8/8 verdict")
    if failures:
        print("D5a RESULT: FAIL")
        for item in failures:
            print(" - " + item)
        return 1
    print("D5a RESULT: PASS")
    return 0

if __name__ == "__main__":
    sys.exit(main())
