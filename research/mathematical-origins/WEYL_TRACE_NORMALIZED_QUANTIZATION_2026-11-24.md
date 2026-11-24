# Trace-normalized cat-map quantization and exact phase-free recursion

For N=3^k, exact Egorov and the regular-power trace theorem imply |Tr U_N|=1. Define V_N=U_N/Tr U_N, and V_1=1. Schur's lemma makes V_N independent of the original exact-Egorov implementer's phase. It is unitary and Tr V_N=1.

The earlier intertwining U_N J_r=C J_r U_M, M=N/3^(2r), and regular trace descent Tr U_N=C Tr U_M imply exactly V_N J_r=J_r V_M. For every exponent satisfying k>=2r+t(m), Tr V_N^m=Tr V_M^m. No assertion of a normalized representation for the entire symplectic group is made.

## Explicit kernel

With inv2 the inverse of 2 modulo N and ζ=exp(2πi/N), set
K(q,p)=N^(-1/2) ζ^(inv2*(q²−2qp+2p²)).
This is unitary by Fourier orthogonality. Direct substitution verifies K Z K*=W(1,1) and K X K*=W(1,2), hence exact Egorov on all Weyl labels. Therefore V_N=K/Tr K, with Tr K=N^(-1/2) Σ_p ζ^(inv2*p²). This is an explicit phase convention and finite formula, not merely a relative phase. The standard quadratic Gauss sum gives Tr K=1 for even k and −i for odd k (the coefficient inv2 is 2 modulo 3). Alternatively retain the finite sum without using the Gauss sum evaluation.

Local NumPy checks executed at N=3,9,27,81: both generator Egorov identities, normalized unitarity, and two-level intertwining for N>=9 passed. These are numerical cross-checks, not exact symbolic tests. Canonical documents unchanged.
