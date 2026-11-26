"""CRC-01 resonance hierarchy and cyclic alignment."""
from cmath import exp, pi
from math import sqrt
def inner(f,g): return sum(a.conjugate()*b for a,b in zip(f,g))
def project(f,j,k=2):
    q=3**k; P=8*3**(k-1)
    if len(f)!=q*q: raise ValueError("state-space length mismatch")
    w=[exp(-2j*pi*j*t/P)/P for t in range(P)]
    out=[]
    for i in range(q*q):
        a,b=i%q,i//q; z=0j
        for t in range(P):
            z+=w[t]*f[a+q*b]; a,b=b,(a+b)%q
        out.append(z)
    return out
def resonance(f,g,k=2):
    q=3**k; P=8*3**(k-1)
    if len(f)!=q*q or len(g)!=q*q: raise ValueError("length mismatch")
    n=sqrt(inner(f,f).real*inner(g,g).real)
    if not n: raise ValueError("zero function")
    z=[]; B=0.
    for j in range(P):
        a,b=project(f,j,k),project(g,j,k)
        z.append(inner(a,b)/n)
        B+=sqrt(inner(a,a).real*inner(b,b).real)/n
    lags=[abs(sum(v*exp(2j*pi*j*t/P) for j,v in enumerate(z))) for t in range(P)]
    return {"S":abs(inner(f,g))/n,"Q":sum(map(abs,z)),"B":B,"lags":lags}
def selftest():
    f=[0]*81; f[2+9*5]=1
    g=[0]*81; g[5+9*7]=1
    h=[0]*81; h[1]=1
    a=resonance(f,g); b=resonance(f,h)
    assert abs(a["B"]-1)<1e-10 and abs(a["Q"]-1)<1e-10
    assert a["S"]==0 and abs(max(a["lags"])-1)<1e-10
    assert abs(b["B"]-1)<1e-10 and b["Q"]<1e-10
if __name__=="__main__": selftest()
