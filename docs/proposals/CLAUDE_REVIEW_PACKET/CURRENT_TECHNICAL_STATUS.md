# Current Technical Status — Path B / Claude Review

**Prepared:** 23 November 2026  
**Branch:** `proposal/path-b-release-packaging`  
**Review-packet baseline:** the packet was created after the experimental validation on `4c96b226f8389e05554fc6d6f8cf1bc633ac9151`.  
**Prototype source commit tested:** `4c96b226f8389e05554fc6d6f8cf1bc633ac9151`

## 1. Workflow evidence

| Workflow | Run | Result at preparation |
|---|---:|---|
| Path B prototype isolation | [45152494717](https://github.com/The-Omega42-Initiative/Omega42/actions/runs/45152494717) | **PASS** |
| Site check | [45152494684](https://github.com/The-Omega42-Initiative/Omega42/actions/runs/45152494684) | **PASS** |
| Full Omega42 CI | [45152494767](https://github.com/The-Omega42-Initiative/Omega42/actions/runs/45152494767) | **IN PROGRESS** |

The isolated prototype job passed. The site workflow passed site build and Pyodide-versus-CPython Strike arithmetic comparison.

Full Omega42 CI had completed its early reference implementation, SHA, MATH-GATE, selection witness, M193/M225/M243a, media calibration, CRC-60, output audit, overlap, ACG, inventory, comparative annex and earlier evidence checks successfully. The verify job was still running at the document's preparation. Document hygiene was in progress; later checks, including M286, output ID, L-284, M314 conformance and L-493 self-contained release, remained pending. No full-CI conclusion is claimed here.

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

The earlier D5a prototype:
- recomputed the public practice-set key for all eight domains;
- checked one historical navigation outside that set;
- verified its A1 anchor, A2 arms, A3 format and A4 layer-one checks;
- correctly returned `NOT YET COMPATIBLE` because the one fixture did not cover the eight-domain set.

This was intentionally a smoke test, not a compatibility certification.

The practice-set domains are CF-01 through CF-08. The first eight historical navigation JSON records inspected do not provide exact matches for those eight prompts; several records instead concern purpose of life or general anesthesia. The D5a smoke-test fixture NAV-2026-0021 is also explicitly outside the public set. Historical files must not be relabelled or edited to manufacture coverage.

The next test is defined in [D5A_EIGHT_DOMAIN_TEST_PLAN.md](D5A_EIGHT_DOMAIN_TEST_PLAN.md). It requires exact-domain fixtures, canonical recomputation, per-file assertions, complete coverage, negative controls and fixture provenance.

## 4. Additional checker questions to test

Source inspection of `tools/conformance.py` shows:
- coverage is represented as a set of exact domain strings;
- a domain is counted only when all required per-file checks pass;
- duplicate valid files do not increase the coverage count, but there is no dedicated duplicate diagnostic in the report;
- malformed or empty files may raise exceptions during parsing rather than producing a controlled non-compatible report; this requires direct negative-control testing;
- advisory B1/B2/B3 results are printed as advisory and do not form part of the required A1–A4 `ok` calculation;
- the overall execution level is derived from whether every supplied file has a valid executed status and output ID.

These are source observations, not yet all experimentally verified. The eight-domain test plan explicitly includes duplicate, malformed and missing-domain controls.

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
