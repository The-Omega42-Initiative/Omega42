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
