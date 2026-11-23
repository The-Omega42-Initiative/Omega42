#!/usr/bin/env python3
"""Exact integer checks of closed-form Weyl stabilizer filtration."""
def check(k):
    n=3**k
    R=k//2
    prev=None
    for r in range(R+1):
        h=3**r
        e=n//h
        assert e*e%n==0
        # Weyl cocycle is identically trivial on the subgroup.
        for a in range(h):
            for b in range(h):
                assert (e*e*a*b)%n==0
        supports=[frozenset((h*t+v*e)%n for v in range(h))
                  for t in range(n//(h*h))]
        assert len(set(supports))==n//(h*h)
        assert all(len(s)==h for s in supports)
        assert all(all(j%h==0 for j in s) for s in supports)
        if prev is not None:
            # Each finer uniform vector is a union of exactly 3 coarser orbits.
            for s in supports:
                blocks=[v for v in prev if v.issubset(s)]
                assert len(blocks)==3
                assert set().union(*blocks)==set(s)
        prev=supports
    print(f'PASS k={k}, N={n}: all subgroup ranks, cocycles, and nesting')

if __name__=='__main__':
    for k in range(2,9):
        check(k)
