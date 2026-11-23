#!/usr/bin/env python3
"""Path B read-only output-form registry/dispatch contract characterization.

No canonical checker is modified. No certificate procedure is executed.
The known Navigator's Account dispatch defect is an EXPECTED characterization,
not a passing substantive validation of that form.
"""
import ast
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = os.path.join(ROOT, "tools", "output_form.py")


def main():
    with open(SOURCE, encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=SOURCE)
    registry = next((node for node in tree.body if isinstance(node, ast.Assign)
                     and any(isinstance(t, ast.Name) and t.id == "FORMS" for t in node.targets)), None)
    dispatch = next((node for node in tree.body if isinstance(node, ast.FunctionDef)
                     and node.name == "form_checks"), None)
    if registry is None or dispatch is None:
        print("FAIL: registry or dispatcher missing")
        return 1
    forms = ast.literal_eval(registry.value)
    names = [row[0] for row in forms]
    failures = []
    if len(names) != 13 or len(set(names)) != 13:
        failures.append("expected 13 distinct registered forms, found %d (%d distinct)" %
                        (len(names), len(set(names))))
    expected_marker_only = {"SR-CAS REPLICATION PACKAGE", "COMPARATIVE EXPLORATION REPORT"}
    declared_marker_only = {name for name, _, _, checker, _ in forms if checker == "markers"}
    if declared_marker_only != expected_marker_only:
        failures.append("marker-only registry changed: %r" % sorted(declared_marker_only))
    account = [row for row in forms if row[0] == "NAVIGATOR'S ACCOUNT"]
    if len(account) != 1 or account[0][3] != "tools/account_check.py":
        failures.append("Navigator's Account checker declaration changed")
    # Inspect explicit equality branches; no import or dynamic execution is needed.
    branch_forms = set()
    for node in ast.walk(dispatch):
        if not isinstance(node, ast.Compare) or not isinstance(node.left, ast.Name) or node.left.id != "form":
            continue
        for op, comparator in zip(node.ops, node.comparators):
            if isinstance(op, ast.Eq) and isinstance(comparator, ast.Constant) and isinstance(comparator.value, str):
                branch_forms.add(comparator.value)
    known_defect = "NAVIGATOR'S ACCOUNT" not in branch_forms
    if not known_defect:
        failures.append("Account dispatch changed; re-audit before replacing known-defect assertion")
    print("Registered forms: %d (expected 13)" % len(names))
    print("Declared marker-only forms: %s" % ", ".join(sorted(declared_marker_only)))
    print("Navigator's Account declared checker: %s" %
          (account[0][3] if account else "MISSING"))
    print("Navigator's Account explicit dispatch: %s" %
          ("KNOWN MISMATCH REPRODUCED" if known_defect else "CHANGED — REVIEW REQUIRED"))
    print("Static-only: no form checker or certificate procedure executed")
    for failure in failures:
        print("FAIL: " + failure)
    print("D2-B REGISTRY CONTRACT: %s" % ("PASS (known defect characterized)" if not failures else "FAIL"))
    return int(bool(failures))


if __name__ == "__main__":
    sys.exit(main())
