#!/usr/bin/env python3
"""Finite statements in ChatGPT's Affinity, Arcana and Worlds proposal (e0ea1ac) and its chat summary
(Claude, 25 November 2026; ledger CB-037), in the Harmonia and Atelier proposal (989de9e; ledger CB-024), and in the Concordia, Theoria and Tier III messages (1e77dc5 to 5ee3a8b; ledger CB-045 to CB-050). Pure standard library. Exit status 0 = every check passed."""
import sys
from math import gcd
from functools import reduce
checks = []
def check(name, ok, detail=''):
    checks.append(bool(ok)); print(('PASS ' if ok else 'FAIL ') + name + (': ' + detail if detail else ''))
lcm = lambda *xs: reduce(lambda a, b: a * b // gcd(a, b), xs)
check('2 x 5 = 1 mod 9 (the seeds are mutual inverses)', (2 * 5) % 9 == 1)
L = lcm(24, 12, 9, 7)
check('lcm(24, 12, 9, 7) = 504', L == 504)
check('intervals on the 504-lattice: 24->21, 12->42, 9->56, 7->72', [L // c for c in (24, 12, 9, 7)] == [21, 42, 56, 72])
check('lcm(9, 12) = 36 (ChatGPT repository example)', lcm(9, 12) == 36)
allc = (5, 7, 8, 9, 10, 12, 24, 60, 64)
print('INFO lcm of every cycle in the explorer (5,7,8,9,10,12,24,60,64) =', lcm(*allc))
check('the 504 figure depends on the chosen cycles: adding 5 gives 2520, adding 64 gives 4032',
      lcm(24, 12, 9, 7, 5) == 2520 and lcm(24, 12, 9, 7, 64) == 4032)
# the 42-unit interval is the 12-fold step only because 504 = 12 * 42; on lcm(12, 24) = 24 the same partition has step 2
check('the 42 interval is a property of the lattice, not of the 12-fold cycle', lcm(12, 24) // 12 == 2)
# Harmonia (989de9e): f_t = f0 * 2^(a_t / 9) from the canonical cycle
x, a_seq = (2, 5), []
for _ in range(48): a_seq.append(x[0]); x = (x[1], (x[0] + x[1]) % 9)
per = next(p for p in range(1, 25) if a_seq[p:p + 24] == a_seq[:24])
check('Harmonia: the first coordinate from (2, 5) has least period 24, so the tone sequence returns after 24 notes, not sooner', per == 24)
f0 = 220.0
fr = sorted({f0 * 2 ** (a / 9) for a in range(9)})
check('Harmonia: 2^(a/9), a = 0..8, gives nine distinct tones inside one octave [f0, 2 f0)', len(fr) == 9 and fr[0] == f0 and fr[-1] < 2 * f0)
# Atelier / Constitutional Aesthetics: the joint representation F = (V, S) has fibers = intersections of the fibers of V and S
S81 = [(a, b) for a in range(9) for b in range(9)]
V = lambda s: s[0] % 3; Sd = lambda s: (s[0] + s[1]) % 3
from collections import Counter
cV, cS, cF = (Counter(map(f, S81)) for f in (V, Sd, lambda s: (V(s), Sd(s))))
check('Aesthetics: a joint representation is never more ambiguous than either part (largest fiber 9 vs 27 and 27, example maps)',
      max(cF.values()) <= min(max(cV.values()), max(cS.values())), 'largest fibers V %d, S %d, joint %d' % (max(cV.values()), max(cS.values()), max(cF.values())))
# ChatGPT on cobuilder/mailbox (6c9202a, e8bcce2): the Affinity questionnaire's 121 pairs, and the orbit census
from collections import Counter as _C
d = _C(min(abs(x - y), 3) for x in range(11) for y in range(11))
check('Affinity (6c9202a): of the 121 pairs of answers 0..10, 31 differ by at most 1, 18 by exactly 2, 72 by 3 or more',
      d[0] + d[1] == 31 and d[2] == 18 and d[3] == 72)
seen, lens = set(), []
for s0 in S81:
    if s0 in seen: continue
    n, y = 0, s0
    while y not in seen: seen.add(y); y = (y[1], (y[0] + y[1]) % 9); n += 1
    lens.append(n)
check('Creative studio (e8bcce2): 1 fixed state, 8 states on the 8-cycle, 72 on the three 24-cycles', sorted(lens) == [1, 8, 24, 24, 24])
# Concordia CON-01 (5ee3a8b): two parties, each accept / reject / undecided
vals = ('A', 'R', 'U')
cls = Counter('shared' if (x, y) == ('A', 'A') else 'rejected' if 'R' in (x, y) else 'unresolved' for x in vals for y in vals)
check('Concordia: of the 9 pairs of answers, 1 shared, 3 unresolved, 5 rejected (an undecided answer is not a rejection)',
      cls == Counter({'shared': 1, 'unresolved': 3, 'rejected': 5}))
# Tier III typed beta (cad71aa): phases 5, 0, 2 (unsorted) reconstruct (2, 5); 81 classes
def rd(x, phases):
    out = []
    for t in sorted(phases):
        y = x
        for _ in range(t): y = (y[1], (y[0] + y[1]) % 9)
        out.append(y[0] % 7)
    return tuple(out)
cand = [x for x in S81 if rd(x, (5, 0, 2)) == rd((2, 5), (5, 0, 2))]
check('Tier III beta: the readings at phases 5, 0, 2 of (2, 5) leave exactly (2, 5); the 81 states give 81 classes',
      cand == [(2, 5)] and len({rd(x, (0, 2, 5)) for x in S81}) == 81)
# Theoria benchmark (e0449e6): pi: Z/27 -> Z/9 coordinatewise; J e_x = (1/3) sum_{pi y = x} e_y is an isometry and intertwines the law
from fractions import Fraction as Fr
lawm = lambda x, m: (x[1], (x[0] + x[1]) % m)
fine = [(a, b) for a in range(27) for b in range(27)]
pre = {}
for y in fine: pre.setdefault((y[0] % 9, y[1] % 9), []).append(y)
iso = all(len(v) == 9 for v in pre.values())          # |J e_x|^2 = 9 * (1/3)^2 = 1, and images of distinct x are disjoint
inter = all(sorted(lawm(y, 27) for y in pre[x]) == sorted(pre[lawm(x, 9)]) for x in pre)   # U_f J = J U_c
check('Theoria benchmark: J is an isometry from l2(81) to l2(729) and intertwines the law (U_f J = J U_c), so J* L_f J = L_c', iso and inter)
print('RESULT: %d checks, %d failed' % (len(checks), checks.count(False)))
sys.exit(0 if all(checks) else 1)
