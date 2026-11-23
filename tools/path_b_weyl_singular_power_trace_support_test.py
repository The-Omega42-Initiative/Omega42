#!/usr/bin/env python3
"""Exact integer verification of singular cat-map power valuations and chirp phase consistency."""
from math import gcd
T=((1,1),(1,2))
def mul(A,B,n):
    return tuple(tuple(sum(A[i][q]*B[q][j] for q in range(2))%n for j in range(2)) for i in range(2))
def power(A,m,n):
    R=((1,0),(0,1))
    for _ in range(m):R=mul(R,A,n)
    return R
def det(A):return A[0][0]*A[1][1]-A[0][1]*A[1][0]
def mv(A,x,n):return tuple(sum(A[i][j]*x[j] for j in range(2))%n for i in range(2))
def bracket(x,y,n):return (x[0]*y[1]-x[1]*y[0])%n
for k in range(2,8):
    n=3**k
    for m in range(1,121):
        G=power(T,m,n)
        A=tuple(tuple((G[i][j]-(i==j))%n for j in range(2)) for i in range(2))
        if m%4: t=0
        else:
            q=m//4;v=0
            while q%3==0:q//=3;v+=1
            t=min(k,1+v)
        assert all(x%3**t==0 for row in A for x in row)
        if t<k:
            assert gcd(det(tuple(tuple(x//3**t for x in row) for row in A)),3)==1
        else:assert all(x==0 for row in A for x in row)
    print(f"PASS k={k}, N={n}: all m=1..120")
