# Exact rank-one joint zero-signature theorem at N=9

**23 November 2026.** This strengthens the exact joint-multiplicity theorem by identifying the rank-one spectral class explicitly.

Let ζ=exp(2πi/9), Q(a,b)=a²+ab−b² mod9, and use the odd-N Weyl convention W_(a,b)=ζ^(−5ab) Z^a X^b with Z|j>=ζ^j|j>, X|j>=|j+1>. For s∈{1,4,7}, set E_s=Σ_(Q(a,b)²=s) W_(a,b). Define

\[
v=|0\rangle+|3\rangle+|6\rangle,\quad \psi_0=v/\sqrt3,\quad P_0=|\psi_0\rangle\langle\psi_0|.
\]

## Theorem

\[
E_1v=E_4v=E_7v=0.
\]

Furthermore, the common kernel ker(E_1)∩ker(E_4)∩ker(E_7) is exactly Cv, and P_0 is the unique rank-one minimal projection of the generated algebra B_9=C*(I,E_1,E_4,E_7).

## Exact finite proof

The r-th coefficient of E_s v is

\[
\sum_{j\in\{0,3,6\}}\ \sum_{\substack{a\in\mathbb Z/9\\Q(a,r-j)^2=s}}
\zeta^{a r-5a(r-j)}.
\]

For every s∈{1,4,7}, direct integer residue enumeration yields the following **complete coefficient count**, independent of s:

- If r≡0 mod3, the exponent residues e=0,3,6 each occur exactly twice and the other six residues never occur. Thus the coefficient is 2(1+ζ³+ζ⁶)=0.
- If r≠0 mod3, each exponent e=0,...,8 occurs exactly once. Thus the coefficient is Σ_(e=0)^8 ζ^e=0.

This is a finite exact combinatorial certificate of all 27 coefficients (3 generators × 9 output positions); the companion Python script checks the counts with integer arithmetic and no numerical roots.

By the prior exact theorem WEYL_MOD9_EXACT_JOINT_SIGNATURE_MULTIPLICITY_THEOREM_2026-11-23.md, the five joint eigenspaces have ranks (1,2,2,2,2). In particular, the joint zero-signature eigenspace containing v has dimension either 1 or 2. To show it is exactly 1, use the exact characteristic-polynomial result for H=E_1+2E_4+3E_7: its eigenvalue 0 is simple (the factor t occurs with exponent one, and the other factors have nonzero constant terms). Any common zero eigenvector lies in ker H, so ker(E_1)∩ker(E_4)∩ker(E_7)=Cv. The spectral projection onto this common eigenspace is P_0. Since the algebra is commutative and its joint signatures are distinct, P_0 is a minimal projection in B_9, with rank one. QED.

## Explicit projector

P_0 has entries (P_0)_(r,j)=1/3 when both r,j belong to {0,3,6}, and 0 otherwise. It is a rank-one self-adjoint idempotent in B_9, although the bare formula alone would not show membership without the joint spectral theorem.

## Scope

This theorem concerns the concrete N=9 Weyl representation. It does not assert a corresponding rank-one class for every N=3^k or establish any physical/semantic correspondence.
