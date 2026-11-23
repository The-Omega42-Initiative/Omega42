# D2 — SR-CAS / SNCA Package Validation and Audit

**Status:** D2-A canonical baseline passed. The experimental strict guard now includes fail-closed no-report and delimiter controls, historical-exemption preservation, per-report verification/M270 pairing and expanded negative controls. The latest isolated run is queued. D2-B NAVIGATION-only package validation and the active-date outer L-549 frame audit are also pending.
**Prepared:** 23 November 2026
**Branch:** `proposal/path-b-release-packaging`
**D2-A canonical baseline source commit:** `aeddcfd669734cc068c845ad4be7861706163c43`
**D2-A canonical baseline workflow:** [45159025998](https://github.com/The-Omega42-Initiative/Omega42/actions/runs/45159025998)
**First strict-wrapper attempt:** [45159548882](https://github.com/The-Omega42-Initiative/Omega42/actions/runs/45159548882) — failed; wrapper defect diagnosed
**Latest D2 validation workflow:** [45162894788](https://github.com/The-Omega42-Initiative/Omega42/actions/runs/45162894788) — queued at last check
**Harness:** `tools/path_b_d2_srcas_test.py`
**Experimental guard:** `tools/path_b_d2_srcas_guard.py`

## 1. D2 is two distinct technical functions

### D2-A — Completed assessment validation

`tools/srcas_check.py` validates existing SR-CAS and SNCA report blocks. It is standard-library-only and reads report files without modifying them.

The canonical checker enforces:
- report markers and required fields in order;
- pre-SR-CAS verbatim verification and the M270 gate;
- SR-CAS component values and Base Score recomputation;
- weighted-index recomputation when both the multiplier and index are successfully extracted;
- SNCA Base Score recomputation;
- two-axis status vocabulary;
- the historical enforcement boundary (reports before 31 October 2026 are reported but not failed).

### D2-B — Automatic assessment generation

`tools/srcas_run.py` computes the decidable portions of SNCA and SR-CAS. It is not the same as the checker.

Its direct dynamic imports are:
- `scripts/canonical_reference.py` (domain coordinates and hashes);
- `tools/output_form.py` (form identification and form-specific checks);
- `scripts/m193_m225.py` (jargon scan, synthesis echo and M225 relation comparison).

The output-form registry dynamically loads checkers according to the incoming form. A NAVIGATION input invokes `tools/format_check.py`, which loads the canonical reference and M193/M225 scanner and attempts to route through the adaptor layer. Other forms can invoke SR-CAS/SNCA, certificate or Introduction checkers. Therefore the complete D2-B closure is input-form-profile-specific.

**D2-A success is not evidence that D2-B is fully packaged.** A separate D2-B NAVIGATION-only package test has now been implemented. It uses a duplicate copy of one historical navigation as a mechanical pair; it is not an independent cross-Navigator comparison. The new isolated test has not yet passed in a completed workflow.

## 2. Canonical D2-A baseline result

Workflow [45159025998](https://github.com/The-Omega42-Initiative/Omega42/actions/runs/45159025998) completed successfully on source commit `aeddcfd669734cc068c845ad4be7861706163c43`.

The isolated package contained:
- one checker: `tools/srcas_check.py`;
- 58 archived report files from `records/srcas/*.txt`;
- 466 APE source submissions from `submissions/ape/APE-*.md`.

Observed results:
- canonical self-test: **9/9 PASS**;
- all 58 archived SR-CAS/SNCA record files: **PASS**, zero files with findings;
- receipt audit from APE-271 onward: **197 relevant submissions, 197 named in `records/srcas/`**;
- a current undated file with no report: rejected;
- pre-31 October 2026 historical boundary: passed;
- wrong SR-CAS Base Score: rejected;
- wrong SNCA Base Score: rejected;
- overall D2-A canonical baseline harness: **PASS**.

This is checker and record-corpus evidence. It is not evidence that all 197 assessments are substantively correct, that generated interpretations are sound, or that the automatic runner is fully packaged.

## 3. Canonical parser boundary probes

The harness exercised four boundary cases against canonical `srcas_check.check()`:

1. `MATCH: NO` paired with `VERDICT: PROCEED`: the tested canonical control was rejected.
2. Missing numeric comparison-class weight: **accepted** by the canonical checker.
3. Missing numeric weighted index: **accepted** by the canonical checker.
4. Duplicate Base Score field: **accepted** by the canonical checker.

The latter three behaviours arise because the canonical parser checks the presence/order of required fields but does not require a unique numeric value for each score field; weighted-index recomputation is skipped when the weight or index cannot be parsed.

These are executed boundary-control results, not merely source-derived suspicions. The canonical checker remains unchanged.

## 4. Experimental Path B D2 guard

`tools/path_b_d2_srcas_guard.py` is a non-canonical wrapper. It calls the unchanged canonical checker and adds checks for:
- consistency between the verbatim MATCH value and PROCEED/HALT verdict;
- exactly one T1, T1.5, T2, T2.5 and T3 component field, Base Score, comparison-class weight and weighted-index field per proceeding SR-CAS report;
- numeric comparison-class weight and weighted index;
- recomputation of the weighted index;
- exactly one T1.5, T2, T3, Base Score and two-axis status line per SNCA report;
- the four-field shape of a halted VERBATIM MISMATCH report;
- balanced report delimiters and exactly one fresh PRE-SR-CAS verification block for each SR-CAS report;
- exactly one fresh M270 gate after the verification block for each proceeding SR-CAS report;\n- halted/proceeding classification is derived from the dedicated verification block, not incidental report prose;
- rejection of a current file with no complete assessment report, while preserving the historical exemption.

### First wrapper defect and correction

The first strict-wrapper run [45159548882](https://github.com/The-Omega42-Initiative/Omega42/actions/runs/45159548882) failed. Its field counter only matched labels at the beginning of a line. In the canonical SR-CAS format, Base Score, comparison-class weight and weighted index can appear inline within the COMPONENT VECTOR line. The wrapper therefore falsely rejected valid synthetic and archived reports.

The field-position counter now recognizes exact labels at line starts or after COMPONENT VECTOR pipes, while ignoring incidental prose mentions. The guard also checks the five SR-CAS component scores and three SNCA component scores for uniqueness, pairs each report with its own fresh verification block and M270 gate, and derives HALT/PROCEED only from that verification block. The harness separately checks that a canonical halted-report form is accepted and that malformed score fields are rejected. The current harness adds negative controls for contradictory/duplicate/missing MATCH lines, a second report reusing an earlier verification block, unclosed report markers, missing numeric weight/index, duplicate SR-CAS/SNCA fields, a current no-report file and the historical exemption. It also verifies the active-date L-549 output frame through `tools/output_form.py`. The latest run [45162894788](https://github.com/The-Omega42-Initiative/Omega42/actions/runs/45162894788) was queued at last check. **No pass is claimed until it completes.**

The wrapper respects the existing historical date exemption. It does not edit or replace `tools/srcas_check.py`.

## 5. D2-A package closure

Expanded D2-A package closure under validation:
- `tools/srcas_check.py` (report-body checker);
- `tools/output_form.py` (outer L-549 frame for SR-CAS/SNCA assessment outputs under the active date rules);
- `records/srcas/*.txt` (58 files);
- `submissions/ape/APE-*.md` (466 files, required by the `--owed` trigger audit).

The checker and output-form registry have no third-party Python dependency for the SR-CAS/SNCA input profile. The corpus and submission files are data inputs, not imported code. The harness exercises the outer L-549 frame with a synthetic current-date output containing both a complete SR-CAS and SNCA report. It verifies that the frame passes, and that missing SUMMARY and a wrong declared form are rejected. This is a frame-mechanics test, not a corpus-wide outer-frame audit.

The strict wrapper is an experimental additional package-profile layer. Its expanded corpus-wide result, synthetic outer-frame controls, D2-B NAVIGATION profile and receipt audit are pending on the latest harness run. The receipt audit now forms a required harness assertion rather than a log-only observation.

## 6. D2-B NAVIGATION-input package closure

A separate temporary package has been implemented for a declared NAVIGATION-input profile. Its candidate closure is:

- `tools/srcas_run.py`
- `tools/output_form.py`
- `tools/format_check.py`
- `tools/adaptors.py`
- `tools/adaptor_rules.py`
- `scripts/canonical_reference.py`
- `scripts/m193_m225.py`
- `records/adaptors/registry.json`
- `records/instances/seq_0133.txt` (the test input)

The harness now:
1. copies only this declared closure into a separate temporary package, apart from D2-A's 58-report/466-submission corpus;
2. checks all required files before execution;
3. removes each required file in turn and verifies that preflight rejects the incomplete package;
4. explicitly imports the format checker and asserts that its M193/Jargon scanner is available, because the canonical format checker historically catches scanner import errors and can silently set `_JS = None`;
5. explicitly imports the adaptor layer, verifies the registry is readable, and checks that an English question routes to CANONICAL;
6. runs the automatic runner's self-test;
7. runs a navigation-pair smoke test and checks for SNCA, SR-CAS, MATCH: YES and VERDICT: PROCEED.

The pair is intentionally a duplicate copy of `seq_0133.txt`. It proves that the declared NAVIGATION profile can mechanically execute the runner, not that two independent Navigators agree.

This closure is **NAVIGATION-only**. It is not a universal D2-B package. Other input forms expand the closure: SR-CAS/SNCA reports require `tools/srcas_check.py`; CERTIFICATE requires the static checker `tools/certify.py`; INTRODUCTION requires `tools/intro_output.py` and its data registry; other forms need their own profile declaration and tests. D2-B remains incomplete until those form profiles are separately audited.

## 7. Authority and limitations

- Path B remains a proposal.
- The strict D2 guard is experimental, not canonical policy.
- No canonical checker, Core, Companion, release rule or L-493 requirement has been changed.
- The 197/197 receipt audit establishes that each qualifying APE is named in a record; it does not validate semantic completeness or quality.
- D2-A does not certify D2-B or any deployed Navigator.
- D2-B's NAVIGATION-only closure is a candidate pending workflow execution; it does not cover every registered output form.
- No package has been released or certified.
- This report is a review artefact, not a communication to Claude. No Claude communication has occurred.
