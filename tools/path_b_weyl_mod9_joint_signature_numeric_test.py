#!/usr/bin/env python3
"""Independent numerical signature multiplicities at N=9; NOT an exact certificate."""
import numpy as np
N=9
z=np.exp(2j*np.pi/N)
Q=lambda a,b:(a*a+a*b-b*b)%N
E={s:np.zeros((N,N),dtype=complex) for s in (1,4,7)}
for a in range(N):
    for b in range(N):
        s=Q(a,b)**2%N
        if s not in E:continue
        for j in range(N):
            E[s][(j+b)%N,j]+=z**((a*(j+b)-5*a*b)%N)
for s,M in E.items():
    assert np.max(np.abs(M-M.conj().T))<1e-10
for A in E.values():
    for B in E.values():
        assert np.max(np.abs(A@B-B@A))<1e-9
H=E[1]+np.sqrt(2)*E[4]+np.sqrt(3)*E[7]
values,V=np.linalg.eigh(H)
signatures=[tuple(float(np.vdot(V[:,j],E[s]@V[:,j]).real) for s in E)
            for j in range(N)]
groups=[]
for sig in signatures:
    for group in groups:
        if max(abs(a-b) for a,b in zip(sig,group[0]))<1e-7:
            group.append(sig)
            break
    else:groups.append([sig])
multiplicities=sorted(len(g) for g in groups)
assert multiplicities==[1,2,2,2,2],multiplicities
print('NUMERIC PASS N=9: five signatures, multiplicities',multiplicities)
print('WARNING: multiplicities require exact characteristic-zero certification')
