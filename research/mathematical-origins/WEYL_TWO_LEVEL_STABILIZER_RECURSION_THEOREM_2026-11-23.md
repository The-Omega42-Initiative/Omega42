# Exact two-level Weyl recursion on the all-depth stabilizer subspace

**23 November 2026.** Let k>=2, N=3^k, M=N/9=3^(k−2), d=N/3=3M. The case k=2 has M=1, with the unique one-dimensional trivial Weyl representation. Let ζ_L=exp(2πi/L), and define for odd L

\[
W_L(a,b)|j\rangle=\zeta_L^{a(j+b)-2_L^{-1}ab}|j+b\rangle
=\zeta_L^{a(j+b/2)}|j+b\rangle
\]

with all indices and modular inverses taken modulo L. For L=1, take W_1(0,0)=1. Define the isometry J_k:C^M→C^N by

\[
J_k|t\rangle=3^{-1/2}\sum_{v=0}^2|3t+vd\rangle,\quad 0\le t<M.
\]

## Theorem A: exact Weyl intertwining

For every a,b∈Z,

\[
\boxed{W_N(3a,3b)J_k=J_kW_M(a,b).}
\]

Consequently, J_k^*W_N(3a,3b)J_k=W_M(a,b), and the representation of the imprimitive Weyl sublattice 3(Z/N)² on V_N=ran J_k factors through the standard irreducible Weyl representation modulo M. The projector J_kJ_k^*=P_N=(1/9)Σ_(u,v∈F3)W_N(du,dv).

**Proof.** Acting on the v-th summand of J_k|t>, the Weyl shift adds 3b. The resulting basis index 3(t+b)+vd reduces modulo N to 3t'+v'd, where t'≡t+b mod M and v' differs from v by the carry in division by M. Summation over v is invariant under this permutation. The Weyl phase is

\[
\zeta_N^{3a(3t+vd+3b)-2_N^{-1}9ab}
=\zeta_N^{9a(t+b)-2_N^{-1}9ab}\,\zeta_N^{3adv}.
\]

Since 3ad=aN, the last factor equals 1. The first factor equals ζ_M^[a(t+b)−2_M^(-1)ab], because reduction of the inverse of 2 modulo N to modulo M is the inverse modulo M. This is exactly the Weyl phase for W_M(a,b), proving the identity.

For k=2, M=1, the phase reduces to 1 and all 3a,3b are multiples of 3; W_9(3a,3b) fixes the unique vector J_2|0>, so the same conclusion holds. QED.

## Theorem B: recursive cat-map restriction, up to phase

Assume exact Egorov at levels N and M for unitary quantizations U_(T,N), U_(T,M) of the same matrix T=A²:

\[
U_{T,L}W_L(x)U_{T,L}^*=W_L(Tx),\qquad L=N,M.
\]

Then V_N is invariant under U_(T,N), and there exists a unit scalar c_k∈U(1) such that

\[
\boxed{J_k^*U_{T,N}J_k=c_k U_{T,M}.}
\]

**Proof.** T permutes the nine labels d(F_3²), hence preserves their average P_N by exact Egorov. Therefore U_(T,N) restricts to a unitary on V_N. By Theorem A, its conjugation on the reduced Weyl matrices is precisely W_M(x)↦W_M(Tx). U_(T,M) has the same action. The ratio of these two unitaries commutes with all W_M(x). Since the clock and shift Weyl matrices generate M_M(C), their commutant consists of scalars. Therefore the two restricted unitaries differ by c_k∈U(1). QED.

## Consequences and limitations

1. The cat-map representation at modulus 3^k contains a canonical invariant block projectively equivalent to the cat-map representation at modulus 3^(k−2).
2. The subspace V_N has dimension M=N/9, and is annihilated by all primitive unit-norm fiber sums F_q and primitive parity-even E_s. The recursion describes the **imprimitive** Weyl operators on this block, not the primitive ones.
3. This identifies the scalar equivalence class of the restricted cat-map unitary but **does not calculate** c_k; exact equality c_k=1 depends on a metaplectic phase convention and cannot be asserted from Egorov alone.
4. This does not prove the full common zero kernel K_N equals V_N at all depths, nor that P_N belongs to the primitive-generated algebra B_N for all k.
5. For k=2, M=1 and the reduced Weyl representation is trivial. For k>=3 the intertwining is nontrivial.

## Independent check

The companion integer/cyclotomic-phase script verifies the intertwining for k=2,3,4,5 using exponent congruences and permutation of basis summands, without floating-point complex arithmetic. The all-depth argument above is the proof.

No physical, quantum-error-correction performance, or consciousness interpretation is claimed.
