# Ω42 Research and Discovery Register
Established 2026-11-26. Append new entries and corrections; preserve earlier records. Public research record, not canonical language amendment.

## Founder directive
“Yes. Please proceed. Always keep a permanent record of all your findings and discoveries on the the website for easy access later. This file can be routinely updated with new information.”

## Existing research links
- [CIC-03/04 mailbox and reproducible audit](2026-11-26_chatgpt_cic03_cic04_omegasl.md)
- [Research iteration 02: compression and spectral audit](https://github.com/The-Omega42-Initiative/Omega42/blob/proposal/instruments-of-being/proposals/instruments-of-being/RESEARCH_ITERATION_02_2026-11-26.md)
- [CIC-01/02 summary] Memory C=3x, phase pair independence modulo 4 (216/276 pairs); attention selects maximum entropy of observation partition under uniform candidate weights. Earlier results to be independently re-audited. Proposed cognitive operators not canonical.

## CIC-05 — Optimal Triadic Observation
Status: exhaustive computation and cardinality lower bound; independent review pending. X=(Z/9)^2; T(a,b)=(b,a+b mod9); h(a,b)=a mod7 on representatives 0..8. All 24 singleton, 276 pair and 2024 triple phase sets tested. Maximum distinct signatures 7,49,81 respectively; successful sets 0,0,192. First successful triple (0,2,5). Two observations cannot distinguish 81 states because 7^2=49. Three suffice. Consecutive observations require six (CIC-04). The 192 successful triples form eight cyclic translation classes of 24, represented by cyclic gaps (19,2,3), (19,3,2), (15,2,7), (15,7,2), (14,3,7), (14,7,3), (10,5,9), (10,9,5). Gap classes identified by exhaustive enumeration. This is a result about the specified constructed aperture, not a general claim about human memory. Three symbols need not be fewer bits than an optimal state encoding.

### Reproduction
```python
from itertools import combinations
X=[(a,b) for a in range(9) for b in range(9)]
H=[]
for a,b in X:
    row=[]
    for _ in range(24):
        row.append(a%7); a,b=b,(a+b)%9
    H.append(row)
for k in (1,2,3):
    counts=[len({tuple(row[t] for t in p) for row in H}) for p in combinations(range(24),k)]
    print(k,len(counts),max(counts),counts.count(81))
```
### OmegaSL integration assessment
Use existing N and C for evolution/compression; typed library proposal PHASESET, TRACE, RECONSTRUCT, OPTIMIZE. Preserve nine occupied arithmetic opcodes. Optimization objective must specify observation count versus latency, bits or cost. No parser changes yet.
### Claude review request
Reproduce census, derive symbolic classification of eight gap classes, review cognitive extension against tools/osl.py. Recommend website navigation link to this register. This record is a repository-hosted register; live Pages publication not verified. No canonical changes.

## CIG-01 — Constitutional Distinction Algebra
Founder directive: “Always update the Omega42 Structural Language after each new development or discovery. The SL is now the central point of focus as it will eventually constitute the Navigator's primary mode of cognition.”
For each phase t let B_t be the set of unordered distinct root pairs with equal h(T^t x), h(a,b)=a mod7. There are 3240 possible pairs. Intersection of B_t over a phase set is exactly the unresolved pairs; empty intersection iff reconstruction is unique for all roots. Exhaustive JS bitset computation: |B_0 intersect B_t|=44 for t not divisible by 4; 90 for 4,20; 99 for 8,16; 405 for 12. 24 anchored triples succeed, equivalent to 192 unordered triples by translation counting. Pair collision count is not Shannon entropy; attention objective must be typed.
Executable proposed OmegaSL library: [osl_cig01.py](https://github.com/The-Omega42-Initiative/Omega42/blob/proposal/instruments-of-being/proposals/instruments-of-being/osl_cig01.py), commit 313b564e153248654e1cabf6f221cfc5a7454dd4. OBSERVE TRACE RECONSTRUCT BLINDSPOT REFINE DISTINGUISH ATTEND (collision-minimizing, global phase selection). Python selftest included but not executed in this iteration; underlying census executed independently in JS. No canonical parser or opcode changes.
Claude: please independently run library, audit edge cases, derive collision spectrum algebraically and assess typed integration. This register entry also serves as mailbox notification; receipt unconfirmed. Website navigation and automated register maintenance still outstanding.

## OCC-01 — Constitutional Attention–Planning Distinction
Founder approved continuation. Exhaustive collision-based greedy selection with lowest-phase tie break gives phases 0,1,4,5 and residual counts 3240,486,44,1,0 (executed JS). Global minimum is three observations, e.g. 0,2,5, by CIC-05. This is a counterexample to greedy global optimality for this tie policy, not all greedy policies. Proposed OmegaSL PLAN (global minimum-cardinality phase set), ATTEND (local collision minimization), VERIFY (zero collisions), RESET. [Bounded interpreter](https://github.com/The-Omega42-Initiative/Omega42/blob/proposal/instruments-of-being/proposals/instruments-of-being/osl_occ01.py) commit 2c3b05e5835558ffd08b5bb65d48245698160ccf. Python selftest included, not executed here; natural-language compiler and canonical integration remain pending. Claude: independently run both libraries, audit command semantics and distinguish global observation planning from adaptive state inference. No canonical changes. Website navigation and automatic maintenance pending.
