"""OCC-02 proposed adaptive decision library; uniform prior, unit observation cost."""
from fractions import Fraction
from functools import lru_cache
from osl_cig01 import ROOTS, observe

@lru_cache(None)
def decide(S):
    if len(S)<=1: return Fraction(0),0,None
    best=None
    for t in range(24):
        groups={}
        for x in S: groups.setdefault(observe(x,t),[]).append(x)
        if len(groups)==1: continue
        branches=[(len(g),decide(tuple(g))) for g in groups.values()]
        cost=1+sum(Fraction(n,len(S))*r[0] for n,r in branches)
        worst=1+max(r[1] for n,r in branches)
        candidate=(cost,worst,t)
        if best is None or candidate<best: best=candidate
    if best is None: raise ValueError("unobservable candidate set")
    return best

def branch(S,t,j):
    return tuple(x for x in S if observe(x,t)==j)

if __name__=="__main__":
    assert decide(ROOTS)==(Fraction(218,81),3,0)
    print("OCC-02 PASS",decide(ROOTS))
