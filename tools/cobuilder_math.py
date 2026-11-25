#!/usr/bin/env python3
"""cobuilder_math.py -- the Co-Builder results, MF-193 to MF-206.

Core Part 0.0.10 holds them as register entries and Companion Part 235 reads them.

The results that ChatGPT and Claude exchanged under the Co-Builder ledger (records/cobuilder/ledger.json), each recomputed
here exhaustively over the native states, or over the named finite family. The fuller search records stay in
records/cobuilder/verify_cobuilder_2026_11_25.py and records/cobuilder/xobs02_search.py.

    python3 tools/cobuilder_math.py --selftest
Standard library only. About ten seconds, most of it the depth-5 observer team.
"""
import cmath, itertools, math, random, sys
from collections import Counter

def law(x, m): return (x[1], (x[0] + x[1]) % m)
def states(m): return [(a, b) for a in range(m) for b in range(m)]
def orbits(m):
    seen, out = set(), []
    for x in states(m):
        if x in seen: continue
        o, y = [x], law(x, m)
        while y != x: o.append(y); y = law(y, m)
        seen |= set(o); out.append(o)
    return out
S9, O9 = states(9), orbits(9)
def jump(x, t, m=9):
    for _ in range(t): x = law(x, m)
    return x
def trace(h, x, n, m=9):
    out = []
    for _ in range(n): out.append(h(x)); x = law(x, m)
    return tuple(out)
h7 = lambda x: x[0] % 7
LINES = []
def line(label, text, ok):
    LINES.append(ok); print('%s %s %s' % (label, text, 'PASS' if ok else 'FAIL'))

