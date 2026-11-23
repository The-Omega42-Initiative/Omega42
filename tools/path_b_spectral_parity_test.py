#!/usr/bin/env python3
"""Exact finite parity and shear-character index checks; no floating point."""
def check(n):
    modulus=3**n
    U=[u for u in range(modulus) if u%3]
    N=3**(n-1)
    assert len(U)==2*N
    squares={u*u%modulus for u in U}
    assert len(squares)==N
    assert all(sum(v*v%modulus==s for v in U)==2 for s in squares)
    # Find a generator of U and explicitly test every Fourier index.
    g=next(g for g in U if len({pow(g,t,modulus) for t in range(2*N)})==2*N)
    assert pow(g,N,modulus)==modulus-1
    for h in range(1,n+1):
        M=3**(h-1)
        reduction={s%3**h for s in squares}
        assert len(reduction)==M
        surviving=[m for m in range(2*N) if m%(2*3**(n-h))==0]
        assert len(surviving)==M
        # Character m is trivial on kernel of q -> q^2 mod 3^h
        kernel_exponents=[t for t in range(2*N)
                          if pow(g,2*t,3**h)==1]
        assert len(kernel_exponents)==2*3**(n-h)
        for m in range(2*N):
            trivial=all((m*t)%(2*N)==0 for t in kernel_exponents)
            assert trivial==(m in surviving), (n,h,m)
        if h<n:
            next_surviving=[m for m in range(2*N)
                            if m%(2*3**(n-h-1))==0]
            assert len(set(next_surviving)-set(surviving))==2*M
    print(f'PASS n={n} unit_labels={2*N} square_labels={N}')

if __name__=='__main__':
    for n in range(1,6):check(n)
    print('SPECTRAL PARITY: PASS')
