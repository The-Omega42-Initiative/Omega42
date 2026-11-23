#!/usr/bin/env python3
"""Experimental Path B D5a strict package guard.

This wrapper adds package-level cardinality and duplicate-domain checks before
delegating per-file arithmetic, format and layer checks to canonical M314.
It does not modify or replace tools/conformance.py.
"""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import conformance as m314

DOMAIN = re.compile(r"DOMAIN VERBATIM:\s*(.+)")

def strict_report(paths, set_path=m314.SET):
    rows = m314.load_set(set_path)
    wanted = {domain: tag for tag, domain in rows}
    errors = []
    if len(wanted) != len(rows):
        errors.append("practice set contains duplicate domain definitions")
    if len(paths) != len(wanted):
        errors.append("file count %d does not equal required domain count %d" % (len(paths), len(wanted)))

    seen = {}
    for path in paths:
        try:
            with open(path, encoding="utf-8") as handle:
                text = handle.read()
        except Exception as exc:
            errors.append("%s: cannot read fixture (%s)" % (os.path.basename(path), exc))
            continue
        match = DOMAIN.search(text)
        if not match:
            errors.append("%s: missing DOMAIN VERBATIM" % os.path.basename(path))
            continue
        domain = match.group(1).strip()
        if domain not in wanted:
            errors.append("%s: domain is outside the exact practice set" % os.path.basename(path))
            continue
        if domain in seen:
            errors.append("%s: duplicate domain %s (already in %s)" %
                          (os.path.basename(path), wanted[domain], os.path.basename(seen[domain])))
        else:
            seen[domain] = path

    missing = [tag for tag, domain in rows if domain not in seen]
    if missing:
        errors.append("missing required domains: " + ", ".join(missing))

    try:
        canonical_text, canonical_verdict = m314.report(paths, set_path)
    except Exception as exc:
        canonical_text = "Canonical M314 report raised: %s" % repr(exc)
        canonical_verdict = "NOT YET COMPATIBLE"

    L = [
        "PATH B D5a STRICT PACKAGE GUARD",
        "PROFILE: exactly one readable navigation per exact practice-set domain",
        "INPUT FILES: %d | REQUIRED DOMAINS: %d" % (len(paths), len(wanted)),
    ]
    if errors:
        L.append("GUARD: FAIL")
        L.extend("  [FAIL] " + item for item in errors)
        verdict = "NOT YET COMPATIBLE"
    else:
        L.append("GUARD: PASS -- exact one-to-one domain/file coverage")
        verdict = canonical_verdict
    L.append("")
    L.append(canonical_text)
    L.append("")
    L.append("PATH B D5a RESULT: " + verdict)
    return "\n".join(L), verdict

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)
    if args[0] == "--check":
        directory = args[1]
        set_path = args[2] if len(args) > 2 else m314.SET
        paths = sorted(path for path in glob.glob(os.path.join(directory, "*")) if os.path.isfile(path))
        report, verdict = strict_report(paths, set_path)
        print(report)
        sys.exit(0 if verdict.startswith("COMPATIBLE") else 1)
    sys.exit("unknown option: " + args[0])
