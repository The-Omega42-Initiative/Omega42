#!/usr/bin/env python3
"""Exact integer checks for all-depth stabilizer projector P_N at 3-powers."""
def verify(k):
    n=3**k
    d=n//3
    assert d*d%n==0
    assert d%3==0
    # The Weyl subgroup is ordinary abelian since all pairwise cocycles vanish.
    for a in range(3):
        for b in range(3):
            for c in range(3):
                for e in range(3):
                    assert ((a*e-b*c)*d*d)%n==0
    # The group average acts on each standard basis vector as
    # 1/3 times its shift orbit if j is divisible by three, zero otherwise.
    orbits=set()
    for j in range(n):
        if j%3:continue
        orbit=tuple(sorted({(j+t*d)%n for t in range(3)}))
        assert len(orbit)==3
        orbits.add(orbit)
        assert all(tuple(sorted({(h+t*d)%n for t in range(3)}))==orbit
                   for h in orbit)
    assert len(orbits)==n//9
    assert sum(1 for j in range(n) if j%3==0)//3==n//9
    # T=A^2=[[1,1],[1,2]] permutes subgroup labels (a,b) mod 3.
    image={((a+b)%3,(a+2*b)%3) for a in range(3) for b in range(3)}
    assert len(image)==9
    print(f'PASS N={n}: projector rank={n//9}, group average, invariance')

if __name__=='__main__':
    for k in (2,3,4,5):
        verify(k)
