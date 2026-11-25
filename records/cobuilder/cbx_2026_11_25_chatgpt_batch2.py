#!/usr/bin/env python3
"""Recomputation of the finite statements in ChatGPT's messages of 25 November 2026, proposal branch commits
5ab2982 to 23c961c (Claude, CBX-1 daily check; ledger CB-008, CB-022 to CB-036).

Pure standard library. Exhaustive wherever the space is finite. Exit status 0 = every check passed.
Run:  python3 records/cobuilder/cbx_2026_11_25_chatgpt_batch2.py          (about one to two minutes)
      python3 records/cobuilder/cbx_2026_11_25_chatgpt_batch2.py --search (adds the seeded depth-5 local search)
"""
import itertools, random, sys
from collections import Counter

checks = []
def check(name, ok, detail=''):
    checks.append(bool(ok)); print(('PASS ' if ok else 'FAIL ') + name + (': ' + detail if detail else ''))

def Nm(x, m): return (x[1], (x[0] + x[1]) % m)

def phase_rows(k, h, P):
    """rows[t][i] = h(N^t(x_i)) for the 9^k states x_i in lexicographic order."""
    m = 3 ** k
    cur = [(a, b) for a in range(m) for b in range(m)]
    rows = []
    for _ in range(P):
        rows.append(bytes(h(a, b, m) for a, b in cur))
        cur = [(b, (a + b) % m) for a, b in cur]
    return rows

def distinct(rows, team):
    return len(set(zip(*[rows[d] for d in team])))

def classes(rows, team):
    return Counter(Counter(zip(*[rows[d] for d in team])).values())

# ---- CB-008: ChatGPT's independent reproduction at depths 2 to 4 -------------------------------------------------
ha = lambda a, b, m: a % 7
r2 = phase_rows(2, ha, 24)
c2 = [(0,) + t for t in itertools.combinations(range(1, 24), 2) if distinct(r2, (0,) + t) == 81]
check('CB-008 depth 2, h=a mod 7: 24 anchored triples, first (0,2,5)', len(c2) == 24 and c2[0] == (0, 2, 5),
      '%d, first %s' % (len(c2), c2[0]))
r3 = phase_rows(3, ha, 72)
c3 = [(0,) + t for t in itertools.combinations(range(1, 72), 3) if distinct(r3, (0,) + t) == 729]
check('CB-008 depth 3, h=a mod 7: 4,856 anchored quadruples, first (0,1,4,19)', len(c3) == 4856 and c3[0] == (0, 1, 4, 19),
      '%d, first %s' % (len(c3), c3[0]))
for label, h in (('(a+b) mod 7', lambda a, b, m: (a + b) % 7), ('((a+b) mod m) mod 7', lambda a, b, m: ((a + b) % m) % 7),
                 ('(a+3b) mod 7', lambda a, b, m: (a + 3 * b) % 7), ('((a+3b) mod m) mod 7', lambda a, b, m: ((a + 3 * b) % m) % 7)):
    rr = phase_rows(3, h, 72)
    cc = [(0,) + t for t in itertools.combinations(range(1, 72), 3) if distinct(rr, (0,) + t) == 729]
    print('INFO depth 3, h=%s: %d anchored certificates%s' % (label, len(cc), (', first %s' % (cc[0],)) if cc else ''))
    if label == '(a+b) mod 7':
        check('CB-008 depth 3, h=(a+b) mod 7 (integer sum): 8 certificates, first (0,1,8,9)', len(cc) == 8 and cc[0] == (0, 1, 8, 9))
    if label == '(a+3b) mod 7':
        check('CB-008 depth 3, h=(a+3b) mod 7 (integer sum): 0 certificates', len(cc) == 0)
r4 = phase_rows(4, ha, 216)
check('CB-008 depth 4 certificate (0,94,145,152,195) separates all 6,561', distinct(r4, (0, 94, 145, 152, 195)) == 6561)
del r4

# ---- CB-022: depth-5 teams (mod 243, 59,049 states, period 648) ---------------------------------------------------
r5 = phase_rows(5, ha, 648)
t_sub = (26, 167, 202, 308, 435, 627)
cl = classes(r5, t_sub)
check('CB-022 team [26,167,202,308,435,627]: 58,067 signatures, 57,085 singletons, 982 doubletons, nothing larger',
      sum(cl.values()) == 58067 and cl == Counter({1: 57085, 2: 982}), str(dict(cl)))
shifted = tuple(sorted((d - 26) % 648 for d in t_sub))
check('CB-022 shift invariance: anchored form %s gives the same count' % (shifted,), distinct(r5, shifted) == 58067)
check('CB-022 ChatGPT team (0,67,145,152,526,627) = 57,454', distinct(r5, (0, 67, 145, 152, 526, 627)) == 57454)
check('CB-022 ChatGPT team (0,67,145,476,526,627) = 57,455', distinct(r5, (0, 67, 145, 476, 526, 627)) == 57455)

if '--search' in sys.argv:
    # Seeded coordinate-descent from the 58,067 team: replace one phase at a time by the best of all 648.
    rng = random.Random(20261125)
    best = list(shifted); bestv = distinct(r5, best)
    for sweep in range(4):
        improved = False
        for pos in rng.sample(range(1, 6), 5):
            rest = [d for i, d in enumerate(best) if i != pos]
            base = list(zip(*[r5[d] for d in rest]))
            for c in range(648):
                if c in rest: continue
                v = len(set(zip(base, r5[c])))
                if v > bestv:
                    bestv, best, improved = v, sorted(rest + [c]), True
        print('INFO search sweep %d: best %d at %s' % (sweep, bestv, tuple(best)))
        if not improved: break

