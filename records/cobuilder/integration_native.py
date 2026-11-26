"""ChatGPT (Co-Builder), Rev451 candidate: exact native integration certificates (observation, reconstruction, adaptive decisions, generation, spectral multiplicities). Run: python3 records/cobuilder/integration_native.py"""
"""Rev451 candidate: exact native certificates; no canonical opcode changes."""
from itertools import combinations
from collections import deque, Counter
from functools import lru_cache

X=tuple((a,b) for a in range(9) for b in range(9))
def trace(x):
    a,b=x
    out=[]
    for _ in range(24):
        out.append(a%7)
        a,b=b,(a+b)%9
    return tuple(out)
H=tuple(map(trace,X))
def profile(phases):
    return Counter(tuple(row[t] for t in phases) for row in H)
def reconstruct(phases,values):
    if len(phases)!=len(values) or any(not isinstance(t,int) or not 0<=t<24 for t in phases) or any(not isinstance(v,int) or not 0<=v<7 for v in values):
        raise ValueError("invalid observation")
    return [x for x,row in zip(X,H) if all(row[t]==v for t,v in zip(phases,values))]
def reach(ops,k=2):
    if not 1<=k<=5 or not set(ops)<=set("AVCS"): raise ValueError("unsupported depth or operator")
    q=3**k
    seed=(2%q,5%q)
    dist={seed:0}; todo=deque([seed])
    while todo:
        a,b=todo.popleft()
        for op in ops:
            y={"A":(b,(a+b)%q),"V":(2*a%q,2*b%q),"C":(3*a%q,3*b%q),"S":(a,(3*a+b)%q)}[op]
            if y not in dist:
                dist[y]=dist[a,b]+1;todo.append(y)
    return len(dist),max(dist.values())
def multiplicities(k):
    if not 1<=k<=5: raise ValueError("unsupported depth")
    return [int(j==0)+sum(3**(m-1) for m in range(1,k+1) if j%3**(k-m)==0) for j in range(8*3**(k-1))]
@lru_cache(None)
def decision_cost(S):
    if len(S)<=1:return 0
    costs=[]
    for t in range(24):
        groups={}
        for i in S:groups.setdefault(H[i][t],[]).append(i)
        if len(groups)>1:costs.append(len(S)+sum(decision_cost(tuple(g)) for g in groups.values()))
    return min(costs)
def selftest():
    triples=list(combinations(range(24),3))
    assert sum(len(profile(p))==81 for p in triples)==192
    assert len({min(tuple(sorted((t+s)%24 for t in p)) for s in range(24)) for p in triples})==85
    assert all(reconstruct((0,2,5),tuple(row[t] for t in (0,2,5)))==[x] for x,row in zip(X,H))
    assert decision_cost(tuple(range(81)))==218
    assert [reach(o) for o in ("AVC","ACS","AVCS")]==[(81,16),(81,10),(81,6)]
    assert sum(multiplicities(2))==81 and multiplicities(2)[0]==5
    print("native integration checks passed")
if __name__=="__main__":selftest()
