# Current Technical Status — Path B / Claude Review

**Prepared:** 23 November 2026  
**Branch:** `proposal/path-b-release-packaging`  
**Review-packet baseline:** the packet was created after the experimental validation on `4c96b226f8389e05554fc6d6f8cf1bc633ac9151`.  
**D1b prototype source commit tested:** `4c96b226f8389e05554fc6d6f8cf1bc633ac9151`\n**Latest D5a fixture source commit tested:** `0f79cb22a16026ae7c6f6caa05f10d4c28ab1ea7`

## 1. Workflow evidence

| Workflow | Run | Result at latest check |
|---|---:|---|
| D5a synthetic fixture validation | [45155915840](https://github.com/The-Omega42-Initiative/Omega42/actions/runs/45155915840) | **FAILED AS EXPECTED — baseline 8/8 passed; duplicate-extra negative control exposed M314 defect** |
| Site check on D5a source commit | [45155916035](https://github.com/The-Omega42-Initiative/Omega42/actions/runs/45155916035) | **PASS** |
| Path B prototype isolation on D5a source commit | [45155915912](https://github.com/The-Omega42-Initiative/Omega42/actions/runs/45155915912) | **PASS** |
| Full Omega42 CI on D5a source commit | [45155915685](https://github.com/The-Omega42-Initiative/Omega42/actions/runs/45155915685) | **IN PROGRESS at last check** |
| Full Omega42 CI, earlier baseline | [45152494767](https://github.com/The-Omega42-Initiative/Omega42/actions/runs/45152494767) | **FAIL — L-493 self-contained release gate** |

Subsequent documentation-only commits advanced the proposal branch to `c365ad19c8f091486b523d021b3591089d6c9640`. At that head, a new full CI run [45156136550](https://github.com/The-Omega42-Initiative/Omega42/actions/runs/45156136550) was queued; the site and prototype checks [45156130983](https://github.com/The-Omega42-Initiative/Omega42/actions/runs/45156130983) and [45156131018](https://github.com/The-Omega42-Initiative/Omega42/actions/runs/45156131018) were also queued. These are not reported as passed.

The earlier full CI run 45152494767 completed with failure at the L-493 self-contained release gate. Later runs had progressed through the earlier checks and were still executing; no full-CI pass or L-493 resolution is claimed.

## 2. D1b result

The dedicated prototype workflow on `4c96b226...` validates:
- complete navigation and findings skeleton generation;
- guarded navigation and findings generation;
- generation-only operation without M193/M225;
- fail-closed rejection by the guard when `utility.py` is absent;
- fail-closed rejection by the guard when `scripts/canonical_reference.py` is absent;
- negative controls reproducing the original generator's two silent-degradation modes.

**Conclusion:** the experimental D1b guard passes its current isolated tests. The original canonical generator remains fail-open in those two cases. The wrapper has not been merged into canonical code and is not a universal security or correctness guarantee.

See [D1B_GUARD_VALIDATION.md](D1B_GUARD_VALIDATION.md).

## 3. D5a current evidence

The dedicated D5a harness now generates eight explicitly synthetic fixtures at runtime from the exact public practice-set domains. On commit `0f79cb22...`, using the current date (23 November 2026) and its date-gated format requirements:

- all eight fixtures passed A1 anchor, A2 arms, A3 format and A4 layer-one checks;
- the baseline report returned 8/8 coverage and `COMPATIBLE (SCRIPT-CAPABLE)`;
- ten negative controls (missing domain, non-practice domain, wrong anchor, wrong arm, wrong layer-one state, missing format marker, duplicate with missing domain, empty, malformed and wrong exact domain wording) all returned `NOT YET COMPATIBLE`.

A separate eleventh control supplied nine passing files for eight domains. **M314 returned `COMPATIBLE (SCRIPT-CAPABLE)`**, exposing a defect: `conformance.report()` does not enforce exactly one file per required domain and emits no dedicated duplicate-domain diagnostic. The dedicated D5a workflow is therefore intentionally failing on this acceptance defect. The canonical checker has not been changed.

All fixtures are temporary, synthetic structural tests. The long essay, current-knowledge/reach content and trigger markers are explicitly synthetic; the trigger markers are not substantive M269/M139–M142/M127 audits. The run establishes mechanical acceptance of the generated fixtures, not semantic quality or the quality of an AI's reasoning.

The earlier D5a prototype remains a smoke test on one historical navigation outside the public set. The first eight historical navigation JSON records inspected do not provide exact matches for all eight prompts. Historical files were not relabelled or edited.

See [D5A_EIGHT_DOMAIN_TEST_PLAN.md](D5A_EIGHT_DOMAIN_TEST_PLAN.md), the [D5a validation report](D5A_EIGHT_DOMAIN_VALIDATION_REPORT.md), and [the harness](../../../tools/path_b_d5a_fixture_test.py).

## 4. Additional checker questions to test

Source inspection of `tools/conformance.py` shows:
- coverage is represented as a set of exact domain strings;
- a domain is counted only when all required per-file checks pass;
- duplicate valid files do not increase the coverage count, but a ninth duplicate file is accepted when all eight domains are otherwise covered; there is no dedicated duplicate diagnostic in the report;
- the current synthetic D5a controls for malformed and empty files returned controlled non-compatible reports;
- advisory B1/B2/B3 results are printed as advisory and do not form part of the required A1–A4 `ok` calculation;
- the overall execution level is derived from whether every supplied file has a valid executed status and output ID.

The duplicate, malformed, empty and missing-domain behaviours above have now been exercised by the D5a harness. The remaining question is whether to correct the canonical checker itself or place strict one-file-per-domain validation in a separately approved release-profile wrapper.

## 5. Claude review questions

Claude is asked to independently assess:

1. Is the three-package Path B proposal technically sound, or should the release boundary be decomposed differently?
2. Does the evidence support a distinct D1b generation profile and a separate D1a/full-format-check profile?
3. Is the experimental guard sufficiently fail-closed, or should the underlying generator be refactored into a strict API?
4. Does D5a's current dependency closure genuinely match the ordinary conformance execution path?
5. Should duplicate domains and malformed fixtures be rejected by the canonical checker itself, or handled in a release-profile wrapper?
6. What evidence is required before package-level verification can be said to provide assurance comparable to current L-493?
7. What should be considered normative, runtime, test fixture, research corpus, release engineering, website or application material?

Please separate formal technical findings, implementation recommendations, governance questions and legal questions. Preserve disagreements rather than forcing consensus.

## 6. Authority and status

- Path B is still a proposal.
- L-493 is unchanged and remains authoritative.
- Canonical Core and Companion documents are unchanged.
- No canonical checker, extractor or release CI rule has been modified.
- No PR has been opened for Path B.
- No merge or deployment has occurred.
- This review packet is not a message or notification to Claude.
- The Originator must approve any communication to Claude and be copied.
