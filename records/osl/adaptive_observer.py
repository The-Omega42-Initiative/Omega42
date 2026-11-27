"""Greedy minimax adaptive observer with native phases of a mod 7 at depth k.
usage: python3 adaptive.py k [max_candidate_phases] [seed]"""
import numpy as np, sys, time
k=int(sys.argv[1]); q=3**k; n=q*q; N=8*3**(k-1); bound=0
while 7**bound < n: bound+=1
cap=int(sys.argv[2]) if len(sys.argv)>2 else N
rng=np.random.default_rng(int(sys.argv[3]) if len(sys.argv)>3 else 0)
F=[0,1]
for _ in range(N+2): F.append((F[-1]+F[-2])%q)
a=np.repeat(np.arange(q,dtype=np.int64),q); b=np.tile(np.arange(q,dtype=np.int64),q)
def res(t, idx=None):
    p=F[t-1] if t>0 else F[N-1]; r=F[t]
    if idx is None: return ((p*a+r*b)%q%7)
    return ((p*a[idx]+r*b[idx])%q%7)
phases=np.arange(N) if cap>=N else np.sort(rng.choice(N,cap,replace=False))
cls=np.zeros(n,dtype=np.int64); t0=time.time()
for level in range(1,bound+3):
    C=int(cls.max())+1
    sizes=np.bincount(cls,minlength=C)
    if sizes.max()==1: break
    best=np.full(C,n+1,dtype=np.int64); bestp=np.zeros(C,dtype=np.int64)
    for t in phases:
        m=np.bincount(cls*7+res(int(t)),minlength=C*7).reshape(C,7).max(axis=1)
        better=m<best; best[better]=m[better]; bestp[better]=t
    sym=np.empty(n,dtype=np.int64); chosen=bestp[cls]
    for t in np.unique(bestp[sizes>0]):
        idx=np.flatnonzero(chosen==t); sym[idx]=res(int(t),idx)
    key=cls*7+sym; _,cls=np.unique(key,return_inverse=True)
    sz=np.bincount(cls)
    print('level',level,'classes',len(sz),'largest',sz.max(),'unresolved pairs',int((sz*(sz-1)//2).sum()),'s',round(time.time()-t0),flush=True)
sz=np.bincount(cls)
print('k',k,'bound',bound,'readings used',level-1 if sz.max()==1 else 'FAIL','candidates',len(phases),'separated' if sz.max()==1 else 'not separated')
