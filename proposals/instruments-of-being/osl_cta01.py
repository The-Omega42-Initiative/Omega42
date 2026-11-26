"""CTA-01 proposed typed equivalence diagnostics."""
from collections import Counter
from itertools import combinations
from osl_cig01 import ROOTS, trace

def reflect(p): return tuple(sorted({(-t)%24 for t in p}))
def profile(p): return tuple(sorted(Counter(trace(x,p) for x in ROOTS).values()))
def compare(p,q):
    a,b=profile(p),profile(q)
    return {"profile_equivalent":a==b,"reconstruction_equivalent":(len(a)==81)==(len(b)==81)}
def aperture_preserving(u):
    return all((a%7==b%7)==((u*a%9)%7==(u*b%9)%7) for a in range(9) for b in range(9))
def selftest():
    r=[compare(p,reflect(p)) for p in combinations(range(24),3)]
    assert sum(not x["profile_equivalent"] for x in r)==480
    assert all(x["reconstruction_equivalent"] for x in r)
    assert [u for u in (1,2,4,5,7,8) if aperture_preserving(u)]==[1]
    print("CTA-01 PASS")
if __name__=="__main__": selftest()
