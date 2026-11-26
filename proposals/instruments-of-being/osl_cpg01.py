"""CPG-01 projective directions over Z/3^k."""
def project(a,b,k=2):
    if type(k) is not int or k<1: raise ValueError("invalid depth")
    q=3**k; a%=q; b%=q
    if a%3: return (1,b*pow(a,-1,q)%q)
    if b%3: return (a*pow(b,-1,q)%q,1)
    raise ValueError("nonprimitive vector")
def directions(k=2):
    q=3**k
    return tuple((1,b) for b in range(q))+tuple((a,1) for a in range(0,q,3))
def orbit(k=2):
    p=(1,0); result=[]
    while p not in result:
        result.append(p); p=project(p[1],sum(p),k)
    return tuple(result)
def selftest():
    for k in range(1,7):
        o=orbit(k)
        assert len(o)==4*3**(k-1)
        assert set(o)==set(directions(k))
if __name__=="__main__": selftest()
