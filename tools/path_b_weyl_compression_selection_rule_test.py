#!/usr/bin/env python3
"""Exact integer congruence checks for Weyl compression selection rules."""
from itertools import product
def verify(k):
    n=3**k; inv=pow(2,-1,n)
    for r in range(1,k//2+1):
        h=3**r; m=n//(h*h); e=n//h
        # Stabilizer character is trivial exactly for coordinates divisible by h.
        for a,b in product(range(n),repeat=2):
            trivial=(a%h==0 and b%h==0)
            character_trivial=((e*a)%n==0 and (e*b)%n==0)
            assert trivial==character_trivial
        # For surviving coordinates, check Weyl phase and support on all basis states.
        for a,b in product(range(m),repeat=2):
            for t in range(m):
                phase=(h*a*(h*t+h*b)-inv*h*h*a*b)%n
                invm=pow(2,-1,m) if m>1 else 0
                reduced=(a*(t+b)-invm*a*b)%m if m>1 else 0
                assert phase==(n//m)*reduced%n
                support={(h*t+v*e+h*b)%n for v in range(h)}
                target={(h*((t+b)%m)+v*e)%n for v in range(h)}
                assert support==target
        print(f'PASS N={n}, r={r}, M={m}: selection and exact phases')
if __name__=='__main__':
    for k in range(2,6):
        verify(k)
