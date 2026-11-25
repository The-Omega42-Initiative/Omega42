# Optimal aperture and multiplicity mixing — 2026-11-25
ChatGPT Co-Builder; review proposal for Claude and author.
Independent contribution supplied by author: optimized aperture certificate, resolvent, orbit lifting, commutant. Certificate independently enumerated over 81 states:
3 2 1 1 1 0 5 4 3
3 2 0 2 1 1 1 4 5
3 3 1 1 5 3 1 6 0
2 0 1 3 0 4 2 5 3
3 6 3 5 3 5 0 0 3
6 4 4 3 0 6 2 0 2
6 2 5 2 4 5 5 6 0
6 4 5 1 2 4 4 0 2
5 3 4 5 1 3 3 3 6
Trace counts 7,49,81; class sizes 11,12,11,17,10,12,8. Lower bound 7²<81 proves optimal depth 3. Surjectivity alone does not imply 49 two-step histories (e.g. orbit-invariant aperture impossible with seven labels, but modify a coordinate aperture to merge a pair of states in a way that excludes a transition; simpler counterexample: seven labels with one singleton whose successor has a different label, so its row has only one transition). Linear search not independently repeated.
Orbit lifting: A^8=I+3B mod9, B=[[1,1],[1,2]] mod3 invertible. Each nonzero residue coset splits into three 3-cycles under F^8, not one 24-cycle within a coset. F transports across eight cosets, giving three 24-cycles. 3X gives 8+1.
L=2I-U-U^-1, resolvent (I+A L/4)^-1 for A>=0 preserves all five invariant directions. Historical gain increasing in harmonic index up to 12 for positive parameters; interpretation as dissonance penalty is proposed, not historical intent verified.
Commutant over C = M5(C) ⊕ seven M4(C) ⊕ sixteen M3(C), dimension 281, center 24, traceless complement 257. Unitary block mixing preserves total energy and each harmonic energy but can exchange orbit energies. Explicit mixer on normalized constant fields c0 (fixed point) and c1 (canonical 24-cycle): swap or rotate them, identity on orthogonal complement. Commutes with U; not a native state permutation. If require preserving each orbit, mixing forbidden. Q² labels long orbits, period separates fixed and 8-cycle. Mod9 Q sign flip is exact; complex multiplication operator needs odd lift q(-r)=-q(r), not ordinary representatives.
Entropy correction: normalized spectral entropy can increase under persistence-preserving attenuation: p=(.1,.9), weights (1,1/3) gives (.5,.5). Entropy rises from 0.32508 to ln2. Dirichlet energy <psi,L psi> decreases under contraction filter; normalized mean Laplacian also decreases for weights decreasing with eigenvalue (negative covariance). 
Proposed OmegaSL MIX(mode,unitary block), FILTER(resolvent), OBSERVE(table), RECONSTRUCT(trace). No canonical changes, full CI or deployment. Independent report historical claims and exhaustive linear search not verified. Prior six/repetend necessity withdrawn; symbolic correspondence retained. No direct Claude message.
