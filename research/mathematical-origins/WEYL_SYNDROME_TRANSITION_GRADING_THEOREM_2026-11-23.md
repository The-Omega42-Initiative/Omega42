# Exact Weyl syndrome-sector transition grading and cat-map covariance

**23 November 2026 — exact all-depth theorem.** Builds on the closed-form stabilizer character projectors and higher-depth orbit classification.

Let N=3^k, 1<=r<=floor(k/2), h=3^r, e=N/h, and ζ_N=e^(2πi/N), ω=e^(2πi/h). In the convention
\[
W_N(a,b)|j\rangle=\zeta_N^{a(j+b)-2_N^{-1}ab}|j+b\rangle,
\]
the stabilizer group H_r={W_N(es,et):s,t∈Z/hZ} is abelian. For each ℓ=(u,v)∈(Z/hZ)² define
\[
P_{r,\ell}=h^{-2}\sum_{s,t\bmod h}\omega^{-us-vt}W_N(es,et).
\]

## Theorem A: exact transition selection rule

For x=(a,b)∈(Z/NZ)² define the syndrome displacement
\[
\boxed{\Delta_r(x)=(b,-a)\pmod h.}
\]
Then for every ℓ,
\[
\boxed{W_N(a,b)P_{r,\ell}W_N(a,b)^*
=P_{r,\ell+\Delta_r(x)}.}
\]
Consequently, for any two syndrome labels ℓ,μ,
\[
\boxed{P_{r,\mu}W_N(a,b)P_{r,\ell}=0
\quad\text{unless}\quad\mu-\ell=(b,-a)\pmod h.}
\]
For the unique allowed destination μ=ℓ+Δ_r(x), the block is the nonzero unitary map W_N(a,b):ran P_(r,ℓ)→ran P_(r,μ).

**Proof.** The Weyl commutator is
\[
W_N(a,b)W_N(es,et)W_N(a,b)^*
=\zeta_N^{e(at-bs)}W_N(es,et)
=\omega^{at-bs}W_N(es,et).
\]
Conjugating the character average therefore changes its weight from ω^(−us−vt) to ω^(−(u+b)s−(v−a)t), which is precisely the projector at label (u+b,v−a). Orthogonality of character projectors proves the block selection rule. QED.

## Theorem B: exact grading of arbitrary operators

Write A=Σ_(a,b mod N) α_(a,b)W_N(a,b), with α_(a,b)=N^(−1)Tr(AW_N(a,b)^*). Define
\[
A_\delta=\sum_{\substack{a,b\bmod N\\(b,-a)\equiv\delta\pmod h}}\alpha_{a,b}W_N(a,b),
\qquad\delta\in(\mathbb Z/h\mathbb Z)^2.
\]
Then
\[
\boxed{A=\sum_\delta A_\delta,\quad
P_{r,\mu}A_\delta P_{r,\ell}=0\ \text{unless}\ \mu-\ell=\delta.}
\]
The decomposition is unique, and multiplication obeys
\[
\boxed{A_\delta B_\epsilon\in\mathcal A_{\delta+\epsilon}}
\]
where \mathcal A_\delta is the linear span of Weyl operators of displacement δ. Adjoint obeys \mathcal A_\delta^*=\mathcal A_{-\delta}. Hence M_N(C) has an exact finite-abelian group grading by (Z/hZ)².

**Proof.** Weyl operators are an orthogonal basis of M_N(C), and each has a unique displacement. Their product is a nonzero scalar times W_N(x+y), so displacements add. Taking adjoints negates the label. QED.

## Theorem C: covariance with exact Egorov

Let T∈SL₂(Z) and U_N obey U_NW_N(x)U_N^*=W_N(Tx). The induced character action is S=T^(−transpose) modulo h. Then
\[
\boxed{\Delta_r(Tx)=S\Delta_r(x),\qquad
U_N\mathcal A_\delta U_N^*=\mathcal A_{S\delta}.}
\]
**Proof.** Write J=[[0,1],[-1,0]], so Δ_r(x)=Jx. In dimension two T is symplectic: T^T J T=J, equivalently JT=T^(−T)J. Thus Δ_r(Tx)=JT x=T^(−T)Jx. Exact Egorov maps each Weyl basis element of degree δ to one of degree Sδ. QED.

## Corollary D: trace and block sparsity

For every A_δ with δ≠0, all diagonal syndrome blocks vanish, and therefore
\[
\boxed{\operatorname{Tr}(A_\delta)=0\quad(\delta\ne0).}
\]
More generally, for any word A_(δ1)...A_(δm) with Σδj≠0, its trace vanishes exactly. In particular a product of Weyl operators can contribute to a trace only if its total syndrome displacement is zero.

This is a **necessary** condition for nonzero trace, not sufficient: the total Weyl label must also vanish modulo N for an individual Weyl-product trace to be nonzero.

## Significance and limitations

This upgrades the previously proved fixed-sector compression selection rule to an exact classification of **all inter-sector Weyl transitions**. It endows the full matrix algebra with a finite abelian grading, covariant under the classical cat-map dual action. This may organize explicit first-return operators, but does not itself calculate those operators, determine metaplectic phases, settle common-kernel equality, or imply any physical interpretation.
