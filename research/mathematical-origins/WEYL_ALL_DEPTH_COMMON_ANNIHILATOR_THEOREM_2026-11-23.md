# All-depth common annihilator theorem for primitive Weyl norm fibers

**23 November 2026 — exact theorem.** This generalizes the N=9 rank-one common zero vector to every N=3^k with k>=2.

Let R=Z/3^k, N=3^k, d=3^(k−1), and ζ=exp(2πi/N). Set Q(a,b)=a²+ab−b². Use the odd-N Weyl convention

\[
W_{(a,b)}|j\rangle=\zeta^{a(j+b)-2^{-1}ab}|j+b\rangle
\]

with 2^(-1) interpreted modulo N. For every unit s∈R^× that is a square, define the primitive norm-square sum

\[
E_s=\sum_{(a,b)\in R^2:\ Q(a,b)^2=s}W_{(a,b)}.
\]

The condition Q(a,b) unit forces (a,b) primitive.

## Theorem

For every k>=2, the nonzero vector

\[
v_k=|0\rangle+|d\rangle+|2d\rangle,\quad d=3^{k−1}
\]

is annihilated by **every** E_s:

\[
\boxed{E_sv_k=0\qquad(s\in(R^\times)^2).}
\]

The stronger statement also holds for each individual *unit norm* fiber F_q=Σ_(Q(a,b)=q)W_(a,b), q∈R^×, not only its parity-even norm-square combination.

## Proof

Fix an output coordinate r∈R and a unit square label s. In the r-th coefficient of E_sv_k, write input j=vd with v∈F_3, b=r−vd, and decompose a=a_0+ud with a_0 chosen modulo d and u∈F_3. Because d²≡0 mod N for k>=2,

\[
Q(a_0+ud,r−vd)
\equiv Q_0+d\{u(2a_0+r)−v(a_0−2r)\}\pmod N,
\quad Q_0=Q(a_0,r).
\]

If Q_0 is not a unit, the norm-square constraint cannot hold; that a_0 contributes zero. Suppose Q_0 is a unit. Squaring shows that Q(a,b)^2=s imposes a single affine linear equation over F_3 on (u,v), whose homogeneous linear form is proportional to

\[
L(u,v)=(2a_0+r)u−(a_0−2r)v.
\]

The Weyl exponent in the r-th coefficient is

\[
a r−2^{-1}ab
\equiv 2^{-1}a_0r+d\,2^{-1}(ru+a_0v)\pmod N.
\]

Thus, up to a constant ninth-or-higher root of unity, its restriction to the admissible affine line is the additive cubic character associated to

\[
M(u,v)=ru+a_0v.
\]

The determinant of the coefficient rows for L and M is

\[
(2a_0+r)a_0+(a_0−2r)r
=2(a_0^2+a_0r−r^2)
=2Q_0\not\equiv0\pmod3.
\]

Hence L and M are independent over F_3. Along the three points of the affine line L=constant, M takes each value 0,1,2 exactly once. Their Weyl phase sum is therefore a constant times

\[
1+\exp(2\pi i/3)+\exp(4\pi i/3)=0.
\]

Summing over a_0 mod d proves the r-th coefficient vanishes. Since r and s were arbitrary, E_sv_k=0.

For the stronger fixed-unit-norm fiber F_q, replace Q(a,b)^2=s by Q(a,b)=q. The constraint has the same homogeneous form L, and the same independent phase form M, so the identical cancellation applies. QED.

## Consequences

1. The full primitive A² Weyl orbit-sum sector (indexed by unit norm q) has a nonzero common annihilator at every k>=2; so does its parity-even subspace.
2. The generated unital algebra B_(3^k) has a joint zero-signature eigenspace of dimension **at least one** for all k>=2.
3. At k=2, previous exact spectral calculations show this eigenspace is exactly one-dimensional. At k=3, an independent numerical stacked-matrix singular-value calculation suggests dimension three; this is **not** an exact theorem.
4. This does not imply that the common zero eigenspace remains rank one, that its projector has rank one, or any all-depth formula for dim B_(3^k).

## Verification

Companion exact integer/cyclotomic-count script checks the theorem for k=2,3,4 without floating-point complex arithmetic. The proof above covers all k>=2 and does not depend on finite checks.

No physical, semantic, consciousness, or quantum-channel interpretation is asserted.
