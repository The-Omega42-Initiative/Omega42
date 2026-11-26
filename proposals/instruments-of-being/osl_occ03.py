"""OCC-03 resource-aware OmegaSL proposal. Uniform prior; positive query costs."""
from fractions import Fraction
from functools import lru_cache
from osl_cig01 import ROOTS, observe

def valuate(phases, costs=None):
    phases=tuple(sorted(set(phases)))
    if any(type(t) is not int or not 0<=t<24 for t in phases):
        raise ValueError("invalid phase")
    costs={t:Fraction(1 if costs is None else costs[t]) for t in phases}
    if any(c<=0 for c in costs.values()): raise ValueError("positive costs required")
    @lru_cache(None)
    def anticipate(S):
        if len(S)<=1: return Fraction(0),None
        best=None
        for t in phases:
            groups={}
            for x in S: groups.setdefault(observe(x,t),[]).append(x)
            if len(groups)==1: continue
            branches=[(len(g),anticipate(tuple(g))) for g in groups.values()]
            if any(r[0] is None for _,r in branches): continue
            cost=costs[t]+sum(Fraction(n,len(S))*r[0] for n,r in branches)
            if best is None or (cost,t)<best: best=(cost,t)
        return best if best is not None else (None,None)
    signatures=len({tuple(observe(x,t) for t in phases) for x in ROOTS})
    return {"phases":phases,"signatures":signatures,"decision":anticipate(ROOTS)}

if __name__=="__main__":
    expected={1:81,2:81,3:81,4:26,6:64,8:25,12:8}
    for d,n in expected.items():
        r=valuate(range(0,24,d))
        assert r["signatures"]==n
        assert r["decision"][0]==(Fraction(218,81) if n==81 else None)
    print("OCC-03 PASS")
