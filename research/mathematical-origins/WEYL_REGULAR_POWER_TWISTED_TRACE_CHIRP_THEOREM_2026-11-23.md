# Regular cat-map powers: exact Weyl-twisted trace chirp and unit trace magnitude

**23 November 2026 — exact theorem at all 3-power moduli.** Let N=3^k (k>=2), ζ=exp(2πi/N), T=[[1,1],[1,2]], U_N a unitary satisfying exact Egorov U_N W_N(x)U_N*=W_N(Tx), and [x,y]=x₁y₂−x₂y₁. For any integer m with 4∤m, set G=T^m mod N and V=U_N^m.

## Theorem A: regularity precisely away from multiples of four

\[
\boxed{G-I\text{ is invertible modulo }N\iff 4\nmid m.}
\]
Indeed T²≡−I mod3 and T has order four mod3. For m=1,2,3 modulo4, T^m has no eigenvalue 1 modulo3 (T has characteristic polynomial λ²+1 over F₃, irreducible), so det(T^m−I) is a 3-adic unit. If 4|m, T^m≡I mod3 and the determinant is divisible by three.

## Theorem B: exact quadratic chirp for every twisted trace

For 4∤m, define for x∈(Z/N)²
\[
y=(G^{-1}-I)^{-1}x.
\]
Then
\[
\boxed{\operatorname{Tr}(V W_N(x))
=\operatorname{Tr}(V)\,
\zeta_N^{+\frac12[G^{-1}y,y]}.}
\]
Here 1/2 means the inverse of two modulo N.

**Proof.** Weyl multiplication obeys W_xW_y=ζ^([x,y]/2)W_(x+y). Exact Egorov gives W_yV=VW_(G^(−1)y). Trace invariance under conjugation by W_y gives, for arbitrary x,
\[
\operatorname{Tr}(VW_x)=
\zeta^{([x,y]+[G^{-1}y,x-y])/2}
\operatorname{Tr}(VW_{x+(G^{-1}-I)y}).
\]
Set x=0 and choose y=(G^(−1)−I)^(−1)x_target. The first term [0,y] vanishes, yielding
\[
\operatorname{Tr}(V)=\zeta^{-[G^{-1}y,y]/2}
\operatorname{Tr}(VW_{x_target}).
\]
Solving this equation for the target trace gives:
\[
\boxed{\operatorname{Tr}(VW_{x_target})=
\operatorname{Tr}(V)\,\zeta^{+[G^{-1}y,y]/2}.}
\]
The plus sign follows from solving the conjugation identity for the target trace. QED.

## Theorem C: unit magnitude of the untwisted trace

\[
\boxed{|\operatorname{Tr}(V)|=1.}
\]
Theorem B makes all N² twisted traces equal in modulus. Weyl orthogonality and unitarity give
\[
\sum_{x\in(Z/N)^2}|\operatorname{Tr}(VW_x)|²=N\operatorname{Tr}(VV^*)=N².
\]
Therefore N²|Tr(V)|²=N². In particular the trace never vanishes for 4∤m.

## Theorem D: stabilizer-twisted traces are constant

Let 1<=r<=floor(k/2), h=3^r, e=N/h. For x=(ea,eb), y=(G^(−1)−I)^(−1)x is also divisible by e, because the inverse matrix has entries in Z/N. Since e² is divisible by N, [G^(−1)y,y]≡0 mod N. Thus
\[
\boxed{\operatorname{Tr}(U_N^mW_N(ea,eb))
=\operatorname{Tr}(U_N^m),\qquad 4\nmid m.}
\]
By Fourier inversion,
\[
\boxed{\operatorname{Tr}(P_{r,\ell}U_N^m)
=\begin{cases}\operatorname{Tr}(U_N^m),&\ell=0,\\0,&\ell\ne0.\end{cases}}
\]
This gives a direct independent proof of full-trace concentration on the zero syndrome sector, at **every** allowed depth, for powers not divisible by four.

## Corollary E: the recursion phase is observable from regular traces

From the previously proved iterated invariant-sector recursion U_N J_r=C_(k,r)J_r U_(N/h²),
\[
\boxed{\operatorname{Tr}(U_N^m)=C_{k,r}^m\operatorname{Tr}(U_{N/h²}^m),\qquad 4\nmid m.}
\]
For m=1 both traces have modulus one when N/h²>=3, so
\[
\boxed{C_{k,r}=\operatorname{Tr}(U_N)/\operatorname{Tr}(U_{N/h²}).}
\]
If N/h²=1, the one-dimensional quantization is scalar unitary and the same ratio applies. This determines the relative phase **from specified quantizations**, not its absolute value without normalization.

## Significance and scope

The result **evaluates the full Weyl-twisted trace table up to one unit-modulus scalar** whenever 4∤m, without assuming a specific metaplectic phase normalization. It strengthens the previous Fourier–Newton framework by showing every stabilizer-twisted trace is identical in these regular cases. The difficult singular cases 4|m remain open for explicit evaluation. The method is compatible with known finite Weil-representation Cayley-transform formulas but is proved directly from Weyl orthogonality and exact Egorov.
