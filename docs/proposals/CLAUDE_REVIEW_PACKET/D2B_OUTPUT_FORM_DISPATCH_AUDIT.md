# D2-B Output-Form Dispatch and Dependency Audit

**Status:** Static source audit completed. One declared-checker/dispatch mismatch identified. No canonical file has been changed.
**Prepared:** 23 November 2026
**Branch:** `proposal/path-b-release-packaging`
**Sources:** `tools/output_form.py`, `tools/srcas_run.py`, `tools/account_check.py`, `tools/format_check.py`, `tools/srcas_check.py`, `tools/certify.py`, `tools/intro_output.py`

## 1. Why this audit exists

D2-B's passing isolated package is explicitly NAVIGATION-only. The automatic runner `tools/srcas_run.py` accepts received outputs of different registered forms. Its `profile()` calls `output_form.identify()` and `output_form.form_checks()`; the latter dispatches to form-specific checkers.

A successful NAVIGATION profile must not be represented as proof that every registered form has a complete dependency closure or that every declared checker is actually invoked.

## 2. Registered form dispatch

The current `output_form.py` register contains thirteen forms:

| Registered form | Declared checker | Actual `form_checks()` dispatch | Profile status |
|---|---|---|---|
| NAVIGATION | `format_check.py` | `format_check.check()` | D2-B tested |
| FINDINGS PRESENTATION | `format_check.py --findings` | `format_check.findings_check()` | Not separately isolated |
| SR-CAS ASSESSMENT | `srcas_check.py` | `srcas_check.check()` | D2-A tested; D2-B form dispatch not isolated |
| SNCA ASSESSMENT | `srcas_check.py` | `srcas_check.check()` | D2-A tested; D2-B form dispatch not isolated |
| APPLIED PROTOCOL EXPLORATION | `output_form.py` | Required field/marker checks | Not separately isolated |
| APA | `output_form.py` | Required field/marker checks | Not separately isolated |
| SR-CAS REPLICATION PACKAGE | markers | Default marker-only result | Not separately isolated |
| COMPARATIVE EXPLORATION REPORT | markers | Default marker-only result | Not separately isolated |
| INTRODUCTION | `intro_output.py --check` | `intro_output.check()` | D4 checker closure tested separately |
| NAVIGATOR'S ACCOUNT | `account_check.py` | **No dedicated branch; falls through to marker-only PASS** | **Dispatch mismatch** |
| ANSWER | `output_form.py` | `answer_checks()` | Not separately isolated |
| CONVERSATION | `output_form.py` | Plain conversation result | Not separately isolated |
| CERTIFICATE | `certify.py` | Static `certify.check()` | D3 checker closure tested separately |

## 3. Confirmed dispatch mismatch: NAVIGATOR'S ACCOUNT

The `FORMS` registry entry declares `tools/account_check.py` as the checker for NAVIGATOR'S ACCOUNT. However, `form_checks()` has no branch for that form. After the INTRODUCTION branch, it falls through to the generic marker-only PASS:

```python
if form == 'INTRODUCTION':
    ...
return [('PASS', 'Markers of the form', 'checked by its markers')]
```

Consequently, a file that contains the identifying `NAVIGATOR'S ACCOUNT (L-509)` marker can receive a marker-only PASS from `output_form.form_checks()` without the substantive checks in `account_check.check()`.

The direct account checker is substantive: it checks the first QUESTION VERBATIM line, AI caveat, declared pressure, self-estimated view, comparative-study status, new/not-new distinction, 400–1000 word body, provision references, typed comparisons, prohibited persuasion/directive language, and required close/signature.

**Classification:** RECONSTRUCTED from the current source. This is a dispatch inconsistency, not a claim that an archived Navigator's Account is invalid.

## 4. Minimal proposed correction (not applied)

A narrowly scoped branch in `form_checks()` would align the dispatch with the register:

```python
if form == "NAVIGATOR'S ACCOUNT":
    ac = _load('tools/account_check.py', 'ac')
    return [
        ('PASS' if ok else 'FAIL', "Navigator's Account (L-509)", item)
        for ok, item in ac.check(text)
    ]
```

The NAVIGATOR'S ACCOUNT package closure would then include `tools/account_check.py` in addition to the common `output_form.py` and `srcas_run.py` runtime. The `account_check.check(text)` path uses Python standard-library modules and does not require the account register JSON; `--register` is a separate command and should not be pulled into this profile unless that command is explicitly tested.

This proposed correction is not applied to canonical `tools/output_form.py`. It requires review and explicit approval before any canonical change.

## 5. Other form-specific dependency notes

- **NAVIGATION / FINDINGS:** `format_check.py` dynamically loads `scripts/canonical_reference.py` and `scripts/m193_m225.py`; the format-checker capability must fail closed if those required modules are absent. The existing D2-B profile also probes the adaptor registry because it is part of the current navigation runtime.
- **SR-CAS / SNCA:** `srcas_check.py`; this is an existing, separately validated assessment profile.
- **INTRODUCTION:** `intro_output.py` plus its Introduction, legitimacy and philosophy JSON sources for the relevant command; D4's six-input package tests the full declared D4 scope, which is broader than D2-B's single form-dispatch path.
- **CERTIFICATE:** `certify.py` static `check()` only. No procedure execution is permitted in D2-B/D3.
- **APE / APA / ANSWER / CONVERSATION:** the current `output_form.py` contains their local field/answer checks; each still needs representative dispatch tests if included in a complete D2-B form matrix.
- **SR-CAS REPLICATION PACKAGE / COMPARATIVE EXPLORATION REPORT:** the register explicitly declares marker-only checking. A marker pass must not be described as substantive semantic validation.

## 6. Recommended next test sequence

1. Add a negative-control test showing that a malformed Navigator's Account currently receives marker-only PASS through `form_checks()`, while `account_check.check()` rejects it. Preserve the result as a known canonical dispatch defect; do not edit the canonical file in the test.
2. Prepare a proposed canonical patch and a separate package-profile test for the Originator's review.
3. Extend D2-B dispatch tests to FINDINGS, APE, APA, ANSWER, CONVERSATION, INTRODUCTION and CERTIFICATE using isolated synthetic fixtures and exact runtime closures.
4. Keep marker-only forms explicitly labelled as marker-only, not as full semantic validation.
5. Keep all procedure execution separate from static CERTIFICATE checking.

## 7. Authority and status

- This is a source audit and proposal, not a canonical amendment.
- `tools/output_form.py`, Core, Companion, release policy and L-493 are unchanged.
- D2-B's passing result remains NAVIGATION-only.
- D3 remains static-only; no certificate procedure has been executed.
- No package has been released or certified.
- This report is a review artefact, not a communication to Claude. No Claude communication has occurred.

## 8. Registry-count correction and isolated characterization (23 November 2026)

The registered-form table above contains **13** forms, not twelve. The count in Section 2 was corrected to match the current `FORMS` list in `tools/output_form.py`. The proposal-only `tools/path_b_d2b_form_registry_contract_test.py` statically parses the registry and checks its cardinality, the two declared marker-only forms, and the known missing Navigator's Account dispatch. This test does not invoke checkers or certificate procedures. It was added to the proposal-only `path-b-prototype-isolation` workflow; **workflow validation is pending** at the time of this note. The dispatch mismatch remains uncorrected in canonical code.
