# Iterated two-level Weyl recursion and canonical spectral layers

**23 November 2026. Exact theorem conditional on the stated exact-Egorov quantization conventions.**

Let N=3^k, k>=2. For each l>=2, let J_l:C^(3^(l−2))→C^(3^l) be the exact isometry from WEYL_TWO_LEVEL_STABILIZER_RECURSION_THEOREM_2026-11-23.md. Set R=floor(k/2), N_r=3^(k−2r) for r=0,...,R, and define

\[
\mathcal J_0=I_N,\qquad
\mathcal J_r=J_kJ_{k-2}\cdots J_{k-2r+2}\quad(1\le r\le R).
\]

For r=R, N_R=1 if k is even, and N_R=3 if k is odd. Let U_(N_r) be unitary quantizations of the same cat map T=A² satisfying exact Egorov at each level. At modulus 1, U_1 is any scalar unitary and Weyl operators are trivial.

## Theorem A: nested invariant flag

1. Each \mathcal J_r is an isometry C^(N_r)→C^N. Its image V_r is U_N-invariant, and
   \[
   C^N=V_0\supset V_1\supset\cdots\supset V_R,\qquad \dim V_r=N_r.
   \]
2. There exist unit scalars c_l∈U(1) (for each l>=2) such that
   \[
   \boxed{U_N\mathcal J_r=C_{k,r}\mathcal J_r U_{N_r},\quad
   C_{k,r}=\prod_{j=0}^{r-1}c_{k-2j}.}
   \]
3. The orthogonal projectors P_r=\mathcal J_r\mathcal J_r^* are mutually nested and commute with U_N. Thus
   \[
   P_rP_s=P_{\max(r,s)}.
   \]
   The differences D_r=P_r−P_(r+1), 0<=r<R, and D_R=P_R are pairwise orthogonal U_N-invariant projections with
   \[
   \operatorname{rank}D_r=N_r−N_(r+1)=8\cdot3^{k-2r-2}\quad(r<R),
   \qquad \operatorname{rank}D_R=N_R.
   \]
   They sum to I_N.
4. The characteristic polynomial has the exact decomposition
   \[
   \chi_{U_N}(z)=\prod_{r=0}^R\chi_{U_N|_{\operatorname{ran}D_r}}(z).
   \]
   More specifically, the inherited spectra on V_r are C_(k,r) Spec(U_(N_r)); by simple spectrum of U_N (MF-185), these are nested subsets of its eigenvalues, with no repetition across the mutually orthogonal layers.

## Proof

Each J_l is an isometry by the disjoint-support normalization of its basis vectors, so every composition \mathcal J_r is an isometry. The images form a nested flag because \mathcal J_(r+1)=\mathcal J_r J_(k−2r). The earlier exact two-level theorem gives U_(3^l)J_l=c_l J_l U_(3^(l−2)). Repeated substitution proves the product-phase intertwining identity and U_N-invariance of each V_r. Since U_N is unitary, each invariant subspace is reducing, hence its orthogonal projector commutes with U_N.

For nested orthogonal projectors, P_rP_s=P_max(r,s). Therefore D_r=P_r−P_(r+1) are orthogonal projections with pairwise orthogonal ranges; they telescope to I_N. Their ranks follow by subtraction of the known dimensions N_r. Since each D_r commutes with U_N, the decomposition into their ranges block-diagonalizes U_N and gives the characteristic-polynomial factorization. Simple spectrum ensures eigenvalues from distinct blocks are disjoint. QED.

## Theorem B: inherited Weyl action at every level

For all r and all a,b∈Z,

\[
\boxed{W_N(3^r a,3^r b)\mathcal J_r
=\mathcal J_r W_{N_r}(a,b).}
\]

**Proof.** Apply the exact two-level identity successively:
W_N(3^r a,3^r b)J_k=J_k W_(N/9)(3^(r−1)a,3^(r−1)b), then repeat for the remaining J's. QED.

## Significance and limits

- The hierarchy is a **canonical filtration** by invariant Weyl-representation copies at levels k,k−2,k−4,... .
- It yields a direct-sum spectral-layer decomposition, with exact ranks and characteristic-polynomial factors.
- Only V_1 is known from the primitive annihilator theorem to be killed by all primitive F_q and E_s; every deeper V_r⊂V_1 is therefore also annihilated. The complementary layers D_r for r>=1 are also contained in V_1, but D_0 is not. Do not claim the entire decomposition is in the primitive common kernel.
- The phases C_(k,r) are convention-dependent and remain undetermined. The theorem does not imply all-depth common-kernel equality or full primitive-generated algebra dimensions.
- The finite k=2 endpoint uses the trivial 1-dimensional Weyl system, while odd k ends at the modulus-3 Weyl system.
- This is a mathematical representation-theoretic result, not a claim of physical scaling or a consciousness model.
