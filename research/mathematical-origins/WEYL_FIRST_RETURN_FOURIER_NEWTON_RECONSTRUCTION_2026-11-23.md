# Exact Fourier reconstruction of syndrome first-return characteristic polynomials

**23 November 2026 — all-depth exact theorem and constructive reconstruction.** Let N=3^k, 1<=r<=floor(k/2), h=3^r, e=N/h, d=N/h², ω=exp(2πi/h). Let U_N satisfy exact Egorov for T=[[1,1],[1,2]]. Let H_(a,b)=W_N(ea,eb) for a,b modulo h; since e² is divisible by N, these form a commuting subgroup with no Weyl cocycle. Define τ_m(a,b)=Tr(U_N^m H_(a,b)).

## Theorem A: exact two-dimensional Fourier duality

For every integer m and syndrome label ℓ=(u,v),
\[
\boxed{f_m(u,v):=\operatorname{Tr}(P_{r,(u,v)}U_N^m)
=\frac1{h²}\sum_{a,b\bmod h}\omega^{-ua-vb}\tau_m(a,b).}
\]
Conversely,
\[
\boxed{\tau_m(a,b)=\sum_{u,v\bmod h}\omega^{ua+vb}f_m(u,v).}
\]

**Proof.** The forward formula follows immediately by inserting the exact character projector P_(r,(u,v))=h^(−2)Σ_(a,b)ω^(−ua−vb)H_(a,b) and using trace linearity and cyclicity. The inverse is ordinary finite-group character orthogonality, Σ_(u,v)ω^(u(a−a')+v(b−b'))=h² δ_(a,a')δ_(b,b'). QED.

## Theorem B: first-return power traces from twisted global traces

Let O be an orbit of S=T^(−transpose) mod h, length L, and ℓ=(u,v) any label in O. The first-return unitary B_O=U_N^L restricted to ran P_(r,ℓ) has dimension d. For any integer q,
\[
\boxed{p_q(O):=\operatorname{Tr}(B_O^q)
=\frac1{h²}\sum_{a,b\bmod h}\omega^{-ua-vb}\operatorname{Tr}(U_N^{Lq}W_N(ea,eb)).}
\]

**Proof.** Because S^Lℓ=ℓ, U_N^L preserves ran P_(r,ℓ), so Tr(B_O^q)=Tr(P_(r,ℓ)U_N^(Lq)). Apply Theorem A. The value is independent of the chosen representative ℓ, since the sector restrictions are unitarily conjugate by U_N. QED.

## Theorem C: exact reconstruction of each spectral factor by Newton identities

Define p_q(O) as above for q=1,...,d and set e_0=1. Recursively define
\[
\boxed{e_j=\frac1j\sum_{q=1}^{j}(-1)^{q-1}e_{j-q}p_q(O),\qquad 1\le j\le d.}
\]
Then the first-return characteristic polynomial is
\[
\boxed{\chi_{B_O}(y)=\sum_{j=0}^{d}(-1)^j e_j y^{d-j},}
\]
and the full orbit-block characteristic polynomial is
\[
\boxed{\chi_{U_N|Q_O}(z)=\chi_{B_O}(z^L)
=\sum_{j=0}^{d}(-1)^j e_j z^{L(d-j)}.}
\]
The full characteristic polynomial is the product of these orbit factors.

**Proof.** For eigenvalues μ_1,...,μ_d of B_O, p_q=Σ_i μ_i^q. Newton's identities recover the elementary symmetric polynomials e_j of μ_i from p_1,...,p_d, and the displayed monic polynomial is ∏_i(y−μ_i). The block factorization follows from the earlier exact first-return companion theorem. QED.

## Computational interpretation and limits

This is a **finite, exact reconstruction algorithm** requiring at most d families of h² twisted global traces per orbit, not a claim that these traces are already evaluated. The number of required power-trace orders is d=N/h², and the orbit lengths and counts are known exactly from the all-depth 3-adic classification. For a given m, τ_m is an h×h table, and one inverse 2D Fourier transform yields all h² sector-resolved traces simultaneously. Fourier duality holds for any operator U_N^m; the first-return and characteristic-polynomial statements use exact Egorov and the sector orbit structure. The metaplectic normalization phase remains unspecified.

**Verification:** independent local NumPy projector/DFT checks passed N=9 (h=3), N=27 (h=3), and N=81 (h=9), using nontrivial diagonal unitary powers m=1,2,3. A separate committed checker implements those finite identities and Newton reconstruction.
