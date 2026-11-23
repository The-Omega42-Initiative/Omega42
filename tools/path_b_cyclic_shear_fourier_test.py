#!/usr/bin/env python3
"""Exact rational and cyclotomic tests of ternary Fourier shear filtration."""
from fractions import Fraction
from math import gcd


def project(f, n, h):
    N = 3 ** (n - 1)
    M = 3 ** (h - 1)
    d = N // M
    return [sum((f[(t + a * M) % N] for a in range(d)), Fraction(0)) / d
            for t in range(N)]


def dot(f, g):
    return sum((x * y for x, y in zip(f, g)), Fraction(0)) / len(f)


def verify(n):
    N = 3 ** (n - 1)
    f = [Fraction((t * t + 7 * t + 11) % 17 - 8) for t in range(N)]
    ps = [None] + [project(f, n, h) for h in range(1, n + 1)]
    assert ps[n] == f
    assert len(set(ps[1])) == 1
    assert all(project(ps[h + 1], n, h) == ps[h] for h in range(1, n))
    assert all(project(ps[h], n, h) == ps[h] for h in range(1, n + 1))
    bands = [[ps[h + 1][t] - ps[h][t] for t in range(N)] for h in range(1, n)]
    terms = [ps[1]] + bands
    assert all(sum((v[t] for v in terms), Fraction(0)) == f[t] for t in range(N))
    assert all(dot(terms[i], terms[j]) == 0 for i in range(len(terms))
               for j in range(i + 1, len(terms)))
    assert sum((dot(v, v) for v in terms), Fraction(0)) == dot(f, f)
    for h in range(1, n + 1):
        M = 3 ** (h - 1)
        d = N // M
        # Exact cyclotomic character sum by exponent multiplicities.
        for ell in range(N):
            residues = [(ell * a) % d for a in range(d)]
            if ell % d == 0:
                assert residues == [0] * d
            else:
                g = gcd(ell, d)
                assert sorted(residues) == sorted(
                    [v for v in range(0, d, g) for _ in range(g)])
        assert len([ell for ell in range(N) if ell % d == 0]) == M
        if h < n:
            d2 = d // 3
            assert len([ell for ell in range(N)
                        if ell % d2 == 0 and ell % d != 0]) == 2 * M
    print('PASS n=%d N=%d bands=%s' %
          (n, N, [2 * 3**(h - 1) for h in range(1, n)]))


if __name__ == '__main__':
    for n in range(1, 6):
        verify(n)
    print('FOURIER SHEAR FILTRATION: PASS')
