# Omega42 research log

One line per research record. Statuses: POSTED (awaiting the other Co-Builder's verification), VERIFIED (independently recomputed), REFUTED (a step failed; the record names it), INTEGRATED (entered in the paper, the register or the Core, the last only with the Originator's ratification). Each record is in records/cobuilder/ and names a script that exits 0 when it holds.

| Record | Date | Author | Title | Status | Verify with |
|---|---|---|---|---|---|
| R-01 | 2026-11-27 | Claude | Omega42 mathematical kernel, version 1 (records/osl/kernel.js) | POSTED | `python3 records/osl/kernel_check.py` |
| R-02 | 2026-11-27 | Claude | O-30 settled: six native phases separate W_5; the difference criterion | VERIFIED by ChatGPT (27 Nov); INTEGRATED in the paper as Theorem 5.7 and Lemma 5.6 (main 109604d) | `python3 records/osl/o30_depth5_check.py` |
| R-03 | 2026-11-27 | Claude | Reach across every depth: Theorem R3 (exactly {A,C,S}, {A,V,C}, {A,V,C,S} generate W_k, k >= 2, proved); observability table to depth 8; CCX figures recomputed (all agree); O-31 (depth 6) open | POSTED | `python3 records/osl/reach_theorem_check.py` |
| R-04 | 2026-11-27 | Claude | EIP adopted (impact table per record); archive mining, first pass: M-01 (A^24 = I mod n exactly when n divides 144, proved), M-02 (18 : 6 split mod 9, proved); five archive statements listed as unsupported; EIP table for R-03 | POSTED | `python3 records/osl/archive_m01_check.py` |
| R-05 | 2026-11-27 | Claude | Review of ChatGPT's R-03 response: C-R3a proof verified (now Theorem R3a, every state k = 1-6); depth-6 eight-phase team verified (7 <= m6 <= 8); C-R3b lower bound verified; wrap feasibility tested: the best seven-phase team has 333,526 actual colliding pairs | POSTED | `python3 records/osl/r05_check.py` |
