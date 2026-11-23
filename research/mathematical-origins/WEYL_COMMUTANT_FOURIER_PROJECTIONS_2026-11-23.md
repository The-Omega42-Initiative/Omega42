# Exact Hilbert–Schmidt projections from shear Fourier labels into the Weyl commutant

**Proposal-only mathematical theorem — 23 November 2026.** Distinguishes linear spectral compatibility from operator-algebra and quantum-channel claims.

Let N=3^k, R=Z/N, A=[[0,1],[1,1]], T=A² in SL₂(R), and W_x (x∈R²) be a standard odd-N Weyl system with Tr(W_x*W_y)=N δ_(x,y). Assume the quantized cat map U_T obeys exact Egorov U_T W_x U_T* = W_(Tx). Write C_T={X:U_T X U_T*=X}. For each T-orbit O let S_O=Σ_(x∈O)W_x and e_O=S_O/sqrt(N|O|). Then {e_O} is an orthonormal Hilbert–Schmidt basis of C_T, and the full commutant projection is the unitary twirl

\[
\mathcal E_T(X)=\frac1{\operatorname{ord}(T)}\sum_{a=0}^{\operatorname{ord}(T)-1}U_T^a X U_T^{-a}.
\]

It is unital, trace-preserving, completely positive and idempotent.

## Theorem 1: canonical orthogonal embedding of the arithmetic Fourier filtration

The primitive T-orbits are indexed by their norm q∈R×, and all have length L=4·3^(k−1). Their parity-even pair sums E_[q]=S_(O_q)+S_(O_-q), with [q]∈R×/{±1}, are mutually Hilbert–Schmidt orthogonal with squared norm 2NL. Define normalized basis

\[
e_{[q]}=\frac{E_{[q]}}{\sqrt{2NL}}.
\]

Let V_even=span{e_[q]}, of dimension 3^(k−1), and J:C^(R×/{±1})→V_even map the standard orthonormal delta basis to e_[q]. Then J is a unitary *linear* isomorphism.

Choose the generator C=I+3A of the norm-square orbit-label quotient. Index [q] by t∈Z/3^(k−1) so that C advances t by one (equivalently q² is multiplied by 25). For 1≤h≤k, define P_h on label functions by averaging over t mod 3^(h−1). Set

\[
\Pi_h=J P_h J^*,
\]

where J* is the Hilbert–Schmidt adjoint and J* vanishes on V_even⊥ in the full operator space. Then Π_h is an exact Hilbert–Schmidt orthogonal projection on B(C^N), of rank 3^(h−1), with Π_h Π_(h+1)=Π_h and Π_k the projection onto V_even. Its spectral bands Π_(h+1)−Π_h have ranks 2·3^(h−1) and are pairwise orthogonal.

All Π_h commute with the unitary conjugation superoperator Ad_(U_T), because their ranges are contained in its fixed-point space and they annihilate its orthogonal complement. They also commute with the full commutant twirl E_T, satisfying E_T Π_h=Π_h E_T=Π_h.

**Proof.** Weyl orthogonality and disjointness of T-orbits give the orbit-sum Gram matrix. Pairing norm labels q and −q yields the asserted normalized basis. Conjugating the finite cyclic conditional-expectation projections by J preserves self-adjointness, idempotence, ranks and nestedness. Every vector in V_even is fixed by Ad_(U_T), so the range of Π_h is contained in C_T. Since Ad_(U_T) is unitary and its fixed-point space is reducing, Π_h annihilates the orthogonal complement and commutes with Ad_(U_T) and its orthogonal fixed-point projection E_T. QED.

## Theorem 2: these filtered projections are not quantum conditional expectations

For every h, Π_h(I)=0, since I=W_0 is orthogonal to all primitive Weyl orbit sums. Thus Π_h is neither unital nor trace-preserving (indeed Tr Π_h(I)=0 while Tr I=N), and cannot be a unital completely positive conditional expectation onto an operator subalgebra.

Adjoining the identity would repair unitality of an orthogonal projection onto the enlarged linear span, but **does not by itself establish** multiplicative closure, positivity, or an operator-algebra conditional expectation. The earlier identity-coefficient obstruction proves nonclosure of V_even itself, not nonclosure of the identity-augmented span; that stronger question is left open here.

## Theorem 3: the centralizer label rotation is not symplectic

The arithmetic centralizer C=I+3A has det(C)=−5, so it is not in SL₂(R) for k≥2 (modulo 3, det(C)=1). In dimension two,

\[
\omega(Cx,Cy)=\det(C)\omega(x,y)=−5\,\omega(x,y).
\]

Thus the relabeling W_x↦W_(Cx) does not preserve the standard Weyl multiplication phase when k≥2. In particular, it cannot be implemented by conjugation with a unitary satisfying V W_x V*=W_(Cx) for all x, because conjugation preserves commutators and the Weyl commutator is ζ^(ω(x,y)). The arithmetic cyclic rotation of the orbit labels is consequently **not** a metaplectic symmetry of the quantum cat map at k≥2.

**Proof.** A direct determinant calculation gives −5. Choose x=(1,0), y=(0,1), so ω(x,y)=1. Preservation of the Weyl commutator would require ζ^(det C)=ζ, hence det C≡1 mod N. For k≥2, −5−1=−6 is not divisible by 9, contradiction. QED.

## Scope

The genuine bridge is an isometric embedding of *label Hilbert spaces* into the Hilbert–Schmidt commutant, and an exact family of commuting orthogonal superoperator projections. It is **not** an operator-algebra isomorphism, a trace-preserving quantum channel, or a physical spectral correspondence. The exact Egorov convention and phase-space indexing must be checked against the canonical Core/Companion documents before claiming canonical parity. The companion test checks orbit counts, Gram combinatorics, projector ranks and nonsymplectic determinant for k=1..4.
