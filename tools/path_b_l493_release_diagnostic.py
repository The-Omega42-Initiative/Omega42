#!/usr/bin/env python3
"""Read-only L-493 release mismatch inventory for the proposal branch.

Runs the canonical extractor's *parsing* functions but does not change its
policy, DOCX files or release contents. No extraction/writes to repository.
This diagnostic intentionally exits 0 even when the canonical contract fails:
it reports evidence and must never be mistaken for a release PASS.
"""
import collections
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import extract_embedded as ee


def main():
    docs = [os.path.join(ROOT, "docs", n) for n in
            ("Omega42_Core_Specification_V335_Rev450_STABLE.docx",
             "Omega42_Companion_Document_V335_Rev450_STABLE.docx")]
    embedded = ee.blocks(docs)
    required = set(ee.required(ROOT))
    missing = sorted(required - embedded.keys())
    extra = sorted(set(embedded) - required - set(ee.OUTSIDE) - set(ee.EXEMPT))
    differs = []
    for name, text in embedded.items():
        file = os.path.join(ROOT, name)
        if not os.path.isfile(file):
            continue
        with open(file, encoding="utf-8", newline="") as f:
            disk = f.read()
        exact = name not in ee.LEGACY.values() and name != "scripts/canonical_reference.py"
        if (disk != text) if exact else (disk.rstrip("\n") + "\n" != text):
            differs.append(name)
    prohibited = sorted(set(embedded) & set(ee.OUTSIDE))
    counts = collections.Counter(p.split("/", 1)[0] for p in missing)
    print("L-493 DIAGNOSTIC ONLY — not a release verification or waiver")
    print("embedded=%d required=%d missing=%d differing=%d extra=%d outside_embedded=%d" %
          (len(embedded), len(required), len(missing), len(differs), len(extra), len(prohibited)))
    print("missing by top-level directory: %s" % dict(sorted(counts.items())))
    for label, items in (("NOT EMBEDDED", missing), ("COPY DIFFERS", sorted(differs)),
                         ("EMBEDDED NOT REQUIRED", extra), ("OUTSIDE EMBEDDED", prohibited)):
        for item in items:
            print("%s: %s" % (label, item))
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as f:
            f.write("### L-493 diagnostic (informational, not a waiver)\n\n")
            f.write("Embedded: %d; required: %d; missing: %d; differing: %d; extra: %d; prohibited: %d.\n\n" %
                    (len(embedded), len(required), len(missing), len(differs), len(extra), len(prohibited)))
            f.write("Missing by top-level directory: `%s`\n\n" % dict(sorted(counts.items())))
            f.write("See job log for full path inventory. The canonical release gate remains authoritative.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
