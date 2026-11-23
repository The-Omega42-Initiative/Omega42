# Exact twisted cat-map trace selection and first-return Weyl filtering

**23 November 2026 — exact all-depth theorem.** Let N=3^k, 1<=r<=floor(k/2), h=3^r. Let P_(r,ℓ) be the rank-N/h² syndrome projectors, ℓ∈(Z/h)². Let U_N obey exact Egorov for T=[[1,1],[1,2]], with dual sector action S=T^(−transpose). Let W_N(x), x=(a,b), have syndrome displacement Δ_r(x)=(b,−a) mod h.

## Theorem A: sector-resolved twisted trace selection

For every integer m, sector label ℓ, and Weyl label x,

\[
\boxed{\operatorname{Tr}(P_{r,\ell}U_N^mW_N(x))=0
\quad\text{unless}\quad S^m(\ell+\Delta_r(x))=\ell.}
\]

Equivalently, the necessary displacement is uniquely prescribed:
\[
\boxed{\Delta_r(x)=S^{-m}\ell-\ell.}
\]

**Proof.** W_N(x) maps ran P_(r,η) unitarily onto ran P_(r,η+Δ_r(x)), and U_N^m maps ran P_(r,η) onto ran P_(r,S^mη). Therefore U_N^mW_N(x) maps ran P_(r,ℓ) to ran P_(r,S^m(ℓ+Δ_r(x))). Its diagonal ℓ-sector block is zero unless this destination equals ℓ. The trace Tr(P_ℓ U_N^mW_x) is exactly the trace of that diagonal block, since inserting P_ℓ on the right does not change the trace. The map S is invertible, so the condition is equivalent to Δ_r(x)=S^(−m)ℓ−ℓ. QED.

## Theorem B: exact first-return filtering

Let O be the S-orbit of ℓ, of length L. Then S^Lℓ=ℓ, and for every integer q,

\[
\boxed{\operatorname{Tr}(P_{r,\ell}U_N^{qL}W_N(a,b))=0
\quad\text{unless}\quad h\mid a,\ h\mid b.}
\]

In particular, the sector-resolved first-return traces with W_N(a,b) vanish for all nonzero syndrome degrees. The condition is necessary, not sufficient: phases and other cancellations may still force zero.

## Theorem C: exact decomposition of arbitrary twisted traces

For A=Σ_x α_xW_N(x), linearity and Theorem A give

\[
\boxed{
\operatorname{Tr}(P_{r,\ell}U_N^m A)
=\sum_{\substack{x\bmod N\\\Delta_r(x)=S^{-m}\ell-\ell}}
\alpha_x\,\operatorname{Tr}(P_{r,\ell}U_N^mW_N(x)).
}
\]

There are exactly (N/h)² Weyl labels in the allowed residue class. Thus a sector-resolved twisted trace requires only a 1/h² fraction of the full Weyl basis, before any additional arithmetic cancellation.

For an orbit sum Q_O=Σ_(ℓ∈O)P_(r,ℓ), the permitted degrees are the set {S^(−m)ℓ−ℓ:ℓ∈O}. At m=L, that set is {0}, and hence Tr(Q_O U_N^L A) depends only on the syndrome-degree-zero component A_0.

## Scope and significance

This theorem is a rigorous **selection/filtering rule** for sector-resolved twisted traces, derived from the previously proved all-sector Weyl grading and cat-map orbit permutation. It does **not** compute the nonzero first-return traces or determine the metaplectic phase. It also does not assert that every allowed coefficient contributes nontrivially. The first-return characteristic polynomial remains det(z^L I−B_O); this theorem restricts possible Weyl contributions to its trace moments.
