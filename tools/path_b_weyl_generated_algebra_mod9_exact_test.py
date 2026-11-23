#!/usr/bin/env python3
"""Characteristic-zero cyclotomic certificate: dim B_9=5 (requires sympy)."""
from fractions import Fraction as F
from functools import lru_cache
import sympy as sp

x=sp.Symbol("x")
phi=sp.Poly(x**6+x**3+1,x,domain=sp.QQ)
zero=(F(0),)*6
one=(F(1),)+(F(0),)*5

@lru_cache(None)
def root(e):
    e%=9
    v=[F(0)]*6
    if e<6:v[e]=1
    else:v[e-6]=-1;v[e-3]=-1
    return tuple(v)

def add(a,b):return tuple(u+v for u,v in zip(a,b))
def sub(a,b):return tuple(u-v for u,v in zip(a,b))

def mul(a,b):
    c=[F(0)]*11
    for i,u in enumerate(a):
        if u:
            for j,v in enumerate(b):
                if v:c[i+j]+=u*v
    for i in range(10,5,-1):
        u=c[i]
        if u:c[i-3]-=u;c[i-6]-=u
    return tuple(c[:6])

@lru_cache(None)
def inv(a):
    p=sp.Poly(sum(sp.Rational(v.numerator,v.denominator)*x**i
                  for i,v in enumerate(a)),x,domain=sp.QQ)
    q=sp.invert(p,phi)
    return tuple(F(q.nth(i)) for i in range(6))

def product(A,B):
    out={}
    for (a,b),u in A.items():
        for (c,d),v in B.items():
            z=((a+c)%9,(b+d)%9)
            phase=root(5*(a*d-b*c))
            out[z]=add(out.get(z,zero),mul(mul(u,v),phase))
    return {z:v for z,v in out.items() if v!=zero}

Q=lambda a,b:(a*a+a*b-b*b)%9
labels=(1,4,7)
Es=[{(a,b):one for a in range(9) for b in range(9)
     if (a%3 or b%3) and Q(a,b)**2%9==s} for s in labels]
assert all(len(E)==24 for E in Es)
basis=[{(0,0):one}]+Es+[product(Es[0],Es[0])]
coords=[(a,b) for a in range(9) for b in range(9)]

# Find five independent coordinate rows over Q(zeta_9).
rows=[]; pivots=[]; selected=[]
for coord in coords:
    w=[B.get(coord,zero) for B in basis]
    for j,r in zip(pivots,rows):
        if w[j]!=zero:
            f=w[j]
            w=[sub(v,mul(f,u)) for v,u in zip(w,r)]
    j=next((i for i,v in enumerate(w) if v!=zero),None)
    if j is not None:
        f=inv(w[j])
        rows.append([mul(f,v) for v in w])
        pivots.append(j)
        selected.append(coord)
        if len(rows)==5:break
assert len(selected)==5

def coefficients(P):
    a=[[B.get(coord,zero) for B in basis]+[P.get(coord,zero)]
       for coord in selected]
    for j in range(5):
        i=next(i for i in range(j,5) if a[i][j]!=zero)
        a[j],a[i]=a[i],a[j]
        f=inv(a[j][j])
        a[j]=[mul(f,v) for v in a[j]]
        for i in range(5):
            if i==j:continue
            f=a[i][j]
            if f!=zero:a[i]=[sub(v,mul(f,u)) for v,u in zip(a[i],a[j])]
    return [a[i][-1] for i in range(5)]

for i in range(5):
    for j in range(i,5):
        P=product(basis[i],basis[j])
        c=coefficients(P)
        for coord in coords:
            v=zero
            for B,f in zip(basis,c):
                v=add(v,mul(B.get(coord,zero),f))
            assert v==P.get(coord,zero),(i,j,coord)
        print(f"PASS exact product {i},{j}")

print("CERTIFIED: dim B_9=5 over Q(zeta_9), hence over C")
