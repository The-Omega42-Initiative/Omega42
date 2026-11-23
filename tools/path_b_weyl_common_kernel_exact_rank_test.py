#!/usr/bin/env python3
"""Exact F_p rank certificates for common Weyl norm-square kernels N=9,27,81."""
from itertools import product

def verify(k,p,expected_root):
    n=3**k
    inv2=pow(2,-1,n)
    Q=lambda a,b:(a*a+a*b-b*b)%n
    root=next(x for x in range(2,p)
              if pow(x,n,p)==1 and pow(x,n//3,p)!=1)
    assert root==expected_root,(n,root)
    labels=sorted({Q(a,b)**2%n for a,b in product(range(n),repeat=2)
                   if a%3 or b%3})
    assert len(labels)==n//3
    piv={}
    for s in labels:
        M=[[0]*n for _ in range(n)]
        for a,b in product(range(n),repeat=2):
            if Q(a,b)**2%n!=s:continue
            for j in range(n):
                i=(j+b)%n
                M[i][j]=(M[i][j]+pow(root,(a*i-inv2*a*b)%n,p))%p
        for row in M:
            v=row[:]
            for col,basis_row in piv.items():
                if v[col]:
                    f=v[col]
                    v=[(x-f*y)%p for x,y in zip(v,basis_row)]
            col=next((i for i,x in enumerate(v) if x),None)
            if col is not None:
                iv=pow(v[col],-1,p)
                piv[col]=[(x*iv)%p for x in v]
    assert len(piv)==n-n//9,(n,len(piv))
    print(f'PASS N={n}, p={p}, zeta={root}, exact rank={len(piv)}, nullity={n//9}')

if __name__=='__main__':
    for args in ((2,19,4),(3,109,3),(4,163,4)):
        verify(*args)
    print('CERTIFIED: dim K_9=1, dim K_27=3, dim K_81=9')
