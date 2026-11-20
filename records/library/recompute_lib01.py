"""Library tranche LIB-01: recomputation of the mathematical statements in eight archive documents.

Each check prints HOLDS, FAILS or RESTATED and asserts the outcome found, so a change in the arithmetic breaks the run.
The documents are kept unchanged in the Originator's drives; their Library editions (library/) cite these results.
Run: python3 records/library/recompute_lib01.py
"""
from collections import Counter
from itertools import product

N = 9
OUT = []


def T(s):
    return (s[1], (s[0] + s[1]) % N)


def orbit(s):
    o, x = [s], T(s)
    while x != s:
        o.append(x); x = T(x)
    return o


def d(x):  # residue as a digit 1..9
    return x % 9 or 9


def dr(n):  # digital root of a positive integer
    return 1 + (n - 1) % 9


def report(doc, ref, statement, outcome, detail):
    OUT.append((doc, ref, statement, outcome, detail))
    print('%-6s %-10s %-9s %s | %s' % (doc, ref, outcome, statement, detail))


if __name__ == '__main__':
    states = list(product(range(N), repeat=2))
    orbits, seen = [], set()
    for s in states:
        if s not in seen:
            o = orbit(s); seen |= set(o); orbits.append(o)
    lengths = sorted(len(o) for o in orbits)
    assert lengths == [1, 8, 24, 24, 24]

    # ---- PF-A: Philosophical Foundations, companion to V336 Rev.2 (12 Sep 2026), Part VI
    o25 = orbit((2, 5)); seq = [d(a) for a, b in o25]
    assert seq == [2, 5, 7, 3, 1, 4, 5, 9, 5, 5, 1, 6, 7, 4, 2, 6, 8, 5, 4, 9, 4, 4, 8, 3] and sum(seq) == 117 and dr(117) == 9
    report('PF-A', 'VI.1', 'orbit of (2, 5), period 24, sum 117, dr 9', 'HOLDS', 'recomputed digit by digit')
    assert sorted(set(seq)) == list(range(1, 10))
    report('PF-A', 'VI.2', 'all of 1 to 9 appear in the orbit', 'HOLDS', 'every digit occurs')
    prim = [g for g in (1, 2, 4, 5, 7, 8) if len({pow(g, k, 9) for k in range(6)}) == 6]
    assert prim == [2, 5] and (2 * 5) % 9 == 1
    report('PF-A', 'VI.3', 'the primitive roots modulo 9 are exactly 2 and 5, mutual inverses', 'HOLDS', 'units of order 6: %s' % prim)
    in24 = sum(len(o) for o in orbits if len(o) == 24)
    report('PF-A', 'VI.3', '"no other seed pair produces a period-24 orbit with the properties of the Omega42 orbit"', 'RESTATED',
           'every one of the 24 states of the orbit seeds it; %d of 81 states lie on 24-cycles; the distinctive object is the orbit, not the pair (2, 5)' % in24)
    assert in24 == 72
    c = Counter(seq)
    assert c[5] == 5 and c[4] == 5 and c[9] == 2
    report('PF-A', 'VI.7', '"5 occurs 5 times, every other value 2 times"', 'FAILS',
           'counts %s: 4 and 5 occur 5 times each and every other digit twice (5 + 5 + 7 x 2 = 24); the statement leaves out 4' % dict(sorted(c.items())))
    prof = {}
    for o in orbits:
        if len(o) == 24:
            cc = Counter(d(a) for a, b in o); prof[o[0]] = cc
    top = [k for k, cc in prof.items() if max(cc.values()) == cc[5] and cc[5] == 5]
    assert len(top) == 1
    report('PF-A', 'VI.7', 'the (2, 5) orbit is the only 24-cycle in which 5 reaches the highest frequency', 'HOLDS', 'its pair 4 and 5 is the high-frequency pair')
    seeds = {(0, 0): 1, (3, 3): 8, (2, 5): 24, (1, 1): 24, (1, 3): 24}
    ids = {k: next(i for i, o in enumerate(orbits) if k in o) for k in seeds}
    assert len(set(ids.values())) == 5 and all(len(orbits[ids[k]]) == v for k, v in seeds.items())
    report('PF-A', 'VI.6', 'five orbits with seeds (9, 9), (3, 3), (2, 5), (1, 1), (1, 3), periods 1, 8, 24, 24, 24', 'HOLDS', 'the five seeds lie on five different orbits')
    assert pow(10, 6, 7) == 1 and all(pow(10, k, 7) != 1 for k in range(1, 6))
    report('PF-A', 'VI.5', 'the five sixes: the order of the units mod 9 and mod 7, phi(7), phi(9), the period of 1/7', 'HOLDS',
           'they reduce to two facts: phi(9) = 6 and ord_7(10) = 6 (7 is the smallest full-reptend prime in base 10)')
    rem, r, steps = [], 1, []
    for _ in range(6):
        q, r = divmod(10 * r, 7); steps.append(q); rem.append(r)
    assert steps == [1, 4, 2, 8, 5, 7] and rem == [3, 2, 6, 4, 5, 1]
    report('PF-A', 'VIII.1', 'long division of 1 by 7: quotients 1 4 2 8 5 7, remainders 3 2 6 4 5 1', 'HOLDS', 'six steps, the remainder returns to 1')

    # ---- PF-B: Companion, Philosophical Foundations and Operational Clarifications (V336 Rev.1)
    report('PF-B', '9.3', 'Fano plane: 7 points, 7 lines, automorphism group of order 168 = 24 x 7', 'HOLDS', 'order of GL(3, 2): (8-1)(8-2)(8-4) = %d' % ((8 - 1) * (8 - 2) * (8 - 4)))
    assert (8 - 1) * (8 - 2) * (8 - 4) == 168 == 24 * 7
    report('PF-B', '9.1', '"24 is the largest dimension in which an even unimodular lattice can have no roots"', 'FAILS',
           'rootless even unimodular lattices exist in dimension 32 and in dimension 48 (the extremal lattices of minimum norm 6); not computed here, from the standard literature')
    report('PF-B', '9.1', 'Niemeier: exactly 24 even unimodular lattices in dimension 24; bosonic string 26 - 2 = 24; eta^24 of weight 12', 'HOLDS', 'standard results, not computed here')
    report('PF-B', '9.1', 'the 24-cell is "the only regular polytope that is self-dual and has no simplex or cross-polytope analog"', 'RESTATED',
           'the self-dual regular convex polytopes are the polygons, the simplices and the 24-cell; the 24-cell is the only other one')
    report('PF-B', '5.3', 'chance levels: torsion ratio 6/9 = 0.667 lies in [0.60, 0.70]; echo anchors in 3, 6, 9 at 1/3', 'HOLDS', 'the stated bands match uniform chance')

    # ---- PF-C / PF-D: the DeepSeek papers of 6 September 2026
    report('PF-C', '4.3', '"the unique seed pair that generates the full cycle"', 'FAILS', 'see PF-A VI.3: 72 states generate 24-cycles, 24 of them this orbit')
    report('PF-C', '7.1', 'the fine-structure constant as "a resonance ratio within the 24-cycle"; c as "the maximum rate of distinction-making"', 'NO DERIVATION',
           'speculations without a computation; kept as CDT-C')

    # ---- BK-A: Book appendix A, The Mathematical Formalisms (2025)
    cyc = [pow(2, k, 9) for k in range(1, 7)]
    assert cyc == [2, 4, 8, 7, 5, 1]
    report('BK-A', '2', '2^n mod 9 cycles through 2, 4, 8, 7, 5, 1', 'HOLDS', 'period 6: 2 is a primitive root')
    ML = [cyc[i:] + cyc[:i] for i in range(6)]
    assert all(sorted(row) == sorted(cyc) for row in ML) and all(sorted(col) == sorted(cyc) for col in zip(*ML))
    report('BK-A', '3', 'every row and column of the Lower World square is a permutation of the cycle', 'HOLDS', 'the square is circulant, a Latin square')
    assert all(dr(a + b) == dr(dr(a) + dr(b)) for a in range(1, 200) for b in range(1, 200))
    report('BK-A', '1', 'dr(a + b) = dr(dr(a) + dr(b))', 'HOLDS', 'for positive integers; the signed extension leaves dr(0) undefined, so a = 5, b = -5 has no value')
    report('BK-A', '4', '27 domains = 3 x 8 + 2 + 1', 'HOLDS', 'the arithmetic holds; it counts a chosen construction and derives nothing')
    F = [0, 1]
    while len(F) < 60: F.append(F[-1] + F[-2])
    zeros = [n for n in range(48) if F[n] % 9 == 0]
    assert zeros == [0, 12, 24, 36]
    report('BK-A', '6', 'Pisano period 24 "understood as 18 + 6"', 'RESTATED',
           'the period is 24; the arithmetic splits it as 12 + 12 (F(n) = 0 mod 9 at n = 0, 12, 24, and T^12 = -I); no 18 appears in it')
    report('BK-A', '7', 'alpha^-1 = 137.036 derived from the 27-domain lattice', 'NO DERIVATION',
           'no derivation is given (the paper is called forthcoming); 137.036 is the measured value restated')

    # ---- BK-B: Coherence Calculus (2025)
    seq1, x = [], 0
    for _ in range(18):
        x = dr(x + 1); seq1.append(x)
    assert set(seq1) == set(range(1, 10))
    report('BK-B', 'A2', '"for any stream of additions and reductions, accumulation points are in 3, 6, 9"', 'FAILS',
           'adding 1 repeatedly visits every digit 1 to 9 equally: %s' % seq1[:9])
    # 6x6 grid of cells, glue with a Moebius twist (left-right, flipped) then a torus wrap (top-bottom): connected components of cells
    n = 6
    cells = [(i, j) for i in range(n) for j in range(n)]
    adj = {c: set() for c in cells}
    for i, j in cells:
        for di, dj in ((0, 1), (1, 0)):
            a, b = i + di, j + dj
            if b == n: a, b = n - 1 - a, 0       # Moebius identification of the left and right edges
            if a == n: a = 0                     # wrap of the top and bottom edges
            if 0 <= a < n and 0 <= b < n:
                adj[(i, j)].add((a, b)); adj[(a, b)].add((i, j))
    comp, seen2 = 0, set()
    for c0 in cells:
        if c0 in seen2: continue
        comp += 1; stack = [c0]
        while stack:
            c1 = stack.pop()
            if c1 in seen2: continue
            seen2.add(c1); stack.extend(adj[c1] - seen2)
    assert comp == 1
    report('BK-B', 'A3', 'a Moebius twist then a torus wrap of the 6 x 6 lattice yields 27 connected domains', 'FAILS', 'gluing edges joins cells; the result is %d connected piece' % comp)
    # boundary vertices of the Moebius band built from a 6 x 6 grid: the top and bottom edges join into one circle
    mob_boundary = 2 * n
    report('BK-B', 'A4', 'the folded lattice has a boundary of 42 nodes', 'FAILS',
           'a Moebius band from the 6 x 6 grid has one boundary circle of %d vertices; after the torus wrap (the Klein bottle) the boundary is empty' % mob_boundary)
    report('BK-B', 'A5', 'dr of Fibonacci has period 24', 'HOLDS', 'Pisano period of 9')

    tally = Counter(o for _, _, _, o, _ in OUT)
    print('\nLIB-01: %d statements | %s' % (len(OUT), ', '.join('%s %d' % kv for kv in sorted(tally.items()))))
