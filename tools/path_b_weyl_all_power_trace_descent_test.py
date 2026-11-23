#!/usr/bin/env python3
"""Exact integer checks of the all-power 3-adic trace-descent phase criterion."""
T=((1,1),(1,2))
def mul(A,B,n):
    return tuple(tuple(sum(A[i][q]*B[q][j] for q in range(2))%n for j in range(2)) for i in range(2))
def power(A,m,n):
    R=((1,0),(0,1))
    for _ in range(m): R=mul(R,A,n)
    return R
def inv(A,n):
    det=(A[0][0]*A[1][1]-A[0][1]*A[1][0])%n
    d=pow(det,-1,n)
    return ((A[1][1]*d%n,-A[0][1]*d%n),(-A[1][0]*d%n,A[0][0]*d%n))
def mv(A,x,n):
    return tuple(sum(A[i][j]*x[j] for j in range(2))%n for i in range(2))
count=0
for k in range(2,9):
    n=3**k
    for m in range(1,121):
        if m%4:t=0
        else:
            q=m//4;t=1
            while q%3==0:q//=3;t+=1
        for r in range(1,k//2+1):
            if k<2*r+t:continue
            h=3**r;e=n//h
            G=power(T,m,n);Gi=inv(G,n)
            D=tuple(tuple((Gi[i][j]-(i==j))%n for j in range(2)) for i in range(2))
            if t:
                A=tuple(tuple(z//3**t for z in row) for row in D)
                Ai=inv(A,n)
            else: Ai=inv(D,n)
            for a in range(min(h,7)):
                for b in range(min(h,7)):
                    x=(e*a%n,e*b%n)
                    if t: y=tuple((3**(k-r-t)*v)%n for v in mv(Ai,(a,b),n))
                    else:y=mv(Ai,x,n)
                    assert mv(D,y,n)==x,(k,m,r,a,b,'preimage')
                    gy=mv(Gi,y,n)
                    assert (gy[0]*y[1]-gy[1]*y[0])%n==0,(k,m,r,a,b,'phase')
                    count+=1
    print('PASS k',k)
print('Total exact checks',count)
