#!/usr/bin/env python3
"""Proposal-only exact Fibonacci/norm/Fourier adapter; standard library only."""
from collections import Counter


def norm(a, b, m):
    return (a*a + a*b - b*b) % m


def step(a, b, m):
    return b, (a+b) % m


def matrix_power(n, m):
    a, b, c, d = 1, 0, 0, 1
    e, f, g, h = 0, 1, 1, 1
    while n:
        if n & 1:
            a, b, c, d = ((a*e+b*g) % m, (a*f+b*h) % m,
                          (c*e+d*g) % m, (c*f+d*h) % m)
        e, f, g, h = ((e*e+f*g) % m, (e*f+f*h) % m,
                      (g*e+h*g) % m, (g*f+h*h) % m)
        n //= 2
    return a, b, c, d


def ramanujan_3power(r, x):
    """Exact sum of exp(2 pi i ux/3^r) over unit u modulo 3^r."""
    q = 3**r
    if x % q == 0:
        return 2 * 3**(r-1)
    if x % (q//3) == 0:
        return -3**(r-1)
    return 0


def norm_fiber_count(k, residue):
    """Fourier inversion with integer Ramanujan sums, no floating point."""
    if k < 1:
        raise ValueError("k must be >= 1")
    m = 3**k
    x = residue % m
    numerator = m*m + sum(
        3**(2*(k-r)) * (-3)**r * ramanujan_3power(r, x)
        for r in range(1, k+1)
    )
    assert numerator % m == 0
    return numerator // m


def selftest(max_k=4):
    for k in range(1, max_k+1):
        m = 3**k
        histogram = Counter(norm(a, b, m)
                            for a in range(m) for b in range(m))
        assert sum(histogram.values()) == m*m
        for x in range(m):
            assert histogram[x] == norm_fiber_count(k, x)
            if x % 3:
                assert histogram[x] == 4*3**(k-1)
        for a in range(m):
            for b in range(m):
                c, d = step(a, b, m)
                assert norm(c, d, m) == (-norm(a, b, m)) % m
                assert norm(c, d, m)**2 % m == norm(a, b, m)**2 % m
        assert matrix_power(8*3**(k-1), m) == (1, 0, 0, 1)
        print("PASS k=%d states=%d exact residue counts=%d" % (k, m*m, m))
    print("EXACT MATH ADAPTER: PASS")


if __name__ == "__main__":
    selftest()