def selftest():
    # MF-193 the optimal seven-symbol aperture (ChatGPT's certificate, rows a, columns b)
    H = [[3,2,1,1,1,0,5,4,3],[3,2,0,2,1,1,1,4,5],[3,3,1,1,5,3,1,6,0],[2,0,1,3,0,4,2,5,3],[3,6,3,5,3,5,0,0,3],
         [6,4,4,3,0,6,2,0,2],[6,2,5,2,4,5,5,6,0],[6,4,5,1,2,4,4,0,2],[5,3,4,5,1,3,3,3,6]]
    hc = lambda x: H[x[0]][x[1]]
    c = [len({trace(hc, x, n) for x in S9}) for n in (1, 2, 3)]
    line('aperture-optimal:', 'a seven-symbol aperture separates all 81 states in three observations (7, 49, 81); 7^2 = 49 < 81, so d_min(7) = 3',
         c == [7, 49, 81] and sorted({v for r in H for v in r}) == list(range(7)) and 7 ** 2 < 81)
    # MF-194 the structural aperture a mod 7 and the law modulo 7
    c7 = [len({trace(h7, x, n) for x in S9}) for n in range(1, 7)]
    first = Counter()
    for x in S9:
        first[next(r for r in range(1, 25) if sum(trace(h7, y, r) == trace(h7, x, r) for y in S9) == 1)] += 1
    o7 = sorted(len(o) for o in orbits(7))
    line('aperture-mod7:', 'h = a mod 7 separates 7, 49, 73, 77, 80, 81 states in 1 to 6 observations; first resolution 2:25, 3:44, 4:4, 5:6, 6:2; '
         'the law mod 7 has order 16 and 49 = 1 + 16 + 16 + 16',
         c7 == [7, 49, 73, 77, 80, 81] and dict(first) == {2: 25, 3: 44, 4: 4, 5: 6, 6: 2} and o7 == [1, 16, 16, 16])
    # MF-195 harmonic multiplicities and the commutant
    mult = Counter()
    for o in O9:
        for k in range(len(o)): mult[(24 // len(o)) * k % 24] += 1
    line('harmonics:', 'the harmonic j of the shift has multiplicity 3 + [3|j] + [j = 0]; the commutant has dimension 281 = 25 + 112 + 144, the generic stabilizer 143',
         all(mult[j] == 3 + (j % 3 == 0) + (j == 0) for j in range(24)) and sum(v * v for v in mult.values()) == 281
         and sum((v - 1) ** 2 for v in mult.values()) == 143)
    # MF-196 the coherence operator
    ok = True
    for alpha in (0.0, 0.25, 1.0, 4.0, 10.0):
        for o in O9:
            l = len(o)
            for k in range(l):
                v = [cmath.exp(2j * math.pi * k * p / l) for p in range(l)]
                j = (24 // l) * k; lam = 4 * math.sin(math.pi * j / 24) ** 2
                Lv = [2 * v[p] - v[(p - 1) % l] - v[(p + 1) % l] for p in range(l)]
                ok &= all(abs(Lv[p] - lam * v[p]) < 1e-9 for p in range(l))
                cj = 1 / (1 + alpha * math.sin(math.pi * j / 24) ** 2)
                ok &= abs(cj - 1 / (1 + alpha * lam / 4)) < 1e-12 and 0 < cj <= 1 and (j != 0 or cj == 1)
    line('coherence:', 'C_alpha = (I + alpha L/4)^-1, L = 2I - U - U*, alpha >= 0, acts on harmonic j by 1/(1 + alpha sin^2(pi j/24)), in (0, 1], 1 at j = 0', ok)
    # MF-197 memory classes
    def cycles(g):
        seen, lens = set(), Counter()
        for x in S9:
            for m in range(9):
                if (x, m) in seen: continue
                y, mm, n = x, m, 0
                while True:
                    seen.add((y, mm)); mm = (mm + g(y)) % 9; y = law(y, 9); n += 1
                    if (y, mm) == (x, m): break
                lens[n] += 1
        return dict(lens)
    o24 = next(o for o in O9 if len(o) == 24)
    sums = lambda g: tuple(sum(g[x] for x in o) % 9 for o in O9)
    random.seed(42); ok = cycles(lambda x: 1 if x == o24[0] else 0).get(216) == 1
    for _ in range(100):
        g = {x: random.randrange(9) for x in S9}; f = {x: random.randrange(9) for x in S9}
        ok &= sums(g) == sums({x: (g[x] + f[law(x, 9)] - f[x]) % 9 for x in S9})
        for o in O9:                        # a zero orbit sum is a coboundary: build f along the orbit
            g[o[-1]] = (g[o[-1]] - sum(g[x] for x in o)) % 9
        f = {}
        for o in O9:
            f[o[0]] = 0
            for i in range(1, len(o)): f[o[i]] = (f[o[i - 1]] - g[o[i - 1]]) % 9
        ok &= all((f[law(x, 9)] - f[x]) % 9 == (-g[x]) % 9 for x in S9)
    reach = all(sums({x: (1 if x == o[0] else 0) for x in S9}) == tuple(int(p == o) for p in O9) for o in O9)
    line('memory:', 'the memory g of T_g(x, m) = (N x, m + g(x)) up to g ~ g + f o N - f is its vector of five orbit sums, every vector in (Z/9)^5 = 59,049 occurs, '
         'and a unit sum on one 24-orbit gives one cycle of length 216', ok and reach)
    # MF-198 renormalization
    OB = {k: orbits(3 ** k) for k in range(1, 5)}
    ok = all(len(OB[k]) == (3 ** k + 1) // 2 for k in OB)
    for k in (1, 2, 3):
        lo = 3 ** k; idx = {x: i for i, o in enumerate(OB[k]) for x in o}; t = Counter()
        for o in OB[k + 1]: t[(len(OB[k][idx[(o[0][0] % lo, o[0][1] % lo)]]), len(o))] += 1
        want = Counter({(1, 1): 1, (1, 8): 1}); L = 8
        while L < 8 * 3 ** (k - 1) + 1: want[(L, 3 * L)] = 3 * (L // 8); L *= 3
        ok &= t == want
    def mults(k):
        P = 8 * 3 ** (k - 1); c = Counter()
        for o in OB[k]:
            for t in range(len(o)): c[(P // len(o)) * t % P] += 1
        return c, P
    ok &= all(mults(k)[0][l] == (l == 0) + sum(3 ** (j - 1) * (l % 3 ** (k - j) == 0) for j in range(1, k + 1)) for k in (2, 3) for l in range(mults(k)[1]))
    lo = 9; vec = [[sum(1 for x in oh if (x[0] % lo, x[1] % lo) == o[0]) % 9 for oh in OB[3]] for o in OB[2]]
    img = len({tuple(sum(c * v[j] for c, v in zip(cf, vec)) % 9 for j in range(len(OB[3]))) for cf in itertools.product(range(9), repeat=5)})
    line('renormalization:', 'from 3^k to 3^(k+1) each nonzero orbit of length L lifts to three of length 3L and the zero orbit to the fixed point and an 8-cycle; '
         'm_l = [l = 0] + sum_j 3^(j-1)[3^(k-j) | l]; the memory pullback from 81 to 729 states has image 729 and kernel 81', ok and img == 729)
    # MF-199 collective observability of a mod 7
    def rounds(offs):
        for r in range(1, 25):
            if len({tuple(h7(jump(x, o + t)) for o in offs for t in range(r)) for x in S9}) == 81: return r
        return 25
    two = [rounds((0, d)) for d in range(1, 24)]
    trip = sum(rounds((0, d, e)) == 1 for d, e in itertools.combinations(range(1, 24), 2))
    line('collective:', 'two observers of a mod 7 at phases 0 and d need 5,4,3,2,2,2,2,2,3,4,5,6,5,4,3,2,2,2,2,2,3,4,5 rounds for d = 1 to 23; '
         '24 of the 253 anchored triples separate all 81 states at once, (0, 2, 5) among them',
         two == [5, 4, 3, 2, 2, 2, 2, 2, 3, 4, 5, 6, 5, 4, 3, 2, 2, 2, 2, 2, 3, 4, 5] and trip == 24 and rounds((0, 2, 5)) == 1)
    # MF-200 partition sensitivity
    dist = Counter()
    for p_, q_ in itertools.combinations(itertools.combinations(range(9), 2), 2):
        if set(p_) & set(q_): continue
        lab = list(range(9)); lab[p_[1]] = p_[0]; lab[q_[1]] = q_[0]
        hh = lambda x, lab=lab: lab[x[0]]
        dist[next((n for n in range(1, 25) if len({trace(hh, x, n) for x in S9}) == 81), 25)] += 1
    line('partition:', 'over the 378 seven-class apertures that merge two disjoint pairs of values of a, the least trace length is 5 for 270, 6 for 78, 7 for 6, 8 for 3 and never for 21',
         dict(dist) == {5: 270, 6: 78, 7: 6, 8: 3, 25: 21})
    # MF-201 the observer bound and its free attainment
    bound = [next(t for t in range(12) if 7 ** t >= 9 ** k) for k in range(1, 6)]
    ok = bound == [2, 3, 4, 5, 6]
    for k in range(1, 4):
        m, r = 3 ** k, bound[k - 1]
        digit = lambda x, i, m=m: ((x[0] * m + x[1]) // 7 ** i) % 7
        ok &= len({tuple(digit(x, i) for i in range(r)) for x in states(m)}) == 9 ** k
    line('observer-bound:', 'r_min(k) = ceil(k log_7 9) = 2, 3, 4, 5, 6 for k = 1 to 5, attained by the base-7 digits of the state index', ok)
    # MF-202 native phases of one shared aperture, depths 2 to 5
    def phase_rows(k, P):
        m = 3 ** k; cur = states(m); rows = []
        for _ in range(P):
            rows.append([x[0] % 7 for x in cur]); cur = [law(x, m) for x in cur]
        return rows
    inj = lambda rows, team, n: len(set(zip(*[rows[d] for d in team]))) == n
    r2 = phase_rows(2, 24); c2 = sum(inj(r2, (0,) + t, 81) for t in itertools.combinations(range(1, 24), 2))
    r3 = phase_rows(3, 20); r4 = phase_rows(4, 196)
    m5, ph = 243, (1, 141, 155, 211, 282, 338, 409)
    cur = states(m5); sig = [[] for _ in cur]
    for t in range(410):
        if t in ph:
            for i, x in enumerate(cur): sig[i].append(x[0] % 7)
        cur = [law(x, m5) for x in cur]
    n7 = len(set(map(tuple, sig))); n6 = len({tuple(s[1:]) for s in sig})
    line('native-phases:', 'a mod 7 read at native phases separates every state: depth 2, 24 anchored three-observer teams; depth 3, (0, 1, 4, 19); '
         'depth 4, (0, 94, 145, 152, 195); depth 5, (141, 155, 211, 282, 338, 409) gives 59,041 readings and adding phase 1 gives all 59,049',
         c2 == 24 and inj(r3, (0, 1, 4, 19), 729) and inj(r4, (0, 94, 145, 152, 195), 6561) and n6 == 59041 and n7 == 59049)
    # MF-203 the split prime 11
    O11 = orbits(11)
    line('split-11:', 'modulo 11 the law has roots 8 and 4 of x^2 = x + 1 and 121 = 1 + 2 x 5 + 11 x 10',
         sorted(Counter(len(o) for o in O11).items()) == [(1, 1), (5, 2), (10, 11)] and (64 - 9) % 11 == 0 and (16 - 5) % 11 == 0)
    # MF-204 the half turn
    Q = lambda x: (x[0] ** 2 + x[0] * x[1] - x[1] ** 2) % 9
    plus = sum(len(o) if 12 % len(o) == 0 else len(o) // 2 for o in O9)
    q2 = sorted((len(o), Q(o[0]) ** 2 % 9) for o in O9)
    neg = all(jump(x, 12) == ((-x[0]) % 9, (-x[1]) % 9) for x in S9) and [x for x in S9 if x == ((-x[0]) % 9, (-x[1]) % 9)] == [(0, 0)]
    line('half-turn:', 'U^12 has eigenspaces of dimension 41 (+1) and 40 (-1); A^12 = -I and (0, 0) is the one state equal to its own negative; '
         'Q^2 is 1, 4, 7 on the three 24-orbits and 0 on the 8-cycle and the still point',
         plus == 41 and 81 - plus == 40 and neg and q2 == [(1, 0), (8, 0), (24, 1), (24, 4), (24, 7)])
    # MF-205 amplitude and probability multipliers
    E = lambda v: -sum(t * math.log(t) for t in v if t > 0)
    norm = lambda v: tuple(t / sum(v) for t in v)
    pr = norm((0.1 * 1, 0.9 / 3)); am = norm((0.1 * 1, 0.9 / 9))
    line('multipliers:', 'p = (0.1, 0.9) under multipliers (1, 1/3) read as probability weights gives (0.25, 0.75); read as amplitudes, the energy weights (1, 1/9) give (0.5, 0.5) and ln 2',
         abs(pr[0] - 0.25) < 1e-12 and abs(am[0] - 0.5) < 1e-12 and abs(E(am) - math.log(2)) < 1e-12 and E(pr) > E((0.1, 0.9)))
    # MF-206 the least triangle, qualified
    best = max((1 / p + 1 / q + 1 / r, (p, q, r)) for p in range(2, 60) for q in range(p, 60) for r in range(q, 60) if 1 / p + 1 / q + 1 / r < 1 - 1e-12)
    line('least-triangle:', 'among hyperbolic triangles with angles pi/p, pi/q, pi/r the least area pi(1 - 1/p - 1/q - 1/r) is pi/42 at (2, 3, 7): p >= 3 gives at least pi/12, '
         '(2, q >= 4) at least pi/20, and (2, 3, r) gives pi(1/6 - 1/r), least at r = 7',
         best[1] == (2, 3, 7) and abs(1 - best[0] - 1 / 42) < 1e-12 and abs(1 - 1/3 - 1/3 - 1/4 - 1/12) < 1e-12 and abs(1 - 1/2 - 1/4 - 1/5 - 1/20) < 1e-12)
    print('COBUILDER MATHEMATICS (MF-193 to MF-206): %d checks | %s' % (len(LINES), 'PASS' if all(LINES) else 'FAIL'))
    return all(LINES)

if __name__ == '__main__':
    if sys.argv[1:2] == ['--selftest']: sys.exit(0 if selftest() else 1)
    print(__doc__)
