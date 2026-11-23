# Exact Fourier–norm adapter contract (MOR / OMIP)

**Proposal-only mathematics — 23 November 2026.** No canonical or website deployment changes.

## Inputs and outputs

The independent standard-library script at tools/path_b_math_exact_adapter.py uses positive depth k, modulus m=3^k, the Fibonacci transformation A(a,b)=(b,a+b), and the quadratic norm Q(a,b)=a²+ab−b². The function norm_fiber_count(k,x) returns the **exact integer** number of pairs modulo m whose norm is congruent to x.

## Fourier inversion theorem

Define the prime-power Ramanujan sum

\[
c_{3^r}(x)=\begin{cases}
2\cdot3^{r-1}&3^r\mid x,\\
-3^{r-1}&3^{r-1}\mid x,\ 3^r\nmid x,\\
0&3^{r-1}\nmid x.
\end{cases}
\]

Then for every k≥1 and integer x,

\[
\boxed{N_k(x)=3^{-k}\left(3^{2k}+\sum_{r=1}^k 3^{2(k-r)}(-3)^r c_{3^r}(x)\right).}
\]

**Proof.** Character orthogonality expresses the indicator of Q(a,b)=x as the average of additive characters:

\[
N_k(x)=3^{-k}\sum_{t\bmod3^k}S_k(t)\exp(-2\pi i tx/3^k).
\]

The zero frequency contributes 3^(2k). The frequencies with exact additive conductor 3^r are t=3^(k-r)u, where u ranges over units modulo 3^r. By the previously proved norm Gauss-sum formula, each has S_k(t)=3^(2(k-r))(-3)^r. Summing their phases gives the Ramanujan sum c_(3^r)(-x)=c_(3^r)(x). Substitution proves the formula. The piecewise Ramanujan expression follows by subtracting the complete additive sum over multiples of 3 from the complete sum over all residues. QED.

## Independent verification and boundaries

The adapter's exhaustive selftest compares every residue fiber obtained by direct enumeration to this integer Fourier inversion at k=1,2,3,4 (9, 81, 729, 6561 states respectively). Equivalent local code **passed** at all four levels; the committed file has not been CI-verified. The test also checks Q(Ax)=-Q(x), invariance of Q², the unit norm fiber count 4*3^(k-1), and A^(8*3^(k-1))=I modulo 3^k.

The Fourier formula itself takes O(k) integer terms; exhaustive enumeration costs O(9^k) operations. This contract makes no physical, semantic, probabilistic sampling or consciousness prediction. The existing shear group (MF-42/MF-43) does not preserve Q², so extending this adapter to the shear requires an independently proved replacement invariant. The published Core/Companion DOCX text has not yet been directly compared against the mathematical register.

## Review questions for Claude

Independently verify the Gauss-sum recurrence, Fourier inversion signs, Ramanujan cases, and whether the resulting formula is already contained in the canonical mathematical record. Confirm the mathematical adapter's exact domain, complexity, and nonclaims before any proposal to integrate it into the canonical documents.
