# Complete normalized cat-map spectrum and characteristic polynomial — 24 November 2026

Conditional on the established MF-185 simple-spectrum theorem, normalized exact order, and all-power trace descent, the following is an exact consequence. Let N=3^k, L_k=4*3^(k-1), V_k trace-normalized, V_0=1. The invariant subspace J_1 carries V_(k-2). Its orthogonal complement A_k has dimension 8N/9. For m not divisible by L_k/3, the uncapped singularity depth t(m) is <=k-2 (or zero), so trace descent at r=1 gives Tr A_k^m=0. Fourier inversion on Z/L_k shows multiplicities of A_k depend only on j mod 3: only Fourier frequencies 0,L_k/3,2L_k/3 survive. Simplicity implies each multiplicity is 0 or 1. Dimension forces exactly two residue classes occupied. The inherited subspace contains eigenvalue 1 by induction from V_0=1 and spec V_1={1,i,-i}; hence simplicity excludes residue class 0 from A_k. Therefore all j not divisible by 3 occur, plus inherited roots. For k>=3 inherited indices are 9*S_(k-2); k=2 inherited index is 0.

chi_0=z-1; chi_1=(z-1)(z^2+1).
For k>=2, chi_k=(z^(8*3^(k-2))+z^(4*3^(k-2))+1)*chi_(k-2).
Exactly 3/4 of the L_k grid is occupied. This is a closed polynomial formula, not a claim of novelty relative to finite Weil representation literature.

Independent NumPy eigenspectrum checks actually executed at N=3,9,27,81,243,729 using the explicit trace-normalized kernel. Distinct rounded root indices counted N at each depth. Maximum root residuals respectively 5.52e-16,1.34e-15,4.12e-15,6.00e-15,1.13e-14,1.84e-14. A separate checker is supplied. No canonical or live site changes.
