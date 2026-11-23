# Spectral compatibility and obstruction: shear Fourier filtration versus cat-map commutants

**Mathematics-only proposal, 23 November 2026.** Relates the finite orbit labels of MF-184/MF-185 to the centralizer/shear Fourier filtration without identifying different operators.

Let R_n=Z/3^n, U_n=R_n^× (cyclic of order 2·3^(n−1)), and let Q(a,b)=a²+ab−b². For primitive vectors modulo 3^n, the established MF-184 theorem identifies A²-orbits with exact unit-norm fibers Q=q∈U_n; MF-55 identifies A-orbits with norm-square fibers Q²=s∈U_n². There are 2·3^(n−1) primitive A²-orbits and 3^(n−1) primitive A-orbits.

## Theorem 1 — exact quotient and spectral parity

The quotient of the primitive A²-orbit label space U_n by q~−q is canonically the primitive A-orbit label space U_n², through q↦q². The pullback

\[
J:\mathbb C^{U_n²}\to\mathbb C^{U_n},\qquad (Jf)(q)=f(q²)
\]

is an isometric embedding for normalized counting inner products. Its range is precisely the even subspace F(q)=F(−q). The orthogonal projector onto that subspace is

\[
(EF)(q)=\tfrac12(F(q)+F(−q)).
\]

Choose a generator g of U_n. With characters χ_m(g^t)=exp(2πimt/(2·3^(n−1))), the even subspace consists exactly of **even Fourier indices m**, since −1=g^(3^(n−1)) and χ_m(−q)=(−1)^m χ_m(q).

**Proof.** U_n has odd prime-power principal-unit subgroup and unique order-two element −1. The square map has kernel {±1}, image U_n², and all fibers size two. The normalized inner products agree under the two-to-one pullback. Evenness and the averaging projector follow. The character calculation proves the spectral criterion. QED.

## Theorem 2 — depth-r Fourier filtration inside the even sector

Let h=min(r,n), M=3^(h−1), N=3^(n−1). The depth-r shear-orbit label is q² modulo 3^h. Under the isometry J, the shear-depth averaging operator on C^(U_n²) becomes the orthogonal conditional expectation on C^(U_n) onto functions depending only on q² mod 3^h. It is the composition of E with averaging over the kernel of reduction U_n²→U_h². In the cyclic Fourier basis of U_n, the surviving characters have indices

\[
\boxed{m\equiv0\pmod{2\cdot3^{n-h}}.}
\]

There are exactly M such characters, and the refinement h→h+1 adds 2·3^(h−1) new characters.

**Proof.** Characters of U_n that factor through q² mod 3^h are precisely those trivial on the kernel of U_n→U_h², a subgroup of order 2·3^(n−h). A character χ_m is trivial on that subgroup iff its index is divisible by 2·3^(n−h). Counting yields M characters and the rank increment. QED.

## Theorem 3 — relationship to MF-185 and a non-equivalence warning

MF-185 describes the commutant of a quantum cat map U_(3^k) by Weyl orbit sums indexed by A²-orbits on the phase-space labels R_k², yielding dimension 3^k. Theorem 1 identifies a **natural finite label-space quotient** of the primitive A²-orbit indices by q↦−q, of dimension 3^(k−1), and Theorem 2 equips it with a nested Fourier filtration.

However, **the Weyl orbit-sum basis is not asserted to be orthonormal** and its multiplication, adjoint, and Hilbert–Schmidt normalization need not coincide with pointwise multiplication and normalized counting on orbit labels. Nor does MF-185 by itself provide a canonical identification of the actual cat-map commutant with the shear-filtered label Hilbert space. Such a statement requires an explicit map preserving the intended operator algebra, inner product, and dynamics, and must confront the differing dimensions (3^k for the full commutant versus 3^(k−1) for the primitive even label sector).

Thus the rigorous correspondence established here is **at the level of orbit-label sets and Fourier representations**, not an intertwiner between physical/quantum operators.

## Testable obstruction / future work

Construct normalized Weyl orbit sums for small k, compute their Hilbert–Schmidt Gram matrix and products, and test whether the parity-even primitive orbit-label subspace is stable under multiplication or conjugation. Failure would disprove an algebra-level identification while leaving Theorems 1–2 intact. The pure arithmetic Fourier projector test is provided separately.

No semantic, consciousness, or experimental conclusion follows from these label-space statements.
