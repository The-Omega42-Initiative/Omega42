#!/usr/bin/env python3
"""X-OBS-02: can one shared seven-symbol aperture, read at different native phases, attain the observer bound
ceil(k log_7 9) at depth k?  (Claude, 25 November 2026; ledger CB-008.)

Aperture h(a, b) = a mod 7 on representatives 0 .. 3^k - 1. Observers read h at phases 0 = d0 < d1 < ... of the native
law N(a, b) = (b, a + b) mod 3^k. A team is a certificate when the joint reading is injective on all 9^k states.

  depth 2 (81 states, 3 observers):   (0, 2, 5) among others             -- exhaustive count printed
  depth 3 (729 states, 4 observers):  exhaustive over all 57,155 anchored teams; 4,856 certificates, e.g. (0, 1, 4, 19)
  depth 4 (6,561 states, 5 observers): the certificate (0, 94, 145, 152, 195) is verified here
  depth 5 (59,049 states, 6 observers): open for six; ChatGPT's six-phase team (141, 155, 211, 282, 338, 409) gives 59,041
                                       readings (8 pairs left, 446 of 648 phases split them all), and adding phase 1 gives all
                                       59,049: seven observers suffice (RP-01, recomputed here)

Pure standard library. The depth-3 count takes about a minute.  Run: python3 records/cobuilder/xobs02_search.py
"""
import itertools, sys

def phases(k, P):
    m = 3 ** k
    S = [(a, b) for a in range(m) for b in range(m)]
    rows, cur = [], S[:]
    for _ in range(P):
        rows.append([x[0] % 7 for x in cur])
        cur = [(x[1], (x[0] + x[1]) % m) for x in cur]
    return rows

def injective(rows, team, n):
    return len(set(zip(*[rows[d] for d in team]))) == n

ok = True
r2 = phases(2, 24)
c2 = [t for t in itertools.combinations(range(1, 24), 2) if injective(r2, (0,) + t, 81)]
print('depth 2: %d anchored three-observer certificates; (0, 2, 5) is one: %s' % (len(c2), (2, 5) in c2))
ok &= len(c2) == 24 and (2, 5) in c2
r3 = phases(3, 72)
c3 = [t for t in itertools.combinations(range(1, 72), 3) if injective(r3, (0,) + t, 729)]
print('depth 3: %d anchored four-observer certificates; first %s' % (len(c3), (0,) + c3[0]))
ok &= len(c3) == 4856 and c3[0] == (1, 4, 19)
r4 = phases(4, 216)
t4 = (0, 94, 145, 152, 195)
print('depth 4: team %s separates all 6,561 states: %s' % (t4, injective(r4, t4, 6561)))
ok &= injective(r4, t4, 6561)

# depth 5: ChatGPT's RP-01 (recomputed by Claude, 25 November 2026)
m5, phs = 243, (141, 155, 211, 282, 338, 409)
cur = [(a, b) for a in range(m5) for b in range(m5)]
sig6 = [[] for _ in cur]; sig7 = [[] for _ in cur]
for t in range(max(phs) + 1):
    if t in phs or t == 1:
        for i, x in enumerate(cur):
            if t in phs: sig6[i].append(x[0] % 7)
            sig7[i].append(x[0] % 7)
    cur = [(x[1], (x[0] + x[1]) % m5) for x in cur]
n6, n7 = len(set(map(tuple, sig6))), len(set(map(tuple, sig7)))
print('depth 5: six phases %s give %d readings; adding phase 1 gives %d of 59,049' % (phs, n6, n7))
ok &= n6 == 59041 and n7 == 59049
print('lower bound ceil(k log_7 9): 2, 3, 4, 5, 6 for k = 1..5 ->', [next(t for t in range(9) if 7 ** t >= 9 ** k) for k in range(1, 6)])
print('RESULT:', 'PASS' if ok else 'FAIL')
sys.exit(0 if ok else 1)
