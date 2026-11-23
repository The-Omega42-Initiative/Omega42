# D5a Eight-Domain Synthetic Validation Report

**Status:** Baseline arithmetic/format/coverage test passed; exact-one-file-per-domain acceptance remains blocked by a reproduced M314 defect.  
**Prepared:** 23 November 2026  
**Branch:** \`proposal/path-b-release-packaging\`  
**Test source:** \`tools/path_b_d5a_fixture_test.py\`  
**Workflow:** \`.github/workflows/path-b-d5a-fixtures.yml\`  
**Validation commit:** \`0f79cb22a16026ae7c6f6caa05f10d4c28ab1ea7\`  
**Workflow run:** [45155915840](https://github.com/The-Omega42-Initiative/Omega42/actions/runs/45155915840)

## 1. Result

The baseline test generated eight synthetic fixtures from the exact eight domains loaded at runtime from \`records/conformance/practice_set.txt\`.

All eight passed the current-date format checker and M314 required checks:

| Domain | Recomputed anchor | State | Norm | A1–A4 | Format |
|---|---:|---:|---:|---|---|
| CF-01 | P1 | (1, 4) | 7 | PASS | PASS |
| CF-02 | P2 | (2, 5) | 7 | PASS | PASS |
| CF-03 | P3 | (3, 5) | 8 | PASS | PASS |
| CF-04 | P5 | (5, 3) | 4 | PASS | PASS |
| CF-05 | P3 | (3, 8) | 5 | PASS | PASS |
| CF-06 | P7 | (7, 1) | 1 | PASS | PASS |
| CF-07 | P7 | (7, 1) | 1 | PASS | PASS |
| CF-08 | P4 | (4, 2) | 2 | PASS | PASS |

M314 reported:

- Set coverage: **8 of 8 domains passed**
- Result: **COMPATIBLE (SCRIPT-CAPABLE)**

The test uses the current date (23 November 2026), not an earlier date chosen to evade later date-gated requirements. It supplies the current L-503 status/reach fields, essay-length requirement, M318 framing structure, L-532 line, L-513 instance metadata and L-549 output-form line as synthetic test content.

## 2. Negative controls

Ten negative controls were exercised. All ten returned \`NOT YET COMPATIBLE\`:

1. Missing one required domain.
2. Non-practice-set domain.
3. Wrong anchor.
4. Wrong arm.
5. Wrong layer-one state.
6. Missing required format marker.
7. Duplicate domain while another required domain is missing.
8. Empty fixture.
9. Malformed fixture.
10. Wrong exact domain wording in the \`DOMAIN VERBATIM\` field.

The malformed and empty cases returned a controlled non-compatible report in this run; they did not need a hard-error fallback.

## 3. Reproduced defect: duplicate accepted when coverage is otherwise complete

A separate negative control supplied **nine passing files for the eight required domains**, with one domain represented twice and all eight domains still covered.

Observed result:

\`COMPATIBLE (SCRIPT-CAPABLE)\`

Expected result under the test plan:

\`NOT YET COMPATIBLE\`

The current \`tools/conformance.py::report()\` uses a set to accumulate covered domain strings and checks whether any required domain is missing. It does not reject a repeated in-set domain or enforce that the number of accepted files is exactly the number of required domains. Consequently, a duplicate extra file is accepted if the other seven domains are also present and all files pass their per-file checks.

A second observation: when a duplicate replaces a missing domain, coverage correctly remains incomplete and the overall verdict is non-compatible, but the report does not provide a dedicated duplicate-domain diagnostic.

**This is a real M314 acceptance defect, not a failure of the synthetic fixture generator.**

## 4. Fixture provenance and limits

All eight fixtures are generated at test runtime in a temporary directory. They are never written into \`submissions/\`, the public practice set, accepted records or prior-art disclosures. No historical navigation was modified or relabelled.

The fixtures are deliberately synthetic:

- The canonical script supplies the domain-specific arithmetic and coordinate/arm output.
- \`tools/congruence.py\` generates the M310 record, including the internal layer.
- The output ID is computed and verified.
- The format skeleton's stand-in filler is used for non-arithmetic prose.
- The 500+ word essay and current-knowledge/reach fields are synthetic structural content.
- M269, M139–M142 and M127 trigger markers are explicitly labelled synthetic markers, not completed mathematical or semantic audits.

Therefore this result demonstrates that the current checker can accept a mechanically complete, script-derived eight-domain fixture set. It does **not** establish the semantic quality of any answer, the quality of an AI's reasoning, meaningful engagement with each question, or certification of a deployed system. The advisory B1–B3 results are recorded separately and are not promoted into required checks.

## 5. Proposed correction — not applied

A future, separately authorised canonical checker change should:

1. Track every in-set domain occurrence, not only the set of covered domains.
2. Require exactly one passing navigation per required domain.
3. Reject duplicate in-set domains with an explicit per-file diagnostic.
4. Reject unexpected extra navigation files unless a separately specified mode permits them.
5. Keep the final coverage count and compatibility verdict consistent with those cardinality checks.
6. Add self-tests for both duplicate-with-missing-domain and duplicate-with-complete-coverage.

No change has been made to \`tools/conformance.py\`, canonical documents, release policy, L-493, the main branch or any canonical checker. This report is evidence for review, not approval to amend the protocol.

## 6. Authority and release status

- Path B remains a proposal.
- D5a's eight-domain baseline is reproduced.
- D5a is **not complete** because the exact-one-file-per-domain negative control is not rejected.
- No package is certified or released by this test.
- L-493 remains unchanged and has not been bypassed.
- No PR has been merged and no deployment has been made.
- This report is a review document, not a message to Claude. No Claude communication has occurred.
