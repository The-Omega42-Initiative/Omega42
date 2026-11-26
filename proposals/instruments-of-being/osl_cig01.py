"""Proposed OmegaSL cognitive library CIG-01. Not a Tier 1 opcode change."""
from itertools import combinations
from collections import Counter

ROOTS=tuple((a,b) for a in range(9) for b in range(9))
PAIRS=tuple(combinations(ROOTS,2))

def observe(x,t):
    a,b=x
    for _ in range(t%24):
        a,b=b,(a+b)%9
    return a%7

def trace(x,phases):
    return tuple(observe(x,t) for t in phases)

def reconstruct(phases,signature):
    phases,signature=tuple(phases),tuple(signature)
    if len(phases)!=len(signature): raise ValueError("length mismatch")
    return tuple(x for x in ROOTS if trace(x,phases)==signature)

def blindspot(phases):
    phases=tuple(phases)
    return frozenset((x,y) for x,y in PAIRS if trace(x,phases)==trace(y,phases))

def refine(a,b):
    return a & b

def distinguish(phases):
    return len(PAIRS)-len(blindspot(phases))

def attend(phases):
    phases=tuple(phases)
    return min(range(24),key=lambda t:(len(blindspot(phases+(t,))),t))

def selftest():
    masks=[blindspot((t,)) for t in range(24)]
    expected=[44 if t%4 else {4:90,8:99,12:405,16:99,20:90}[t] for t in range(1,24)]
    assert [len(refine(masks[0],masks[t])) for t in range(1,24)]==expected
    assert sum(not (masks[a]&masks[b]&masks[c]) for a,b,c in combinations(range(24),3))==192
    assert not blindspot((0,2,5))
    assert all(reconstruct((0,2,5),trace(x,(0,2,5)))==(x,) for x in ROOTS)
    assert len(blindspot(()))==3240
    print("CIG-01 checks PASS")

if __name__=="__main__": selftest()
