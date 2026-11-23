#!/usr/bin/env python3
"""Independent exact test of commuting Fibonacci-orbit rotation."""
def q(a,b,m):
    return (a*a+a*b-b*b)%m

def A(x,m):
    a,b=x
    return (b,(a+b)%m)

def C(x,m):
    a,b=x
    return ((a+3*b)%m,(3*a+4*b)%m)

def orbit_label(x,m):
    return q(*x,m)**2 % m

def test(k):
    m=3**k
    assert (25*pow(25,3**(k-1)-1,m))%m==1
    labels=set()
    x=(1,0)
    for _ in range(3**(k-1)):
        labels.add(orbit_label(x,m))
        assert A(C(x,m),m)==C(A(x,m),m)
        assert q(*C(x,m),m)==(-5*q(*x,m))%m
        x=C(x,m)
    assert len(labels)==3**(k-1)
    assert orbit_label(x,m)==1
    assert labels=={(u*u)%m for u in range(m) if u%3}
    for j in range(k):
        n=k-j
        seed=(3**j,0)
        y=seed
        shell_labels=set()
        for _ in range(3**(n-1)):
            d=3**j
            shell_labels.add(orbit_label((y[0]//d,y[1]//d),3**n))
            y=C(y,m)
        assert len(shell_labels)==3**(n-1)
        assert orbit_label((y[0]//d,y[1]//d),3**n)==1
    print(f'PASS k={k} primitive_orbits={len(labels)}')

if __name__=='__main__':
    for k in range(1,6): test(k)
    print('CENTRALIZER ORBIT ROTATION: PASS')
