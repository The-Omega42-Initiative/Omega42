# Exact additive-character sums of the Omega42 quadratic norm

**Proposal-only mathematics, 23 November 2026.** New candidate extension beyond the mathematical-register results examined to date; independent review pending. No website, canonical, governance or release changes.

Let \(Q(a,b)=a^2+ab-b^2\) and, for \(k\ge1\), let

\[
S_k(t)=\sum_{a,b\in\mathbb Z/3^k\mathbb Z}
\exp(2\pi i\,tQ(a,b)/3^k).
\]

## Theorem (closed Gauss sum)

If \(t\equiv0\pmod{3^k}\), then \(S_k(t)=3^{2k}\). Otherwise let \(v=v_3(t)<k\). Then

\[
\boxed{S_k(t)=3^{2v}(-3)^{k-v}.}
\]

In particular, for unit frequencies \(t\), the sum is the real integer \((-3)^k\); its magnitude is \(3^k\), exactly the square root of the number of states \(3^{2k}\).

## Proof

**Reduction of imprimitive frequency.** If \(t=3^v u\) with \(u\) a unit modulo \(3^{k-v}\), the phase depends only on \((a,b)\) modulo \(3^{k-v}\). Every pair at the smaller level has \(3^{2v}\) lifts, so \(S_k(t)=3^{2v}S_{k-v}(u)\). It suffices to evaluate unit frequencies.

**Base case.** Modulo 3, \(Q\) is anisotropic: only \((0,0)\) has norm zero. The eight primitive vectors split equally between norm 1 and norm 2, as follows either by direct enumeration or the surjective norm on \(\mathbb F_9^\times\). Writing \(\zeta=\exp(2\pi i/3)\), for unit \(u\) we have \(S_1(u)=1+4\zeta^u+4\zeta^{2u}=1+4(-1)=-3\).

**Two-level recurrence.** Fix \(k\ge2\), and write each \(x=(a,b)\) modulo \(3^k\) uniquely as \(x=y+3^{k-1}z\), where \(y\) is a vector modulo \(3^{k-1}\) and \(z\) a vector modulo 3. By quadratic expansion,

\[
Q(y+3^{k-1}z)\equiv Q(y)+3^{k-1}\nabla Q(y)\cdot z\pmod{3^k},
\]

since \(2(k-1)\ge k\). The sum over \(z\) vanishes unless \(\nabla Q(y)\equiv0\pmod3\), in which case it is 9. Here \(\nabla Q(a,b)=(2a+b,a-2b)\); its coefficient matrix has determinant \(-5\equiv1\pmod3\), so this condition is exactly \(y\equiv(0,0)\pmod3\). Write \(y=3w\), with \(w\) modulo \(3^{k-2}\). Homogeneity gives \(Q(y)=9Q(w)\), hence

\[
S_k(u)=9\sum_{w\bmod3^{k-2}}\exp(2\pi i\,uQ(w)/3^{k-2})=9S_{k-2}(u).
\]

Use \(S_0(u)=1\), the one-point sum at modulus 1. The recurrence and \(S_1(u)=-3\) yield \(S_k(u)=(-3)^k\), as claimed. QED.

## Fourier transform of the pushforward norm measure

Let \(p_k(r)=3^{-2k}\#\{(a,b):Q(a,b)\equiv r\pmod{3^k}\}\). Its finite Fourier transform at \(t\) is

\[
\widehat p_k(t)=3^{-2k}S_k(t)
=\begin{cases}
1,&t=0,\\
(-1)^{k-v}3^{-(2k-v)},&0\ne t,\ v=v_3(t).
\end{cases}
\]

Thus every nonzero Fourier coefficient is explicitly determined by the 3-adic valuation of its frequency, not by its unit part. This is a mathematically exact **radial spectral law**.

Fourier inversion recovers every residue probability, and provides an independent check against the norm-distribution theorem. It does not define a physical signal spectrum or semantic feature of text.

## Relation to established Omega42 results and roadmap

The existing register MF-39 and MF-55 covers norm surjectivity and orbit closures, and the recent proposal note derived shell/Haar probabilities and the local zeta integral. This theorem supplies their additive Fourier counterpart. A search over the *statements and derivations* of the 192-entry register did not find an entry explicitly stating this norm Gauss sum, but this is **not a claim of priority or comprehensive literature novelty**.

**Next adapter task:** package the finite group \(R_k^2\), transformation \(A\), invariant \(Q^2\), and normalized norm spectrum as an exact algebraic adapter with domains, codomains, proofs, tests and nonclaims. Compare this baseline against the MF-42/MF-43 shear action, which does not preserve \(Q^2\).

## Independent verification

A separate test enumerates the norm residue histogram for \(k=1,2,3,4\), calculates Fourier sums at representative frequency valuations, and compares to the closed formula. The general theorem rests on the proof above; numerical tests are not a replacement for it.
