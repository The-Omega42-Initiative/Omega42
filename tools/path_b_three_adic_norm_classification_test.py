#!/usr/bin/env python3
"""Exhaustive independent test of the proposed quadratic norm orbit classification."""
from collections import defaultdict


def q(a, b, n):
    return (a*a + a*b - b*b) % n


def v3(x, k):
    if x == 0:
        return k
    v = 0
    while x % 3 == 0:
        x //= 3
        v += 1
    return v


def main():
    for k in range(1, 5):
        n = 3**k
        unseen = set((a, b) for a in range(n) for b in range(n))
        classes = defaultdict(list)
        while unseen:
            start = min(unseen)
            orbit = []
            x = start
            while x in unseen:
                unseen.remove(x)
                orbit.append(x)
                a, b = x
                x = (b, (a+b) % n)
            assert x == start
            s = min(v3(start[0], k), v3(start[1], k))
            if s == k:
                assert orbit == [(0, 0)]
                continue
            r = k-s
            m = 3**r
            values = {q(a // (3**s), b // (3**s), m) for a, b in orbit}
            representative = q(start[0] // (3**s), start[1] // (3**s), m)
            sign_class = frozenset((representative, (-representative) % m))
            assert values == sign_class, (k, start, values, sign_class)
            assert len(orbit) == 8 * 3**(r-1)
            classes[r].append(sign_class)
        for r in range(1, k+1):
            actual = classes[r]
            expected = {frozenset((x, (-x) % (3**r)))
                        for x in range(3**r) if x % 3}
            assert len(actual) == len(set(actual)) == 3**(r-1)
            assert set(actual) == expected
        print("k=%d norm-sign classification PASS (%d nonzero cycles)" %
              (k, sum(map(len, classes.values()))))
    print("THREE-ADIC NORM CLASSIFICATION: PASS")


if __name__ == "__main__":
    main()
