#!/usr/bin/env python3
"""Numerical matrix cross-check of exact Weyl syndrome-sector transition theorem.

Run: python tools/path_b_weyl_syndrome_transition_grading_test.py
Requires numpy. Algebraic proof is independent of this numerical cross-check.
"""
import numpy as np
from itertools import product

def check(k, r):
    n = 3**k
    h = 3**r
    e = n//h
    zeta = np.exp(2j*np.pi/n)
    omega = np.exp(2j*np.pi/h)
    inv2 = pow(2,-1,n)
    def W(a,b):
        mat = np.zeros((n,n),complex)
        for j in range(n):
            mat[(j+b)%n,j] = zeta**((a*(j+b)-inv2*a*b)%n)
        return mat
    projections = {}
    for u,v in product(range(h),repeat=2):
        P = np.zeros((n,n),complex)
        for s,t in product(range(h),repeat=2):
            P += omega**((-u*s-v*t)%h)*W(e*s,e*t)
        projections[(u,v)] = P/(h*h)
    assert np.linalg.norm(sum(projections.values())-np.eye(n)) < 1e-8
    for a,b in product(range(min(n,7)),repeat=2):
        V = W(a,b)
        for (u,v),P in projections.items():
            target = ((u+b)%h,(v-a)%h)
            assert np.linalg.norm(V@P@V.conj().T-projections[target]) < 1e-8, (k,r,a,b,u,v)
    print(f'PASS N={n}, depth={r}, sectors={h*h}: Weyl transition conjugation')

if __name__=='__main__':
    for k,r in [(2,1),(3,1),(4,1),(4,2)]:
        check(k,r)
