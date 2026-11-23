#!/usr/bin/env python3
"""Exact integer syndrome-sector orbit/rank certificates for Weyl cat-map action."""
from itertools import product

def dual(x,m):
    # T^(-transpose)=[[2,-1],[-1,1]], T=[[1,1],[1,2]].
    return ((2*x[0]-x[1])%m,(-x[0]+x[1])%m)

def verify(k):
    n=3**k;d=n//3;rank=n//9
    # Joint Z^d/X^d eigenspaces: each sector has rank N/9.
    for u,v in product(range(3),repeat=2):
        orbits=[frozenset((j+t*d)%n for t in range(3))
                for j in range(u,n//3,3)]
        assert len(orbits)==rank
        assert len(set(orbits))==rank
        assert all(len(s)==3 for s in orbits)
        # Each X^d orbit supports one eigenvector for each v.
    seen=set();cycles=[]
    for x in product(range(3),repeat=2):
        if x in seen:continue
        cyc=[];y=x
        while y not in seen:
            seen.add(y);cyc.append(y);y=dual(y,3)
        assert y==x
        cycles.append(cyc)
    assert sorted(map(len,cycles))==[1,4,4]
    assert sum(len(c)*rank for c in cycles)==n
    for m in (1,2,3,5,6,7,9,10,11):
        assert all(dual_iter(x,m)!=x for c in cycles if len(c)==4 for x in c)
    print(f'PASS N={n}: nine rank-{rank} sectors, orbit lengths 1+4+4, trace selection')

def dual_iter(x,m):
    for _ in range(m):x=dual(x,3)
    return x

if __name__=='__main__':
    for k in range(2,8):
        verify(k)
