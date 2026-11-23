#!/usr/bin/env python3
"""Exact integer checks for the iterated Weyl isometric filtration."""
def verify(k):
    n=3**k
    R=k//2
    for r in range(1,R+1):
        m=3**(k-2*r)
        # Iterated isometry maps |t> to uniform sum of 3^r states
        # |3^r*t + h*3^(k-r)> for h=0,...,3^r-1.
        step=3**(k-r)
        support=lambda t:{(3**r*t+h*step)%n for h in range(3**r)}
        assert len(support(0))==3**r
        assert all(len(support(t))==3**r for t in range(m))
        assert len(set().union(*(support(t) for t in range(m))))==m*3**r
        # Nestedness: the finer-level support is a union of three
        # supports at the previous filtration level.
        if r>1:
            for t in range(m):
                prior=3**(k-2*(r-1))
                union=set().union(*( {(3**(r-1)*((3*t+h*3**(k-2*r+1))%prior)+v*3**(k-r+1))%n
                                      for v in range(3**(r-1))}
                                    for h in range(3)))
                assert union==support(t),(k,r,t)
    ranks=[3**(k-2*r)-3**(k-2*r-2) for r in range(R)]
    ranks.append(3**(k-2*R))
    assert sum(ranks)==n
    print(f'PASS N={n}: layer ranks={ranks}, sum={n}')

if __name__=='__main__':
    for k in range(2,9):
        verify(k)
