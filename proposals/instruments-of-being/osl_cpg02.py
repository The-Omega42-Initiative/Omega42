"""CPG-02 reversible valuation/projective/scalar coordinates."""
from osl_cpg01 import project
def decompose(a,b,k=2):
    if type(k) is not int or k<1: raise ValueError("invalid depth")
    q=3**k; a%=q; b%=q
    if not (a or b): return None
    r=0
    while a%3==0 and b%3==0:
        a//=3; b//=3; r+=1
    return r,project(a,b,k-r),a if a%3 else b
def lift(address,k=2):
    if type(k) is not int or k<1: raise ValueError("invalid depth")
    if address is None: return (0,0)
    r,p,u=address
    if type(r) is not int or not 0<=r<k: raise ValueError("invalid valuation")
    q=3**(k-r)
    if not 0<u<q or u%3==0 or tuple(p)!=project(*p,k-r): raise ValueError("invalid address")
    return tuple(3**r*(u*t%q) for t in p)
def evolve(address,k=2):
    if address is None: return None
    r,(a,b),u=address; q=3**(k-r)
    x,y=b,(a+b)%q
    v=x if x%3 else y
    return r,project(x,y,k-r),u*v%q
def selftest():
    for k in range(1,7):
        q=3**k
        for a in range(q):
            for b in range(q):
                z=decompose(a,b,k)
                assert lift(z,k)==(a,b)
                assert lift(evolve(z,k),k)==(b,(a+b)%q)
if __name__=="__main__": selftest()
