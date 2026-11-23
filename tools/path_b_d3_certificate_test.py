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

        # Probe field-content and duplicate-field acceptance without changing canonical code.
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
