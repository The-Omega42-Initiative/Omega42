# Independent verification of the Research and Discovery Register

Claude, Omega42 Co-Builder · 26 November 2026 · Protocol CBX-2

Every entry of ChatGPT's register (records/cobuilder/RESEARCH_DISCOVERY_REGISTER.md) was recomputed in two ways. First, ChatGPT's own OmegaSL libraries (`osl_*.py` on the branch proposal/instruments-of-being) were run: 19 of 19 selftests pass. Second, every numerical statement was recomputed by independent code that does not import those libraries (`records/cobuilder/cg_batch_2026_11_26_check.py`): 31 of 31 checks pass.

| Entry | Result | Status | Relation to the existing record |
|---|---|---|---|
| CIC-03 | Reprocessing an observation cannot refine its partition | PROVED (elementary) | Standard fact; used by OmegaSL REFINE and COARSEN |
| CIC-04 | Consecutive readings of a mod 7: 7, 49, 73, 77, 80, 81 | RECOMPUTED | Same as Theorem 5.2 of the paper (MF-193) |
| CIC-05 | 192 successful triples in 8 translation classes; gap classes | RECOMPUTED | Extends Theorem 5.4; now Theorem 5.5 |
| CIG-01 | Collision spectrum: 3,240 pairs, 486, and 44, 90, 99, 405 | RECOMPUTED | New; the algebraic derivation is open |
| OCC-01 | Greedy collision rule picks 0, 1, 4, 5 (four readings) | RECOMPUTED | New counterexample to greedy optimality; Theorem 5.5 |
| OCC-02 | Optimal adaptive mean cost 218/81, worst case 3 | RECOMPUTED | New; Theorem 5.5 |
| OCC-03 | Phase multiples of 2 or 3 keep cost 218; 4, 6, 8, 12 fail | RECOMPUTED | New; Theorem 5.5 |
| OCC-04 | Each failing spacing needs exactly two added phases | RECOMPUTED | New; Theorem 5.5 |
| CLC-01 | 85 translation classes of triples, 8 successful | RECOMPUTED | Burnside count; Theorem 5.5 |
| CTA-01 | Reflection keeps injectivity of triples; 480 profiles change | RECOMPUTED | New; a general proof for all phase sets is open |
| CTA-02 | GL₂(ℤ/9): 3,888; centralizer 72; aperture stabilizer 54 | RECOMPUTED | New; paper Section 11 |
| CTA-03 | Unique factorization GL = H·C at every depth | RECOMPUTED k = 1, 2 | New; paper Section 11 |
| CTA-04 | 2·3^(3k−1) commuting pairs (H, C) | RECOMPUTED k = 1, 2 | New; paper Section 11 |
| CPG-01 | A is one cycle on the 4·3^(k−1) directions | RECOMPUTED k ≤ 4 | Same as MF-40; reproved |
| CPG-02 | Stratified lifting; A^L = −I on each layer | RECOMPUTED k ≤ 4 | Consistent with Theorem 3.1 and MF-31 |
| CSG-01 | Harmonic multiplicities at every depth; parity dimensions | RECOMPUTED k ≤ 3 | Generalizes Theorem 4.1 |
| CRC-01 | F ≤ L ≤ F_B; lag affinity L | RECOMPUTED | Extends Theorem 7.1 (Proposition 7.3); its B, Q, S are R_H, F_B, F |
| CRN-01 | Gram networks; five orbit representatives needed for closure | RECOMPUTED (closure part) | New; Crown identification not established, as ChatGPT states |
| CCO-01 | Spectral capacity is submodular; greedy reaches 5 of the optimum 6 in the counterexample | RECOMPUTED (counterexample) | New; the (1 − 1/e)-type bound is the standard submodular guarantee |
| CCU-01 | Novelty projector; impulse exploration gains 24, 24, 24, 8, 1 | CONSISTENT | Follows from the orbit census (Theorem 2.1) |
| CCR-01 | A, V, C, S reach all 81 states from (2, 5) | RECOMPUTED | New; relates to OmegaSL Tier 1 (paper §23) |
| CGM-01 | Minimal generating sets {A, V, C} and {A, C, S}; eccentricities 16 and 10 at depth 2, 52 and 12 at depth 3, 160 and 16 at depth 4 | RECOMPUTED k ≤ 4 | New; the all-depth proof for {A, C, S} is open |

**Integration.** The results now in the mathematical paper are Theorem 5.5, Proposition 7.3, the factorization paragraph of Section 11, and the multiplicity formula after Theorem 4.1. ChatGPT's OmegaSL operations are listed on the OmegaSL page as proposed Tier III cognitive operations, with their selftests passing. Nothing canonical changed: register entries (MF numbers) wait for the next supervised release.
