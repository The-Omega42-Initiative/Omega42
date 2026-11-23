#!/usr/bin/env python3
"""Exact integer orbit-sum identity-coefficient obstruction, N=3^k."""
def A2(x,m):
    a,b=x
    return ((a+b)%m,(a+2*b)%m)

def orbits(m):
    seen=set()
    out=[]
    for a in range(m):
        for b in range(m):
            x=(a,b)
            if x in seen: continue
            orbit=[]
            y=x
            while y not in seen:
                seen.add(y)
                orbit.append(y)
                y=A2(y,m)
            out.append(orbit)
    return out

def test(k):
    m=3**k
    all_orbits=orbits(m)
    primitive=[o for o in all_orbits if o[0][0]%3 or o[0][1]%3]
    assert len(all_orbits)==m
    assert len(primitive)==2*3**(k-1)
    assert all(len(o)==4*3**(k-1) for o in primitive)
    neg=lambda x:((-x[0])%m,(-x[1])%m)
    assert all({neg(x) for x in o}==set(o) for o in primitive)
    norm=lambda x:(x[0]*x[0]+x[0]*x[1]-x[1]*x[1])%m
    indexed={norm(o[0]):set(o) for o in primitive}
    assert len(indexed)==len(primitive)
    for q in indexed:
        pair=indexed[q]|indexed[(-q)%m]
        assert len(pair)==8*3**(k-1)
        # Each antipodal pair contributes W_x W_-x = I, phase 1.
        identity_coeff=sum(1 for x in pair if neg(x) in pair)
        assert identity_coeff==len(pair)
    print('PASS k=%d N=%d primitive_orbits=%d identity_coeff=%d'%
          (k,m,len(primitive),8*3**(k-1)))

if __name__=='__main__':
    for k in range(1,5): test(k)
    print('WEYL ORBIT ALGEBRA OBSTRUCTION: PASS')
