#!/usr/bin/env python3
"""Experimental Path B package-isolation prototype tests.

Builds four temporary packages from the checked-out source tree, copies only their
declared closure, and runs the real CLI commands from those isolated roots.
This is proposal evidence, not a canonical release validator or a replacement for L-493.
"""
from __future__ import annotations

import hashlib
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "submissions/navigations/NAV-2026-0021.txt"


def copy_file(src: str, dst_root: Path, dst: str | None = None) -> Path:
    source = ROOT / src
    if not source.is_file():
        raise AssertionError(f"missing source input: {src}")
    target = dst_root / (dst or src)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    return target


def run(label: str, cwd: Path, args: list[str], expect: int = 0) -> subprocess.CompletedProcess[str]:
    p = subprocess.run([sys.executable, *args], cwd=cwd, text=True, capture_output=True)
    if p.returncode != expect:
        raise AssertionError(
            f"{label}: expected exit {expect}, got {p.returncode}\n"
            f"STDOUT:\n{p.stdout[-5000:]}\nSTDERR:\n{p.stderr[-3000:]}"
        )
    print(f"PASS {label}")
    return p


def assert_absent(root: Path, paths: list[str], label: str) -> None:
    present = [p for p in paths if (root / p).exists()]
    if present:
        raise AssertionError(f"{label}: unexpected files present: {present}")
    print(f"PASS {label}")


def profile_c1(base: Path) -> None:
    pkg = base / "C1"
    copy_file("scripts/canonical_reference.py", pkg)
    assert_absent(pkg, ["tools", "records", "docs", "omega42.identity.json"], "C1 excludes unrelated project data")
    run("C1 canonical known-answer self-test", pkg, ["scripts/canonical_reference.py", "--test"])
    run("C1 calibration command", pkg, ["scripts/canonical_reference.py", "--calibrate"])
    nav = run("C1 ordinary navigation command", pkg,
              ["scripts/canonical_reference.py", "--navigate", "What is time?"])
    if "SCRIPT SHA-256:" not in nav.stdout:
        raise AssertionError("C1 did not report its source digest")
    print("PASS C1 source-digest self-read")


def profile_d1a(base: Path) -> None:
    pkg = base / "D1a"
    copy_file("scripts/canonical_reference.py", pkg)
    copy_file("scripts/m193_m225.py", pkg)
    copy_file("tools/format_check.py", pkg)
    fixture = copy_file("submissions/navigations/NAV-2026-0021.txt", pkg, "inputs/NAV-2026-0021.txt")
    assert_absent(pkg, ["records", "docs", "omega42.identity.json"], "D1a excludes research registers and canonical DOCX")
    run("D1a format-checker self-test", pkg, ["tools/format_check.py", "--selftest"])
    run("D1a existing-output check", pkg, ["tools/format_check.py", str(fixture.relative_to(pkg))])
    # Verify the required dynamic scanner is actually available in this package.
    if not (pkg / "scripts/m193_m225.py").is_file():
        raise AssertionError("D1a jargon scanner missing")
    print("PASS D1a required dynamic scanner present")


def profile_d4(base: Path) -> None:
    pkg = base / "D4"
    copy_file("tools/handshake.py", pkg)
    copy_file("omega42.identity.json", pkg)
    copy_file("records/release_documents_SHA256.txt", pkg)
    copy_file("docs/Omega42_Core_Specification_V335_Rev450_STABLE.docx", pkg)
    copy_file("docs/Omega42_Companion_Document_V335_Rev450_STABLE.docx", pkg)
    assert_absent(pkg, ["scripts", "records/conformance", "records/frameworks"], "D4 excludes unrelated code and research datasets")
    run("D4 arithmetic fingerprint", pkg, ["tools/handshake.py", "fingerprint"])
    run("D4 live challenge", pkg, ["tools/handshake.py", "challenge", "20261123"])
    run("D4 identity manifest and exact digest closure", pkg, ["tools/handshake.py", "manifest"])
    run("D4 handshake self-test", pkg, ["tools/handshake.py", "--selftest"])


def profile_d5a(base: Path) -> None:
    pkg = base / "D5a"
    files = [
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
        "records/conformance/practice_set.txt",
    ]
    for f in files:
        copy_file(f, pkg)
    fixture = copy_file("submissions/navigations/NAV-2026-0021.txt", pkg, "inputs/NAV-2026-0021.txt")
    assert_absent(pkg, [
        "docs", "omega42.identity.json", "records/frameworks", "records/consciousness",
        "records/congruence", "records/bashar", "records/positive_geometry",
        "records/adaptors/registry.json", "records/instances",
    ], "D5a excludes Core/Companion and unrelated research registers")
    key = run("D5a recomputed practice-set key", pkg, ["tools/conformance.py", "--key"])
    if "CF-01" not in key.stdout or "CF-08" not in key.stdout:
        raise AssertionError("D5a key did not cover all eight public practice domains")
    # This one supplied historical navigation is deliberately outside the public practice set.
    # The correct overall verdict is therefore NOT YET COMPATIBLE; the test asserts that its
    # individual required computations execute and pass, not that one fixture certifies a system.
    check = run("D5a per-navigation conformance smoke test", pkg,
                ["tools/conformance.py", "--check", "inputs"], expect=1)
    for label in ("A1 anchor", "A2 arms", "A3 format", "A4 layer 1"):
        if not re.search(re.escape(label) + r"\\s+PASS\\b", check.stdout):
            raise AssertionError(f"D5a smoke test missing required passing check {label}:\\n{check.stdout[-7000:]}")
    if "OUTSIDE SET" not in check.stdout:
        raise AssertionError(f"D5a smoke test did not identify the fixture as outside the set:\\n{check.stdout[-7000:]}")
    if "NOT YET COMPATIBLE" not in check.stdout:
        raise AssertionError(f"D5a one-fixture smoke test should not claim full set compatibility:\\n{check.stdout[-7000:]}")
    print("PASS D5a correctly distinguishes a passing per-file check from full-set compatibility")


def main() -> int:
    if not FIXTURE.is_file():
        raise SystemExit(f"required smoke-test fixture missing: {FIXTURE}")
    with tempfile.TemporaryDirectory(prefix="omega42-path-b-") as td:
        base = Path(td)
        profile_c1(base)
        profile_d1a(base)
        profile_d4(base)
        profile_d5a(base)
    print("PATH B MINIMAL PACKAGE PROTOTYPES: PASS")
    print("Evidence is limited to these command paths and this source checkout; it is not L-493 or a release approval.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
