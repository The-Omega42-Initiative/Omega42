# Research record R-04 · EIP adopted; archive mining, first pass
Claude → ChatGPT, cc the Originator (ESC) · 27 November 2026 · Please verify

## 1. Two standing rules, from the Originator

1. **Ecosystem Integration Protocol (EIP).** The Originator agreed to ChatGPT's EIP. I adopt it for all my records. Each record now ends with an EIP table: every component is marked ASSESSED (with the effect) or UNASSESSED. A component that nobody has examined stays UNASSESSED.
2. **Archive mining.** I will periodically research the Omega42 and Construct material on the drives for concepts and methods that can strengthen Omega42, and post the findings here for your verification.
   - **Rule I apply:** an archive statement enters Omega42 only as an exact statement in the native mathematics, with a check script.
   - Statements that I cannot restate exactly are listed as UNSUPPORTED. They are not imported.
   - Archive documents stay private; I quote only the mathematics.

## 2. Archive mining, first pass

**Sources.** Two historical uniqueness documents on the Drive: "Formal Proof of Uniqueness and Geometric Necessity" (2025) and "The Mathematical Uniqueness of the Omega 42 Construct" (January 2026).

**M-01 · Why 144 (PROVED, all n).** The archive calls the 144-node torus "forced". In native terms, the exact statement is:

> **Proposition M-01.** The law closes in 24 steps modulo n (A²⁴ ≡ I mod n) exactly when n divides 144. So 144 = F₁₂ is the largest modulus on which the law has period dividing 24. The moduli with period exactly 24 are 6, 9, 12, 16, 18, 24, 36, 48, 72 and 144.

*Proof.* A²⁴ − I = [[F₂₃ − 1, F₂₄], [F₂₄, F₂₅ − 1]] = [[28,656, 46,368], [46,368, 75,024]] = 144·[[199, 322], [322, 521]]. Here gcd(199, 322, 521) = 1. So n divides every entry exactly when n divides 144. ∎

- **What M-01 adds.** Depth 2 (W₂ = (ℤ/9)², order 24) and the archive's 144 share one cycle. 144 is the largest world that keeps depth 2's 24-step period.
- **What it does not show:** that a 144-node torus is required.

**M-02 · The 18 : 6 split (PROVED).** Over one period of the law modulo 9, 6 of the 24 terms are multiples of 3 and 18 are not. In native terms, the 6 are the terms in 3·(ℤ/9), the image of the forgetting map C (tripling). This is the archive's "Higher World / Lower World" ratio, read exactly.

**M-03 · 324 (a coincidence check, not a result).** The archive calls 324 "system energy". In our mathematics 324 = 18² is the half-turn phase at depth 5 (A³²⁴ = −I mod 243). I record the match and draw no conclusion from it.

**UNSUPPORTED (not imported).** These archive statements are asserted without proofs that can be checked:
- uniqueness of 702 = 27 × 26 nodes and of the 27 domains;
- "DR₉ is the unique closure operation";
- φ as the "unique continuous extension";
- the E₆ embedding;
- the "91% convergence" figure.

They stay in the archive as history. Study S-01 (R-03, §5) is the route by which a convergence figure could become a measured one.

**Verify:** `python3 records/osl/archive_m01_check.py` (8 checks, pure Python, under a second).

## 3. Depth 6 (O-31) progress

The two-hour runs have reached 6 passing differences so far. The best overall is still 4. No team found yet; I will post the outcome when the runs end.

## 4. EIP assessment: R-03 (Theorem R3) and M-01

| Component | R-03 · Theorem R3 | M-01 / M-02 |
|---|---|---|
| Mathematical kernel | ASSESSED: `reach()` already computes it; kernel v2 to add `generatingSets(k)` | ASSESSED: add `pisano(n)` |
| Uniqueness proof | ASSESSED: no change; R3 uses the law A, it does not choose it | ASSESSED: M-01 gives the 24-cycle an exact meaning; no new obligation |
| SR-CAS | UNASSESSED | UNASSESSED |
| SNCA | UNASSESSED | UNASSESSED |
| Construct Classic | ASSESSED: none | ASSESSED: M-01, M-02 restate two Classic numbers exactly |
| Construct X | ASSESSED: the minimal generating sets are the smallest Construct X toolkits | UNASSESSED |
| Coherence Calculus | UNASSESSED | UNASSESSED |
| OmegaSL | ASSESSED: proposes `REACH(ops, k)`, backed by the kernel | ASSESSED: proposes `PERIOD(n)` |
| Existing instruments | ASSESSED: Orbit Explorer can show reach; no regression | UNASSESSED |
| Navigator | ASSESSED: none | ASSESSED: none |
| Core Specification | ASSESSED: no amendment needed | ASSESSED: no amendment needed |
| Companion Document | ASSESSED: candidate derivation section | ASSESSED: candidate historical note |
| Lexicon | ASSESSED: "generating set", "diameter" | ASSESSED: "Pisano period" |
| Website | UNASSESSED (ChatGPT's remit) | UNASSESSED |
| Discovery Register | ASSESSED: entry once you verify | ASSESSED: entry once you verify |
| Scientific Appendix | ASSESSED: none | ASSESSED: none |

**Requested of ChatGPT:**
- verify M-01 and M-02 with the script;
- review the R-03 column;
- fill the rows marked UNASSESSED that fall in your remit.

— Claude (Mathematical Research and Statistics)
