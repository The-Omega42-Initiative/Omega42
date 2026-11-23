# Current Technical Status — Path B / Claude Review

**Prepared:** 23 November 2026  
**Branch:** `proposal/path-b-release-packaging`  
**Review-packet baseline:** the packet was created after the experimental validation on `4c96b226f8389e05554fc6d6f8cf1bc633ac9151`.  
**D1b prototype source commit tested:** `4c96b226f8389e05554fc6d6f8cf1bc633ac9151`
**Latest D5a fixture source commit tested:** `54e0e338a95d7af68604ff15ef50a1cc22818eee`

## 1. Workflow evidence

The latest tested source commit is `54e0e338a95d7af68604ff15ef50a1cc22818eee`.

| Workflow | Run | Result |
|---|---:|---|
| D2 SR-CAS/SNCA isolation | [45174322899](https://github.com/The-Omega42-Initiative/Omega42/actions/runs/45174322899) | **PASS** |
| D3 certificate static validation | [45174322889](https://github.com/The-Omega42-Initiative/Omega42/actions/runs/45174322889) | **PASS** |
| D4 Introduction validation | [45174322954](https://github.com/The-Omega42-Initiative/Omega42/actions/runs/45174322954) | **PASS** |
| D5a eight-domain fixture validation | [45174322983](https://github.com/The-Omega42-Initiative/Omega42/actions/runs/45174322983) | **PASS — 8/8 baseline; 11/11 negative controls** |
| Path B prototype isolation | [45174322881](https://github.com/The-Omega42-Initiative/Omega42/actions/runs/45174322881) | **PASS** |
| Site check | [45174323046](https://github.com/The-Omega42-Initiative/Omega42/actions/runs/45174323046) | **PASS** |
| Full Omega42 CI | [45174323030](https://github.com/The-Omega42-Initiative/Omega42/actions/runs/45174323030) | **IN PROGRESS** |

The D2-D5a, prototype-isolation and site-check workflows above completed successfully on the same source commit. The full Omega42 CI is still in progress. No full-CI pass or L-493 resolution is claimed. Earlier failed D2 runs are retained in the history and documented below; the latest corrected D2 run passed.
## 2. D2 — SR-CAS/SNCA validation

D2 is split into D2-A (completed assessment checking) and D2-B (automatic assessment generation).

**D2-A canonical baseline:** [run 45159025998](https://github.com/The-Omega42-Initiative/Omega42/actions/runs/45159025998) passed on source commit `aeddcfd669734cc068c845ad4be7861706163c43`:
- 9/9 canonical `srcas_check.py --selftest` cases passed.
- All 58 archived `records/srcas/*.txt` files passed with zero findings.
- The receipt audit copied 466 APE submissions and found 197 qualifying APEs from APE-271 onward; all 197 were named in `records/srcas/`.
- No-report, historical date-boundary, wrong SR-CAS Base Score and wrong SNCA Base Score controls behaved as expected.

**Canonical parser boundary probes:** the harness found three accepted malformed cases: missing numeric comparison-class weight, missing numeric weighted index, and duplicate Base Score field. The tested `MATCH: NO` / `VERDICT: PROCEED` control was rejected. Canonical `tools/srcas_check.py` remains unchanged.

**Strict Path B wrapper:** two expanded attempts exposed harness defects, not canonical record failures. The first [45163557806](https://github.com/The-Omega42-Initiative/Omega42/actions/runs/45163557806) found that the duplicate-SNCA-T2 negative control had a literal backslash-n instead of a real second line, and the D2-B synthetic pair did not supply the per-relation verdict map required by M193/M225. The second [45174263744](https://github.com/The-Omega42-Initiative/Omega42/actions/runs/45174263744) confirmed all 13 strict negative controls passed after correcting the newline, but D2-B still failed on the missing verdict map.

The corrected harness now:
- creates a real duplicate SNCA T2 field for the negative control;
- invokes the runner's `run()` function with an explicit synthetic per-relation MATCH map for the identical-record pair;
- keeps the canonical runner's requirement for per-relation MATCH/PARTIAL/DIFFERENT judgments explicit rather than implying that the tool independently decides them.

**Latest expanded D2 validation:** [run 45174322899](https://github.com/The-Omega42-Initiative/Omega42/actions/runs/45174322899) **PASS**:
- D2-B nine-file NAVIGATION-only package preflight passed.
- All nine missing-dependency controls rejected the incomplete package.
- Dynamic M193/Jargon scanner and adaptor-registry capability probe passed.
- Runner self-test passed.
- Duplicate-record mechanical pair passed with explicit relation verdicts.
- Synthetic active-date L-549 outer frame passed.
- All 13 strict negative controls were rejected.
- All 58 archived SR-CAS/SNCA records passed the canonical format check and the experimental strict guard.
- The 197/197 owed-on-receipt audit passed.

The D2-B pair is a duplicate copy of `seq_0133.txt` and the synthetic driver supplies MATCH for each relation in the declared relation order. It demonstrates mechanical execution when required adjudication input is supplied. It does not demonstrate independent Navigator agreement, prove that MATCH is the correct judgment, or make the runner autonomous in T1.5-S.

The D2-B closure is **NAVIGATION-only**. Other registered input forms require their own dependency closures and tests. No canonical checker was changed.

See the [D2 validation report](D2_SR_CAS_SNCA_VALIDATION_REPORT.md), [harness](../../../tools/path_b_d2_srcas_test.py) and [strict guard](../../../tools/path_b_d2_srcas_guard.py).
## 3. D1b result

The dedicated prototype workflow on `4c96b226...` validates:
- complete navigation and findings skeleton generation;
- guarded navigation and findings generation;
- generation-only operation without M193/M225;
- fail-closed rejection by the guard when `utility.py` is absent;
- fail-closed rejection by the guard when `scripts/canonical_reference.py` is absent;
- negative controls reproducing the original generator's two silent-degradation modes.

**Conclusion:** the experimental D1b guard passes its current isolated tests. The original canonical generator remains fail-open in those two cases. The wrapper has not been merged into canonical code and is not a universal security or correctness guarantee.

See [D1B_GUARD_VALIDATION.md](D1B_GUARD_VALIDATION.md).

## 4. D5a current evidence

The Path B D5a harness now generates eight explicitly synthetic fixtures at runtime from the exact public practice-set domains, using the current date (23 November 2026) and current date-gated format requirements.

On the latest full isolated validation [run 45174322983](https://github.com/The-Omega42-Initiative/Omega42/actions/runs/45174322983):

- all eight fixtures passed A1 anchor, A2 arms, A3 format and A4 layer-one checks;
- the baseline report returned 8/8 coverage and `COMPATIBLE (SCRIPT-CAPABLE)`;
- eleven negative controls returned `NOT YET COMPATIBLE`, including missing/extra domains, wrong arithmetic fields, malformed/empty fixtures, exact-domain mismatch and multiple DOMAIN VERBATIM lines;
- the strict guard rejected a duplicate extra file while raw M314 accepted it.

The new `tools/path_b_d5a_guard.py` adds exact one-file-per-domain and exactly-one-DOMAIN-VERBATIM-line preflight checks, then delegates per-file conformance to canonical M314. It is experimental and does not modify canonical checker behaviour. The duplicate-extra defect remains in raw `tools/conformance.py::report()`.

The harness also tests a minimal temporary package. Its first isolation attempt exposed an active dependency on `records/frameworks/lens_relevance.json`, loaded by `tools/congruence.py::lenses_of()`. That file has been added to the closure; the rerun [45157034105](https://github.com/The-Omega42-Initiative/Omega42/actions/runs/45157034105) passed.

All fixtures are synthetic structural test artefacts. The essay, current-knowledge/reach content and M269/M139–M142/M127 trigger markers are not substantive research or semantic navigation. The result demonstrates mechanical acceptance, not answer quality or the quality of AI reasoning.

See [D5A_EIGHT_DOMAIN_TEST_PLAN.md](D5A_EIGHT_DOMAIN_TEST_PLAN.md), the [D5a validation report](D5A_EIGHT_DOMAIN_VALIDATION_REPORT.md), [the harness](../../../tools/path_b_d5a_fixture_test.py) and [the strict guard](../../../tools/path_b_d5a_guard.py).
## 5. D3 — Static certificate validation

D3 is deliberately separated from D5 procedure execution.

- The isolated static package contains `tools/certify.py` and the 10 archived certificate records.
- The harness uses `--check`, `--list` and direct static `check()` calls only. It deliberately does not invoke `--selftest`, because the canonical self-test calls `verify()` and executes a shell procedure.
- The synthetic procedure field contains a side-effect command; the harness verifies that `--check` does not execute it.
- Source and controls show that canonical `certify.check()` accepts blank and duplicate SUBJECT fields. The experimental strict guard rejects these.
- The strict guard also requires one balanced certificate block, unique fields, a `CERT-####` identifier, a relative non-traversing CWD, a valid digest unless REGISTERED, and a nonempty finding statement.
- Nine strict negative controls cover blank/duplicate fields, malformed ID, traversal, Windows UNC path, invalid digest, duplicate block and unbalanced opening/closing markers.

The latest D3 workflow [45174322889](https://github.com/The-Omega42-Initiative/Omega42/actions/runs/45174322889) passed. Ten archived certificates passed the static check and all nine strict negative controls were rejected. No procedure was executed. No certificate procedure has been executed, no certificate has been re-certified or withdrawn, and no canonical checker has been changed.

See the [D3 validation report](D3_CERTIFICATE_STATIC_VALIDATION_REPORT.md), [harness](../../../tools/path_b_d3_certificate_test.py), [strict guard](../../../tools/path_b_d3_certificate_guard.py) and [D5 execution-boundary audit](D5_CERTIFICATE_EXECUTION_BOUNDARY_AUDIT.md).

## 6. Additional checker questions to test

Source inspection of `tools/conformance.py` shows:
- coverage is represented as a set of exact domain strings;
- a domain is counted only when all required per-file checks pass;
- duplicate valid files do not increase the coverage count, but a ninth duplicate file is accepted when all eight domains are otherwise covered; there is no dedicated duplicate diagnostic in the report;
- the current synthetic D5a controls for malformed and empty files returned controlled non-compatible reports;
- advisory B1/B2/B3 results are printed as advisory and do not form part of the required A1–A4 `ok` calculation;
- the overall execution level is derived from whether every supplied file has a valid executed status and output ID.

The duplicate, malformed, empty, missing-domain, wrong-domain and multiple-domain-line behaviours have been exercised. The strict release-profile wrapper catches the raw M314 duplicate defect without changing canonical code. Minimal-package isolation passed with the declared closure. This profile is limited to the eight English/Latin practice-set domains; it does not establish a cross-lingual adaptor package closure.

## 7. D4 — Introduction validation

The isolated D4 harness copies six declared inputs into a temporary package: `intro_output.py`, the Introduction/legitimacy/philosophy JSON registers, the canonical Opening example, and the Core DOCX. It runs the 13-case canonical self-test, Words Explained, Opening example, IN-OPEN/IN-00 correspondence, legitimacy and philosophical register checks, then renders a current-date Opening and rechecks it.

The checks establish mechanical/textual correspondence under the canonical checker, not the truth or persuasiveness of the underlying philosophical or legitimacy arguments. The harness now round-trips `--first-render` through `--first` to validate the Friendly Notes and Navigator Identity Block template. This is not yet a check of a real first-navigation record from a live session.

The latest D4 workflow [45174322954](https://github.com/The-Omega42-Initiative/Omega42/actions/runs/45174322954) passed. The 13-case self-test, glossary, Opening, Core/register correspondence, current-date render/check and first-navigation close round-trip all passed.

See the [D4 validation report](D4_INTRODUCTION_VALIDATION_REPORT.md), [harness](../../../tools/path_b_d4_introduction_test.py) and [workflow](../../../.github/workflows/path-b-d4-introduction.yml).

## 8. Claude review questions

Claude is asked to independently assess:

1. Is the three-package Path B proposal technically sound, or should the release boundary be decomposed differently?
2. Does the evidence support a distinct D1b generation profile and a separate D1a/full-format-check profile?
3. Is the experimental guard sufficiently fail-closed, or should the underlying generator be refactored into a strict API?
4. Does D5a's current dependency closure genuinely match the ordinary conformance execution path?
5. Should duplicate domains and malformed fixtures be rejected by the canonical checker itself, or handled in a release-profile wrapper?
6. What evidence is required before package-level verification can be said to provide assurance comparable to current L-493?
7. What should be considered normative, runtime, test fixture, research corpus, release engineering, website or application material?

Please separate formal technical findings, implementation recommendations, governance questions and legal questions. Preserve disagreements rather than forcing consensus.

## 9. Authority and status

- Path B is still a proposal.
- L-493 is unchanged and remains authoritative.
- Canonical Core and Companion documents are unchanged.
- No canonical checker, extractor or release CI rule has been modified.
- No PR has been opened for Path B.
- No merge or deployment has occurred.
- This review packet is not a message or notification to Claude.
- The Originator must approve any communication to Claude and be copied.
