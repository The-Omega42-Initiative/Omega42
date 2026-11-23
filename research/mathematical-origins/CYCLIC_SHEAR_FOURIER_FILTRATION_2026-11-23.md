# Exact Fourier filtration of the Fibonacci–shear orbit hierarchy

**Proposal-only arithmetic theorem, 23 November 2026.** Finite cyclic harmonic analysis of previously proved MF-43 and centralizer orbit-rotation results. Not a physical frequency spectrum.

Fix k>=1 and valuation shell j<k; put n=k-j, N=3^(n-1). Choose a primitive Fibonacci-orbit seed (1,0) modulo 3^n. The commuting matrix C=I+3A cyclically indexes all N primitive Fibonacci orbits by t in Z/N, with representative C^t(1,0). For shear depth r>=1, put h=min(r,n), M=3^(h-1), and d=N/M=3^(n-h). The shear-orbit partition is precisely t mod M; equivalently, the shear orbit containing t is the coset t+M(Z/N), with d members.

Use the Hilbert space H_n=C^(Z/N) with normalized inner product <f,g>=N^(-1) sum_t f(t) conjugate(g(t)). Define characters chi_l(t)=exp(2 pi i l t/N), l=0,...,N-1, and Fourier coefficients fhat(l)=N^(-1) sum_t f(t) conjugate(chi_l(t)).

## Theorem 1 — exact Fourier multiplier of shear averaging

The conditional expectation onto functions constant on depth-r shear orbits is

\[
(P_h f)(t)=\frac1d\sum_{a=0}^{d-1}f(t+aM).
\]

It is an orthogonal projection and its exact Fourier action is

\[
\boxed{\widehat{P_h f}(\ell)=
\begin{cases}
\widehat f(\ell),& d\mid\ell,\\
0,&d\nmid\ell.
\end{cases}}
\]

Consequently rank(P_h)=M=3^(h-1), and its range is spanned by chi_(d q), q=0,...,M-1. The cyclic centralizer shift (Tf)(t)=f(t+1) commutes with every P_h, and on chi_(dq) has eigenvalue exp(2 pi i q/M).

**Proof.** For each Fourier character,
P_h chi_l(t)=chi_l(t) d^(-1) sum_(a=0)^(d-1) exp(2 pi i l a/d).
The geometric sum is 1 if d divides l, otherwise 0. Thus P_h is a self-adjoint idempotent with the stated range. Its dimension is the number of allowed frequencies, M. Translation commutes with averaging by translations, and T chi_l=exp(2 pi i l/N) chi_l. QED.

## Theorem 2 — exact ternary spectral bands and energy identity

For 1<=h<n, the projections are nested: P_h P_(h+1)=P_h. Define D_(h+1)=P_(h+1)-P_h. Then D_(h+1) is an orthogonal projection of rank

\[
\boxed{\operatorname{rank}D_{h+1}=2\cdot3^{h-1}.}
\]

It retains exactly those Fourier modes l divisible by 3^(n-h-1) but **not** by 3^(n-h). In particular,

\[
\boxed{f=P_1 f+\sum_{h=1}^{n-1}D_{h+1}f,\qquad
\|f\|_2^2=\|P_1f\|_2^2+\sum_{h=1}^{n-1}\|D_{h+1}f\|_2^2.}
\]

For h=n, P_n is the identity. The coarse-to-fine decomposition is an exact orthogonal multiresolution decomposition on the finite cyclic orbit-index space.

**Proof.** The permitted frequency sets are nested because 3^(n-h) divides 3^(n-h-1) times 3. Their cardinalities are 3^(h-1) and 3^h. The difference has 2·3^(h-1) frequencies. Orthogonality of distinct Fourier characters proves the projector identity, decomposition, and Parseval energy identity. QED.

## Theorem 3 — inverse-limit interpretation

As n increases, the cyclic orbit-index sets Z/3^(n-1) form the standard inverse system of residue rings, with limit Z_3. Their normalized counting measures are compatible and define Haar probability measure on Z_3. For fixed h, P_h becomes conditional expectation onto the sigma-algebra of residues modulo 3^(h-1). The P_h form a martingale filtration of orthogonal projections on L²(Z_3), with P_h f -> f in L² as h -> infinity. Its finite-level spectral bands have dimensions 2·3^(h-1); in the infinite limit the bands consist of characters of exact conductor 3^h (indexed by the Pontryagin dual Q_3/Z_3).

**Proof.** Residue cylinder sets generate the Borel sigma-algebra of Z_3, and locally constant functions are dense in L²(Z_3). P_h fixes every locally constant function depending only on residues modulo 3^(h-1) once h is large enough. Since P_h are norm-one orthogonal projections, density implies strong L² convergence. The character description is the finite theorem applied to cylinder functions. QED.

## Example: n=4

There are N=27 primitive Fibonacci-orbit labels. The ranks of P_1,P_2,P_3,P_4 are 1,3,9,27; the added spectral bands have ranks 2,6,18. The shift C acts on the depth-h quotient through a cyclic representation of order 3^(h-1).

## Interpretation and boundaries

The filtration provides an exact meaning of “coarse shear-depth observables”: only Fourier characters factoring through Z/3^(h-1) survive averaging. The band energies are deterministic L² quantities on orbit-index functions, not physical energies or measured spectra. Results are mathematical consequences of MF-43, the centralizer rotation theorem and standard finite Fourier analysis; no external originality or consciousness claim is made. A companion independent Python checker verifies exact projectors and Fourier multipliers at n<=5 using exact integer and cyclotomic checks (no floating point needed).
