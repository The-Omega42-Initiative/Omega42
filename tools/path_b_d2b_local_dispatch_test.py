#!/usr/bin/env python3
"""Path B local form-dispatch regression tests (non-canonical).

Exercises only local, non-executing form checks. Certificate validation calls
certify.check (static) and NEVER certify.verify or run_procedure. The Account
defect is checked as a known negative characterization, not a success claim.
"""
import datetime
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import output_form as of


def fill(s):
    return re.sub(r"\[FILL: [^\]]*\]", "synthetic", s)


def rejected(rows):
    return any(row[0] == "FAIL" for row in rows)


def main():
    d = datetime.date(2026, 11, 7)
    cases = []
    def record(name, ok):
        cases.append((name, bool(ok)))

    for name, constructor, missing in [
        ("ANSWER", of.answer_skeleton, "BASIS: "),
        ("APPLIED PROTOCOL EXPLORATION", of.ape_skeleton, "UNVERIFIED STATEMENTS:"),
        ("APA", of.apa_skeleton, "VERDICT: "),
    ]:
        text = fill(constructor("synthetic question", d))
        record(name + " recognized", of.identify(text) == name)
        record(name + " positive frame/dispatch", not rejected(of.declaration_checks(text, name) + of.form_checks(text, name)))
        changed = text.replace(missing, "REMOVED: ", 1)
        record(name + " missing mandatory field rejected", rejected(of.form_checks(changed, name)))
    conv = fill(of.conversation_skeleton("Hello", d))
    record("CONVERSATION positive frame/dispatch", of.identify(conv) == "CONVERSATION" and
           not rejected(of.declaration_checks(conv, "CONVERSATION") + of.form_checks(conv, "CONVERSATION")))
    record("CONVERSATION missing signature rejected", rejected(of.declaration_checks(
        conv.rsplit("NAVIGATOR:", 1)[0], "CONVERSATION")))

    for name in ("SR-CAS REPLICATION PACKAGE", "COMPARATIVE EXPLORATION REPORT"):
        row = next(row for row in of.FORMS if row[0] == name)
        record(name + " declared marker-only", row[3] == "markers")
        record(name + " returns marker-only (not substantive)", of.form_checks(
            "======= %s =======" % name, name) ==
            [("PASS", "Markers of the form", "checked by its markers")])

    # This static checker must not run any certificate procedure. A deliberately
    # invalid certificate frame should produce a FAIL through certify.check.
    certificate = "======= Ω42 CERTIFICATE =======\nINVALID SYNTHETIC CERTIFICATE\n"
    record("CERTIFICATE invalid static input rejected", rejected(of.form_checks(certificate, "CERTIFICATE")))

    account = "NAVIGATOR'S ACCOUNT (L-509)\nINVALID SYNTHETIC ACCOUNT\n"
    account_row = next(row for row in of.FORMS if row[0] == "NAVIGATOR'S ACCOUNT")
    record("ACCOUNT declared checker but marker-only dispatch (known defect)",
           account_row[3] == "tools/account_check.py" and
           of.form_checks(account, "NAVIGATOR'S ACCOUNT") ==
           [("PASS", "Markers of the form", "checked by its markers")])

    for name, ok in cases:
        print(("%s " % ("PASS" if ok else "FAIL")) + name)
    print("D2-B LOCAL DISPATCH: %d/%d checks; %s" %
          (sum(ok for _, ok in cases), len(cases),
           "PASS (known Account defect remains)" if all(ok for _, ok in cases) else "FAIL"))
    return 0 if all(ok for _, ok in cases) else 1


if __name__ == "__main__":
    sys.exit(main())
