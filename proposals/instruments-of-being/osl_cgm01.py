"""CGM-01 subset census using CCR-01 reachability."""
from itertools import combinations
from osl_ccr01 import reach
def census(k=2):
    return [(s,len(p),max(map(len,p.values()))) for n in range(1,5) for c in combinations("AVCS",n) for s in ["".join(c)] for p in [reach(k=k,operations=s)]]
def selftest():
    rows=census()
    assert {s for s,n,d in rows if n==81}=={"AVC","ACS","AVCS"}
    assert {s:d for s,n,d in rows if n==81}=={"AVC":16,"ACS":10,"AVCS":6}
if __name__=="__main__": selftest()
