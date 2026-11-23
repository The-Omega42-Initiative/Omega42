#!/usr/bin/env python3
"""Exact combinatorial verification of Weyl commutant Fourier filtration."""
from fractions import Fraction

def T(x,m):
    a,b=x
    return ((a+b)%m,(a+2*b)%m)

def orbit_census(m):
    seen=set()
    out=[]
    for a in range(m):
        for b in range(m):
            x=(a,b)
            if x in seen:continue
            o=[]
            y=x
            while y not in seen:
                seen.add(y)
                o.append(y)
                y=T(y,m)
            out.append(o)
    return out

def project(f,k,h):
    N=3**(k-1)
    M=3**(h-1)
    d=N//M
    return [sum((f[(t+a*M)%N] for a in range(d)),Fraction(0))/d
            for t in range(N)]

def check(k):
    m=3**k
    orbits=orbit_census(m)
    primitive=[o for o in orbits if any(z%3 for z in o[0])]
    L=4*3**(k-1)
    assert len(orbits)==m
    assert len(primitive)==2*3**(k-1)
    assert all(len(o)==L for o in primitive)
    norm=lambda x:(x[0]**2+x[0]*x[1]-x[1]**2)%m
    bynorm={norm(o[0]):set(o) for o in primitive}
    assert len(bynorm)==len(primitive)
    pairs=[]
    for q in sorted(bynorm):
        if q>m-q:continue
        pair=bynorm[q]|bynorm[m-q]
        assert len(pair)==2*L
        pairs.append(pair)
    assert len(pairs)==3**(k-1)
    assert all(not (pairs[i]&pairs[j])
               for i in range(len(pairs)) for j in range(i+1,len(pairs)))
    # Weyl orthogonality gives Gram N*|pair| for each pair.
    assert all(m*len(pair)==m*2*L for pair in pairs)
    assert (-5)%m==(1%m) if k==1 else (-5)%m!=(1%m)
    N=3**(k-1)
    f=[Fraction((t*t+3*t+7)%11) for t in range(N)]
    p=[None]+[project(f,k,h) for h in range(1,k+1)]
    assert p[k]==f
    assert all(project(p[h+1],k,h)==p[h] for h in range(1,k))
    assert all(len({(t%3**(h-1)) for t in range(N)})==3**(h-1)
               for h in range(1,k+1))
    print(f'PASS k={k} commutant_dim={m} even_dim={N} gram={m*2*L}')

if __name__=='__main__':
    for k in range(1,5):check(k)
    print('WEYL COMMUTANT FOURIER PROJECTIONS: PASS')
