#!/usr/bin/env python3
"""Exact modular checks of regular-power twisted-trace chirp consequences."""
from math import gcd

T=((1,1),(1,2))
def mul(A,B,n):
    return tuple(tuple(sum(A[i][q]*B[q][j] for q in range(2))%n for j in range(2)) for i in range(2))
def power(A,m,n):
    R=((1,0),(0,1))
    for _ in range(m):R=mul(R,A,n)
    return R
def det(A):return A[0][0]*A[1][1]-A[0][1]*A[1][0]
def inv(A,n):
    d=pow(det(A)%n,-1,n)
    return ((A[1][1]*d%n,-A[0][1]*d%n),(-A[1][0]*d%n,A[0][0]*d%n))
def vec(A,x,n):
    return ((A[0][0]*x[0]+A[0][1]*x[1])%n,(A[1][0]*x[0]+A[1][1]*x[1])%n)
def sym(x,y,n):return (x[0]*y[1]-x[1]*y[0])%n

for k in range(2,8):
    n=3**k
    for m in range(1,21):
        G=power(T,m,n)
        A=((G[0][0]-1,G[0][1]),(G[1][0],G[1][1]-1))
        assert (gcd(det(A),3)==1)==(m%4!=0)
        if m%4==0:continue
        Gi=inv(G,n)
        D=((Gi[0][0]-1,Gi[0][1]),(Gi[1][0],Gi[1][1]-1))
        Di=inv(D,n)
        for r in range(1,k//2+1):
            h=3**r;e=n//h
            for a in range(min(h,8)):
                for b in range(min(h,8)):
                    x=(e*a%n,e*b%n)
                    y=vec(Di,x,n)
                    assert sym(vec(Gi,y,n),y,n)==0,(k,m,r,a,b)
    print(f"PASS k={k}, N={n}: m=1..20, regularity and zero stabilizer chirp")
