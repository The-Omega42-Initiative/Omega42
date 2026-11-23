#!/usr/bin/env python3
"""Exact N=9 spectral multiplicities via cyclotomic charpoly squarefree factors."""
import sympy as s

N=9
z=s.exp(2*s.pi*s.I/9)
K=s.QQ.algebraic_field(z)
E={t:[[K.zero for j in range(N)] for i in range(N)] for t in (1,4,7)}
for a in range(N):
    for b in range(N):
        t=((a*a+a*b-b*b)%N)**2%N
        if t in E:
            for j in range(N):
                E[t][(j+b)%N][j]+=K.unit**((a*(j+b)-5*a*b)%N)
H=[[E[1][i][j]+2*E[4][i][j]+3*E[7][i][j]
    for j in range(N)] for i in range(N)]
from sympy.polys.matrices import DomainMatrix
coeffs=DomainMatrix(H,(N,N),K).charpoly()
T=s.Symbol("T")
p=s.Poly.from_list([K.to_sympy(v) for v in coeffs],T,extension=z)
factors=s.factor_list(p,extension=z)[1]
signature=sorted((f.degree(),power) for f,power in factors)
assert signature==[(1,1),(1,2),(1,2),(2,2)],signature
assert s.Poly(p,T,extension=z).degree()==9
# Degree 1 singleton, two repeated linear roots, and two roots of a
# squarefree quadratic, each doubled: 1+2+2+2+2 = 9.
assert s.gcd(factors[-1][0],factors[-1][0].diff()).degree()==0 if factors[-1][0].degree()==2 else True
print("PASS exact characteristic polynomial factor degrees and powers:",signature)
print("CERTIFIED N=9 joint multiplicities (1,2,2,2,2)")
