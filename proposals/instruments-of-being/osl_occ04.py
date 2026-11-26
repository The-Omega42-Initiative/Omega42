"""OCC-04 proposed metacognitive repair library."""
from itertools import combinations
from osl_cig01 import ROOTS, trace

def diagnose(phases):
    phases=tuple(sorted(set(phases)))
    if any(type(t) is not int or not 0<=t<24 for t in phases):
        raise ValueError("invalid phase")
    groups={}
    for x in ROOTS: groups.setdefault(trace(x,phases),[]).append(x)
    return {"signatures":len(groups),"unresolved_pairs":sum(len(g)*(len(g)-1)//2 for g in groups.values()),"complete":len(groups)==81}

def revise(phases, available=range(24)):
    phases=tuple(sorted(set(phases)))
    available=tuple(sorted(set(available)))
    diagnose(phases); diagnose(available)
    remaining=tuple(t for t in available if t not in phases)
    for k in range(len(remaining)+1):
        repairs=tuple(q for q in combinations(remaining,k) if diagnose(phases+q)["complete"])
        if repairs: return {"added_count":k,"repairs":repairs}
    return None

if __name__=="__main__":
    for d,n,c in [(4,26,108),(6,64,132),(8,25,108),(12,8,24),(24,7,24)]:
        p=tuple(range(0,24,d))
        assert diagnose(p)["signatures"]==n
        r=revise(p)
        assert r["added_count"]==2 and len(r["repairs"])==c
    assert revise((0,2,5))["added_count"]==0
    assert revise((0,), (0,)) is None
    print("OCC-04 PASS")
