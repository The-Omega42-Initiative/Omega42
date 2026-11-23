# All-power 3-adic stabilizer trace descent theorem

**23 November 2026 — exact theorem.** Let N=3^k, k>=2, T=[[1,1],[1,2]], and let U_N be an exact-Egorov unitary. For nonzero integer m define the *uncapped* singularity depth
\[
t(m)=0\ (4\nmid m),\qquad t(m)=1+v_3(m/4)\ (4\mid m).
\]
For r>=1 with k>=2r+t(m), set h=3^r, e=N/h, and M=N/h². Let P_(r,ℓ) be the syndrome character projectors, and let C_(k,r) denote the phase of the established iterated intertwiner U_N J_r=C_(k,r)J_r U_M.

## Theorem: all-power trace descent under the sharp valuation condition

If k>=2r+t(m), then for all a,b modulo h,
\[
\boxed{\operatorname{Tr}(U_N^mW_N(ea,eb))=\operatorname{Tr}(U_N^m).}
\]
Consequently,
\[
\boxed{\operatorname{Tr}(P_{r,\ell}U_N^m)=\delta_{\ell,0}\operatorname{Tr}(U_N^m),}
\]
and
\[
\boxed{\operatorname{Tr}(U_N^m)=C_{k,r}^m\operatorname{Tr}(U_M^m).}
\]

**Proof.** If t=0, the regular-power Weyl trace chirp theorem already proves constancy at all permitted depths. Suppose t>=1. The exact 3-adic matrix theorem gives D=T^(−m)−I=3^t A modulo N with A invertible modulo N (as t<k by k>=2r+t). For x=(ea,eb), choose
\[
y=3^{k-r-t}A^{-1}(a,b),
\]
so Dy=x. The singular-power trace chirp formula is
\[
F_m(x)=F_m(0)\zeta_N^{[T^{-m}y,y]/2}.
\]
Since T^(−m)y=y+x, the numerator is [x,y]. The two factors x and y are divisible respectively by 3^(k−r) and 3^(k−r−t). Therefore [x,y] is divisible by 3^(2k−2r−t), which is divisible by N=3^k under k>=2r+t. Hence the chirp equals one for all stabilizer labels. Finite Fourier inversion of the syndrome projectors gives the zero-sector concentration. The exact invariant-sector intertwiner U_N J_r=C_(k,r)J_r U_M gives Tr(P_(r,0)U_N^m)=C_(k,r)^m Tr(U_M^m). QED.

## Examples

- m=4: t=1, so r=1 descent is valid for all k>=3 (N>=27).
- m=12: t=2, so r=1 descent is valid for all k>=4 (N>=81).
- m=36: t=3, so r=1 descent is valid for all k>=5 (N>=243).
- For m with 4∤m, t=0 and all depths r<=floor(k/2) are valid, including descent to modulus 1 or 3.
- At fixed k,m, the largest valid depth is floor((k−t(m))/2), provided it is >=1.

The condition is sufficient, and no necessity or optimality is claimed. If k<2r+t(m), the argument does not imply the trace recursion and it may fail.

## Independent arithmetic verification

A local Python integer-matrix test verified D y=x and [T^(−m)y,y]=0 modulo N for k=2,...,8, m=1,...,120, all depths satisfying the hypothesis, and representative a,b modulo h; 54,351 exact cases passed. The check validates the finite arithmetic underpinning the algebraic proof, not a separately executed metaplectic matrix construction.

## Significance and limitations

This extends exact global trace recursion beyond the 4∤m case to singular exponents, with an explicit 3-adic depth threshold. It is consistent with the independently established exact trace magnitude |Tr(U_N^m)|=3^t when t<k: under k>=2r+t the reduced modulus M=3^(k−2r) has the same singularity depth t. The relative phase C_(k,r) remains quantization-dependent and is not set to one. It does not evaluate the absolute metaplectic phase or all first-return spectral coefficients.
