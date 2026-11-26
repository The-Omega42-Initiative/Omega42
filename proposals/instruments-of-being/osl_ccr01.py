"""CCR-01 native transformation reachability (state impulses)."""
from collections import deque
def reach(seed=(2,5),k=2,operations="AVCS"):
    q=3**k
    ops={"A":lambda a,b:(b,(a+b)%q),"V":lambda a,b:(2*a%q,2*b%q),"C":lambda a,b:(3*a%q,3*b%q),"S":lambda a,b:(a,(3*a+b)%q)}
    seed=tuple(x%q for x in seed)
    paths={seed:""}; queue=deque([seed])
    while queue:
        x=queue.popleft()
        for name in operations:
            y=ops[name](*x)
            if y not in paths:
                paths[y]=paths[x]+name; queue.append(y)
    return paths
def selftest():
    assert len(reach(operations="A"))==24
    assert len(reach())==81
    assert reach()[(0,0)]=="CC"
if __name__=="__main__": selftest()
