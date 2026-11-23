# Exact joint spectral multiplicity theorem for the modulus-nine Weyl algebra

**23 November 2026.** This upgrades the previously numerical multiplicities in WEYL_MOD9_JOINT_SIGNATURE_MULTIPLICITY_AUDIT_2026-11-23.md to a characteristic-zero theorem.

Let ζ=exp(2πi/9), K=Q(ζ), Q(a,b)=a²+ab−b² modulo9, and W_(a,b)=ζ^(−5ab) Z^a X^b, with Z|j>=ζ^j|j>, X|j>=|j+1>. Let E_s=Σ_(Q(a,b)²=s)W_(a,b) for s∈{1,4,7}. These are commuting self-adjoint matrices in M_9(C). Let B_9=C*(I,E_1,E_4,E_7). The earlier exact theorem established dim B_9=5.

## Theorem

The joint eigenspace multiplicities of E_1,E_4,E_7 on C^9 are exactly

\[
\boxed{(1,2,2,2,2).}
\]

In particular, B_9 has five minimal central spectral projections with ranks 1,2,2,2,2. Since B_9 is commutative, these are also its minimal nonzero projections.

## Proof

Choose the rational linear combination H=E_1+2E_4+3E_7∈B_9. Compute its 9×9 characteristic polynomial exactly over K using the six-dimensional cyclotomic presentation K=Q[x]/(x⁶+x³+1). The exact factorization has the shape

\[
\chi_H(t)=t\,L_1(t)^2L_2(t)^2R_2(t)^2,
\]

where L_1 and L_2 are distinct degree-one monic polynomials, R_2 is monic, irreducible of degree two over K (in particular squarefree), and all four displayed factors are pairwise coprime. Hence H has precisely five distinct eigenvalues over C: one simple root t=0, one root from each linear factor of multiplicity two, and two roots from R_2, each of multiplicity two.

The exact factorization is independently reproducible by the companion SymPy script. The script constructs each Weyl matrix over K without numerical approximation, computes the characteristic polynomial by exact DomainMatrix arithmetic, factors it over K, and asserts the factor degree/exponent multiset [(1,1),(1,2),(1,2),(2,2)]. This factorization includes five distinct roots because the factorization routine returns distinct irreducible factors and characteristic zero makes each irreducible factor separable.

Because H belongs to B_9, its five distinct spectral projections lie in B_9 (each is a polynomial in H by Lagrange interpolation over C). The exact prior theorem gives dim_C B_9=5. Therefore those five spectral projections form a basis for B_9, and no other joint spectral subdivision is possible. Their ranks are exactly the five H-eigenspace multiplicities 1,2,2,2,2. QED.

## Verification and caveats

- Reproducible exact test: tools/path_b_weyl_mod9_signature_multiplicity_exact_test.py (requires SymPy).
- Independent local exact computation **executed and passed**: characteristic polynomial over Q(ζ_9), factor degree/power pattern (1,1),(1,2),(1,2),(2,2), and squarefree part degree five. The committed test and GitHub CI have not been separately run.
- This proves the multiplicities at k=2, not at k>=3.
- Identifying the rank-one class as the joint zero-signature class remains a separate statement; the numerical audit suggests it, but it is not required for this theorem.
- MF-185 and exact Egorov are needed only to identify B_9 as a proper subalgebra of the cat-map commutant; the spectral multiplicity statement itself follows directly from the explicit Weyl matrices and exact B_9 algebra theorem.

No physical, consciousness, or quantum-channel interpretation is claimed.
