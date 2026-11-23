# Spectral inheritance and characteristic-polynomial factorization across two 3-adic levels

**23 November 2026 — exact conditional-on-Egorov theorem.** Builds on WEYL_TWO_LEVEL_STABILIZER_RECURSION_THEOREM_2026-11-23.md and MF-185.

Let N=3^k (k>=2), M=N/9, and let J_k:C^M→C^N be the exact Weyl intertwiner

\[
J_k|t\rangle=3^{-1/2}\sum_{v=0}^2|3t+vN/3\rangle.
\]

Write P_N=J_kJ_k^*. Assume unitary cat-map quantizations U_N and U_M obey exact Egorov for T=A². The prior recursion theorem gives U_N J_k=c_k J_k U_M with |c_k|=1, where c_k depends on the chosen phase conventions.

## Theorem: spectral inheritance

1. The decomposition C^N=ran J_k ⊕ (ran J_k)^⊥ is a **reducing decomposition** for U_N and every primitive parity-even generator E_s. In the corresponding orthonormal basis,
   \[
   U_N\cong(c_k U_M)\oplus U_N^\perp,\qquad
   E_s\cong 0_M\oplus E_s^\perp.
   \]
2. Consequently, as an exact identity of polynomials over C,
   \[
   \boxed{\chi_{U_N}(z)=\chi_{c_kU_M}(z)\,\chi_{U_N^\perp}(z).}
   \]
   In particular every eigenvalue λ of U_M gives an eigenvalue c_k λ of U_N, with the same multiplicity in the invariant block.
3. Under MF-185's **simple spectrum** at both levels, the M inherited eigenvalues c_k Spec(U_M) are all distinct and disjoint from Spec(U_N^\perp). Hence they specify M distinct U_N eigenlines, and every such eigenline has **zero primitive Weyl joint signature**.
4. For every polynomial p, the trace of the cat-map block satisfies
   \[
   \boxed{\operatorname{Tr}(P_N p(U_N))=\operatorname{Tr}(p(c_kU_M)).}
   \]
   In particular Tr(P_N U_N^r)=c_k^r Tr(U_M^r) for all integers r (negative powers are allowed since U_N is unitary).
5. The operator P_N belongs to the **full** commutant D_N and its rank is M. The primitive-generated algebra B_N acts as scalars on ran P_N. The assertion P_N∈B_N is **not** made for k>=5, where equality of the full zero-signature kernel with ran P_N is open.

## Proof

The exact intertwining U_NJ_k=c_kJ_kU_M implies ran J_k is U_N-invariant. Since U_N is unitary and finite-dimensional, its orthogonal complement is invariant as well: the invariant subspace is a sum of U_N eigenlines, or equivalently its projector commutes with U_N by the exact stabilizer averaging theorem. The primitive Weyl annihilator theorem gives E_sJ_k=0, and self-adjointness gives J_k^*E_s=0, yielding the displayed simultaneous block forms.

The characteristic-polynomial factorization follows from block diagonality. If U_N has simple spectrum, no eigenvalue of c_kU_M can occur in the complementary block, or U_N would have a repeated eigenvalue. The inherited eigenvectors are killed by all E_s, giving the zero signature. Finally, the trace identities follow by taking traces of the upper-left M×M blocks of p(U_N). QED.

## Significance and boundaries

- This is an **exact spectral recursion**, not merely an invariant-subspace statement. It constrains characteristic polynomials, spectra, and all trace moments.
- The inherited block is spectrally identifiable inside U_N by the subset c_k Spec(U_M), even when the full primitive Weyl common kernel is larger.
- The phase c_k remains unspecified: exact Egorov alone determines the restricted quantization only projectively.
- The factorization is not claimed to have coefficients in Q or in a specified cyclotomic subfield without choosing metaplectic phases and a coefficient field.
- It does **not** establish an all-depth formula for dim B_N or dim ker E_s. No physical or consciousness interpretation follows.

## Suggested next proof obligations

1. Fix an explicit metaplectic normalization and calculate c_k.
2. Test whether the full zero-signature kernel equals ran J_k at N=243 by exact modular rank, if computationally feasible.
3. Derive trace formulas for U_N and compare with inherited trace moments, potentially isolating arithmetic phase patterns.
