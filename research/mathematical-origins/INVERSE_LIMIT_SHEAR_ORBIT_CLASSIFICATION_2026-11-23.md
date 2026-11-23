# Inverse-limit classification of Fibonacci–shear orbit closures

**Mathematics-only proposal — 23 November 2026.** A topological and Haar-measure consequence of existing MF-43; not a claim of independent proof of MF-43 or of physical meaning.

Let \(\mathcal O=\mathbb Z_3[\phi]\), \(\phi^2=\phi+1\), identified with \(\mathbb Z_3^2\). Write \(Q(a,b)=a^2+ab-b^2\), \(A(a,b)=(b,a+b)\), and \(B_r(a,b)=(a,b+3^ra)\), with fixed integer \(r\ge1\). Let \(\Gamma_r=\langle A,B_r\rangle\subset\mathrm{GL}_2(\mathbb Z_3)\), and let \(K_r\) denote its closure in the compact group \(\mathrm{GL}_2(\mathbb Z_3)\).

For \(x\ne0\), write \(x=3^j u\) with \(j=\min(v_3(a),v_3(b))\) and primitive \(u\in\mathbb Z_3^2\).

## Theorem 1 — exact inverse-limit orbit closure

\[
\boxed{K_r x=\overline{\Gamma_r x}
=\{3^j v:\ v\in\mathbb Z_3^2\text{ primitive},\
Q(v)^2\equiv Q(u)^2\pmod{3^r}\}.}
\]

The orbit of zero is the singleton \(\{0\}\). At each fixed nonzero valuation \(j\), there are exactly \(3^{r-1}\) distinct \(K_r\)-orbits. They are simultaneously closed and open *relative to the valuation shell*, and have equal normalized Haar measure

\[
\boxed{\mu(K_r x)=\frac89\,9^{-j}\,3^{-(r-1)}.}
\]

**Proof.** Let \(S_{j,r}(x)\) be the displayed set. It is closed, because it is specified by a valuation and a congruence modulo \(3^r\); its image at any finite level \(3^k\), for \(k>j\), is the orbit predicted by MF-43 when \(k\ge j+r\). Invariance follows from the same finite theorem at all levels, so \(\overline{\Gamma_r x}\subseteq S_{j,r}(x)\).

Conversely, take \(y\in S_{j,r}(x)\). For every \(k\ge j+r\), MF-43 says the reductions of \(x\) and \(y\) lie in the same orbit under the reductions of \(A\) and \(B_r\) modulo \(3^k\). Hence there exists \(g_k\in\Gamma_r\) such that \(g_kx\equiv y\pmod{3^k}\). This sequence of orbit points converges to \(y\) in \(\mathbb Z_3^2\), so \(y\in\overline{\Gamma_r x}\). Thus equality holds. Compactness of \(K_r\) and continuity of its action imply \(K_rx=\overline{\Gamma_rx}\): the continuous image \(K_rx\) is compact and therefore closed, and every element of \(K_r\) is a limit of elements of \(\Gamma_r\).

For each primitive \(u\), \(Q(u)\) is a unit because \(Q\) is anisotropic modulo 3. Unit norm values are uniformly distributed under Haar measure on the primitive shell, by the norm-surjectivity theorem MF-39. The \(3^{r-1}\) norm-square values modulo \(3^r\) each receive equal weight. The full shell \(3^j\mathbb Z_3^2\setminus3^{j+1}\mathbb Z_3^2\) has measure \(9^{-j}-9^{-(j+1)}=(8/9)9^{-j}\). Dividing by \(3^{r-1}\) yields the orbit mass. Since the shell is clopen in \(\mathbb Z_3^2\), each orbit is also clopen in \(\mathbb Z_3^2\). QED.

## Theorem 2 — refinement and the limiting Fibonacci partition

For each \(r\), \(K_{r+1}\subseteq K_r\) because \(B_{r+1}=B_r^3\). On every nonzero valuation shell, each \(K_r\)-orbit is the disjoint union of exactly three \(K_{r+1}\)-orbits, each of one-third its Haar measure. Moreover,

\[
\boxed{\bigcap_{r\ge1}K_r x
=\{3^jv:\ v\text{ primitive and }Q(v)^2=Q(u)^2\text{ in }\mathbb Z_3\}.}
\]

By the established MF-55 orbit-closure theorem, this intersection is precisely the closure of the pure Fibonacci orbit \(\langle A\rangle x\).

**Proof.** The first assertion follows from the fact that every unit-square residue modulo \(3^r\) has exactly three unit-square lifts modulo \(3^{r+1}\), and the classification in Theorem 1. Intersecting the nested congruence classes imposes equality in the separated complete ring \(\mathbb Z_3\). The last equality is MF-55. QED.

## Theorem 3 — a finite-depth observable cannot distinguish finer orbits

Fix \(r\) and a nonzero shell \(j\). Any function \(f\) on that shell that is invariant under \(K_r\) factors uniquely through the finite label set

\[
\mathcal L_r=\{z^2\bmod3^r:z\in\mathbb Z_3^\times\},
\qquad|\mathcal L_r|=3^{r-1}.
\]

In particular, there are no further continuous \(K_r\)-invariants on a fixed shell beyond arbitrary functions of \(Q(u)^2\bmod3^r\).

**Proof.** By Theorem 1 the fibers of the label map are exactly the orbits. Any invariant is constant on each fiber, hence factors uniquely through the label set. Conversely, every function on the finite label set pulls back to a continuous invariant on the shell. QED.

This is a classification of **mathematical observables**, not a statement about the adequacy of any physical or semantic measurement.

## Verification and scope

The theorem is an inverse-limit consequence of the **existing** finite-level completeness claim MF-43 and norm-surjectivity MF-39. A standalone checker, tools/path_b_inverse_limit_shear_test.py, verifies finite projections, nested refinement and the predicted Haar masses for k<=4. This does not independently reprove the arbitrary-depth finite group theorem; that remains a separate audit item. No canonical, website deployment, or legal changes.
