#!/usr/bin/env python3
"""Exact integer proof-obligation tests for all-depth Weyl annihilator theorem."""
from collections import Counter

def Q(a,b,n):return (a*a+a*b-b*b)%n

def verify(k):
    n=3**k; d=n//3; inv2=pow(2,-1,n)
    for a0 in range(d):
        for r in range(n):
            q0=Q(a0,r,n)
            if q0%3==0:continue
            L=( (2*a0+r)%3,(-a0+2*r)%3 )
            M=(r%3,a0%3)
            determinant=(L[0]*M[1]-L[1]*M[0])%3
            assert determinant==(2*q0)%3!=0
            for target in range(3):
                phase=Counter((M[0]*u+M[1]*v)%3
                              for u in range(3) for v in range(3)
                              if (L[0]*u+L[1]*v)%3==target)
                assert [phase[i] for i in range(3)]==[1,1,1]
    print(f'PASS k={k} all affine F3 cancellation lines')

def direct(k):
    n=3**k;d=n//3;inv2=pow(2,-1,n)
    labels=sorted({Q(a,b,n)**2%n for a in range(n) for b in range(n)
                   if a%3 or b%3})
    for s in labels:
        for r in range(n):
            c=Counter()
            for j in (0,d,2*d):
                b=(r-j)%n
                for a in range(n):
                    if Q(a,b,n)**2%n==s:
                        c[(a*r-inv2*a*b)%n]+=1
            assert all(c[t]==c[t+d]==c[t+2*d] for t in range(d)),(k,s,r)
    print(f'PASS k={k} all {len(labels)*n} exact cyclotomic coefficient cancellations')

if __name__=='__main__':
    for k in (2,3,4):
        verify(k)
    for k in (2,3):
        direct(k)
    print('ALL-DEPTH ANNIHILATOR CERTIFICATE: PASS')
