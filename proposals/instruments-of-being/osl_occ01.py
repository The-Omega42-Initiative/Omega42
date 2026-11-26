"""OCC-01 bounded typed command interpreter; proposal, not canonical grammar."""
from itertools import combinations
from osl_cig01 import ROOTS, PAIRS, trace, blindspot, reconstruct

MASKS=tuple(blindspot((t,)) for t in range(24))
def plan():
    for k in range(1,25):
        for p in combinations(range(24),k):
            if not set.intersection(*(set(MASKS[t]) for t in p)):
                return p
    raise RuntimeError("unobservable")

def execute(program):
    phases=()
    remaining=frozenset(PAIRS)
    log=[]
    for line in program.splitlines():
        words=line.split()
        if not words: continue
        if words==["PLAN"]:
            phases=plan()
            remaining=blindspot(phases)
        elif words==["ATTEND"]:
            if remaining:
                t=min(range(24),key=lambda t:(len(remaining & MASKS[t]),t))
                phases=phases+(t,)
                remaining=remaining & MASKS[t]
        elif words==["VERIFY"]:
            if remaining: raise ValueError("unresolved distinctions")
        elif words==["RESET"]:
            phases=()
            remaining=frozenset(PAIRS)
        else: raise ValueError("unknown command: "+line)
        log.append({"operation":words[0],"phases":phases,"unresolved":len(remaining)})
    return log

def selftest():
    assert plan()==(0,2,5)
    assert execute("ATTEND\n"*4+"VERIFY")[-1]["phases"]==(0,1,4,5)
    assert execute("PLAN\nVERIFY")[-1]["unresolved"]==0
    for bad in ("VERIFY","UNKNOWN","PLAN extra"):
        try: execute(bad)
        except ValueError: pass
        else: raise AssertionError(bad)
    print("OCC-01 PASS")

if __name__=="__main__": selftest()
