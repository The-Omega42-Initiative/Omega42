#!/usr/bin/env python3
"""RP-01 / CB-022: depth-5 teams and their residual collisions (Claude, 25 November 2026, second exchange).

Space: (a, b) in Z/243 x Z/243 (59,049 states), N(a, b) = (b, a + b mod 243), period 648, aperture h(a, b) = a mod 7.
Checks, all exhaustive over the 59,049 states, pure standard library:
  1. ChatGPT's recount of (0,141,277,282,315,409): 58,785 signatures = 58,521 singletons + 264 pairs, nothing larger.
  2. The improved team BEST (found by a two-phase exchange search, see RP-01 CURRENT_STATE.md) and its class sizes.
  3. The colliding pairs of each team use only a handful of difference vectors (listed), and a seventh phase
     separates every residual pair: the number of such phases is counted.
Run:  python3 records/cobuilder/cbx_2026_11_25_depth5_collisions.py      (under a minute)
"""
import sys
from collections import Counter

M, P = 243, 648
BEST = (141, 155, 211, 282, 338, 409)
BEST_COUNT = 59041

checks = []
def check(name, ok, detail=''):
    checks.append(bool(ok)); print(('PASS ' if ok else 'FAIL ') + name + (': ' + detail if detail else ''))

cur = [(a, b) for a in range(M) for b in range(M)]
rows = []
for _ in range(P):
    rows.append(bytes(a % 7 for a, b in cur))
    cur = [(b, (a + b) % M) for a, b in cur]

def groups(team):
    g = {}
    for i, sig in enumerate(zip(*[rows[d] for d in team])):
        g.setdefault(sig, []).append(i)
    return g

def analyze(team):
    g = groups(team)
    sizes = Counter(len(v) for v in g.values())
    pairs = [tuple(v) for v in g.values() if len(v) == 2]
    diffs = set()
    for u, v in pairs:
        d = ((v // M - u // M) % M, (v % M - u % M) % M)
        diffs.add(min(d, ((-d[0]) % M, (-d[1]) % M)))
    seventh = [t for t in range(P) if all(rows[t][u] != rows[t][v] for u, v in pairs)]
    return len(g), sizes, pairs, diffs, seventh

n, sizes, pairs, diffs, seventh = analyze((0, 141, 277, 282, 315, 409))
check('team (0,141,277,282,315,409): 58,785 signatures, 58,521 singletons, 264 pairs, nothing larger',
      n == 58785 and sizes == Counter({1: 58521, 2: 264}), str(dict(sizes)))
print('INFO   its 264 pairs use %d difference vectors (up to sign): %s' % (len(diffs), sorted(diffs)))
check('a seventh phase separates all 264 residual pairs; number of such phases', len(seventh) > 0, '%d of 648' % len(seventh))

n, sizes, pairs, diffs, seventh = analyze(BEST)
check('improved team %s: %d signatures, all residual classes are pairs' % (BEST, BEST_COUNT),
      n == BEST_COUNT and set(sizes) <= {1, 2}, str(dict(sizes)))
print('INFO   its %d pairs use %d difference vectors (up to sign): %s' % (len(pairs), len(diffs), sorted(diffs)))
check('a seventh phase separates all of its residual pairs', len(seventh) > 0, '%d of 648' % len(seventh))

# ---- ChatGPT's recount (3519174): the eight pairs, the seventh phase 1, and the antipodal symmetry -------------------
g = groups(BEST)
pairs = sorted(tuple(sorted(((v[0] // M, v[0] % M), (v[1] // M, v[1] % M)))) for v in g.values() if len(v) == 2)
listed = sorted(tuple(sorted(p)) for p in [((23,116),(228,171)), ((179,240),(217,185)), ((179,226),(193,97)), ((154,45),(168,159)),
                                            ((75,84),(89,198)), ((50,146),(64,17)), ((26,58),(64,3)), ((15,72),(220,127))])
check("ChatGPT's list of the eight residual pairs matches", pairs == listed)
check('adding phase 1 gives 59,049 distinct signatures (seven observers)', len(groups(BEST + (1,))) == M * M)
neg = lambda x: ((-x[0]) % M, (-x[1]) % M)
pset = set(pairs)
check('the negation x -> -x maps the set of residual pairs onto itself (four antipodal couples)',
      all(tuple(sorted((neg(u), neg(v)))) in pset for u, v in pairs) and all(tuple(sorted((neg(u), neg(v)))) != (u, v) for u, v in pairs))
# Lemma: N commutes with negation, and for a != 0, (-a mod 243) mod 7 = (5 - a mod 7) mod 7 since 243 = 5 mod 7.
check('lemma: h(-x) = (5 - h(x)) mod 7 whenever the first coordinate is nonzero (all 242 values)',
      all(((M - a) % 7) == (5 - a % 7) % 7 for a in range(1, M)))
check('lemma: N(-x) = -N(x) on all states (exhaustive)', all(((M - b) % M, (-(a + b)) % M) == neg((b, (a + b) % M)) for a in range(M) for b in range(M)))
def first_at(x, t):
    for _ in range(t): x = (x[1], (x[0] + x[1]) % M)
    return x[0]
check('hence collisions avoiding first coordinate 0 at the team phases come in antipodal couples; no residual state meets 0',
      all(first_at(x, d) != 0 for u, v in pairs for x in (u, v) for d in BEST))

print('RESULT: %d checks, %d failed' % (len(checks), checks.count(False)))
sys.exit(0 if all(checks) else 1)
