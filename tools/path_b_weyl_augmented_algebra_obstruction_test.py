#!/usr/bin/env python3
"""Exact cyclotomic verification of the all-depth augmented Weyl obstruction."""
from collections import Counter


def verify(k):
    N = 3**k
    t = 3**(k-1)
    inv2 = pow(2, -1, N)
    Q = lambda a, b: (a*a + a*b - b*b) % N
    S = {(a, b) for a in range(N) for b in range(N)
         if Q(a, b)**2 % N == 1}
    assert len(S) == 8*3**(k-1)
    phases = Counter()
    for a, b in S:
        y = ((t-a) % N, (-b) % N)
        if y in S:
            phases[(-inv2*b) % 3] += 1
    assert phases[0] == 0
    assert phases[1] == phases[2] == 3**(k-1), (k, phases)
    # omega+omega**2 = -1, so the coefficient is exactly -3**(k-1).
    print('PASS k=%d N=%d coeff=%d' % (k, N, -3**(k-1)))


if __name__ == '__main__':
    for k in (2, 3, 4):
        verify(k)
    print('WEYL AUGMENTED ALGEBRA OBSTRUCTION: PASS')
