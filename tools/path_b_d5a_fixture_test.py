#!/usr/bin/env python3
"""Experimental D5a eight-domain conformance and negative-control harness.

All generated navigations are synthetic test fixtures in a temporary directory.
They are never submissions, accepted records, or prior-art disclosures.
"""
import datetime
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import conformance as cf
import congruence as cg
import format_check as fc
import output_id as oi
import path_b_d5a_guard as guard

SET = os.path.join(ROOT, "records", "conformance", "practice_set.txt")
FIXED_DATE = datetime.date(2026, 11, 23)
INSTANCE = ("INSTANCE (L-513): NI-0123456789abcdef | ISSUER: SCRIPT | "
            "ISSUED: 2026-11-23T00:00:00Z | SEQ: 1 | PREV: NONE")

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

    # The current L-503 rules require a 500+ word essay and an explicit reach status.
    essay_start = text.index("┌─ EXTENDED RESONANCE ESSAY ─┐")
    essay_end = text.index("└──────────────┘", essay_start) + len("└──────────────┘")
    essay = "SYNTHETIC TEST FIXTURE ONLY. " + " ".join(["inquiry"] * 510)
    essay_block = "┌─ EXTENDED RESONANCE ESSAY ─┐\n" + essay + "\n└──────────────┘"
    text = text[:essay_start] + essay_block + text[essay_end:]

    # No external retrieval is performed by a synthetic fixture.
    ck_start = text.index("======= CURRENT KNOWLEDGE (L-503) =======")
    ck_end_marker = "======= END CURRENT KNOWLEDGE ======="
    ck_end = text.index(ck_end_marker, ck_start) + len(ck_end_marker)
    text = text[:ck_start] + "CURRENT KNOWLEDGE (L-503): NOT REQUESTED" + text[ck_end:]
    text = re.sub(r"^RESEARCHED REACH \(L-503 \(5\)\):.*$", "RESEARCHED REACH (L-503 (5)): NOT REQUESTED", text, flags=re.M)

    contribution = "NAVIGATOR'S CONTRIBUTION (Domain Zero): COMMON -- synthetic test fixture; STRIKER -- supplied practice-set domain; NAVIGATOR -- generated fixture; OPEN -- no semantic claim."
    text = text.replace("======= END GENERATIVE OBSERVATIONS =======",
                        contribution + "\n======= END GENERATIVE OBSERVATIONS =======", 1)

    text = replace_m310(text)
    trigger_lines = []
    if fc._math(domain):
        trigger_lines += [
            "M269 MATHEMATICAL DOMAIN EXTRACTION AUDIT TRAIL",
            "SYNTHETIC FIXTURE: trigger marker only; not a mathematical audit.",
            "M139 SYNTHETIC FIXTURE TRIGGER MARKER",
            "M142 SYNTHETIC FIXTURE TRIGGER MARKER",
        ]
    if len(domain.split()) > 30:
        trigger_lines += ["M127 SYNTHETIC FIXTURE TRIGGER MARKER"]
    if trigger_lines:
        marker = "M207 NAVIGATOR INTERFERENCE"
        text = text.replace(marker, "\n".join(trigger_lines) + "\n" + marker, 1)
    return finish_output_id(text)

def run_report(items, strict=True):
    with tempfile.TemporaryDirectory(prefix="omega42-d5a-") as tmp:
        for name, text in items:
            with open(os.path.join(tmp, name), "w", encoding="utf-8") as handle:
                handle.write(text)
        paths = sorted(os.path.join(tmp, name) for name in os.listdir(tmp))
        if strict:
            return guard.strict_report(paths, SET)
        return cf.report(paths, SET)

def verdict_for(items):
    return run_report(items, strict=True)

def mutate_first(text, pattern, replacement):
    changed, n = re.subn(pattern, replacement, text, count=1, flags=re.M)
    if n != 1:
        raise AssertionError("negative-control mutation did not match: " + pattern)
    return changed


