#!/usr/bin/env python3
"""Check exact cyclic centralizer action on depth-r shear orbit labels."""


def Q(a,b,m):
    return (a*a+a*b-b*b)%m


def C(a,b,m):
    return (a+3*b)%m,(3*a+4*b)%m


def label(a,b,k,r):
    m=3**k
    j=0
    while j<k and a%3**(j+1)==0 and b%3**(j+1)==0:
        j+=1
    if j==k:
        return ("zero",)
    h=min(r,k-j)
    d=3**j
    return (j, Q(a//d,b//d,3**h)**2 % 3**h)


def check(k):
    m=3**k
    for j in range(k):
        n=k-j
        orbit_reps=[]
        x=(3**j,0)
        for t in range(3**(n-1)):
            orbit_reps.append(x)
            x=C(*x,m)
        assert x==(3**j,0), (k,j,x)
        for r in range(1,k+1):
            h=min(r,n)
            classes={}
            for t,x in enumerate(orbit_reps):
                key=label(*x,k,r)
                classes.setdefault(key,[]).append(t)
                assert label(*C(*x,m),k,r)==(j,25*key[1] % 3**h)
            assert len(classes)==3**(h-1)
            assert all(len(indices)==3**(n-h) for indices in classes.values())
            assert all(len({t%3**(h-1) for t in indices})==1
                       for indices in classes.values())
            print("PASS k=%d j=%d r=%d classes=%d" %
                  (k,j,r,len(classes)))


if __name__=="__main__":
    for k in range(1,6):
        check(k)
    print("CENTRALIZER SHEAR PARTITION: PASS")
