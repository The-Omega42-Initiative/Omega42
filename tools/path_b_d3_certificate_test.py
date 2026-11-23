#!/usr/bin/env python3
"""Path B D3 static certificate syntax validation.

This profile invokes --check only. It deliberately never invokes --verify,
run_procedure(), shell commands, or any certificate procedure.
"""
import glob
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    failures = []
    with tempfile.TemporaryDirectory(prefix="omega42-d3-certificates-") as package_root:
        source = os.path.join(ROOT, "tools", "certify.py")
        if not os.path.isfile(source):
            print("D3 FAIL: tools/certify.py missing")
            return 1
        checker = os.path.join(package_root, "tools", "certify.py")
        os.makedirs(os.path.dirname(checker), exist_ok=True)
        shutil.copy2(source, checker)
        guard_source = os.path.join(ROOT, "tools", "path_b_d3_certificate_guard.py")
        guard = os.path.join(package_root, "tools", "path_b_d3_certificate_guard.py")
        if not os.path.isfile(guard_source):
            print("D3 FAIL: strict certificate guard missing")
            return 1
        shutil.copy2(guard_source, guard)
        certs = []
        for path in sorted(glob.glob(os.path.join(ROOT, "records", "certificates", "CERT-*.txt"))):
            rel = os.path.relpath(path, ROOT)
            dest = os.path.join(package_root, rel)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.copy2(path, dest)
            certs.append(dest)
        print("D3 isolated package inputs: checker=1, certificate records=%d" % len(certs))

        def run(args, label, expected=0):
            p = subprocess.run([sys.executable, checker] + args, cwd=package_root,
                               capture_output=True, text=True, timeout=120)
            ok = p.returncode == expected
            print("%-58s %s (exit %d, expected %d)" %
                  (label, "PASS" if ok else "FAIL", p.returncode, expected))
            if p.stdout:
                print(p.stdout[-7000:])
            if p.stderr:
                print("STDERR:", p.stderr[-2000:])
            if not ok:
                failures.append(label)
            return p

        run(["--selftest"], "Canonical certificate checker selftest")
        if certs:
            run(["--check"] + certs, "All archived certificates pass static syntax check")
        else:
            failures.append("no certificate records copied")
            print("No certificate records found")
        run(["--list"], "Certificate inventory command")
        if certs:
            strict_run = subprocess.run([sys.executable, guard] + certs, cwd=package_root,
                                        capture_output=True, text=True, timeout=120)
            strict_ok = strict_run.returncode == 0
            print("All archived certificates strict-guard: %s (exit %d)" %
                  ("PASS" if strict_ok else "FINDINGS", strict_run.returncode))
            print((strict_run.stdout or "")[-8000:])
            if strict_run.stderr:
                print("STRICT STDERR:", strict_run.stderr[-2000:])
            if not strict_ok:
                failures.append("strict guard reported findings in archived certificate corpus")

        # Static validation must not execute the command named in PROCEDURE.
        sys.path.insert(0, os.path.join(package_root, "tools"))
        import certify
        probe = os.path.join(package_root, "side-effect-probe.txt")
        sample = certify.skeleton("D3 static execution boundary test")
        sample = sample.replace("[FILL: four digits]", "9998")
        sample = sample.replace("[FILL: " + " / ".join(certify.KINDS) + "]", "COMPUTATIONAL")
        sample = sample.replace("[FILL: the command anyone can run]", "touch side-effect-probe.txt")
        sample = sample.replace("[FILL: the folder it runs in, or .]", ".")
        sample = sample.replace("[FILL: SHA-256 of the procedure's output]", "0" * 64)
        sample = sample.replace("[FILL: " + " / ".join(certify.STATUSES) + "]", "CERTIFIED")
        import re
        sample = re.sub(r"\[FILL: [^\]]*\]", "x", sample)
        test_file = os.path.join(package_root, "static-probe.txt")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(sample)
        p = subprocess.run([sys.executable, checker, "--check", test_file], cwd=package_root,
                           capture_output=True, text=True, timeout=30)
        not_executed = not os.path.exists(probe)
        print("%-58s %s" % ("--check does not execute PROCEDURE shell text",
                            "PASS" if not_executed else "FAIL"))
        if not not_executed:
            failures.append("static --check executed a procedure")
        if p.returncode != 0:
            print(p.stdout)
            print(p.stderr)
            failures.append("synthetic certificate failed static syntax check")

        # Probe canonical field-content and duplicate-field handling.
        blank_subject = sample.replace("SUBJECT: x", "SUBJECT: ")
        blank_ok = certify.check(blank_subject) == []
        print("%-58s %s" % ("Canonical checker rejects blank SUBJECT",
                            "PASS" if not blank_ok else "KNOWN DEFECT: ACCEPTED"))
        duplicate_subject = sample.replace("RESULT: x", "SUBJECT: duplicate\nRESULT: x")
        duplicate_ok = certify.check(duplicate_subject) == []
        print("%-58s %s" % ("Canonical checker rejects duplicate SUBJECT",
                            "PASS" if not duplicate_ok else "KNOWN DEFECT: ACCEPTED"))

        # The strict wrapper must reject both malformed controls.
        strict_controls = [
            ("blank SUBJECT", blank_subject),
            ("duplicate SUBJECT", duplicate_subject),
        ]
        strict_ok = True
        for name, content in strict_controls:
            path = os.path.join(package_root, "strict-negative-" + str(len(name)) + ".txt")
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            p = subprocess.run([sys.executable, guard, path], cwd=package_root,
                               capture_output=True, text=True, timeout=30)
            rejected = p.returncode == 1
            print("  strict negative control %-35s %s" % (name, "REJECTED" if rejected else "ACCEPTED"))
            strict_ok &= rejected
        if not strict_ok:
            failures.append("strict guard accepted a blank or duplicate field")
        blank_subject = sample.replace("SUBJECT: x", "SUBJECT: ")
        blank_ok = certify.check(blank_subject) == []
        print("%-58s %s" % ("Canonical checker rejects blank SUBJECT",
                            "PASS" if not blank_ok else "KNOWN DEFECT: ACCEPTED"))
        duplicate_subject = sample.replace("RESULT: x", "SUBJECT: duplicate\nRESULT: x")
        duplicate_ok = certify.check(duplicate_subject) == []
        print("%-58s %s" % ("Canonical checker rejects duplicate SUBJECT",
                            "PASS" if not duplicate_ok else "KNOWN DEFECT: ACCEPTED"))

    print("D3 RESULT: %s" % ("FAIL" if failures else "PASS"))
    for failure in failures:
        print(" - " + failure)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
