#!/usr/bin/env python3
"""Proposal-only D2-B delegated-dispatch contract test.

Mocks checker loading: tests output_form's forwarding and FAIL propagation for
NAVIGATION, FINDINGS, SR-CAS, SNCA, INTRODUCTION. Does not execute real checkers
or certificate procedures; not evidence of substantive form validity.
"""
import os
import sys
from unittest.mock import patch

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import output_form as of


class Format:
    def __init__(self):
        self.calls = []
    def check(self, text):
        self.calls.append(("navigation", text))
        return [("FAIL", "navigation negative control", "rejected")]
    def findings_check(self, text):
        self.calls.append(("findings", text))
        return [("FAIL", "findings negative control", "rejected")]


class Srcas:
    def __init__(self):
        self.calls = []
    def check(self, text):
        self.calls.append(text)
        return [("SR-CAS", "synthetic", ["negative control"]),
                ("SNCA", "synthetic", [])]


class Intro:
    SRC = "synthetic-json-path"
    class json:
        @staticmethod
        def load(stream):
            return {"synthetic": True}
    def __init__(self):
        self.calls = []
    def check(self, text, data):
        self.calls.append((text, data))
        return ["negative control"]


def main():
    errors = []
    fmt, srcas, intro = Format(), Srcas(), Intro()
    loaders = {"tools/format_check.py": fmt, "tools/srcas_check.py": srcas,
               "tools/intro_output.py": intro}
    def loader(rel, alias):
        if rel not in loaders:
            raise AssertionError("Unexpected checker import: " + rel)
        return loaders[rel]

    # The Introduction dispatcher reads SRC. Patch builtins.open narrowly:
    # no filesystem or canonical content is needed for this mocked contract.
    class DummyFile:
        def __enter__(self):
            return self
        def __exit__(self, *args):
            return False
    def fake_open(path, **kwargs):
        if path != intro.SRC:
            raise AssertionError("Unexpected file read: " + str(path))
        return DummyFile()

    with patch.object(of, "_load", side_effect=loader), patch("builtins.open", side_effect=fake_open):
        for name, expected_label in [
            ("NAVIGATION", "navigation negative control"),
            ("FINDINGS PRESENTATION", "findings negative control"),
            ("SR-CAS ASSESSMENT", "SR-CAS report: synthetic"),
            ("SNCA ASSESSMENT", "SR-CAS report: synthetic"),
            ("INTRODUCTION", "Introduction (tools/intro_output.py --check)"),
        ]:
            result = of.form_checks("SYNTHETIC INVALID", name)
            ok = bool(result) and result[0][0] == "FAIL" and result[0][1] == expected_label
            if not ok:
                errors.append(name + " did not propagate checker failure: " + repr(result))
            print("%s %s — delegated negative checker outcome" % ("PASS" if ok else "FAIL", name))
    if fmt.calls != [("navigation", "SYNTHETIC INVALID"), ("findings", "SYNTHETIC INVALID")]:
        errors.append("format checker forwarding mismatch")
    if srcas.calls != ["SYNTHETIC INVALID", "SYNTHETIC INVALID"]:
        errors.append("SR-CAS/SNCA checker forwarding mismatch")
    if intro.calls != [("SYNTHETIC INVALID", {"synthetic": True})]:
        errors.append("Introduction checker forwarding mismatch")
    for e in errors:
        print("FAIL: " + e)
    print("D2-B DELEGATED DISPATCH: %s (mocked checkers, no procedures executed)" %
          ("FAIL" if errors else "PASS"))
    return int(bool(errors))


if __name__ == "__main__":
    sys.exit(main())
