#!/usr/bin/env python3
"""Exact F_p reduction of N=9 Weyl generators; rank 5 is a C lower bound."""
from itertools import product

N=9

def rank(vectors,p):
    piv={}
    for row in vectors:
        v=list(row)
        for j,b in sorted(piv.items()):
            if v[j]:
                a=v[j]
                v=[(x-a*y)%p for x,y in zip(v,b)]
        j=next((j for j,x in enumerate(v) if x),None)
        if j is not None:
            iv=pow(v[j],-1,p)
            piv[j]=[(x*iv)%p for x in v]
    return len(piv)

def check(p):
    z=next(x for x in range(2,p) if pow(x,9,p)==1 and pow(x,3,p)!=1)
    def add(A,B):
        return [[(A[i][j]+B[i][j])%p for j in range(N)] for i in range(N)]
    def mul(A,B):
        return [[sum(A[i][r]*B[r][j] for r in range(N))%p
                 for j in range(N)] for i in range(N)]
    def W(a,b):
        M=[[0]*N for _ in range(N)]
        for j in range(N):
            M[(j+b)%N][j]=pow(z,(-5*a*b+a*(j+b))%N,p)
        return M
    Q=lambda a,b:(a*a+a*b-b*b)%N
    labels=(1,4,7)
    Es=[]
    for label in labels:
        E=[[0]*N for _ in range(N)]
        for a,b in product(range(N),repeat=2):
            if (a%3 or b%3) and Q(a,b)**2%N==label:
                E=add(E,W(a,b))
        Es.append(E)
    assert all(mul(A,B)==mul(B,A) for A in Es for B in Es)
    I=[[int(i==j) for j in range(N)] for i in range(N)]
    vec=lambda M:[v for row in M for v in row]
    initial=[I]+Es
    assert rank([vec(x) for x in initial],p)==4
    assert rank([vec(x) for x in initial+[mul(Es[0],Es[0])]],p)==5
    basis=initial
    dimensions=[4]
    for degree in range(1,4):
        candidates=basis+[mul(w,E) for w in basis for E in Es]
        new=[]
        for M in candidates:
            if rank([vec(x) for x in new+[M]],p)>len(new):
                new.append(M)
        basis=new
        dimensions.append(len(basis))
    assert dimensions==[4,5,5,5], (p,dimensions)
    print(f'PASS p={p} zeta={z} dimensions={dimensions}; C-rank >= 5')

if __name__=='__main__':
    for p in (19,37,73,109,127):
        check(p)
