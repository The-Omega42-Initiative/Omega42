#!/usr/bin/env python3
"""Finite Weyl Fourier projector and Newton polynomial checks (NumPy)."""
import numpy as np

def verify(k,r):
    n,h=3**k,3**r
    e=n//h
    zeta=np.exp(2j*np.pi/n)
    omega=np.exp(2j*np.pi/h)
    inv2=pow(2,-1,n)
    def weyl(a,b):
        out=np.zeros((n,n),dtype=complex)
        for j in range(n):
            out[(j+b)%n,j]=zeta**((a*(j+b)-inv2*a*b)%n)
        return out
    stabilizers={(a,b):weyl(e*a,e*b) for a in range(h) for b in range(h)}
    projections={(u,v):sum((omega**((-u*a-v*b)%h)*M for (a,b),M in stabilizers.items()),np.zeros((n,n),complex))/(h*h) for u in range(h) for v in range(h)}
    assert np.linalg.norm(sum(projections.values())-np.eye(n))<1e-8
    for P in projections.values():
        assert np.linalg.norm(P@P-P)<1e-8
        assert abs(np.trace(P)-n/h**2)<1e-8
    U=np.diag(np.exp(2j*np.pi*np.arange(n)**2/n))
    for m in (1,2,3):
        Um=np.linalg.matrix_power(U,m)
        tau={(a,b):np.trace(Um@M) for (a,b),M in stabilizers.items()}
        f={(u,v):np.trace(P@Um) for (u,v),P in projections.items()}
        for u in range(h):
            for v in range(h):
                assert abs(sum(omega**((-u*a-v*b)%h)*val for (a,b),val in tau.items())/(h*h)-f[u,v])<1e-8
        for a in range(h):
            for b in range(h):
                assert abs(sum(omega**((u*a+v*b)%h)*val for (u,v),val in f.items())-tau[a,b])<1e-8
    roots=np.array([2.,-3.,5.])
    coeff=[1.]
    for j in range(1,len(roots)+1):
        coeff.append(sum((-1)**(q-1)*coeff[j-q]*sum(roots**q) for q in range(1,j+1))/j)
    assert np.allclose([(-1)**j*coeff[j] for j in range(len(coeff))],np.poly(roots))
    print(f'PASS N={n}, h={h}: projectors, forward/inverse Fourier, Newton')

if __name__=='__main__':
    for k,r in [(2,1),(3,1),(4,2)]:
        verify(k,r)
