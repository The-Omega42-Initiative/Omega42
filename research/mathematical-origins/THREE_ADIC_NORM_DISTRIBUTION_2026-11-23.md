# Three-adic norm distribution and orbit masses

**Proposal-only proof note — 23 November 2026.** No website or canonical changes. This derives a counting-measure consequence of existing MF-39/MF-55, not a new claim about consciousness or physics.

Put \(R_k=\mathbb Z/3^k\mathbb Z\), \(S_k=R_k^2\), \(\phi^2=\phi+1\), and \(N(a+b\phi)=a^2+ab-b^2\). The Fibonacci map \(A(a,b)=(b,a+b)\) is multiplication by \(\phi\).

## Theorem 1 — exact unit norm fibers

For every \(k\ge1\) and unit \(u\in R_k^\times\), precisely \(4\cdot3^{k-1}\) elements of \(S_k\) have norm \(u\). Thus a uniformly sampled state has probability \(4/3^{k+1}\) of any specified unit norm.

**Proof.** The polynomial \(t^2-t-1\) is irreducible modulo 3, so \(R_k[\phi]\) is an unramified quadratic extension. It has \(8\cdot9^{k-1}\) units. Its norm onto \(R_k^\times\) is surjective: modulo 3 this is the surjective finite-field norm from \(\mathbb F_9^\times\) to \(\mathbb F_3^\times\); lifting follows from \(N(1+3^j x)\equiv1+3^j\operatorname{Tr}(x)\pmod{3^{j+1}}\) for \(j\ge1\), since the residue trace is onto. There are \(2\cdot3^{k-1}\) unit targets, all with equal-sized fibers, giving \(4\cdot3^{k-1}\). QED.

## Theorem 2 — shell distribution

Let \(v(s)=\min(v_3(a),v_3(b),k)\). For \(0\le j<k\), the number of vectors in shell \(j\) is \(8\cdot3^{2(k-j-1)}\), so

\[
\Pr[v(s)=j]=\frac89\,9^{-j},\qquad \Pr[s=0]=9^{-k}.
\]

Conditional on shell \(j\), the reduced unit norm \(N(s/3^j)\bmod 3^{k-j}\) is uniform among the \(2\cdot3^{k-j-1}\) units.

**Proof.** Dividing by \(3^j\) identifies the shell with primitive vectors modulo \(3^{k-j}\), whose number is \(3^{2(k-j)}-3^{2(k-j-1)}\). Uniformity follows from Theorem 1. QED.

## Theorem 3 — orbit masses

At modulus \(3^m\), each primitive Fibonacci orbit has \(8\cdot3^{m-1}\) points (MF-39/MF-55), so shell \(j\) at level \(k\) consists of \(3^{k-j-1}\) equally sized orbits. The invariant \(N(t)^2\), with \(t=s/3^j\), takes \(3^{k-j-1}\) values, uniformly over shell \(j\). Indeed, \(u\) and \(-u\) are the two unit norms with the same square: they are distinct modulo 3, and together their norm fibers have \(8\cdot3^{m-1}\) points, exactly one orbit.

In the inverse limit \(\mathbb Z_3^2\), normalized Haar measure gives \(\Pr[v(s)=j]=(8/9)9^{-j}\) for all \(j\ge0\), and the origin has measure zero. The reduced unit norm in each shell has Haar-uniform distribution.

**Interpretation boundary:** these probabilities are exact under counting/Haar measure. They are not empirical frequencies of question phrasing, decisions, consciousness, or physical systems.

**Verification:** the independent enumeration in tools/path_b_math_norm_distribution_test.py checks k=1..4. Finite tests do not substitute for the proofs above. Direct published Core/Companion DOCX parity remains unverified.