def run_isolated_package():
    """Copy only the declared D5a execution closure and run this harness there."""
    closure = [
        "scripts/canonical_reference.py",
        "scripts/m193_m225.py",
        "scripts/crc60_and_m267.py",
        "tools/conformance.py",
        "tools/congruence.py",
        "tools/bashar_lens.py",
        "tools/format_check.py",
        "tools/aperture_audit.py",
        "tools/frame_audit.py",
        "tools/output_id.py",
        "tools/manifestation.py",
        "tools/consciousness.py",
        "tools/adaptors.py",
        "tools/adaptor_rules.py",
        "tools/utility.py",
        "tools/path_b_d5a_guard.py",
        "tools/path_b_d5a_fixture_test.py",
        "records/conformance/practice_set.txt",
    ]
    with tempfile.TemporaryDirectory(prefix="omega42-d5a-package-") as package_root:
        for rel in closure:
            source = os.path.join(ROOT, rel)
            if not os.path.isfile(source):
                return 1, "", "missing declared closure file: " + rel
            target = os.path.join(package_root, rel)
            os.makedirs(os.path.dirname(target), exist_ok=True)
            shutil.copy2(source, target)
        script = os.path.join(package_root, "tools", "path_b_d5a_fixture_test.py")
        result = subprocess.run(
            [sys.executable, script, "--isolated-child"],
            cwd=package_root, capture_output=True, text=True, timeout=180
        )
        return result.returncode, result.stdout, result.stderr

