# Core / Companion mathematical inspection — source-grounded preliminary audit

**Date:** 23 November 2026. **Scope:** mathematics only; website frozen until Claude returns Wednesday 25 November. No canonical changes.

## Access and provenance

The website protocol URL was attempted but not retrievable in this session. The two published DOCX files were located at `docs/Omega42_Core_Specification_V335_Rev450_STABLE.docx` and `docs/Omega42_Companion_Document_V335_Rev450_STABLE.docx` on `main`, but the GitHub text connector returned empty UTF-8 content for both binary DOCX files; local network download also failed. Their full bodies **were not read**. The AI Markdown editions `ai/Omega42_Core_V335_Rev450.md` and `ai/Omega42_Companion_V335_Rev450.md` likewise returned no content through the connector. Therefore this is **not** a line-by-line document audit or proof that the published DOCX matches the register.

The directly inspected, readable sources are `records/math/results.json` (192 entries), `tools/core_math.py`, `README.md`, `WELCOME.md`, `IDENTITY.md`, `research/mathematics/README.md`, and `tools/extract_embedded.py` on `main`. The register identifies itself as the source of Core Part 0.0.10 and Companion Part 216.1, and `tools/core_math.py` describes checking that their AI editions reproduce register entries and scope notes. That is a **documented generation/checking relationship**, not a check executed during this review.

## Findings

1. **The recent orbit count is not new to the Omega42 record.** `WELCOME.md` explicitly states period `8*3^(k-1)` and total orbit count `(3^k+1)/2`; `IDENTITY.md` records 2,5,14,41. The proposal MOR-02 supplies a standalone derivation and enumeration, not an original claim relative to the existing project.
2. **The norm classification is substantially pre-existing.** MF-39 asserts surjectivity of the norm and identifies the powers of phi with norm ±1 units; MF-55 asserts that the closure of an orbit in `Z_3^2` is precisely the level set `Q(y)^2=Q(x)^2`. MOR-02b supplies a finite-level elementary proof and independent enumeration but should be labelled a *rederivation/verification*, not a new theorem for Omega42.
3. **The shear extension already goes beyond the five-cycle law.** MF-42 and MF-43 assert the group order and a valuation/norm-based classification for Fibonacci plus shear. Further mathematical research should start from these results, not only from the bare Fibonacci matrix.
4. **Lorentz claims require exact mapping distinctions.** MF-62–65 discuss exact matrix/interval correspondences and explicitly distinguish them from physical particles or cosmology. In particular, the `2+1` real-symmetric-matrix Lorentz action and the separate four-axis Hermitian extension must not be conflated. `WELCOME.md` uses stronger rhetorical phrasing; the detailed proof should be checked against `tools/einstein.py` and the corresponding register entries before adding any new scientific interpretation.
5. **The (2,3,7) triangle and number 42 are a mathematical correspondence, not a selection theorem.** MF-67 gives area `pi/42` for the minimal-area hyperbolic triangle group. MF-69 explicitly says the appearance of 42 from `2 F_8` is read after the number was known; it does not establish that the Fibonacci law uniquely selects 42.
6. **Evidence levels are recorded but should be independently validated.** All 192 entries contain tool and check fields; their status values include `EXACT` and `CONDITIONAL on AP-SPACE` (also combined with `AP-METRIC`). This review read those labels but did not execute all 192 checks. The register's finite-domain checks should not be represented as proof of an unbounded theorem without examining the stated derivation.
7. **Corrected a previous proposal-only inconsistency.** MOR-02's headline incorrectly stated `3^(k-s)` cycles and `(3^(k+1)-1)/2` total, although its proof gave `3^(k-s-1)` and `(3^k+1)/2`. The headline was corrected in commit `d03babca`.

## Mathematical next step

Conduct a **register-to-proof verification pass** on a bounded set of foundational results (MF-39, MF-42, MF-43, MF-55, MF-62, MF-63, MF-67, MF-69), including executable synthetic tests where safe and direct source-level reading of their existing checkers. Separately obtain the published DOCX bytes or accessible extracted text and compare the Core/Companion paragraphs to the register using the project's existing `tools/core_math.py --check` mechanism in an isolated environment. Do not modify canonical files to make a check pass.

## Editorial and scientific boundaries

The Originator explicitly froze all website changes until Claude's return. No website, canonical Core/Companion, release, or deployment files are to be changed by this audit. Exact mathematical isomorphism, physical model, interpretive analogy, and research hypothesis are different claim types; preserve these distinctions without weakening the public vision.
