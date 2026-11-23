# Singular cat-map powers: exact 3-adic Weyl trace support, chirp, and trace magnitude

**23 November 2026 — exact theorem completing the regular/singular trace classification.** Let N=3^k, k>=2, R=Z/NZ, T=[[1,1],[1,2]], and U_N unitary with exact Egorov U_N W_N(x) U_N*=W_N(Tx). Write [x,y]=x_1y_2−x_2y_1, ζ=exp(2πi/N), and V=U_N^m. For any nonzero integer m define
\[
t(m)=\begin{cases}
0,&4\nmid m,\\
\min(k,1+v_3(m/4)),&4\mid m.
\end{cases}
\]
Let G=T^m mod N and D=G^{-1}−I.

## Theorem A: exact Smith-type image and kernel

\[
\boxed{\operatorname{im}D=3^{t(m)}R^2,\qquad
\ker D=3^{k-t(m)}R^2.}
\]
For t=k the image is {0}, and the kernel is all R².

**Proof.** T²+I=3T and T²≡−I mod3. Thus T⁴−I=3B with B=T(T²−I) invertible mod3. For every j>=0, (T⁴)^(3^j)=I+3^(j+1)B_j with B_j invertible mod3, by cubing and induction. For any q≠0, writing q=3^j u, 3∤u, gives T^(4q)−I=3^(j+1)C with C invertible mod3 (using binomial expansion for positive u and inversion for negative u). Reduction modulo N yields T^m−I=3^t times an invertible matrix for t<k, or zero for t=k. Since G is invertible, D=−G^(-1)(G−I) has the same image and kernel. For 4∤m, T^m−I is invertible mod3, so t=0. QED.

## Theorem B: exact support and quadratic chirp of all Weyl-twisted traces

Define F_m(x)=Tr(VW_N(x)). Then
\[
\boxed{F_m(x)=0\quad\text{for }x\notin\operatorname{im}D.}
\]
For x∈im D choose any y∈R² with Dy=x. Then
\[
\boxed{F_m(x)=F_m(0)\,\zeta^{[G^{-1}y,y]/2}.}
\]
The exponent is independent of the choice of y modulo N. In particular, F_m is nonzero at every x∈im D.

**Proof.** For any y, the Weyl commutator and exact Egorov give the trace-conjugation identity
\[
\operatorname{Tr}(VW_x)
=\zeta^{-[x,y]/2+[G^{-1}y,x-y]/2}\,
\operatorname{Tr}(VW_{x+Dy}).
\]
Taking x=0 yields F_m(Dy)=F_m(0)ζ^([G^(-1)y,y]/2). If y is in ker D, then G^(-1)y=y, and the same conjugation identity at arbitrary x yields F_m(x)=ζ^{-[x,y]}F_m(x). Hence F_m(x) can be nonzero only if [x,y]=0 for all y∈ker D, i.e. x lies in the symplectic annihilator of ker D. By Theorem A, (ker D)^⊥=3^tR²=im D. If y and y+z both solve Dy=x, then z∈ker D and G^(-1)z=z. The difference of the numerators is [G^(-1)y,z]+[z,y]=[G^(-1)y−y,z]=[x,z]=0 modulo N, since x belongs to the annihilator of ker D. Thus the phase is independent of the chosen preimage. QED.

## Theorem C: exact magnitude

\[
\boxed{|\operatorname{Tr}(U_N^m)|=3^{t(m)}.}
\]
For m=0, V=I and |Tr V|=N, consistent with t=k.

**Proof.** The image of D has (N/3^t)² elements. By Theorem B, F_m has constant magnitude |F_m(0)| on its support and vanishes elsewhere. Weyl orthogonality yields
\[
\sum_{x\in R²}|F_m(x)|²=N\operatorname{Tr}(VV^*)=N².
\]
Thus (N/3^t)²|F_m(0)|²=N² and |F_m(0)|=3^t>0. QED.

## Theorem D: explicit character-table support at arbitrary stabilizer depth

Let h=3^r, 1<=r<=floor(k/2), e=N/h. The stabilizer twisted trace τ_m(a,b)=F_m(ea,eb) vanishes unless 3^t divides ea and eb modulo N. If t<=k−r, every stabilizer label lies in the support; if t>k−r, only a,b divisible by 3^(t−(k−r)) can contribute. The nonzero values have magnitude 3^t and a quadratic phase given by Theorem B. These values can be Fourier-transformed to reconstruct sector-resolved first-return traces by the previously proved Fourier–Newton theorem.

## Scope and significance

The regular case 4∤m is t=0; the singular case 4|m is now classified as well. This gives exact 3-adic support, constant modulus, and quadratic chirp of **every** Weyl-twisted trace for **every** integer exponent m, up to one overall metaplectic phase. It does not determine that absolute phase, nor explicitly evaluate all first-return characteristic-polynomial coefficients.
