#!/usr/bin/env python3
"""Experimental fail-closed launcher for Path B D1b skeleton generation.

This is a proposal-branch prototype. It does not modify format_check.py or canonical
protocol code. It preflights the generation closure, checks the request classifier,
and validates canonical subprocess output before returning a generated skeleton.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
SCRIPTS = ROOT / "scripts"

REQUIRED = (
    TOOLS / "format_check.py",
    TOOLS / "utility.py",
    TOOLS / "manifestation.py",
    SCRIPTS / "canonical_reference.py",
)


def fail(message: str, code: int = 2) -> int:
    print(f"D1b GUARD: FAIL: {message}", file=sys.stderr)
    return code


def main(argv: list[str]) -> int:
    if len(argv) < 3 or argv[1] not in ("navigation", "findings"):
        return fail("usage: path_b_d1b_guard.py navigation|findings QUESTION")

    mode = argv[1]
    question = " ".join(argv[2:]).strip()
    if not question:
        return fail("question must not be empty")

    missing = [str(p.relative_to(ROOT)) for p in REQUIRED if not p.is_file()]
    if missing:
        return fail("required D1b source file(s) missing: " + ", ".join(missing))

    # Load the same request classifier the skeleton calls. Do not accept its generic
    # fallback placeholders as a successful request classification.
    sys.path[:0] = [str(TOOLS), str(SCRIPTS)]
    try:
        import utility
        kind, avenues = utility.request_of(question)
    except Exception as exc:
        return fail(f"utility request classification failed: {type(exc).__name__}: {exc}")
    if kind == "request kind" or not isinstance(avenues, list) or any(
        str(x).startswith("⟨FILL:") for x in avenues
    ):
        return fail("request classifier returned generic or unfilled fallback values")

    if mode == "navigation":
        canonical = subprocess.run(
            [sys.executable, str(SCRIPTS / "canonical_reference.py"),
             "--navigate", question, "--session", "1"],
            cwd=ROOT, text=True, capture_output=True,
        )
        if canonical.returncode != 0:
            return fail(f"canonical navigation subprocess exited {canonical.returncode}: {canonical.stderr[-1000:]}")
        if "MATH-GATE" not in canonical.stdout or "DOMAIN VERBATIM:" not in canonical.stdout:
            return fail("canonical navigation subprocess returned incomplete output")

        cmd = [sys.executable, str(TOOLS / "format_check.py"), "--skeleton", question]
    else:
        cmd = [sys.executable, str(TOOLS / "format_check.py"),
               "--skeleton", "findings", question]

    generated = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    if generated.returncode != 0:
        return fail(f"skeleton generator exited {generated.returncode}: {generated.stderr[-1000:]}")
    if mode == "navigation":
        required_markers = ("DOMAIN VERBATIM:", "MATH-GATE", "FIRST-DRAFT SEAL")
    else:
        required_markers = ("FINDINGS BY AVENUE", "ACROSS THE AVENUES")
    absent = [m for m in required_markers if m not in generated.stdout]
    if absent:
        return fail("generated skeleton is incomplete; missing markers: " + ", ".join(absent))
    if "FILL: request kind" in generated.stdout or "FILL: avenues" in generated.stdout:
        return fail("generated skeleton contains the generic request-classification fallback")

    print(generated.stdout, end="")
    print(f"D1b GUARD: PASS ({mode}; request {kind}; avenues {len(avenues)})", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
