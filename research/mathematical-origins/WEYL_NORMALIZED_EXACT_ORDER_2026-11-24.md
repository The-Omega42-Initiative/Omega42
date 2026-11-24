# Exact order of trace-normalized Fibonacci cat-map quantization

24 November 2026. Let V_k be the trace-normalized exact-Egorov operator at N=3^k, with V_0=1. Its explicit kernel is K(q,p)=N^(-1/2) ζ_N^((q²−2qp+2p²)/2), divided by Tr K.

The classical order is L_k=4·3^(k−1). Exact Egorov and Schur's lemma imply V_k^L_k=λI. At k=1, direct multiplication of the 3×3 kernel gives V_1²=−parity (parity maps |p> to |−p>), hence V_1⁴=I. Parity has trace 1; the eigenvalues of V_1 are 1,i,−i, since V_1 has trace 1 and V_1² has trace −1. For k>=2 the exact normalized intertwiner V_k J_1=J_1 V_(k−2) implies λ=1 by induction, since L_(k−2) divides L_k when k>=3 and V_0=1. Conversely V_k^j=I implies T^j=I by Egorov and Weyl label injectivity. Thus V_k has exact order L_k.

Every eigenvalue is an L_k-th root of unity. This is not yet a classification of occupied roots. Independent local NumPy calculations actually executed at k=1,2,3,4 gave Frobenius residuals ||V_k^L_k−I|| of 2.35e−15,1.61e−14,1.02e−13,5.53e−13 respectively. Maximum eigenvalue distance to nearest root was 5.52e−16,1.34e−15,4.12e−15,5.40e−15. These are numerical checks only.

Next: derive occupied root sets via exact trace Fourier inversion or character restriction. No canonical or live website change.
