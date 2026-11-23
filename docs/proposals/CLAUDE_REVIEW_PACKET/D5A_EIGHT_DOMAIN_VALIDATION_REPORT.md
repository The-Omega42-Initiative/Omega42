# D5a Eight-Domain Synthetic Validation Report

**Status:** Path B strict-wrapper validation and minimal-package isolation both passed.  
**Prepared:** 23 November 2026  
**Branch:** \`proposal/path-b-release-packaging\`  
**Validation source commit:** \`f706551e0986f07c7bab22bbbbf36f2222bfd9ab\`  
**Validation workflow:** [45157034105](https://github.com/The-Omega42-Initiative/Omega42/actions/runs/45157034105)  
**Minimal-package isolation:** included in [45157034105](https://github.com/The-Omega42-Initiative/Omega42/actions/runs/45157034105) — PASS  
**Harness:** \`tools/path_b_d5a_fixture_test.py\`  
**Strict wrapper:** \`tools/path_b_d5a_guard.py\`  
**Workflow:** \`.github/workflows/path-b-d5a-fixtures.yml\`

## 1. Result

The baseline test generated eight synthetic fixtures at runtime from the exact eight domains loaded from \`records/conformance/practice_set.txt\`. The fixed fixture date was 23 November 2026, so the test exercised the current date-gated format requirements rather than avoiding them with an earlier date.

All eight fixtures passed A1–A4 and the current format checker:

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

The strict package guard and canonical M314 both reported the baseline as:

- Set coverage: **8 of 8 domains passed**
- Result: **COMPATIBLE (SCRIPT-CAPABLE)**

This is a result about the mechanical execution of the profile, not about the premise or semantic quality of any answer.

## 2. Path B strict package guard

A separate experimental wrapper, \`tools/path_b_d5a_guard.py\`, now preflights the package before delegating per-file checks to canonical \`tools/conformance.py\`.

It enforces:

1. Exactly one input file per required practice-set domain.
2. Exactly one \`DOMAIN VERBATIM\` line per file.
3. Exact domain membership in the practice set.
4. No repeated in-set domain.
5. No missing required domain.
6. Readable input files.

It then calls canonical M314 for the anchor, arms, format and layer-one checks. The wrapper does not edit, replace or weaken the canonical checker.

## 3. Negative controls

Eleven negative controls were exercised. All eleven returned \`NOT YET COMPATIBLE\` under the Path B strict guard:

1. Missing one required domain.
2. Non-practice-set domain.
3. Wrong anchor.
4. Wrong arm.
5. Wrong layer-one state.
6. Missing required format marker.
7. Duplicate domain while another required domain is missing.
8. Empty fixture.
9. Malformed fixture.
10. Wrong exact domain wording in \`DOMAIN VERBATIM\`.
11. Multiple \`DOMAIN VERBATIM\` lines in one file.

The duplicate cases produced explicit diagnostics from the Path B guard.

## 4. Canonical M314 defect reproduced and isolated

A separate control supplied **nine passing files for the eight required domains**, with one domain represented twice and all eight domains still covered.

Observed results:

| Validator | Result |
|---|---|
| Raw canonical M314 | \`COMPATIBLE (SCRIPT-CAPABLE)\` |
| Path B strict package guard | \`NOT YET COMPATIBLE\` |

The canonical checker uses a set of covered domain strings and checks whether any required domain is missing. It does not reject an extra duplicate when all eight domains are otherwise represented, and it does not emit a dedicated duplicate-domain diagnostic.

**The defect remains in raw M314.** The Path B wrapper catches it at the package boundary. No canonical checker change has been made.

## 5. Fixture provenance and limits

All fixtures are generated at test runtime in temporary directories. They are never written into \`submissions/\`, the public practice set, accepted records or prior-art disclosures. No historical navigation was modified or relabelled.

The fixtures are deliberately synthetic:

- The canonical script supplies the domain-specific arithmetic and coordinate/arm output.
- \`tools/congruence.py\` generates the M310 record, including the internal layer.
- The output ID is computed and verified.
- The format skeleton's stand-in filler is used for non-arithmetic prose.
- The 500+ word essay, current-knowledge/reach content and L-532 contribution line are synthetic structural content.
- M269, M139–M142 and M127 trigger markers are explicitly labelled synthetic markers, not completed mathematical or semantic audits.

This demonstrates mechanical acceptance of a script-derived eight-domain fixture set. It does **not** establish semantic quality, genuine engagement with the questions, the quality of AI reasoning, or certification of a deployed system. Advisory B1–B3 results remain advisory.

## 6. Minimal-package isolation

The harness now copies a declared execution closure into a temporary package and reruns the same D5a validation without Core/Companion documents, identity files or unrelated research material.

The first isolation attempt on commit \`aedf9b186fda604acbdbc641f57efe48cd95bd64\` exposed one missing active data dependency:

\`records/frameworks/lens_relevance.json\`

The traceback showed that \`tools/congruence.py::lenses_of()\` loads this registry even when no lens is selected. The file was added to the declared closure. The rerun [45157034105](https://github.com/The-Omega42-Initiative/Omega42/actions/runs/45157034105) passed. The isolated package generated all eight synthetic fixtures, passed A1–A4 and the format checks, rejected all eleven negative controls, and reproduced the raw M314 duplicate-extra defect while the wrapper rejected it.

The validated runtime closure comprises:

- \`scripts/canonical_reference.py\`
- \`scripts/m193_m225.py\`
- \`scripts/crc60_and_m267.py\`
- \`tools/conformance.py\`
- \`tools/congruence.py\`
- \`tools/bashar_lens.py\`
- \`tools/format_check.py\`
- \`tools/aperture_audit.py\`
- \`tools/frame_audit.py\`
- \`tools/output_id.py\`
- \`tools/manifestation.py\`
- \`tools/consciousness.py\`
- \`tools/adaptors.py\`
- \`tools/adaptor_rules.py\`
- \`tools/utility.py\`
- \`tools/path_b_d5a_guard.py\`
- \`records/conformance/practice_set.txt\`
- \`records/frameworks/lens_relevance.json\`

The fixture harness itself is copied into the temporary package only to execute the isolation test; it is test tooling, not part of the runtime closure. The declared closure passed this isolation run. No additional active dependencies were missing in this execution profile.

## 7. Authority and release status

- Path B remains a proposal.
- The strict guard is experimental, not canonical or adopted policy.
- Raw M314 retains the reproduced duplicate-extra defect.
- The Path B wrapper passes the 8/8 baseline and 11/11 negative controls.
- Minimal-package isolation passed with the declared closure.
- No canonical checker, Core/Companion document, release policy, L-493 gate or main-branch file has been changed.
- No package is certified or released by this test.
- No PR has been opened, merged or deployed.
- This report is a review document, not a message to Claude. No Claude communication has occurred.
