#!/usr/bin/env python3
"""Exact integer certificate: complete dual cat-map orbit inventory modulo 3^r.

Run: python tools/path_b_weyl_all_depth_syndrome_orbits_test.py
"""
from collections import Counter

def dual(x, modulus):
    return ((2*x[0]-x[1]) % modulus, (-x[0]+x[1]) % modulus)

def check(r):
    h = 3**r
    seen = set()
    by_length = Counter()
    for a in range(h):
        for b in range(h):
            x = (a,b)
            if x in seen:
                continue
            y=x
            orbit=[]
            while y not in seen:
                seen.add(y)
                orbit.append(y)
                y=dual(y,h)
            assert y==x
            length=len(orbit)
            by_length[length]+=1
            if x==(0,0):
                assert length==1
            else:
                s=0
                while a%3**(s+1)==0 and b%3**(s+1)==0:
                    s+=1
                assert length==4*3**(r-s-1), (r,x,length,s)
    expected=Counter({1:1})
    for t in range(1,r+1):
        expected[4*3**(t-1)]=2*3**(t-1)
    assert by_length==expected, (by_length,expected)
    print('PASS',r,h,sorted(by_length.items()))

if __name__=='__main__':
    for r in range(1,5):
        check(r)
