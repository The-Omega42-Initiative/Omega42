#!/usr/bin/env python3
"""Exact modular checks of the twisted-trace syndrome selection condition."""
from itertools import product

def S(x,h):
    return ((2*x[0]-x[1])%h,(-x[0]+x[1])%h)
def Sinv(x,h):
    return ((x[0]+x[1])%h,(x[0]+2*x[1])%h)
def power(x,m,h):
    for _ in range(abs(m)):
        x=(S if m>=0 else Sinv)(x,h)
    return x
for r in range(1,5):
    h=3**r
    for m in range(-5,6):
        for ell in product(range(h),repeat=2):
            target=power(ell,-m,h)
            delta=((target[0]-ell[0])%h,(target[1]-ell[1])%h)
            a,b=(-delta[1])%h,delta[0]
            destination=power(((ell[0]+b)%h,(ell[1]-a)%h),m,h)
            assert destination==ell
            assert ((b,-a)[0]%h,(b,-a)[1]%h)==delta
    print(f"PASS depth={r}, modulus={h}, labels={h*h}")
