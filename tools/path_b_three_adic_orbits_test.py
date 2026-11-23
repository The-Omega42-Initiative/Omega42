#!/usr/bin/env python3
"""Independent finite enumeration of the proposal-only 3-adic Fibonacci orbit theorem.

No canonical files, website files, subprocesses, network, or certificate execution.
"""
from collections import Counter


def valuation(x, p, cap):
    if x == 0:
        return cap
    v = 0
    while x % p == 0 and v < cap:
        x //= p
        v += 1
    return v


def observed_orbits(k):
    n = 3 ** k
    unseen = {(a, b) for a in range(n) for b in range(n)}
    counts = Counter()
    while unseen:
        start = min(unseen)
        current = start
        length = 0
        while current in unseen:
            unseen.remove(current)
            length += 1
            a, b = current
            current = (b, (a + b) % n)
        assert current == start, (k, start, current)
        s = min(valuation(start[0], 3, k), valuation(start[1], 3, k))
        counts[(s, length)] += 1
    return counts


def expected_orbits(k):
    expected = Counter({(k, 1): 1})
    for r in range(1, k + 1):
        expected[(k - r, 8 * 3 ** (r - 1))] = 3 ** (r - 1)
    return expected


def main():
    for k in range(1, 5):
        actual = observed_orbits(k)
        expected = expected_orbits(k)
        assert actual == expected, (k, actual, expected)
        assert sum(length * count for (_, length), count in actual.items()) == 3 ** (2 * k)
        assert sum(actual.values()) == (3 ** k + 1) // 2
        print("k=%d states=%d cycles=%d strata=%s PASS" %
              (k, 3 ** (2 * k), sum(actual.values()), sorted(actual.items())))
    print("THREE-ADIC ORBIT ENUMERATION: PASS")


if __name__ == "__main__":
    main()
