#!/usr/bin/env python3
"""Pure independent enumeration of quadratic norm Gauss sums, k=1..4."""
import cmath
from collections import Counter


def v3(n):
    v = 0
    while n % 3 == 0:
        n //= 3
        v += 1
    return v


def test_level(k):
    modulus = 3 ** k
    histogram = Counter(
        (a*a + a*b - b*b) % modulus
        for a in range(modulus)
        for b in range(modulus)
    )
    assert sum(histogram.values()) == modulus * modulus
    frequencies = {0, 1, 2}
    for v in range(1, k):
        frequencies.update({3 ** v, 2 * 3 ** v})
    for t in sorted(frequencies):
        if t >= modulus:
            continue
        observed = sum(
            count * cmath.exp(2j * cmath.pi * t * residue / modulus)
            for residue, count in histogram.items()
        )
        expected = modulus ** 2 if t == 0 else 3 ** (2 * v3(t)) * (-3) ** (k - v3(t))
        assert abs(observed - expected) < 1e-7, (k, t, observed, expected)
    print("PASS k=%d modulus=%d states=%d" % (k, modulus, modulus**2))


if __name__ == "__main__":
    for k in range(1, 5):
        test_level(k)
    print("NORM GAUSS SUMS: PASS")
