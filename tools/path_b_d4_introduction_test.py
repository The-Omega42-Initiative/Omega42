#!/usr/bin/env python3
"""Path B D4 Introduction validation in an isolated read-only package."""
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE = "docs/Omega42_Core_Specification_V335_Rev450_STABLE.docx"
INPUTS = [
    "tools/intro_output.py",
    "records/introduction/introduction.json",
    "records/introduction/legitimacy.json",
    "records/introduction/philosophy.json",
    "examples/introduction_opening.txt",
    CORE,
]


def main():
    failures = []
    with tempfile.TemporaryDirectory(prefix="omega42-d4-introduction-") as package_root:
        for rel in INPUTS:
            source = os.path.join(ROOT, rel)
            if not os.path.isfile(source):
                print("D4 FAIL: missing declared input " + rel)
                failures.append("missing " + rel)
                continue
            target = os.path.join(package_root, rel)
            os.makedirs(os.path.dirname(target), exist_ok=True)
            shutil.copy2(source, target)
        script = os.path.join(package_root, "tools", "intro_output.py")

        def run(args, label, expected=0):
            p = subprocess.run([sys.executable, script] + args, cwd=package_root,
                               capture_output=True, text=True, timeout=120)
            ok = p.returncode == expected
            print("%-62s %s (exit %d, expected %d)" %
                  (label, "PASS" if ok else "FAIL", p.returncode, expected))
            if p.stdout:
                print(p.stdout[-7000:])
            if p.stderr:
                print("STDERR:", p.stderr[-2000:])
            if not ok:
                failures.append(label)
            return p

        run(["--selftest"], "Introduction renderer/checker selftest")
        run(["--terms"], "Words Explained consistency")
        run(["--check", os.path.join(package_root, "examples", "introduction_opening.txt")],
            "Canonical Opening example")
        run(["--core", os.path.join(package_root, CORE)], "Core IN-OPEN / IN-00 correspondence")
        run(["--legitimacy", os.path.join(package_root, CORE)], "Legitimacy register against Core")
        run(["--philosophy", os.path.join(package_root, CORE)], "Philosophical register against Core")

        # Render an Opening using the current renderer and re-check the exact output.
        rendered = subprocess.run(
            [sys.executable, script, "--render", "--navigator", "D4-Test-Model",
             "--org", "Omega42 Test", "--date", "23 November 2026",
             "--execution", "SCRIPT-CAPABLE"],
            cwd=package_root, capture_output=True, text=True, timeout=60)
        rendered_path = os.path.join(package_root, "rendered-opening.txt")
        with open(rendered_path, "w", encoding="utf-8") as f:
            f.write(rendered.stdout)
        render_ok = rendered.returncode == 0 and not rendered.stderr
        print("%-62s %s" % ("Renderer produces output", "PASS" if render_ok else "FAIL"))
        if not render_ok:
            failures.append("renderer failed")
        if render_ok:
            run(["--check", rendered_path], "Rendered Opening passes checker")

        # Round-trip the first-navigation close (Friendly Notes + Identity
        # Block) through the same isolated renderer and its --first checker.
        first_rendered = subprocess.run(
            [sys.executable, script, "--first-render"],
            cwd=package_root, capture_output=True, text=True, timeout=60)
        first_path = os.path.join(package_root, "rendered-first-close.txt")
        with open(first_path, "w", encoding="utf-8") as f:
            f.write(first_rendered.stdout)
        first_render_ok = first_rendered.returncode == 0 and not first_rendered.stderr
        print("%-62s %s" % ("Renderer produces first-navigation close", "PASS" if first_render_ok else "FAIL"))
        if not first_render_ok:
            failures.append("first-navigation close renderer failed")
        if first_render_ok:
            run(["--first", first_path], "Rendered first-navigation close passes checker")

    print("D4 RESULT: %s" % ("FAIL" if failures else "PASS"))
    for failure in failures:
        print(" - " + failure)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
