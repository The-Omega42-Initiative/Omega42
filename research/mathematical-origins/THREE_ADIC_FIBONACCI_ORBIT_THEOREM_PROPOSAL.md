# MOR-02 — exact orbit structure of the Fibonacci map modulo powers of three

**Status:** Proposal-only mathematical derivation, 23 November 2026. Not a canonical Core/Companion amendment, physical ontology, or empirical finding. Independent mathematical review pending.

## Statement

Let \(R_k=\mathbb Z/3^k\mathbb Z\), \(k\ge1\), and \(T_k(a,b)=(b,a+b)\), with matrix \(A=\begin{pmatrix}0&1\\1&1\end{pmatrix}\). Write \(v_3(a,b)=\min(v_3(a),v_3(b),k)\).

**Theorem.** Every vector with \(v_3(a,b)=s<k\) has exact orbit length
\[
L_{k,s}=8\cdot3^{k-s-1}.
\]
There are exactly \(3^{k-s-1}\) distinct cycles in that valuation stratum. The zero vector is the sole fixed point. Consequently the total number of cycles is
\[
C_k=1+\sum_{r=1}^k3^{r-1}=\frac{3^k+1}{2}.
\]
At \(k=2\), the 81 states have cycle lengths \(1,8,24,24,24\). At \(k=3\), the 729 states have one 1-cycle, one 8-cycle, three 24-cycles and nine 72-cycles.

## Proof

1. Reduction modulo three has one orbit of length eight on the eight nonzero vectors. This can be checked directly from \((1,0)\) under \(T\): \((1,0)\), \((0,1)\), \((1,1)\), \((1,2)\), \((2,0)\), \((0,2)\), \((2,2)\), \((2,1)\), then back. Hence any period of a primitive vector (at least one coordinate a unit) is divisible by eight.
2. Direct integer multiplication gives \(A^8=\begin{pmatrix}13&21\\21&34\end{pmatrix}=I+3B\), where \(B=\begin{pmatrix}4&7\\7&11\end{pmatrix}\) has determinant \(-5\equiv1\pmod3\). Thus \(B\) is invertible modulo three.
3. For each \(j\ge0\), the binomial theorem gives \((I+3^{j+1}B_j)^3=I+3^{j+2}B_{j+1}\) with \(B_{j+1}\equiv B_j\pmod3\), provided \(B_j\equiv B\pmod3\). Therefore \(A^{8\cdot3^j}=I+3^{j+1}B_j\), with \(B_j\) invertible modulo three. For a primitive vector \(u\), \((A^{8\cdot3^j}-I)u\) has exact coordinatewise 3-adic valuation \(j+1\), until the modulus is reached.
4. Any return exponent is \(8m\). Write \(m=3^jt\) with \(3\nmid t\). Expanding \((I+3^{j+1}B_j)^t\) shows \((A^{8m}-I)u\) has valuation exactly \(j+1\): the linear term has that valuation, and all higher terms have larger valuation. Thus return modulo \(3^r\) occurs exactly when \(3^{r-1}\mid m\). Every primitive vector modulo \(3^r\) has exact period \(8\cdot3^{r-1}\).
5. A vector in \(R_k^2\) of valuation \(s\) is uniquely \(3^su\) for a primitive vector \(u\) modulo \(3^{k-s}\), and has the same period as \(u\). The number of such vectors is \(3^{2r}-3^{2r-2}=8\cdot3^{2r-2}\), where \(r=k-s\). Dividing by the period \(8\cdot3^{r-1}\) gives \(3^{r-1}\) cycles **(not \(3^r\))**.

**Corrected theorem and total:** the stratum with \(r=k-s\) has \(3^{r-1}\) cycles, so
\[
\boxed{C_k=1+\sum_{r=1}^k3^{r-1}=\frac{3^k+1}{2}.}
\]
For \(k=2\), this is \(1+1+3=5\); for \(k=3\), \(1+1+3+9=14\). The first displayed count and formula above are intentionally superseded by this explicit correction; only the boxed formula is claimed.

## Interpretation

The five cycles at modulus nine follow from a uniform 3-adic lifting mechanism: the matrix has order eight modulo three and its eighth power is an invertible first-order perturbation of identity. Increasing \(k\) by one triples the primitive orbit length and triples the number of primitive cycles. The resulting compatible finite dynamics provide a rigorous research bridge toward the inverse-limit space \(\mathbb Z_3^2\). They do **not** establish that physical reality, consciousness or AI representations instantiate this dynamical system.

## Independent reproduction

Compute the orbit decomposition by direct enumeration for \(k=1,2,3\), compare against the period and multiplicity formulas, and independently verify \(A^8\), \(\det B=-5\), and the 3-adic binomial lifting. The calculation should not use the asserted orbit formula to construct its observed cycles.

## Open research directions

- Describe the compatible orbit classes and invariant measures on \(\mathbb Z_3^2\).
- Classify centralisers and symmetries of \(A\) over \(\mathbb Z_3\).
- Compare the 3-adic stratification with the quadratic field \(\mathbb Q(\sqrt5)\) and the norm \(a^2+ab-b^2\), including parity under \(T\).
- Determine which structural properties distinguish this map from other invertible 2×2 recurrences.
