# Complete 3-adic dual cat-map orbit classification and trace selection at every stabilizer depth

**23 November 2026 — exact all-depth theorem.** This extends WEYL_SYNDROME_FOUR_CYCLE_TRACE_RECURSION_THEOREM_2026-11-23.md.

Let T=[[1,1],[1,2]]∈SL₂(Z), r>=1, h=3^r. On character labels x∈(Z/hZ)², the exact-Egorov action is S=T^(−transpose) mod h. For nonzero x let s=min(v₃(x₁),v₃(x₂),r), so 0<=s<r. Set t=r−s.

## Theorem A: exact order and orbit lengths

1. The order of T and S modulo 3^r is **4·3^(r−1)**.
2. Every nonzero x of valuation s has orbit length exactly
   \[
   \boxed{L_{r,s}=4\cdot3^{r-s-1}=4\cdot3^{t-1}.}
   \]
3. For each t=1,...,r, the number of distinct cycles of length 4·3^(t−1) is exactly
   \[
   \boxed{2\cdot3^{t-1}.}
   \]
   Zero is the unique fixed label. Consequently the complete orbit-length inventory is
   \[
   \boxed{\{1:1\}\ \cup\ \{4\cdot3^{t-1}:2\cdot3^{t-1}\text{ cycles},\ 1\le t\le r\}.}
   \]

## Proof

The characteristic identity T²−3T+I=0 gives T²+I=3T and T²≡−I (mod 3). Hence T has order four modulo three. Moreover
\[
T^4−I=(T²+I)(T²−I)=3T(T²−I)=3B,
\]
where B=T(T²−I) is invertible modulo three, because T is invertible and T²−I≡−2I≡I (mod 3). Thus T^4=I+3B with B∈GL₂(Z₃).

Inductively, for each j>=0,
\[
T^{4\cdot3^j}=I+3^{j+1}B_j,\qquad B_j\equiv B\pmod3.
\]
Indeed, cubing I+3^(j+1)B_j gives I+3^(j+2)(B_j+3^(j+1)B_j²+3^(2j+1)B_j³), and the bracket reduces to B_j mod 3. Thus the first power of T^4 congruent to I modulo 3^t is 3^(t−1), and no smaller positive exponent of T can be identity modulo 3^t because reduction modulo three requires a multiple of four. This proves the matrix order. The same holds for S=T^(−transpose).

For a primitive vector y modulo 3^t, the invertibility of B_j mod 3 ensures (T^(4·3^j)−I)y has exact valuation j+1 when j+1<t. No smaller positive power can fix y: powers not divisible by four have no nonzero fixed vectors mod3 (T,T²,T³ all have no eigenvalue 1 mod3); and powers 4q with 3-adic valuation v₃(q)=j have the same first nonzero 3-adic order as T^(4·3^j)−I because (I+3^(j+1)B_j)^u−I has leading coefficient uB_j mod3 for 3∤u. Hence every primitive y modulo 3^t has orbit length 4·3^(t−1).

A label x of valuation s is 3^s times a primitive vector modulo 3^(r−s), and its orbit length equals the primitive length at t=r−s. There are 3^(2t)−3^(2t−2)=8·3^(2t−2) primitive vectors modulo 3^t. Dividing by their common orbit length 4·3^(t−1) gives 2·3^(t−1) cycles. QED.

## Theorem B: all-depth syndrome-sector trace selection

Let N=3^k, 1<=r<=floor(k/2), h=3^r, e=N/h. Define character projections
\[
P_{r,\ell}=h^{-2}\sum_{a,b\bmod h}\exp(-2\pi i(\ell_1a+\ell_2b)/h)W_N(ea,eb).
\]
Each has rank N/h². Under exact Egorov U_NP_(r,ℓ)U_N*=P_(r,Sℓ).

For any S-orbit O of length L, let Q_O=Σ_(ℓ∈O)P_(r,ℓ). Then
\[
[Q_O,U_N]=0,\quad \operatorname{rank}Q_O=L N/h²,
\]
and
\[
\boxed{\operatorname{Tr}(Q_OU_N^m)=0\quad\text{if }L\nmid m.}
\]
The spectrum of U_N on ran Q_O is invariant under multiplication by any Lth root of unity, counting multiplicity, and decomposes into full L-tuples. For L=1 this imposes no cancellation.

**Proof.** U_N^m maps the mutually orthogonal sector ran P_(r,ℓ) to ran P_(r,S^mℓ). If L∤m, no sector on O maps to itself, so each diagonal sector trace vanishes. For the spectral statement, define the grading unitary G_O=Σ_(j=0)^(L−1) exp(2πij/L)P_(r,S^jℓ₀) on ran Q_O. It satisfies G_O U_N G_O*=exp(2πi/L) U_N (up to inverse depending on the orientation), which forces root-of-unity spectral symmetry. QED.

## Corollary: global traces and the deepest primitive cycles

At r=1 the two nonzero cycles have L=4, recovering Tr(U_N^m)=c_k^m Tr(U_(N/9)^m) whenever 4∤m. At general r, each orbit of primitive character labels (s=0) has length 4·3^(r−1), so its block contributes zero to every trace moment m not divisible by 4·3^(r−1). The number of such blocks is 2·3^(r−1), each of dimension (4·3^(r−1))N/3^(2r).

These are **orbitwise** trace cancellations. The stronger global trace recursion for 4∤m is inherited from r=1; do not assert a new global trace recursion for arbitrary m divisible by four, since shorter nonzero cycles can contribute.

## Significance and boundaries

The theorem gives a complete exact classification of all higher-depth syndrome orbits, rather than finite-depth extrapolation, and produces explicit spectral root-of-unity multiplets and trace vanishing at every valuation stratum. It does not determine the phase c_k, settle all-depth primitive common-kernel equality, or assert a physical interpretation.
