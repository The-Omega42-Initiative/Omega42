# The 3-adic norm zeta function and its square-class distribution

**Proposal-only mathematics — 23 November 2026.** Derived from the established Omega42 norm \(Q(a,b)=a^2+ab-b^2\), with no physical interpretation.

## Theorem: exact valuation and zeta integral

Let \(x=(a,b)\) be Haar-uniform on \(\mathbb Z_3^2\), and \(Q(x)=a^2+ab-b^2\). Since the reduction of \(Q\) modulo 3 is anisotropic, \(Q(x)\equiv0\pmod3\) implies \(a\equiv b\equiv0\pmod3\). Iteration gives

\[
v_3(Q(x))=2\min(v_3(a),v_3(b))
\]

for every nonzero \(x\). In particular, the norm has **no odd 3-adic valuation**. The valuation distribution is

\[
\Pr[v_3(Q(x))=2j]=\frac89\,9^{-j}\quad(j=0,1,2,\ldots),\qquad
\Pr[v_3(Q(x))\text{ odd}]=0.
\]

For any complex \(s\) with \(\operatorname{Re}(s)>-1\), the local zeta integral is therefore

\[
Z_Q(s)=\int_{\mathbb Z_3^2}|Q(x)|_3^s\,dx
=\sum_{j=0}^\infty\frac89\,9^{-j}3^{-2js}
=\boxed{\frac{1-3^{-2}}{1-3^{-2(s+1)}}}.
\]

The pole at \(s=-1\) reflects the order of vanishing of this anisotropic quadratic norm; it is a property of the local integral, not a physical critical point. For example, \(Z_Q(0)=1\) and \(Z_Q(1)=(8/9)/(1-1/81)=9/10\).

**Proof of anisotropy.** If \(b\not\equiv0\pmod3\), then \(Q(a,b)=0\) would imply a root of \(t^2+t-1\) in \(\mathbb F_3\), whose discriminant \(5\equiv2\) is a nonsquare. If \(b=0\), then \(Q(a,0)=a^2\), forcing \(a=0\). Homogeneity gives \(Q(3^j y)=3^{2j}Q(y)\), and the primitive norm is a unit. The shell law follows by counting primitive vectors in \(\mathbb F_3^2\) and independent lifts. The geometric series gives the integral. QED.

## Theorem: pushforward of Haar measure by Q

Let \(\mu\) denote normalized Haar measure on \(\mathbb Z_3^2\), and \(\nu=Q_*\mu\) its pushforward on \(\mathbb Z_3\). For every \(j\ge0\), the shell \(3^{2j}\mathbb Z_3^\times\) has mass \((8/9)9^{-j}\); all odd-valuation shells have mass zero. Conditional on the even shell, the unit factor \(3^{-2j}Q(x)\) is Haar-uniform on \(\mathbb Z_3^\times\).

For any \(k\ge1\), and any unit residue \(u\bmod3^k\),

\[
\Pr[Q(x)\equiv u\pmod{3^k}]=\frac4{3^{k+1}}.
\]

This follows from surjectivity and equal cardinality of the finite norm fibers, as established in the companion norm-distribution note. More generally, for \(j\ge0\), \(m\ge1\), and unit \(u\bmod3^m\),

\[
\Pr[v_3(Q(x))=2j,\;3^{-2j}Q(x)\equiv u\pmod{3^m}]
=\frac89\,9^{-j}\frac1{2\cdot3^{m-1}}.
\]

These formulas explicitly characterize the norm distribution, including the singular mass accumulation near zero. There is no atom at zero because the only exact zero of this anisotropic form in \(\mathbb Z_3^2\) is \(x=0\), a Haar-null singleton.

## Research consequences

1. **Exact baseline:** any future proposed Omega42 probability interpretation must specify a sampling measure and justify departing from this Haar baseline.
2. **Non-surjectivity of the raw norm:** although the norm map on *units* is onto the unit group, the full norm image in \(\mathbb Z_3\) consists of zero and elements with even valuation. Do not confuse unit norm surjectivity with surjectivity onto all of \(\mathbb Z_3\).
3. **Structural extension:** investigate zeta integrals for the Fibonacci-plus-shear invariants (MF-42/MF-43), and compare with anisotropic quadratic forms at other primes. No such extension is claimed proved here.

**Review status:** algebraic proof given; independent automated finite-level checks of the earlier shell and unit-fiber laws have been committed but not yet run through verified CI. Published Core/Companion DOCX parity remains outstanding.
