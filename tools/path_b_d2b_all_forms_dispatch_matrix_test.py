#!/usr/bin/env python3
"""Proposal-only 13-form dispatch matrix: static source characterization.

Does not import checkers, execute certificate procedures, or claim semantic
validation. Explicitly records the Navigator's Account fallback as a defect.
"""
import ast
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, "tools", "output_form.py")
EXPECTED = {
    "NAVIGATION": "tools/format_check.py",
    "FINDINGS PRESENTATION": "tools/format_check.py --findings",
    "SR-CAS ASSESSMENT": "tools/srcas_check.py",
    "SNCA ASSESSMENT": "tools/srcas_check.py",
    "APPLIED PROTOCOL EXPLORATION": "tools/output_form.py",
    "APA": "tools/output_form.py",
    "SR-CAS REPLICATION PACKAGE": "markers",
    "COMPARATIVE EXPLORATION REPORT": "markers",
    "INTRODUCTION": "tools/intro_output.py --check",
    "NAVIGATOR'S ACCOUNT": "tools/account_check.py",
    "ANSWER": "tools/output_form.py",
    "CONVERSATION": "tools/output_form.py",
    "CERTIFICATE": "tools/certify.py",
}
EXPLICIT = set(EXPECTED) - {
    "SR-CAS REPLICATION PACKAGE", "COMPARATIVE EXPLORATION REPORT",
    "NAVIGATOR'S ACCOUNT",
}


def main():
    with open(PATH, encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=PATH)
    forms_node = next(n for n in tree.body if isinstance(n, ast.Assign)
                      and any(isinstance(t, ast.Name) and t.id == "FORMS" for t in n.targets))
    dispatch = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "form_checks")
    rows = ast.literal_eval(forms_node.value)
    registered = {row[0]: row[3] for row in rows}
    failures = []
    if len(rows) != 13 or registered != EXPECTED:
        failures.append("13-form registry/checker declarations differ from characterized baseline")
    branches = set()
    for node in ast.walk(dispatch):
        if not isinstance(node, ast.Compare) or not isinstance(node.left, ast.Name) or node.left.id != "form":
            continue
        for op, comp in zip(node.ops, node.comparators):
            if isinstance(op, ast.Eq) and isinstance(comp, ast.Constant) and isinstance(comp.value, str):
                branches.add(comp.value)
            if isinstance(op, ast.In) and isinstance(comp, (ast.Tuple, ast.List)):
                branches.update(e.value for e in comp.elts if isinstance(e, ast.Constant) and isinstance(e.value, str))
    for name in EXPECTED:
        explicit = name in branches
        expected = name in EXPLICIT
        print("%s | checker=%s | dispatch=%s | %s" %
              (name, registered.get(name, "MISSING"), "explicit" if explicit else "fallback",
               "KNOWN DEFECT" if name == "NAVIGATOR'S ACCOUNT" and not explicit else
               "MARKER-ONLY BY DESIGN" if registered.get(name) == "markers" and not explicit else
               "EXPECTED" if explicit == expected else "UNEXPECTED"))
        if explicit != expected:
            failures.append("dispatch changed for %s: explicit=%s expected=%s" % (name, explicit, expected))
    # Confirm that the generic fallback is the exact marker-only PASS in
    # the characterized source, rather than assuming every fallback is safe.
    tail = dispatch.body[-1]
    if not (isinstance(tail, ast.Return) and
            isinstance(tail.value, ast.List) and len(tail.value.elts) == 1 and
            isinstance(tail.value.elts[0], ast.Tuple) and
            isinstance(tail.value.elts[0].elts[0], ast.Constant) and
            tail.value.elts[0].elts[0].value == "PASS"):
        failures.append("fallback structure changed: inspect before interpreting matrix")
    print("D2-B ALL-FORMS STATIC DISPATCH MATRIX: %s" %
          ("PASS (Account defect characterized; no checker execution)" if not failures else "FAIL"))
    for f in failures:
        print("FAIL: " + f)
    return int(bool(failures))


if __name__ == "__main__":
    sys.exit(main())
