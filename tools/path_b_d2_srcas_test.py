#!/usr/bin/env python3
"""Path B D2 isolated validation for SR-CAS/SNCA format checking.

Copies the standard-library checker and its explicit assessment/trigger inputs
into a temporary package. Does not invoke the automatic review generator.
"""
import glob
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = ROOT


def copy_tree_files(source_pattern, package_root, prefix):
    copied = []
    for source in sorted(glob.glob(os.path.join(ROOT, source_pattern))):
        if not os.path.isfile(source):
            continue
        rel = os.path.relpath(source, ROOT)
        target = os.path.join(package_root, rel)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        shutil.copy2(source, target)
        copied.append(target)
    return copied


def main():
    failures = []
    with tempfile.TemporaryDirectory(prefix="omega42-d2-srcas-") as package_root:
        checker_src = os.path.join(ROOT, "tools", "srcas_check.py")
        if not os.path.isfile(checker_src):
            print("D2 FAIL: tools/srcas_check.py is missing")
            return 1
        checker = os.path.join(package_root, "tools", "srcas_check.py")
        os.makedirs(os.path.dirname(checker), exist_ok=True)
        shutil.copy2(checker_src, checker)
        guard_src = os.path.join(ROOT, "tools", "path_b_d2_srcas_guard.py")
        guard = os.path.join(package_root, "tools", "path_b_d2_srcas_guard.py")
        if not os.path.isfile(guard_src):
            print("D2 FAIL: tools/path_b_d2_srcas_guard.py is missing")
            return 1
        shutil.copy2(guard_src, guard)

        reports = copy_tree_files("records/srcas/*.txt", package_root, "records/srcas")
        submissions = copy_tree_files("submissions/ape/APE-*.md", package_root, "submissions/ape")
        print("D2 isolated package inputs: checker=1, SR-CAS/SNCA records=%d, APE submissions=%d" %
              (len(reports), len(submissions)))

        def run(args, label, expected=0):
            p = subprocess.run([sys.executable, checker] + args, cwd=package_root,
                               capture_output=True, text=True, timeout=180)
            ok = p.returncode == expected
            print("%-58s %s (exit %d, expected %d)" % (label, "PASS" if ok else "FAIL", p.returncode, expected))
            if p.stdout:
                print(p.stdout[-9000:])
            if p.stderr:
                print("STDERR:", p.stderr[-2500:])
            if not ok:
                failures.append(label)
            return p

        run(["--selftest"], "Canonical SR-CAS/SNCA checker selftest")

        # The Path B wrapper is tested separately from the unchanged canonical checker.
        sys.path.insert(0, os.path.join(package_root, "tools"))
        import srcas_check
        import path_b_d2_srcas_guard as strict_guard
        good_sr = srcas_check.GOOD_V + srcas_check.GOOD_R
        good_sn = srcas_check.GOOD_S
        sr_path = os.path.join(package_root, "synthetic-sr.txt")
        sn_path = os.path.join(package_root, "synthetic-sn.txt")
        with open(sr_path, "w", encoding="utf-8") as f:
            f.write(good_sr)
        with open(sn_path, "w", encoding="utf-8") as f:
            f.write(good_sn)
        good_profile = strict_guard.check_file(sr_path) and strict_guard.check_file(sn_path)
        halt_path = os.path.join(package_root, "synthetic-halt.txt")
        with open(halt_path, "w", encoding="utf-8") as f:
            f.write(srcas_check.HALT)
        halt_profile = strict_guard.check_file(halt_path)
        print("%-58s %s" % ("Strict guard accepts the canonical halted-report form",
                            "PASS" if halt_profile else "FAIL"))
        if not halt_profile:
            failures.append("strict guard rejected canonical halted-report form")
        print("%-58s %s" % ("Strict guard accepts complete SR-CAS and SNCA baselines",
                            "PASS" if good_profile else "FAIL"))
        if not good_profile:
            failures.append("strict guard rejected complete synthetic baseline")

        strict_controls = [
            ("MATCH NO with PROCEED", good_sr.replace("MATCH: YES", "MATCH: NO")),
            ("missing numeric comparison weight", good_sr.replace("Comparison-class weight (L-416): x1.5", "Comparison-class weight (L-416): N/A")),
            ("missing numeric weighted index", good_sr.replace("Weighted index: 1.00", "Weighted index: N/A")),
            ("duplicate Base Score field", good_sr.replace("MANDATORY CORRECTIONS: none", "Base Score: 0.79\nMANDATORY CORRECTIONS: none")),
        ]
        strict_ok = True
        for name, content in strict_controls:
            path = os.path.join(package_root, "negative-" + str(len(name)) + ".txt")
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            rejected = not strict_guard.check_file(path)
            print("  strict negative control %-35s %s" % (name, "REJECTED" if rejected else "ACCEPTED"))
            strict_ok &= rejected
        if not strict_ok:
            failures.append("strict guard accepted one or more negative controls")

        if reports:
            run(reports, "All archived SR-CAS/SNCA records format-check")
            strict_run = subprocess.run([sys.executable, guard] + reports, cwd=package_root,
                                        capture_output=True, text=True, timeout=180)
            strict_ok = strict_run.returncode == 0
            print("All archived SR-CAS/SNCA records strict-guard: %s (exit %d)" %
                  ("PASS" if strict_ok else "FINDINGS", strict_run.returncode))
            print((strict_run.stdout or "")[-12000:])
            if strict_run.stderr:
                print("STRICT GUARD STDERR:", strict_run.stderr[-2000:])
            if not strict_ok:
                failures.append("strict guard reported findings in archived SR-CAS/SNCA corpus")
        else:
            failures.append("no records/srcas/*.txt inputs copied")
            print("No SR-CAS/SNCA records found")

        # The owed trigger is a separate operational assertion. Preserve its
        # actual result as evidence; do not conflate it with checker integrity.
        owed = subprocess.run([sys.executable, checker, "--owed"], cwd=package_root,
                              capture_output=True, text=True, timeout=180)
        print("OWED-ON-RECEIPT AUDIT: %s (exit %d)" %
              ("PASS" if owed.returncode == 0 else "FINDINGS", owed.returncode))
        print((owed.stdout or "")[-12000:])
        if owed.stderr:
            print("OWED STDERR:", owed.stderr[-2000:])

        # Exercise the command's no-report failure and historical date boundary.
        import srcas_check
        no_report = os.path.join(package_root, "no-report.txt")
        with open(no_report, "w", encoding="utf-8") as f:
            f.write("A plain text file with no assessment block.\n")
        p = subprocess.run([sys.executable, checker, no_report], cwd=package_root,
                           capture_output=True, text=True, timeout=30)
        ok = p.returncode == 1 and "no SR-CAS or SNCA report found" in p.stdout
        print("%-58s %s" % ("A current undated file with no report fails", "PASS" if ok else "FAIL"))
        if not ok:
            failures.append("no-report file was not rejected")

        # Date exemption is a reporting rule, not a blanket bypass of the checker.
        historical = "DATED 29 October 2026\n"
        current = "DATED 30 October 2026\n"
        old_ok = srcas_check.dated_from(historical) is False
        new_ok = srcas_check.dated_from(current) is True
        print("%-58s %s" % ("Pre-31-Oct historical exemption boundary", "PASS" if old_ok and new_ok else "FAIL"))
        if not (old_ok and new_ok):
            failures.append("historical date boundary incorrect")

        # Probe the canonical parser's enforcement boundaries. These are
        # diagnostic findings, not yet adopted policy or patched behaviour.
        mismatch_proceed = srcas_check.GOOD_V.replace("MATCH: YES", "MATCH: NO")
        mismatch_result = srcas_check.check(mismatch_proceed)
        mismatch_accepted = bool(mismatch_result) and not mismatch_result[0][2]
        print("%-58s %s" % ("Canonical checker rejects MATCH: NO with PROCEED",
                            "PASS" if not mismatch_accepted else "KNOWN DEFECT: ACCEPTED"))

        missing_weight = srcas_check.GOOD_V + srcas_check.GOOD_R.replace(
            "Comparison-class weight (L-416): x1.5", "Comparison-class weight (L-416): N/A")
        weight_result = srcas_check.check(missing_weight)
        weight_accepted = bool(weight_result) and not weight_result[0][2]
        print("%-58s %s" % ("Canonical checker requires numeric comparison weight",
                            "PASS" if not weight_accepted else "KNOWN DEFECT: ACCEPTED"))

        missing_index = srcas_check.GOOD_V + srcas_check.GOOD_R.replace(
            "Weighted index: 1.00", "Weighted index: N/A")
        index_result = srcas_check.check(missing_index)
        index_accepted = bool(index_result) and not index_result[0][2]
        print("%-58s %s" % ("Canonical checker requires numeric weighted index",
                            "PASS" if not index_accepted else "KNOWN DEFECT: ACCEPTED"))

        duplicate_base = srcas_check.GOOD_V + srcas_check.GOOD_R.replace(
            "MANDATORY CORRECTIONS: none",
            "Base Score: 0.79\nMANDATORY CORRECTIONS: none")
        duplicate_result = srcas_check.check(duplicate_base)
        duplicate_accepted = bool(duplicate_result) and not duplicate_result[0][2]
        print("%-58s %s" % ("Canonical checker rejects duplicate Base Score field",
                            "PASS" if not duplicate_accepted else "KNOWN DEFECT: ACCEPTED"))

        # Negative arithmetic control against the canonical checker function.
        bad = srcas_check.GOOD_V + srcas_check.GOOD_R.replace("Base Score: 0.79", "Base Score: 0.90")
        results = srcas_check.check(bad)
        arithmetic_rejected = bool(results) and any("does not recompute" in x for x in results[0][2])
        print("%-58s %s" % ("Incorrect SR-CAS Base Score is rejected", "PASS" if arithmetic_rejected else "FAIL"))
        if not arithmetic_rejected:
            failures.append("incorrect SR-CAS Base Score accepted")

        # Negative SNCA control: wrong weighted formula must fail.
        bad_sn = srcas_check.GOOD_S.replace("Base Score: 0.31", "Base Score: 0.50")
        results = srcas_check.check(bad_sn)
        snca_rejected = bool(results) and any("does not recompute" in x for x in results[0][2])
        print("%-58s %s" % ("Incorrect SNCA Base Score is rejected", "PASS" if snca_rejected else "FAIL"))
        if not snca_rejected:
            failures.append("incorrect SNCA Base Score accepted")

    print("D2 RESULT: %s" % ("FAIL" if failures else "PASS"))
    for failure in failures:
        print(" - " + failure)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
