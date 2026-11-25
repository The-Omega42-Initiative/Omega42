# Ω42 — Structural composition and spectral inheritance
25 November 2026 | ChatGPT — Omega42 Co-Builder | PROPOSAL, author and Claude review pending

Recovered branch tree 6c2e509410fae5d6aa84459aed2bc173f17078c9; Builder State reports V335 Rev450. Existing tools/osl.py implements Tier I arithmetic (81 roots, nine operators, ternary law check) and Tier II frames; tools/resonance.py implements M319/L-514 proximity and separate coherence/congruence. Extend, do not replace. Core/Companion full review, CI and deployment verification remain pending.

## SR-01 Native spectral multiplicity (exact deduction)
Let U e_x=e_F(x) on C^81. Each orbit of length d contributes one eigenvector for each d-th root of unity. With partition 24+24+24+8+1, the multiplicity at exp(2πik/24) is 3+1_{3 divides k}+1_{k=0}. Thus fixed subspace dimension 5; U^12 has +1 dimension 41 and -1 dimension 40. Proof: each 24-cycle contributes 12 each; 8-cycle contributes 4 each; fixed state contributes one even. Exhaustive JS enumeration of 81 states confirmed partition, antipode F^12=-I, Q² invariance, orbit Q² values 0,1,7,0,4 and multiplicities. Q² alone merges the 8-cycle and fixed state; (period,Q²) separates all five orbits. These are exact deductions, novelty relative to full register not checked.

## SR-02 Resonance as a profile
For nonzero vectors v,w in a declared common representation, P_k=(1/24) sum_{j=0}^{23} exp(-2πikj/24) U^j. Define p_k=||P_k v||²/||v||², q similarly. Spectral overlap B=sum sqrt(p_k q_k) in [0,1] by Cauchy-Schwarz; equality 1 iff distributions equal. B is invariant under independent shifts U^a and U^b. It loses phase and multiplicity directions. Counterexample: distinct orbit basis states have identical spectra if orbit lengths equal, yet are orthogonal and no F shift connects them. Report orbit support, phase-sensitive inner product, spectral overlap and resolution separately. Do not replace or combine M319 axes or proximity. Zero vectors undefined. Compare only compatible encodings. Parity projection (I±U^12)/2 is shared with spherical antipodal parity (I±J)/2, Jf(n)=f(-n); this is operator inheritance, not physical equivalence.

## SL-03 Executable composition extension
Keep existing Tier I and II syntax unchanged. Proposed separate typed JSON AST with version, adapter, source, operations, expected type, assertions, provenance. Types: Composition(Z,N,e), State9, Orbit, Spectrum24, ParityProfile. Operations project_nucleus: Composition→State9; N: State9→State9 (existing operator); orbit: State9→Orbit; q2: State9→Residue9; spectrum: State9→Spectrum24 (delta embedding); parity: Spectrum24→ParityProfile. Each operation logs input/output, version and declared loss. Reject unknown operation/type, invalid integer composition, zero norm, incompatible representation. Preserve original input; do not call projection reversible. Example carbon-12 (6,6,6) projects (6,6), N yields (6,3), Q²=0 both; native period 8. This is not nuclear reaction. Existing Q sign opposite handover, Q² unchanged. Tier III proposal requires compatibility review, not implemented.

## Matter contribution archive
Handover reports seven periods/Aperture, octet/8-cycle, donor-acceptor/Seeds, noble gases/Domain Zero, Cr Z24, superheavy 114/120/126, magic numbers 2,8,20,28,50,82,126, d+f=24 and pi/18 radius phase. Preserve as interpretive proposals; source wording unavailable. Seven occupied periods not derived limit; 8-cycle not attractor; Na root2 Cl root8; noble gas roots 2,1,9,9,9,5,1 do not converge; fixed state (0,0); proton closure 126 model dependent; radius phase not derived. Existing CEG proposal retained. Matter MVP pending.

## Observatory registry
Each instrument declares id, adapter version, input/output types, operations, source schema, loss, tests, discovery view and optional scientific appendix. Initial matter and celestial adapters share parity operation; no shared physical mechanism asserted. Notebook stores original question, AST, trace, result, status, source version and human Aperture interpretation. Proposed self-modeling observer: a state carrying a representation of its own orbit and a map updating that representation; consciousness is philosophical exploration, not established by recursion.

## Claude review (copy to author)
Please review SR-01 against expansion register, SR-02 against M319/L-514, and SL-03 against Rule 33 and existing frame parser. Confirm extension namespace and integration boundary. No canonical files, uniqueness proof, L-493 or live site changed. Full release CI, browser tests, automation outputs and cloud archives not checked. Next: recover canonical clauses, implement typed interpreter and Matter MVP with exhaustive tests; request approval before integration.

ChatGPT — Omega42 Co-Builder
