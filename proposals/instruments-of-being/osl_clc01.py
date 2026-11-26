"""CLC-01 proposed symmetry-aware OmegaSL library."""
from itertools import combinations
from collections import Counter
from osl_cig01 import ROOTS, trace

def translate(phases,s):
    return tuple(sorted({(t+s)%24 for t in phases}))

def orbit(phases):
    phases=tuple(phases)
    return tuple(sorted({translate(phases,s) for s in range(24)}))

def recognize(phases):
    return min(orbit(phases))

def generalize(phases):
    p=recognize(phases)
    counts=Counter(trace(x,p) for x in ROOTS)
    return {"representative":p,"orbit_size":len(orbit(p)),
            "signatures":len(counts),"fiber_sizes":tuple(sorted(counts.values()))}

def learn(k):
    return tuple(generalize(p) for p in combinations(range(24),k) if p==recognize(p))

if __name__=="__main__":
    r=learn(3)
    assert len(r)==85
    assert Counter(x["orbit_size"] for x in r)=={24:84,8:1}
    assert sum(x["signatures"]==81 for x in r)==8
    assert sum(x["orbit_size"] for x in r if x["signatures"]==81)==192
    print("CLC-01 PASS")
