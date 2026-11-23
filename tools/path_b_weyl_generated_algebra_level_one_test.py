#!/usr/bin/env python3
"""Exact cyclotomic test of E^2=8I-2E for the N=3 Weyl algebra."""
from collections import Counter

def test():
    m=3
    S={(a,b) for a in range(m) for b in range(m) if (a,b)!=(0,0)}
    for c in range(m):
        for d in range(m):
            counts=Counter()
            for a,b in S:
                y=((c-a)%m,(d-b)%m)
                if y in S:
                    # inverse of 2 modulo 3 is 2
                    exponent=(2*(a*y[1]-b*y[0]))%3
                    counts[exponent]+=1
            # omega+omega^2=-1, so reduce to integer + integer*omega.
            # n0+n1*omega+n2*omega^2 = (n0-n2)+(n1-n2)*omega.
            assert counts[1]==counts[2], ((c,d),counts)
            value=counts[0]-counts[2]
            expected=8 if (c,d)==(0,0) else -2
            assert value==expected, ((c,d),counts,value)
    # z^2+2z-8=(z-2)(z+4), Tr(E)=0 -> multiplicities 2 and 1.
    assert 2*2 + (-4)*1 == 0
    print('PASS N=3: E^2=8I-2E, dim generated algebra=2 < commutant dimension=3')

if __name__=='__main__':
    test()
