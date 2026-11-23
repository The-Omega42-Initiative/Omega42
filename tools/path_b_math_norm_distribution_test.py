#!/usr/bin/env python3
"""Independent finite checks of 3-adic norm/shell distribution; no execution of certificates."""
from collections import Counter


def v3_pair(a, b, k):
    j = 0
    while j < k and a % (3 ** (j + 1)) == b % (3 ** (j + 1)) == 0:
        j += 1
    return j


def test_level(k):
    m = 3 ** k
    fibers = Counter()
    shells = Counter()
    reduced_norms = {}
    for a in range(m):
        for b in range(m):
            n = (a*a + a*b - b*b) % m
            fibers[n] += 1
            j = v3_pair(a, b, k)
            shells[j] += 1
            if j < k:
                d = 3 ** j
                q = 3 ** (k-j)
                u = ((a//d)**2 + (a//d)*(b//d) - (b//d)**2) % q
                reduced_norms.setdefault(j, Counter())[u] += 1
    assert shells[k] == 1
    assert sum(shells.values()) == m*m
    for u in range(m):
        if u % 3:
            assert fibers[u] == 4 * 3 ** (k-1), (k, u, fibers[u])
    for j in range(k):
        q = 3 ** (k-j)
        assert shells[j] == 8 * 3 ** (2*(k-j-1))
        c = reduced_norms[j]
        assert len(c) == 2 * 3 ** (k-j-1)
        assert all(u % 3 and count == 4 * 3 ** (k-j-1) for u, count in c.items())
        square_counts = Counter()
        for u, count in c.items():
            square_counts[(u*u) % q] += count
        assert len(square_counts) == 3 ** (k-j-1)
        assert set(square_counts.values()) == {8 * 3 ** (k-j-1)}
    return k, m*m


if __name__ == "__main__":
    for k in range(1, 5):
        level, count = test_level(k)
        print("PASS k=%d states=%d" % (level, count))
