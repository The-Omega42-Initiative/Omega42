#!/usr/bin/env python3
"""Exact integer certificate of N=9 common zero Weyl eigenvector."""
from collections import Counter

def test():
    for s in (1,4,7):
        for r in range(9):
            exponents=Counter()
            for j in (0,3,6):
                b=(r-j)%9
                for a in range(9):
                    q=(a*a+a*b-b*b)%9
                    if q*q%9==s:
                        exponents[(a*r-5*a*b)%9]+=1
            observed=[exponents[e] for e in range(9)]
            expected=([2,0,0]*3 if r%3==0 else [1]*9)
            assert observed==expected,(s,r,observed)
    print('PASS exact integer counts: E_s(|0>+|3>+|6>)=0 for s=1,4,7')

if __name__=='__main__':
    test()
