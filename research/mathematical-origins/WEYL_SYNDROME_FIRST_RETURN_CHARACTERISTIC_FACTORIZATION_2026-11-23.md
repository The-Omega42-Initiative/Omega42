# Exact syndrome-orbit characteristic-polynomial factorization via first-return maps

**23 November 2026. New all-depth algebraic theorem.** Assumes the exact Weyl/Egorov conventions and orbit classification in WEYL_ALL_DEPTH_SYNDROME_ORBIT_CLASSIFICATION_2026-11-23.md.

Let N=3^k, 1<=r<=floor(k/2), h=3^r, d=N/h², and let O=(ℓ_0,...,ℓ_(L−1)) be an orbit of the dual cat-map action S=T^(−transpose) on (Z/hZ)², ordered so Sℓ_j=ℓ_(j+1 mod L). Let H_j=ran P_(r,ℓ_j), each of dimension d, and Q_O=Σ_j P_(r,ℓ_j). Exact Egorov gives U_N H_j=H_(j+1 mod L).

Define the first-return unitary B_O=(U_N^L)|_(H_0):H_0→H_0.

## Theorem A: exact characteristic polynomial identity

\[
\boxed{\det(zI_(Ld)-U_N|_(\operatorname{ran}Q_O))
=\det(z^L I_d-B_O).}
\]

**Proof.** Choose an orthonormal basis of H_0, and transport it to H_j by U_N^j for 0<=j<L. In the resulting orthonormal basis of ⊕_j H_j, U_N is the block-cyclic companion operator
\[
(x_0,x_1,\ldots,x_(L−1))\mapsto(B_Ox_(L−1),x_0,\ldots,x_(L−2)).
\]
The eigenvector equation for eigenvalue z≠0 gives x_j=z^(−j)x_0 and B_O x_0=z^L x_0. Equivalently, by block determinant elimination,
\[
\det(zI_(Ld)-U_N|Q_O)=\det(z^L I_d-B_O)
\]
for z≠0; both sides are monic polynomials of degree Ld, so the identity holds for every z∈C. Since U_N is unitary, z=0 was not an eigenvalue in any case. QED.

## Corollary B: exact full characteristic-polynomial decomposition

Let O range over all dual syndrome-label orbits modulo 3^r. Then
\[
\boxed{\chi_{U_N}(z)=\prod_O \det(z^{|O|}I_d-B_O).}
\]

For nonzero labels of valuation s (0<=s<r), |O|=4·3^(r−s−1), and there are exactly 2·3^(r−s−1) such orbits. The zero orbit contributes det(zI_d−B_0), where B_0=U_N|_(ran P_(r,0)) is projectively equivalent to the cat map U_(N/h²) by the iterated Weyl recursion:
\[
B_0\cong C_(k,r)U_(N/h²),\qquad |C_(k,r)|=1.
\]
Thus the complete factorization has one inherited lower-modulus factor and, for every t=1,...,r, exactly 2·3^(t−1) factors that are polynomials in z^(4·3^(t−1)), each of degree d in that variable.

## Corollary C: first-return trace formula

For any integer m,
\[
\boxed{\operatorname{Tr}(Q_OU_N^m)=
\begin{cases}
0,&L\nmid m,\\
L\operatorname{Tr}(B_O^{m/L}),&L\mid m.
\end{cases}}
\]

**Proof.** For L∤m the cyclic shift has zero diagonal sector blocks. For m=Lq, U_N^(Lq) preserves every H_j, and its restriction to each H_j is unitarily conjugate to B_O^q via U_N^j. There are L equal trace contributions. QED.

## Corollary D: spectral root-of-unity multiplets

If μ is an eigenvalue of B_O, then every L-th root of μ is an eigenvalue of U_N|Q_O. In particular, if z is such a root and ξ=exp(2πi/L), then z,ξz,...,ξ^(L−1)z form a full spectral multiplet with the same multiplicity as μ. If MF-185's U_N simple-spectrum theorem applies, B_O also has simple spectrum and different μ yield disjoint multiplets.

## Why this matters

The complete spectral problem for each orbit block of dimension Ld reduces to a **d-dimensional first-return unitary**, with an exact polynomial identity rather than only symmetry constraints. The orbit classification fixes all possible exponents L and their factor counts at every depth. The theorem does not determine the matrices B_O, their arithmetic coefficient fields, or the metaplectic phase C_(k,r); nor does it establish common-kernel equality or a physical interpretation.
