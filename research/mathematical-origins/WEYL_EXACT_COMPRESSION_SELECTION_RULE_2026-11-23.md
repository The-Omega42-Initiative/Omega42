# Exact Weyl compression selection rule and reduced operator calculus

**23 November 2026.** Let N=3^k, 0<=r<=floor(k/2), h=3^r, M=N/h², e=N/h, and let J=𝒥_r:C^M→C^N denote the iterated stabilizer isometry. Let P=JJ*=h^(−2)Σ_(u,v mod h)W_N(eu,ev). The case r=0 is the identity.

## Theorem A: exact compression selection rule

For all x=(a,b)∈(Z/N)²,

\[
\boxed{J^*W_N(a,b)J=
\begin{cases}
W_M(a/h,b/h),&h\mid a,\ h\mid b,\\
0,&\text{otherwise}.
\end{cases}}
\]

Equivalently, P W_N(a,b) P=0 unless both a and b are divisible by h; for a=ha',b=hb', P W_N(ha',hb')P=J W_M(a',b')J*.

**Proof.** The stabilizer group H=e(Z/h)² acts as identity on ran P. For any y∈H, the Weyl commutator gives W_y W_x W_y*=ζ_N^⟨y,x⟩ W_x, where ⟨y,x⟩ is the integral symplectic pairing (the overall sign depends on convention but not the triviality criterion). Consequently

\[
P W_xP=P W_yW_xW_y^*P=\zeta_N^{\langle y,x\rangle}P W_xP.
\]

If PW_xP is nonzero, the character must be trivial for all y∈H. Choosing y=(e,0) and y=(0,e) shows ζ_N^(ea)=ζ_N^(eb)=1, equivalently h|a and h|b. Conversely, when x=(ha',hb'), the exact iterated Weyl intertwiner W_N(ha',hb')J=J W_M(a',b') gives the displayed nonzero compression. QED.

## Theorem B: explicit Weyl-symbol reduction for arbitrary operators

Every A∈M_N(C) has a unique Weyl expansion

\[
A=\sum_{a,b\bmod N}\alpha_{a,b}W_N(a,b),\quad
\alpha_{a,b}=\frac1N\operatorname{Tr}(A W_N(a,b)^*).
\]

Its compression to the reduced M-dimensional block is exactly

\[
\boxed{
J^*AJ=\sum_{a',b'\bmod M}
\left(\sum_{\substack{a,b\bmod N\\h\mid a,\ h\mid b\\
a/h\equiv a'\,(\mathrm{mod}\ M)\\
b/h\equiv b'\,(\mathrm{mod}\ M)}}\alpha_{a,b}\right)W_M(a',b').
}
\]

The inner sum contains exactly h² terms, corresponding to lifts of (a',b') modulo N/h. Thus the compression map A↦J*AJ is a **unital completely positive map** from M_N(C) to M_M(C), and is surjective (because it maps W_N(ha,hb) onto W_M(a,b)). It is not a homomorphism on arbitrary A, only on operators preserving ran J appropriately.

## Theorem C: reduced traces

For every A,

\[
\boxed{\operatorname{Tr}(PA)=\operatorname{Tr}(J^*AJ)
=M\sum_{\substack{a,b\bmod N\\(a,b)\in H}}\alpha_{a,b}.}
\]

In particular Tr(PW_N(x))=M for x∈H and zero otherwise, recovering the Fourier coefficients of the closed-form projector. More generally, if U_N is the exact-Egorov cat map and U_NJ=C_(k,r)J U_M, then

\[
\operatorname{Tr}(P U_N^m)=C_{k,r}^m\operatorname{Tr}(U_M^m)
\]

for every integer m. The Weyl-symbol formula provides an independent way to compute the left-hand side from the Weyl expansion of U_N^m.

## Significance and limits

The exact selection rule describes **all** Weyl operators, not just the primitive norm-fiber sums. It turns every compression into an explicit arithmetic filter followed by a lower-modulus Weyl expansion, supplying a concrete computational reduction. It does not calculate the convention-dependent cat-map phases or imply an all-depth common-kernel equality. No physical interpretation is asserted.
