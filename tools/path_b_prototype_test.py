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

    # Negative control: remove the scanner while keeping the format checker.
    # Current code catches the dynamic-load exception, sets _JS=None, and continues.
    degraded = base / "D1a-missing-scanner"
    copy_file("scripts/canonical_reference.py", degraded)
    copy_file("tools/format_check.py", degraded)
    probe = run("D1a negative-control scanner probe", degraded, [
        "-c",
        "import sys; sys.path.insert(0, 'tools'); import format_check; "
        "assert format_check._JS is None; print('FULL M193 SCANNER UNAVAILABLE')",
    ])
    if "FULL M193 SCANNER UNAVAILABLE" not in probe.stdout:
        raise AssertionError("D1a negative control did not confirm the scanner was absent")
    run("D1a known degraded-mode self-test (must be recorded as a gap)", degraded,
        ["tools/format_check.py", "--selftest"])
    print("KNOWN GAP D1a: checker self-test still passes when the full M193 scanner is absent")


def profile_d1b(base: Path) -> None:
    pkg = base / "D1b"
    for src in (
        "scripts/canonical_reference.py",
        "scripts/m193_m225.py",
        "tools/format_check.py",
        "tools/utility.py",
        "tools/manifestation.py",
        "tools/path_b_d1b_guard.py",
    ):
        copy_file(src, pkg)
    assert_absent(pkg, ["records", "docs", "omega42.identity.json"], "D1b excludes repository registers and canonical DOCX")
    skeleton = run("D1b navigation skeleton generation", pkg,
                   ["tools/format_check.py", "--skeleton", "What is time?"])
    if "DOMAIN VERBATIM: What is time?" not in skeleton.stdout or "MATH-GATE" not in skeleton.stdout:
        raise AssertionError("D1b did not generate the expected canonical navigation skeleton")
    findings = run("D1b findings skeleton generation", pkg,
                   ["tools/format_check.py", "--skeleton", "findings", "What is time?"])
    if "FINDINGS BY AVENUE" not in findings.stdout:
        raise AssertionError("D1b did not generate the findings presentation skeleton")
    run("D1b guarded navigation generation", pkg,
        ["tools/path_b_d1b_guard.py", "navigation", "What is time?"])
    run("D1b guarded findings generation", pkg,
        ["tools/path_b_d1b_guard.py", "findings", "What is time?"])
    run("D1b combined format and skeleton self-test", pkg, ["tools/format_check.py", "--selftest"])

    # Minimal generation-only package: M193 is not called by skeleton rendering.
    skeleton_only = base / "D1b-skeleton-only"
    for src in ("scripts/canonical_reference.py", "tools/format_check.py",
                "tools/utility.py", "tools/manifestation.py", "tools/path_b_d1b_guard.py"):
        copy_file(src, skeleton_only)
    minimal = run("D1b minimal generation without M193 scanner", skeleton_only,
                  ["tools/format_check.py", "--skeleton", "What is time?"])
    if "DOMAIN VERBATIM: What is time?" not in minimal.stdout:
        raise AssertionError("D1b minimal generation-only package did not generate the domain block")
    run("D1b guard works without optional M193 scanner", skeleton_only,
        ["tools/path_b_d1b_guard.py", "navigation", "What is time?"])
    print("PASS D1b minimal skeleton-generation closure excludes M193 scanner")

    # Negative control 1: utility.py is absent. skeleton() catches the import failure
    # and substitutes generic request labels instead of failing.
    no_utility = base / "D1b-missing-utility"
    copy_file("scripts/canonical_reference.py", no_utility)
    copy_file("scripts/m193_m225.py", no_utility)
    copy_file("tools/format_check.py", no_utility)
    copy_file("tools/manifestation.py", no_utility)
    copy_file("tools/path_b_d1b_guard.py", no_utility)
    guarded_u = run("D1b guard refuses missing utility", no_utility,
                    ["tools/path_b_d1b_guard.py", "navigation", "What is time?"], expect=2)
    if "required D1b source file(s) missing" not in guarded_u.stderr:
        raise AssertionError("D1b guard did not fail closed on missing utility.py")
    degraded_u = run("D1b negative-control missing utility", no_utility,
                     ["tools/format_check.py", "--skeleton", "What is time?"])
    if "FILL: request kind" not in degraded_u.stdout or "FILL: avenues" not in degraded_u.stdout:
        raise AssertionError(f"D1b missing-utility fallback was not observed:\\n{degraded_u.stdout[-5000:]}")
    print("KNOWN GAP D1b: skeleton generation silently substitutes generic request labels without utility.py")

    # Negative control 2: canonical_reference.py is absent. The subprocess return code
    # is ignored and skeleton generation still exits successfully without generated blocks.
    no_canonical = base / "D1b-missing-canonical"
    copy_file("scripts/m193_m225.py", no_canonical)
    copy_file("tools/format_check.py", no_canonical)
    copy_file("tools/utility.py", no_canonical)
    copy_file("tools/manifestation.py", no_canonical)
    copy_file("tools/path_b_d1b_guard.py", no_canonical)
    guarded_c = run("D1b guard refuses missing canonical reference", no_canonical,
                    ["tools/path_b_d1b_guard.py", "navigation", "What is time?"], expect=2)
    if "required D1b source file(s) missing" not in guarded_c.stderr:
        raise AssertionError("D1b guard did not fail closed on missing canonical_reference.py")
    degraded_c = run("D1b negative-control missing canonical subprocess", no_canonical,
                     ["tools/format_check.py", "--skeleton", "What is time?"])
    if "[1] MATH-GATE" in degraded_c.stdout:
        raise AssertionError("D1b missing-canonical control unexpectedly generated canonical blocks")
    print("KNOWN GAP D1b: skeleton generation ignores a failed canonical subprocess and exits successfully")


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
        if not re.search(re.escape(label) + r"\s+PASS\b", check.stdout):
            raise AssertionError(f"D5a smoke test missing required passing check {label}:\n{check.stdout[-7000:]}")
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
        profile_d1b(base)
        profile_d4(base)
        profile_d5a(base)
    print("PATH B MINIMAL PACKAGE PROTOTYPES: PASS")
    print("Evidence is limited to these command paths and this source checkout; it is not L-493 or a release approval.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
