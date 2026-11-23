# Path B Minimal Package Prototype — Test Results

**Status:** Experimental package-isolation tests completed  
**Date:** 23 November 2026  
**Source branch:** `proposal/path-b-release-packaging`  
**Tested source commit:** `b8e7b0384aa86b53ca526d4c28d6ddb1196fa55d`  
**Workflow:** [path-b-prototype-isolation run 45151260191](https://github.com/The-Omega42-Initiative/Omega42/actions/runs/45151260191)  
**Harness:** `tools/path_b_prototype_test.py`  
**Normative status:** Non-normative experimental evidence only.

## 1. Result

**Result: PASS — experimental prototype workflow.**

The dedicated isolation workflow passed all four package profiles on the tested source commit. The workflow creates four temporary package roots, copies only the declared source/data closure into each, checks that selected unrelated files are absent, and runs the relevant commands under Python 3.11.

This is not a full Omega42 CI pass, not a release candidate, not an amendment to L-493 and not approval of Path B.

## 2. Profile results

| Profile | Isolation and commands | Result |
|---|---|---|
| C1 — canonical arithmetic | Only `scripts/canonical_reference.py`; unrelated `tools/`, `records/`, `docs/` and identity manifest absent. Ran `--test`, `--calibrate`, `--navigate "What is time?"`; verified source SHA output. | PASS |
| D1a — existing-output format check | Canonical reference, M193/M225 scanner, format checker and one supplied historical navigation. Research registers and canonical DOCX absent. Ran checker self-test and normal existing-output check. | PASS |
| D4 — identity handshake | Handshake script, identity JSON, digest list and the two canonical DOCX files only. Ran fingerprint, live challenge, manifest check and handshake self-test. | PASS |
| D5a — ordinary conformance | Active computational modules, standard library and public practice set; one supplied historical navigation. Core/Companion DOCX and selected research registers, including adaptor registry, absent. Ran `--key` and per-navigation `--check`. | PASS — smoke test |

## 3. Detailed observations

### C1

The arithmetic reference executed its known-answer self-test, calibration and navigation in a temporary root containing no records, canonical DOCX documents, identity manifest or wider tool directory. It printed its source digest. This supports treating C1 as a genuinely small independently executable profile.

### D1a

The format checker passed its built-in self-test and checked the supplied historical navigation in an isolated package containing its canonical reference and M193/M225 scanner. No Core/Companion DOCX or research register was needed.

This test confirms the declared scanner was present in the package. The negative-control package deliberately omitted `scripts/m193_m225.py`; the dynamic import set `_JS = None`, yet `format_check.py --selftest` still exited successfully. This is direct executable evidence of degraded-mode acceptance. A future package claiming full conformance must fail closed or explicitly mark the result as reduced coverage. No canonical checker was modified.

### D4

Fingerprint, deterministic live challenge, manifest check and handshake self-test all passed. The manifest check succeeded with exactly the two canonical DOCX artifacts named by the release digest list. No wider research corpus or navigation tools were needed.

### D5a

The practice-set key recomputed all eight public domains. The per-navigation smoke test used `submissions/navigations/NAV-2026-0021.txt`, an actual historical navigation whose domain is not one of the eight practice-set domains.

The expected command result was therefore **NOT YET COMPATIBLE**: one out-of-set navigation cannot establish full-set coverage. The harness verified that the individual required checks A1 anchor, A2 arms, A3 format and A4 layer 1 passed, and that the report correctly marked the navigation OUTSIDE SET. This distinction is deliberate: a passing per-file check is not a system compatibility verdict.

The isolated D5a package did not contain the Core or Companion DOCX, the adaptor registry, or the selected framework, consciousness, congruence, Bashar and positive-geometry research registers. The tested English navigation did not require those conditional datasets.

## 4. Test harness correction

The first workflow run failed at the harness's string assertion for report spacing, after C1, D1a and D4 had passed. The conformance command itself ran and returned the expected one-file/not-full-set status. The assertion was corrected to parse the report fields using whitespace-tolerant matching. The corrected workflow then passed.

The initial failure was a test-harness formatting defect, not evidence of a source-code failure. It is retained here for transparent test provenance.

## 5. What this evidence supports

1. The C1 arithmetic package can be executed independently of the rest of the repository.
2. The D1a existing-output checker has a compact declared closure for the tested historical navigation.
3. The D4 manifest closure is confirmed operationally against the two exact canonical documents and their digest list.
4. The D5a ordinary conformance command can recompute the practice-set key and perform a per-navigation check without the full research corpus or canonical DOCX files.
5. The package boundary should be expressed as capability-specific profiles, not as one undifferentiated runtime.

## 6. What this evidence does not yet establish

- It does not establish full conformance for every possible navigation, language or adapted script.
- It does not test D1a with the dynamic scanner deliberately missing; the known degraded-mode behaviour remains open.
- It does not test skeleton generation (D1b), specialised SR-CAS/Introduction/certificate profiles, or privileged certificate procedure execution.
- It does not establish a full eight-domain compatibility result for D5a; the fixture used was intentionally outside the practice set.
- It does not prove every transitive file-read closure for every command option.
- It does not reconstruct the entire protocol or prove that the proposed three-package architecture is legally or constitutionally sufficient.
- It does not replace the existing L-493 release test.

## 7. Next work

1. Convert the observed D1a missing-scanner gap into an approved fail-closed design change or a package wrapper that refuses to claim full conformance when a required scanner is absent. The negative control is now in the harness.
2. Build a D5a fixture suite with one valid navigation for each practice-set domain, or an approved synthetic fixture set with independently recomputed outputs.
3. Trace and prototype D1b skeleton generation separately, including `tools/utility.py` and its selected data dependencies.
4. Prototype specialised Introduction, SR-CAS and certificate profiles individually; keep certificate procedure execution isolated and disabled by default.
5. Compare package-level assurance against the unchanged L-493 rule before any proposed canonical amendment.

No canonical documents, `tools/extract_embedded.py`, existing CI rules, release policy, main branch, PR, merge or deployment was changed by this test work.
