"""Constitutional Geometry: exact checks of the proposed results (Claude, 26 Nov 2026)."""
from fractions import Fraction as Fr
from collections import Counter
import itertools, math
A=((0,1),(1,1))
def mul(X,Y,m=None):
    R=tuple(tuple(sum(X[i][k]*Y[k][j] for k in range(2)) for j in range(2)) for i in range(2))
    return tuple(tuple(v%m for v in r) for r in R) if m else R
def mpow(X,n,m=None):
    R=((1,0),(0,1))
    for _ in range(n): R=mul(R,X,m)
    return R
def det(X): return X[0][0]*X[1][1]-X[0][1]*X[1][0]
ok=True
# CG-02a: A^2 is Arnold's cat map
cat=((1,1),(1,2)); ok&= mul(A,A)==cat; print('A^2 = [[1,1],[1,2]] (the cat map):', mul(A,A)==cat)
# order of A and of the cat map mod 3^k
def order(X,m):
    n,R=1,X
    while R!=((1,0),(0,1)): R=mul(R,X,m); n+=1
    return n
ords=[(order(A,3**k),order(cat,3**k)) for k in (1,2,3,4)]
print('orders of A and of the cat map mod 3, 9, 27, 81:',ords); ok&= ords==[(8,4),(24,12),(72,36),(216,108)]
# CG-02b: the 81 states are the 9-division points of the torus R^2/Z^2; A acts on them as on (Z/9)^2
# fixed points of A^n on the torus: |det(A^n - I)|; Lucas form |L_n - (-1)^n - 1|
def lucas(n):
    a,b=2,1
    for _ in range(n): a,b=b,a+b
    return a
fix={n:abs(det(tuple(tuple(mpow(A,n)[i][j]-(i==j) for j in range(2)) for i in range(2)))) for n in range(1,25)}
ok&= all(fix[n]==abs(lucas(n)-(-1)**n-1) for n in fix)
print('Fix(A^n) on the torus, n=1..12:',[fix[n] for n in range(1,13)],' n=24:',fix[24])
# the 9-division points are all fixed by A^24, and they form a subgroup of index 1280
ok&= fix[24]==103680 and fix[24]%81==0 and fix[24]//81==1280
print('81 states inside Fix(A^24): index', fix[24]//81)
# exact: a torus point of denominator 9 has period = its orbit length under A mod 9, so periods 1, 8, 24 only
def orbits(m):
    seen=set(); out=[]
    for a in range(m):
        for b in range(m):
            x=(a,b)
            if x in seen: continue
            o=[x]; y=(b,(a+b)%m)
            while y!=x: o.append(y); y=(y[1],(y[0]+y[1])%m)
            seen|=set(o); out.append(o)
    return out
print('periods of the 9-division points:',sorted(Counter(len(o) for o in orbits(9)).items()))
# real-plane geometry: |det| = 1, eigenvalues phi and -1/phi; orientation reversed at odd n
phi=(1+5**.5)/2
ok&= det(A)==-1 and abs(phi*phi-phi-1)<1e-12 and all(det(mpow(A,n))==(-1)**n for n in range(1,10))
# CG-05: the spectrum of the shift U determines the orbit census exactly (permutation dynamics are audible)
def census_from_spectrum(mult):          # mult[d] = number of eigenvalues that are primitive d-th roots of unity
    # number of cycles with length divisible by d equals mult[d]/phi(d); then invert over multiples
    tot=lambda d: sum(1 for k in range(1,d+1) if math.gcd(k,d)==1)
    N=max(mult); div={d:mult.get(d,0)//tot(d) for d in range(1,N+1)}
    c={}
    for d in range(N,0,-1):
        c[d]=div[d]-sum(c[e] for e in range(2*d,N+1,d))
    return {d:v for d,v in c.items() if v}
for k in (1,2,3,4):
    m=3**k; cen=Counter(len(o) for o in orbits(m)); mult=Counter()
    for l,cnt in cen.items():
        for j in range(l): mult[l//math.gcd(j,l)]+=cnt
    rec=census_from_spectrum(dict(mult)); ok&= rec==dict(cen)
    print('depth %d: census %s recovered from the spectrum of U: %s'%(k,dict(sorted(cen.items())),rec==dict(cen)))
# CG-03 in the finite world: projections of the torus point (a/9, b/9) to its coordinates; first coordinate under A^t is the aperture of the Observatory
print('RESULT','PASS' if ok else 'FAIL')
