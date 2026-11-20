"""DF-005 (Discovery Bulletin): the nine-point figure and the Omega42 loop.

The traditional nine-point figure (the Enneagram) places 9 at the top and 1 to 8 clockwise. It draws a triangle 3-6-9 and
a six-point path 1-4-2-8-5-7-1, the repeating digits of 1/7. Compare it with the Omega42 law T(a, b) = (b, a + b) mod 9,
with 0 written as 9. Computed while exploring; not a registered STP test. Every statement printed is asserted.
"""
from fractions import Fraction
from math import gcd

TRI = [3, 6, 9]
HEX = [1, 4, 2, 8, 5, 7]


def d(x):  # residue written as a digit 1..9
    return x % 9 or 9


def edges(path, closed=True):
    pts = path + ([path[0]] if closed else [])
    return {frozenset((a, b)) for a, b in zip(pts, pts[1:]) if a != b}


def mirror(k):  # the Antipode, 9 - k; on the figure, the reflection across the vertical axis
    return d(9 - k)


if __name__ == '__main__':
    # 1/7 and the six-point path
    s = str(10 ** 6 // 7).zfill(6)
    assert [int(c) for c in s] == HEX and Fraction(int(s), 10 ** 6 - 1) == Fraction(1, 7)
    print('1/7 = 0.(142857): the six-point path', HEX)
    # the partition
    units = sorted(k for k in range(1, 10) if gcd(k, 9) == 1)
    assert units == sorted(HEX) and sorted(TRI) == [k for k in range(1, 10) if k % 3 == 0]
    print('the six-point path visits exactly the units modulo 9', units, '; the triangle is the 3-layer 3, 6, 9 = 0')
    dbl, x = [], 1
    for _ in range(6):
        dbl.append(x); x = d(2 * x)
    assert sorted(dbl) == units and x == 1
    print('doubling from 1 visits the same six digits in another order:', dbl)
    # the mirror
    fig = edges(TRI) | edges(HEX)
    assert {frozenset(map(mirror, e)) for e in fig} == fig
    print('the Antipode (k -> 9 - k) is the left-right mirror of the figure, and the figure is symmetric under it')
    # the loop
    a, b, loop = 0, 1, []
    for _ in range(24):
        loop.append(d(a)); a, b = b, (a + b) % 9
    assert all(mirror(loop[i]) == loop[i + 12] for i in range(12))
    first, second = edges(loop[:13], False), edges(loop[12:] + loop[:1], False)
    assert {frozenset(map(mirror, e)) for e in first} == second
    print('the loop', loop, ': its second half is the mirror of its first (T^12 = -I), so its chord figure is mirror symmetric too')
    le = edges(loop)
    shared = le & fig
    print('chords of the loop:', len(le), '| lines of the figure:', len(fig), '| shared:', sorted(tuple(sorted(e)) for e in shared))
    assert len(fig) == 9
    lay = [k for k in loop if k % 3 == 0]
    assert [i for i, k in enumerate(loop) if k % 3 == 0] == list(range(0, 24, 4))
    print('the loop touches the triangle', len(lay), 'times in 24 steps: every fourth step, since F(n) is divisible by 3 exactly when 4 divides n')
