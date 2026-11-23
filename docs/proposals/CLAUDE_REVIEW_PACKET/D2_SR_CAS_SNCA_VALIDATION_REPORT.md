# D2 — SR-CAS / SNCA Package Validation and Audit

**Status:** Canonical checker profile passed; strict Path B guard validation is pending.  
**Prepared:** 23 November 2026  
**Branch:** \`proposal/path-b-release-packaging\`  
**Canonical baseline source commit:** \`aeddcfd669734cc068c845ad4be7861706163c43\`  
**Canonical baseline workflow:** [45159025998](https://github.com/The-Omega42-Initiative/Omega42/actions/runs/45159025998)  
**Current strict-wrapper workflow:** [45159548882](https://github.com/The-Omega42-Initiative/Omega42/actions/runs/45159548882) — queued at last check  
**Harness:** \`tools/path_b_d2_srcas_test.py\`  
**Experimental guard:** \`tools/path_b_d2_srcas_guard.py\`

## 1. D2 is two distinct technical functions

### D2-A — Completed assessment validation

\`tools/srcas_check.py\` validates existing SR-CAS and SNCA report blocks. It is standard-library-only and reads report files without modifying them.

The canonical checker enforces:
- report markers and required fields in order;
- pre-SR-CAS verbatim verification and the M270 gate;
- SR-CAS component values and Base Score recomputation;
- weighted index when the parser successfully extracts both the weight and index;
- SNCA Base Score recomputation;
- two-axis status vocabulary;
- the historical enforcement boundary (reports before 31 October 2026 are reported but not failed).

### D2-B — Automatic assessment generation

\`tools/srcas_run.py\` computes the decidable portions of SNCA and SR-CAS. It is not the same as the checker.

Its direct dynamic imports are:
- \`scripts/canonical_reference.py\` (domain coordinates and hashes);
- \`tools/output_form.py\` (form identification and form-specific checks);
- \`scripts/m193_m225.py\` (jargon scan, synthesis echo and M225 relation comparison).

The output-form registry dynamically loads different checkers according to the incoming form. A navigation invokes \`tools/format_check.py\`, which in turn loads the canonical reference and M193/M225 scanner. Other forms can invoke certificate, Introduction or other checkers. Therefore the full D2-B closure depends on the declared input-form profile; it cannot be inferred from the three direct imports alone.

**No claim is made that the full automatic generation runner has been isolated or validated by D2-A.** The D2-A package must not be described as the complete SR-CAS/SNCA runtime.

## 2. Canonical D2-A baseline result

Workflow [45159025998](https://github.com/The-Omega42-Initiative/Omega42/actions/runs/45159025998) completed successfully on source commit \`aeddcfd669734cc068c845ad4be7861706163c43\`.

The isolated package contained:
- one checker: \`tools/srcas_check.py\`;
- 58 archived report files from \`records/srcas/*.txt\`;
- 466 APE source submissions from \`submissions/ape/APE-*.md\`.

Observed results:
- canonical self-test: **9/9 PASS**;
- all 58 archived SR-CAS/SNCA record files: **PASS**, zero files with findings;
- receipt audit from APE-271 onward: **197 relevant submissions, 197 named in \`records/srcas/\`**;
- a current undated file with no report: rejected;
- pre-31 October 2026 historical boundary: passed;
- wrong SR-CAS Base Score: rejected;
- wrong SNCA Base Score: rejected;
- overall D2-A baseline harness: **PASS**.

This is checker and record-corpus evidence. It is not evidence that all 197 assessments are substantively correct, that the generated interpretations are sound, or that the automatic runner is fully packaged.

## 3. Canonical parser boundary probes

The later harness probes four cases that are not covered by the original nine self-tests:

1. \`MATCH: NO\` paired with \`VERDICT: PROCEED\`;
2. a missing numeric comparison-class weight;
3. a missing numeric weighted index;
4. a duplicate Base Score field.

Source inspection indicates that the canonical parser may accept these cases because:
- it searches for the word \`MATCH\` rather than requiring the value \`YES\` for PROCEED;
- weighted-index recomputation is skipped when the multiplier or parsed index is absent;
- ordered-field presence does not itself enforce uniqueness.

These are **source-derived suspected weaknesses**, not yet presented as executed results. The updated harness tests them against canonical \`srcas_check.check()\` and the experimental Path B wrapper. The latest strict-wrapper run was queued at last check.

## 4. Experimental Path B D2 guard

\`tools/path_b_d2_srcas_guard.py\` is a non-canonical wrapper. It calls the unchanged canonical checker and adds checks for:
- consistency between the verbatim MATCH value and PROCEED/HALT verdict;
- exactly one Base Score, comparison-class weight and weighted-index line per SR-CAS report;
- numeric comparison-class weight and weighted index;
- recomputation of the weighted index;
- exactly one Base Score and two-axis status line per SNCA report.

It respects the existing historical date exemption. It does not edit or replace \`tools/srcas_check.py\`.

The strict wrapper is intentionally conservative. It must pass the complete archived corpus before it can be considered a usable Path B profile. If it rejects existing reports, those cases must be examined rather than waived automatically.

## 5. Package closure

### D2-A completed assessment checker

Validated isolated closure:
- \`tools/srcas_check.py\`;
- \`records/srcas/*.txt\` (58 files);
- \`submissions/ape/APE-*.md\` (466 files, required by the \`--owed\` trigger audit).

The checker itself has no third-party Python dependency. The corpus and submission files are data inputs, not imported code.

### D2-B automatic review runner

Provisional direct code closure:
- \`tools/srcas_run.py\`;
- \`scripts/canonical_reference.py\`;
- \`tools/output_form.py\`;
- \`scripts/m193_m225.py\`.

For actual navigation-form inputs, the transitive checker closure also includes at least:
- \`tools/format_check.py\`;
- the canonical reference and M193/M225 scanner it dynamically loads.

Other form types can expand the closure further. A separate input-profile and read-closure audit is required before D2-B can be called isolated.

## 6. Authority and limitations

- Path B remains a proposal.
- The strict D2 guard is experimental, not canonical policy.
- No canonical checker, Core, Companion, release rule or L-493 requirement has been changed.
- The 197/197 receipt audit establishes that each qualifying APE is named in a record; it does not validate semantic completeness or quality.
- The D2-A result does not certify the D2-B generator or any deployed Navigator.
- No package has been released or certified.
- This report is a review artefact, not a communication to Claude. No Claude communication has occurred.
