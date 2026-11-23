# Joint signature multiplicities of the N=9 primitive parity-even Weyl algebra

**23 November 2026.** Exact dimension five is already proved in WEYL_GENERATED_ALGEBRA_MOD9_EXACT_THEOREM_2026-11-23.md. This note reports an independent *numerical* multiplicity observation and identifies the exact certification still required.

Let E_s (s=1,4,7) be the three commuting self-adjoint primitive parity-even Weyl sums on C^9. By the exact algebra theorem, their joint eigenvalue map has exactly five distinct signatures, because the generated commutative C*-algebra has dimension five.

## Numerically observed joint multiplicities

Direct diagonalization of H=E_1+sqrt(2) E_4+sqrt(3) E_7 with independent floating-point Weyl matrices finds five joint signatures, with multiplicities

\[
\boxed{(1,2,2,2,2)\quad\text{(numerically observed, not yet exactly certified).}}
\]

Representative joint signatures, rounded to six decimals, in (E_1,E_4,E_7) order:

| Multiplicity | E_1 | E_4 | E_7 |
|---:|---:|---:|---:|
| 2 | 2.908847 | −5.052121 | −6.856726 |
| 2 | −8.908847 | −0.947879 | 0.856726 |
| 1 | 0 | 0 | 0 |
| 2 | 1.958111 | 8.638156 | −1.596267 |
| 2 | 4.041889 | −2.638156 | 7.596267 |

The companion NumPy script reproduces this observation and checks Hermiticity and pairwise commutativity numerically.

## What is exact versus provisional

**Exact:** there are five joint signature classes, by the previously established exact dimension-five theorem and the finite-dimensional spectral-separation criterion. **Provisional:** their multiplicities are 1,2,2,2,2 and the displayed decimal eigenvalues. Floating-point clustering does not certify exact multiplicities, and the numerical test is not a replacement for a cyclotomic characteristic-polynomial calculation.

## Exact certification route

Compute the characteristic polynomial of a generic linear combination H=t_1E_1+t_4E_4+t_7E_7 over K(t_1,t_4,t_7), K=Q(zeta_9), or use a rational choice of coefficients separating the five joint signatures. Factor over K, identify distinct irreducible eigenvalue factors and multiplicities, and verify corresponding joint idempotent ranks via exact traces. An exact 9×9 characteristic polynomial or a trace-idempotent certificate would settle the reported (1,2,2,2,2) pattern.

The multiplicity pattern does not imply a formula at k>=3. No physical interpretation follows.
