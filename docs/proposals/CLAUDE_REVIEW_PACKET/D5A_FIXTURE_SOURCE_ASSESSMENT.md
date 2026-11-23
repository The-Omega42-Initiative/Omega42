# D5a Fixture Source Assessment

**Date:** 23 November 2026  
**Status:** Preliminary source inspection; no fixture set generated yet.

## 1. Candidate historical template inspected

`submissions/navigations/NAV-2026-0021.txt` was used by the earlier D5a smoke test. The smoke test established that its required per-file checks A1–A4 pass, while its domain is outside the eight-domain practice set and the overall verdict correctly remains `NOT YET COMPATIBLE`.

The file contains:
- the required navigation structure;
- the first and answer-header QUESTION VERBATIM lines;
- a DOMAIN VERBATIM line;
- an executed canonical reference status;
- an anchor and four arms;
- an M310 congruence record with the `(1) INTERNAL` line required by the D5a layer-one parser;
- the standard format-completeness block and signature.

It is therefore a candidate **structural template** for disposable synthetic tests, not an eligible CF-01–CF-08 fixture.

## 2. Why the historical file must not be relabelled

The file's domain is a Pythagoreanism/creation question, not one of the public practice-set domains. Its text also records prior readings, exposure and contamination. Changing its domain line or metadata and then presenting it as a historical practice-set navigation would falsify provenance.

Any derivatives must be generated only in the temporary D5a test workspace, carry synthetic fixture filenames, and be listed in a separate fixture manifest as test artefacts. Do not commit them under `submissions/navigations/` or represent them as accepted readings.

## 3. Viable test-generation approach

A synthetic fixture generator may use NAV-2026-0021 as a **format skeleton only**, provided it:
1. reads the eight exact domain strings from `records/conformance/practice_set.txt`;
2. recomputes every A1/A2/A4 field through the D5a package's canonical `expected(domain)` path;
3. replaces both QUESTION VERBATIM lines and the DOMAIN VERBATIM line with the exact domain;
4. sets the reported anchor and all four arms from the recomputed values;
5. replaces the M310 `(1) INTERNAL` state, voice, norm, stratum and half with recomputed values;
6. adds required trigger markers for domains that contain mathematical notation (M269 and M139–M142) or exceed 30 words (M127), and verifies their exact placement/contents against the canonical format contract rather than inserting unexplained marker strings;
7. makes the execution status explicitly TEXT-ONLY unless a valid output ID and executed-script evidence are genuinely regenerated;
8. stores fixture provenance and generator version outside the navigation text.

The source template's answer and extended essay will remain domain-incongruent if only these machine-checked fields are replaced. Such fixtures can test the present conformance checker's arithmetic, structure and coverage logic, but **cannot** be represented as semantically complete navigations or as evidence that an AI generated an appropriate answer to each domain.

## 4. Stronger alternative

Prefer a purpose-built fixture builder that starts from the current canonical skeleton and fills every required field deterministically. The builder should produce a minimal but structurally valid, explicitly synthetic navigation and should not carry the unrelated prose, claims or provenance of NAV-2026-0021.

If the canonical skeleton cannot produce a valid A3 fixture without human-authored sections, split the test into:
- checker-engine tests using synthetic machine-checkable fixtures; and
- end-to-end navigation examples authored and independently reviewed for each domain.

Do not weaken A3 or the canonical conformance checker merely to make synthetic fixtures pass.

## 5. Acceptance language

If synthetic fixtures are used, report the result as:

> The D5a checker accepted an eight-domain synthetic fixture suite at the tested arithmetic and format layers.

Do not report this as a live Navigator's full compatibility or as an Omega42 release certification. Preserve the distinction between protocol execution checks, semantic quality, research validity and release self-containment.
