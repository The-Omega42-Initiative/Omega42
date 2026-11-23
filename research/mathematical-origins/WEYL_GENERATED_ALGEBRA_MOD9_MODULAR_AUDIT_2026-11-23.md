# N=9 generated Weyl algebra: exact finite-field lower bound and an unresolved characteristic-zero upper bound

**Independent arithmetic audit, 23 November 2026.** This note deliberately distinguishes a proved lower bound from a computationally suggested equality.

For N=9, the primitive parity-even norm-square labels are s∈{1,4,7}. Let E_s=Σ_(x:Q(x)²=s) W_x in the odd-N Weyl system and B_9=C*(I,E_1,E_4,E_7), contained in the 9-dimensional cat-map commutant under MF-185 and exact Egorov.

## Theorem — rigorous lower bound

\[
\boxed{5\le\dim_\mathbb C B_9\le9.}
\]

In particular, I,E_1,E_4,E_7,E_1² are linearly independent over C.

**Proof.** All entries of these matrices belong to the cyclotomic integer ring Z[ζ_9], with ζ_9 primitive of order 9. Reduce the ring via the homomorphism Z[ζ_9]→F_19 defined by ζ_9↦4 (indeed 4 has multiplicative order 9 modulo 19). The accompanying exact modular test constructs the five 9×9 matrices, computes their row-vector rank over F_19, and obtains rank 5. If the original matrices were linearly dependent over Q(ζ_9), every 5×5 minor would vanish as an algebraic integer, hence its reduction modulo 19 would vanish. The rank-5 modular result contradicts this, proving independence over Q(ζ_9) and hence over C (rank of a matrix over an extension field is unchanged). The upper bound 9 is the MF-185 commutant dimension. QED.

## Reproducible finite-field observation (not yet a theorem over C)

Using exact modular matrix multiplication and iterative span closure for primes 19,37,73,109,127 (each ≡1 mod9), the generated matrix algebra has dimension **5** in every tested reduction. This suggests dim_C B_9=5, but **modular ranks cannot establish an upper bound in characteristic zero**: extra characteristic-zero directions may vanish after reduction. To claim exact equality, exhibit a cyclotomic-field basis with exact structure constants, a characteristic-zero rank certificate, or an independent structural proof.

At each tested prime, the initial linear span has dimension 4; adjoining quadratic products raises it to 5; higher products through degree 3 add no new direction. Cross products E_1E_4, E_1E_7, E_4E_7 stay in the four-dimensional initial span modulo each tested prime, while E_1² supplies the fifth direction.

## Conventions and scope

W_(a,b)=ζ_9^(−ab/2) Z^a X^b, with Z|j>=ζ_9^j|j>, X|j>=|j+1>, and inverse of 2 interpreted modulo9. The phase-space symplectic form is ad−bc. Exact Egorov for T=A² is assumed when identifying the span with the quantum cat-map commutant; the rank-5 matrix lower bound itself uses only the Weyl matrices and norm-square fibers.

This is a useful discriminating computation, **not** a complete answer to whether B_9 is the full commutant. The next required step is a characteristic-zero certificate of the upper bound 5 or evidence of additional directions.