def main():
    rows = domains()
    if len(rows) != 8 or len({domain for _, domain in rows}) != 8:
        raise SystemExit("practice set is not exactly eight unique domains")
    fixtures = [(tag + ".txt", build_fixture(tag, domain)) for tag, domain in rows]

    print("D5a SYNTHETIC FIXTURE INVENTORY")
    for (tag, domain), (name, text) in zip(rows, fixtures):
        e = cf.expected(domain)
        _, checks, _, script = cf.check_one(text)
        fmt = [item for item in fc.check(text) if item[0] == "FAIL"]
        print("%s | synthetic | %s | anchor P%d | state %s | norm %d | format failures %d | required %s | %s" %
              (tag, name, e["anchor"], e["state"], e["norm"], len(fmt),
               "PASS" if all(item[1] for item in checks) else "FAIL",
               "SCRIPT-CAPABLE" if script else "TEXT-ONLY"))

    report, verdict = verdict_for(fixtures)
    raw_report, raw_verdict = run_report(fixtures, strict=False)
    print("\nBASELINE REPORT")
    print(report)
    print("BASELINE VERDICT (Path B guard): " + verdict)
    print("RAW M314 BASELINE VERDICT: " + raw_verdict)

    first_name, first_text = fixtures[0]
    tests = [
        ("missing one domain", fixtures[:-1]),
        ("non-practice domain", [(first_name, first_text.replace(rows[0][1], "A domain outside this practice set", 1))] + fixtures[1:]),
        ("wrong anchor", [(first_name, mutate_first(first_text, r"ANCHOR P\d+", "ANCHOR P9"))] + fixtures[1:]),
        ("wrong arm", [(first_name, mutate_first(first_text, r"Yang P\d+", "Yang P1"))] + fixtures[1:]),
        ("wrong layer-one state", [(first_name, mutate_first(first_text, r"(?m)(^\(1\) INTERNAL.*?state )\(\d+, \d+\)", r"\g<1>(8, 8)"))] + fixtures[1:]),
        ("missing required format marker", [(first_name, first_text.replace("LENSES SELECTED (L-494): NONE", "LENS SELECTION OMITTED", 1))] + fixtures[1:]),
        ("duplicate while another domain absent", fixtures[:-1] + [("duplicate.txt", fixtures[0][1])]),
        ("empty fixture", [(first_name, "")] + fixtures[1:]),
        ("malformed fixture", [(first_name, "not a navigation\n")] + fixtures[1:]),
        ("wrong exact domain wording", [(first_name, first_text.replace("DOMAIN VERBATIM: " + rows[0][1], "DOMAIN VERBATIM: " + rows[0][1].replace("time", "Time"), 1))] + fixtures[1:]),
        ("multiple DOMAIN VERBATIM lines", [(first_name, first_text.replace("DOMAIN VERBATIM: " + rows[0][1], "DOMAIN VERBATIM: " + rows[0][1] + "\nDOMAIN VERBATIM: " + rows[0][1], 1))] + fixtures[1:]),
    ]

    print("\nNEGATIVE-CONTROL MATRIX (Path B strict guard)")
    failures = []
    passed_controls = 0
    for label, items in tests:
        try:
            _, got = verdict_for(items)
            ok = got == "NOT YET COMPATIBLE"
            print("[%s] %s -> %s" % ("PASS" if ok else "FAIL", label, got))
            if ok:
                passed_controls += 1
            else:
                failures.append(label + ": verdict " + got)
        except Exception as exc:
            print("[FAIL] %s -> unexpected hard error %s" % (label, repr(exc)))
            failures.append(label + ": " + repr(exc))

    duplicate_report, duplicate_verdict = verdict_for(fixtures[:-1] + [("duplicate.txt", fixtures[0][1])])
    duplicate_diagnostic = bool(re.search(r"\bduplicate domain\b", duplicate_report, re.I))
    print("DUPLICATE-WITH-MISSING-DOMAIN: %s; explicit diagnostic: %s" %
          (duplicate_verdict, "PRESENT" if duplicate_diagnostic else "ABSENT"))

    duplicate_items = fixtures + [("duplicate-extra.txt", fixtures[0][1])]
    _, guarded_duplicate_verdict = run_report(duplicate_items, strict=True)
    _, raw_duplicate_verdict = run_report(duplicate_items, strict=False)
    guard_rejects_duplicate = guarded_duplicate_verdict == "NOT YET COMPATIBLE"
    raw_m314_defect_reproduced = raw_duplicate_verdict.startswith("COMPATIBLE")
    print("DUPLICATE-WITH-COMPLETE-COVERAGE: Path B guard %s | raw M314 %s" %
          (guarded_duplicate_verdict, raw_duplicate_verdict))
    print("RAW M314 DUPLICATE ACCEPTANCE REPRODUCED: %s" % ("YES" if raw_m314_defect_reproduced else "NO"))

    print("\nSUMMARY")
    print("Synthetic fixtures: %d" % len(fixtures))
    print("Baseline (Path B guard): %s" % verdict)
    print("Negative controls rejected: %d/%d" % (passed_controls, len(tests)))
    print("Explicit duplicate diagnostic: %s" % ("present" if duplicate_diagnostic else "absent"))
    print("Path B exact-one-file-per-domain guard: %s" % ("PASS" if guard_rejects_duplicate else "FAIL"))
    print("Raw M314 duplicate defect reproduced: %s" % ("YES" if raw_m314_defect_reproduced else "NO"))
    print("No historical navigation was edited or relabelled.")
    print("No synthetic fixture was written into the repository.")

    if verdict not in ("COMPATIBLE (SCRIPT-CAPABLE)", "COMPATIBLE (TEXT-ONLY)"):
        failures.append("baseline did not achieve a compatible 8/8 verdict")
    if passed_controls != len(tests):
        failures.append("one or more negative controls were not rejected")
    if not guard_rejects_duplicate:
        failures.append("Path B guard did not reject a duplicate extra file")
    if not raw_m314_defect_reproduced:
        failures.append("raw M314 duplicate acceptance was not reproduced; inspect canonical checker")
    if not duplicate_diagnostic:
        failures.append("Path B guard did not provide a duplicate-domain diagnostic")
    if "--isolated-child" not in sys.argv:
        isolated_rc, isolated_out, isolated_err = run_isolated_package()
        isolated_ok = isolated_rc == 0 and "D5a RESULT: PASS" in isolated_out
        print("\nISOLATED MINIMAL-PACKAGE RESULT: %s" % ("PASS" if isolated_ok else "FAIL"))
        print(isolated_out[-3000:])
        if isolated_err:
            print("ISOLATED STDERR: " + isolated_err[-2000:])
        if not isolated_ok:
            failures.append("D5a isolated package closure did not pass")

    if failures:
        print("D5a RESULT: FAIL")
        for item in failures:
            print(" - " + item)
        return 1
    print("D5a RESULT: PASS (Path B strict wrapper; canonical M314 defect isolated)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
