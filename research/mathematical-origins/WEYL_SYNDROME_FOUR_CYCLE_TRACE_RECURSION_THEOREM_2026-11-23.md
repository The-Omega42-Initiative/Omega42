# Nine Weyl syndrome sectors, cat-map four-cycles, and exact trace recursion

**23 November 2026. Exact theorem, assuming exact Egorov and the Weyl conventions in the previous all-depth work.**

Let N=3^k, k>=2, d=N/3, ω=exp(2πi/3), and W_N(a,b)=ζ_N^(−2_N^(−1)ab) Z^a X^b. Because d²≡0 mod N, the nine operators W_N(da,db)=Z^(da)X^(db), a,b∈F_3, form an ordinary abelian group H≅F_3².

For each character label ℓ=(u,v)∈F_3² define

\[
\boxed{P_\ell=\frac19\sum_{a,b\in\mathbb F_3}\omega^{-ua-vb}W_N(da,db).}
\]

## Theorem A: full syndrome-sector resolution

The nine P_ℓ are mutually orthogonal self-adjoint projections, satisfy Σ_ℓP_ℓ=I_N, and have identical rank N/9. P_(0,0) is the canonical all-depth annihilator projector from WEYL_ALL_DEPTH_STABILIZER_PROJECTOR_THEOREM_2026-11-23.md.

**Proof.** Character orthogonality in the group algebra C[H] gives P_ℓP_ℓ'=δ_(ℓ,ℓ')P_ℓ, P_ℓ*=P_ℓ, and ΣP_ℓ=I. Weyl trace orthogonality gives Tr P_ℓ=N/9 because only the identity summand has nonzero trace. QED.

## Theorem B: exact Egorov permutation and four-cycle splitting

Let T=A²=[[1,1],[1,2]] with determinant 1, and let U_N obey U_N W_N(x) U_N*=W_N(Tx). Then

\[
\boxed{U_NP_\ell U_N^*=P_{T^{-T}\ell}.}
\]

**Proof.** Egorov reindexes the sum by x'=Tx. The character transforms as ℓ·T^(−1)x'=(T^(−T)ℓ)·x'. QED.

Over F_3, T²=−I and T⁴=I, so T^(−T) has one fixed point (0,0) and two nonzero cycles of length four. Explicitly, for the dual action T^(−T)=[[2,−1],[−1,1]] mod3, the cycles are

\[
(0,0);
\quad(0,1)\to(2,1)\to(0,2)\to(1,2)\to(0,1);
\quad(1,0)\to(2,2)\to(2,0)\to(1,1)\to(1,0).
\]

Let Q_1 and Q_2 denote the sums of P_ℓ over the respective nonzero cycles. Then

\[
I_N=P_{(0,0)}+Q_1+Q_2,\quad
[U_N,Q_i]=0,\quad
\operatorname{rank}P_{(0,0)}=N/9,\quad
\operatorname{rank}Q_i=4N/9.
\]

## Theorem C: four-cycle trace cancellation and full trace recursion

For any integer m not divisible by 4,

\[
\boxed{\operatorname{Tr}(Q_iU_N^m)=0,\quad i=1,2.}
\]

Consequently,

\[
\boxed{\operatorname{Tr}(U_N^m)=\operatorname{Tr}(P_{(0,0)}U_N^m)
=c_k^m\operatorname{Tr}(U_{N/9}^m),\qquad 4\nmid m,}
\]

where U_N J_k=c_k J_k U_(N/9) and |c_k|=1 as in WEYL_TWO_LEVEL_STABILIZER_RECURSION_THEOREM_2026-11-23.md.

**Proof.** U_N^m maps ran P_ℓ onto ran P_(T^(−T))^mℓ. In a four-cycle, when 4∤m this target is orthogonal to ran P_ℓ, so every diagonal sector block P_ℓ U_N^m P_ℓ vanishes. Summing its traces over the four sectors gives Tr(Q_iU_N^m)=0. The fixed sector P_(0,0)=J_kJ_k* is reduced to the lower-level cat-map representation up to phase, giving the last equality. QED.

## Corollary: quartet spectra on the nonzero orbit blocks

On each Q_i block, the spectrum of U_N is invariant under multiplication by i, and the eigenvalues occur in complete quartets λ,iλ,−λ,−iλ (counting multiplicities). Indeed the block cyclicity gives a unitary grading operator G_i with G_i U_N G_i*=i U_N (or its inverse, depending on the grading orientation). The total block dimension 4N/9 is consistent with N/9 quartets. Under MF-185 simple spectrum, all these eigenvalues are distinct within the full cat-map spectrum.

This quartet symmetry is **specific to the two nonzero four-cycle blocks**, not a claim that the entire spectrum is closed under multiplication by i. The fixed block generally breaks that symmetry.

## Generalization to higher syndrome depth

For h=3^r, 0<=r<=floor(k/2), the h² commuting Weyl operators W_N((N/h)a,(N/h)b) admit h² character projectors

\[
P_{r,\ell}=\frac1{h²}\sum_{a,b\bmod h}
e^{-2\pi i(\ell_1a+\ell_2b)/h}W_N((N/h)a,(N/h)b).
\]

Each has rank N/h², and exact Egorov permutes the labels by T^(−T) mod h. Thus the sector decomposition and orbit-based trace selection rules extend to every permitted stabilizer depth. The orbit lengths at h>3 need separate arithmetic analysis; the two four-cycles above are specific to h=3.

## Scope and significance

This resolves the **entire** Hilbert space into nine explicit equal-rank syndrome sectors and proves an exact global trace recursion for 4∤m. It strengthens the earlier fixed-sector recursion, without fixing the metaplectic phase c_k or asserting that all sector projections belong to the primitive Weyl-generated algebra. The results concern finite-dimensional arithmetic representations only.
