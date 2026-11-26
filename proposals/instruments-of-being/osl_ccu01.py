"""CCU-01 exact curiosity for orbit-supported impulse candidates."""
def orbit(x,k=2):
    q=3**k; x=tuple(a%q for a in x); o={x}; y=(x[1],sum(x)%q)
    while y!=x:
        o.add(y); y=(y[1],sum(y)%q)
    return o
def explore(k=2,initial=(),candidates=None):
    q=3**k; covered=set()
    for x in initial: covered.update(orbit(x,k))
    pool=list(candidates) if candidates is not None else [(a,b) for a in range(q) for b in range(q)]
    groups={}
    for x in pool:
        o=orbit(x,k); groups.setdefault(min(o),o)
    steps=[]
    while groups:
        x=max(groups,key=lambda x:(len(groups[x]-covered),tuple(-a for a in x)))
        o=groups.pop(x); gain=len(o-covered)
        if not gain: break
        covered.update(o); steps.append((x,gain,q*q-len(covered)))
    return {"steps":steps,"remaining":q*q-len(covered),"complete":len(covered)==q*q}
def selftest():
    assert [s[1] for s in explore()["steps"]]==[24,24,24,8,1]
    assert explore(candidates=[(2,5)])["remaining"]==57
if __name__=="__main__": selftest()
