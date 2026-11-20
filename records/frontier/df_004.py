"""DF-004 (Discovery Bulletin): the four operations on the Antipodes.

The Antipode of a digit x is 9 - x, so the pair adds to 9 (0 modulo 9). Apply the other three operations (difference,
ratio, product) to every pair, over the integers and modulo 9, and connect the digit rule to the law T(a, b) = (b, a + b).
Computed while exploring; not a registered STP test. Every statement printed is asserted.
"""
from fractions import Fraction as Fr

N = 9


def T(s):
    return (s[1], (s[0] + s[1]) % N)


def power(s, k):
    for _ in range(k):
        s = T(s)
    return s


def inv(x):
    return next((y for y in range(N) if (x * y) % N == 1), None)


if __name__ == '__main__':
    # 1. Integers: the table and the exact identity linking product and difference.
    print('integer pairs (x, 9 - x): sum, difference, ratio, product')
    for x in range(1, 5):
        a = 9 - x
        print('  (%d, %d): %d, %d, %s, %d' % (x, a, x + a, x - a, Fr(x, a), x * a))
    for x in range(0, 10):
        assert Fr(x * (9 - x)) == Fr(81, 4) - Fr((x - (9 - x)) ** 2, 4)
    print('identity x(9 - x) = 81/4 - (x - (9 - x))^2 / 4 holds for x = 0..9; integer maximum 20 at (4, 5); no integer x has x = 9 - x')

    # 2. Modulo 9: the Antipode is negation.
    half, quarter = inv(2), inv(4)
    assert half == 5 and (-half) % N == 4
    print('modulo 9: A(x) = -x; 0 is its own Antipode (9 = 0); 1/2 = %d and -1/2 = %d, so the central pair (4, 5) is (-1/2, +1/2)' % (half, (-half) % N))
    assert (5 - 4) % N == 1
    print('  difference x - A(x) = 2x: one-to-one, since 2 is a unit; the difference 1 belongs to x = 5 = 1/2 alone')
    assert sorted(x for x in range(N) if (2 * x) % N == 1) == [5]
    units = [x for x in range(N) if inv(x)]
    for x in units:
        assert (x * inv((-x) % N)) % N == N - 1
    print('  ratio x / A(x) = -1 = 8 for every unit x %s; undefined for 0, 3, 6' % units)
    prods = [(x * ((-x) % N)) % N for x in range(N)]
    assert prods == [(-x * x) % N for x in range(N)]
    assert prods[5] == (-quarter) % N == 2
    print('  product x A(x) = -x^2:', prods, '; at the central pair it is -1/4 = 2, the residue of the integer 20')

    # 3. The digit rule is the half-turn of the loop.
    states = [(a, b) for a in range(N) for b in range(N)]
    assert all(power(s, 12) == ((-s[0]) % N, (-s[1]) % N) for s in states)
    print('the law: T^12 = -I modulo 9, so the Antipode of every state is the state 12 steps ahead')

    def period(s):
        k, x = 1, T(s)
        while x != s:
            x, k = T(x), k + 1
        return k
    for s in states:
        if s != (0, 0):
            p = period(s)
            assert p % 2 == 0 and power(s, p // 2) == ((-s[0]) % N, (-s[1]) % N) != s
    print('  every nonzero state has a distinct Antipode at exactly half its period: 12 of 24, 4 of 8; (0, 0) is its own')
    seq, x = [], (0, 1)
    for _ in range(24):
        seq.append(x[0]); x = T(x)
    assert all((seq[i] + seq[i + 12]) % N == 0 for i in range(12))
    print('  on the canonical loop', seq, 'each digit and the digit 12 places on add to 9 or to 0')
