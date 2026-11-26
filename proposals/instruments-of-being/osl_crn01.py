"""CRN-01 harmonic Gram networks and exact impulse ranks."""
from osl_crc01 import project, inner
def gram(functions,j,k=2):
    v=[project(f,j,k) for f in functions]
    return [[inner(a,b) for b in v] for a in v]
def impulse_ranks(states,k=2):
    q=3**k; P=8*3**(k-1); orbits={}
    for a,b in states:
        x=(a%q,b%q); o=[x]; y=(x[1],sum(x)%q)
        while y!=x:
            o.append(y); y=(y[1],sum(y)%q)
        orbits[min(o)]=len(o)
    return tuple(sum(j%(P//n)==0 for n in orbits.values()) for j in range(P))
def selftest():
    from osl_csg01 import multiplicities
    assert impulse_ranks([(a,b) for a in range(9) for b in range(9)])==multiplicities()
    assert impulse_ranks([(2,5),(5,7)])==(1,)*24
    assert impulse_ranks([(0,1),(0,2),(0,4)])==(3,)*24
if __name__=="__main__": selftest()
