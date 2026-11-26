"""CTA-02 linear symmetry groups of the mod-9 aperture."""
from itertools import product
def automorphisms():
    return tuple(m for m in product(range(9),repeat=4) if (m[0]*m[3]-m[1]*m[2])%3)
def centralizer():
    return tuple(m for m in automorphisms() if m[1]==m[2] and m[3]==(m[0]+m[1])%9)
def stabilizer():
    return tuple(m for m in automorphisms() if m[:2]==(1,0))
def classify(m):
    if m not in automorphisms(): raise ValueError("not invertible")
    return {"evolution":m in centralizer(),"aperture":m in stabilizer()}
def selftest():
    g,c,h=automorphisms(),centralizer(),stabilizer()
    assert (len(g),len(c),len(h))==(3888,72,54)
    assert set(c)&set(h)=={(1,0,0,1)}
    for a,b,c,d in g:
        pairs={(x%7,((a*x+b*y)%9)%7) for x,y in product(range(9),repeat=2)}
        assert (len(pairs)==7)==((a,b)==(1,0))
if __name__=="__main__": selftest()