# ---- CB-028: Tier III alpha orbit census -------------------------------------------------------------------------
def orbit_lengths(m):
    seen, out = set(), []
    for a in range(m):
        for b in range(m):
            if (a, b) in seen: continue
            x, n = (a, b), 0
            while x not in seen:
                seen.add(x); x = Nm(x, m); n += 1
            out.append(n)
    return out
counts = [len(orbit_lengths(3 ** k)) for k in range(1, 6)]
check('CB-028 orbit counts mod 3,9,27,81,243 = 2,5,14,41,122', counts == [2, 5, 14, 41, 122], str(counts))
L27 = Counter()
seen = set()
for a in range(27):
    for b in range(27):
        if (a, b) in seen: continue
        x, o = (a, b), []
        while x not in seen: seen.add(x); o.append(x); x = Nm(x, 27)
        L27[(all(v % 3 == 0 for v in (a, b)), len(o))] += 1
units = 27 * 27 - 81
check('CB-028 mod 27: 81 states in the ideal 3Z27^2, 648 others forming nine 72-cycles',
      units == 648 and L27[(False, 72)] == 9 and sum(n for (i, l), n in L27.items() if not i) == 9, str(dict(L27)))
q = lambda a, b, m: ((a * a + a * b - b * b) ** 2) % m
check('CB-028 Q^2 = (a^2+ab-b^2)^2 mod 9 is N-invariant on all 81 states',
      all(q(a, b, 9) == q(*Nm((a, b), 9), 9) for a in range(9) for b in range(9)))
check('CB-028 a^2+ab-b^2 changes sign under N (mod 9, all 81 states)',
      all((a*a+a*b-b*b + (lambda c, d: c*c+c*d-d*d)(*Nm((a, b), 9))) % 9 == 0 for a in range(9) for b in range(9)))

# ---- CB-029: archive salvage, CROWN and the inflation count map --------------------------------------------------
check('CB-029 CROWN mod 9: (1,8) and (2,7) collide; residue 0 distinct from digital root 9',
      (1 + 8) % 9 == (2 + 7) % 9 == 0 and 9 % 9 == 0)
def subst(w): return ''.join({'L': 'LS', 'S': 'L'}[c] for c in w)
w, ok = 'L', True
for _ in range(12):
    nL, nS = w.count('L'), w.count('S'); w2 = subst(w)
    ok &= (w2.count('L'), w2.count('S')) == (nL + nS, nL)
    w = w2
check('CB-029 L->LS, S->L has count matrix [[1,1],[1,0]] (12 steps)', ok)
# swap conjugate: P[[1,1],[1,0]]P = [[0,1],[1,1]], the matrix of N(a,b) = (b, a+b)
Mc, P = [[1, 1], [1, 0]], [[0, 1], [1, 0]]
mul = lambda A, B: [[sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
check('CB-029 swap-conjugate of the count matrix is N = [[0,1],[1,1]]', mul(mul(P, Mc), P) == [[0, 1], [1, 1]])

# ---- CB-030: website review, antipodal twelve steps --------------------------------------------------------------
def Nt(x, t, m):
    for _ in range(t): x = Nm(x, m)
    return x
neg = all(Nt((a, b), 12, 9) == ((-a) % 9, (-b) % 9) for a in range(9) for b in range(9))
fix12 = [x for x in [(a, b) for a in range(9) for b in range(9)] if Nt(x, 12, 9) == x]
check('CB-030 N^12 = -I mod 9 on all 81 states (antipodal, not identity); only (0,0) fixed', neg and fix12 == [(0, 0)],
      'fixed by N^12: %s' % fix12)

# ---- CB-034: 27 researchers, 13 rounds of AG(3,3) parallel classes -----------------------------------------------
pts = list(itertools.product(range(3), repeat=3))
dirs = []
for d in itertools.product(range(3), repeat=3):
    if d == (0, 0, 0): continue
    first = next(v for v in d if v)
    if first == 1: dirs.append(d)
pair_count = Counter()
rounds_ok = True
for d in dirs:
    lines = {frozenset(tuple((p[i] + s * d[i]) % 3 for i in range(3)) for s in range(3)) for p in pts}
    rounds_ok &= len(lines) == 9 and set().union(*lines) == set(pts)
    for L in lines:
        for u, v in itertools.combinations(sorted(L), 2): pair_count[(u, v)] += 1
check('CB-034 AG(3,3): 13 parallel classes of 9 triples; all 351 pairs meet exactly once',
      len(dirs) == 13 and rounds_ok and len(pair_count) == 351 and set(pair_count.values()) == {1})

# ---- CB-035: Seven Veils game rule ------------------------------------------------------------------------------
check('CB-035 Seven Veils: phases 0,2,5 with h=a mod 7 identify every one of the 81 states', distinct(r2, (0, 2, 5)) == 81)
one = Counter(r2[0]); check('CB-035 a single phase-0 reading leaves 9 or 18 candidates', set(one.values()) == {9, 18}, str(dict(one)))

print('RESULT: %d checks, %d failed' % (len(checks), checks.count(False)))
sys.exit(0 if all(checks) else 1)
