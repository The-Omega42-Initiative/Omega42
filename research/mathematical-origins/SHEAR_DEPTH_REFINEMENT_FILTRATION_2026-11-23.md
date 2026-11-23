# Shear-depth refinement filtration: exact ternary branching and information

**Proposal-only mathematical corollary of MF-43, 23 November 2026.** No canonical, deployment, or semantic claims.

Let \(G_{k,r}=\langle A,B_r\rangle\) on \((\mathbb Z/3^k)^2\), with \(A(a,b)=(b,a+b)\), \(B_r(a,b)=(a,b+3^ra)\), \(1\le r\le k\). Because \(B_{r+1}=B_r^3\) as integer unipotent matrices, the groups form a descending filtration:

\[
G_{k,1}\supseteq G_{k,2}\supseteq\cdots\supseteq G_{k,k}=\langle A\rangle.
\]

Thus their orbit partitions form a refinement filtration.

## Theorem 1 — exact branching at every depth

For \(2\le r\le k\), the transition from \(G_{k,r-1}\) to \(G_{k,r}\) has the following structure on valuation shell \(j\), where \(n=k-j\):

- If \(n<r\), every orbit is unchanged.
- If \(n\ge r\), **every** \(G_{k,r-1}\)-orbit splits into exactly **three** \(G_{k,r}\)-orbits of **equal size**.

**Proof.** MF-43 says the complete orbit label in shell \(j\) at shear depth \(r\) is \(Q(u)^2\bmod 3^{h}\), with \(h=\min(r,n)\). If \(n<r\), both depths \(r-1\) and \(r\) give \(h=n\), hence the same partition. If \(n\ge r\), the labels pass from unit-square residues modulo \(3^{r-1}\) to those modulo \(3^r\). Each unit square modulo \(3^{r-1}\) has exactly three unit-square lifts modulo \(3^r\): squaring is an isomorphism from \(1+3\mathbb Z/3^r\) to itself, since 2 is a unit in \(\mathbb Z_3\). The completeness of MF-43 identifies each distinct lift with one orbit. The exact orbit-size census gives a factor of three in the size of the parent relative to each child. QED.

## Theorem 2 — orbit-count increments

Let \(\mathcal C(k,r)\) denote the total number of orbits. For \(2\le r\le k\),

\[
\boxed{\mathcal C(k,r)-\mathcal C(k,r-1)=2\cdot3^{r-2}(k-r+1).}
\]

**Proof.** There are \(k-r+1\) valuation shells with \(n\ge r\). Each contains \(3^{r-2}\) parent orbits, each of which becomes three children, increasing the count by two. Sum over these shells. QED.

In particular,

\[
\mathcal C(k,k)=k+1+\sum_{r=2}^k2\cdot3^{r-2}(k-r+1)=\frac{3^k+1}{2}.
\]

This recovers the full Fibonacci orbit census by telescoping a chain of exact ternary refinements.

## Theorem 3 — conditional information is exactly quantized

Sample a state uniformly from a **fixed nonzero valuation shell** \(j\). Let \(L_{k,r}\) be its \(G_{k,r}\)-orbit label and \(n=k-j\). By the equal-size orbit census, the label is uniform on \(3^{\min(r,n)-1}\) possibilities. Its Shannon entropy in nats is

\[
\boxed{H(L_{k,r}\mid v_3(x)=j)=(\min(r,n)-1)\log3.}
\]

For \(2\le r\le n\), the refinement \(r-1\to r\) adds exactly \(\log3\) nats (one ternary digit) of conditional label information. For \(r>n\), it adds zero. The conditional distribution of the three child labels given a parent is exactly \((1/3,1/3,1/3)\).

**Proof.** Each orbit in a fixed shell has the same number of states, so the orbit label is uniform. Its support size is \(3^{\min(r,n)-1}\). Entropy of a uniform distribution is the logarithm of support size. The branching theorem proves the conditional ternary distribution. QED.

These entropies are defined **only** under uniform finite-state counting measure; they are not entropies of language, cognition, decisions, or physical systems.

## Example: k=4

The orbit counts at r=1,2,3,4 are \(5,11,23,41\); successive increments are \(6,12,18\), exactly the formula. For the primitive shell \(j=0\), the orbit counts are \(1,3,9,27\), and each depth increment adds one ternary digit to the norm-square label.

## Relation to the roadmap and tests

This is a **newly articulated refinement and information-theoretic corollary** of the pre-existing MF-43 orbit classification, not a new proof of MF-43. The companion script tools/path_b_shear_refinement_test.py independently constructs orbit partitions for all \(1\le r\le k\le4\), checks nesting, three-way equal splitting, count increments, and the conditional label multiplicities. All interpretive extensions require separate assumptions and evidence.
