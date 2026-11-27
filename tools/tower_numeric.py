#!/usr/bin/env python3
"""tower_numeric.py -- the tower results that need NumPy (register entries MF-215, MF-217 and MF-221; paper Corollary 5.10, Proposition 5.11, Theorem 22.1).

    python3 tools/tower_numeric.py --selftest      # about two and a half minutes
Lines:
  o31-exclusion:    Cor. 5.10      every lift of the depth-5 team to depth 6 leaves a class of at least 9 states after six readings
  seven-plus-one:   Prop. 5.11     seven fixed phases leave classes of at most 3; one phase from 0..14 completes each (mean 7.13575)
  adaptive-depth6:  Theorem 22.1   greedy minimax over all 1,944 phases separates the 531,441 states of W_6 in 7 readings
Depth 7 (8 readings, 4,782,969 states, about an hour) is recomputed by records/osl/adaptive_observer.py 7.
"""
import itertools, sys
import numpy as np

def reader(k):
    q = 3 ** k; N = 8 * 3 ** (k - 1); F = [0, 1]
    for _ in range(N + 2): F.append((F[-1] + F[-2]) % q)
    a = np.repeat(np.arange(q, dtype=np.int64), q); b = np.tile(np.arange(q, dtype=np.int64), q)
    return (lambda t: ((F[t - 1] if t > 0 else F[N - 1]) * a + F[t] * b) % q % 7), q * q, N

def selftest():
    R = []
    def line(n, ok): R.append(ok); print('%-100s %s' % (n, 'PASS' if ok else 'FAIL'), flush=True)
    rd, n, N = reader(6); T5 = [0, 5, 44, 199, 243, 562]; worst = None
    for j in itertools.product(range(3), repeat=5):
        code = np.zeros(n, dtype=np.int64)
        for t in [0] + [T5[i + 1] + 648 * j[i] for i in range(5)]: code = code * 7 + rd(t)
        m = int(np.unique(code, return_counts=True)[1].max()); worst = m if worst is None else min(worst, m)
    line('o31-exclusion: all 243 lifts of (0, 5, 44, 199, 243, 562) leave a class of >= 9 states at depth 6 (least: %d)' % worst, worst >= 8)
    code = np.zeros(n, dtype=np.int64)
    for t in [0, 10, 1346, 716, 147, 1005, 1218]: code = code * 7 + rd(t)
    _, inv, cnt = np.unique(code, return_inverse=True, return_counts=True); sz = np.bincount(cnt)
    amb = np.flatnonzero(cnt > 1); split = np.zeros(len(cnt), dtype=bool); first = np.full(len(cnt), -1)
    for t in range(15):
        r = rd(t); key = inv * 7 + r; u = np.unique(key); c2 = np.bincount(u // 7, minlength=len(cnt))
        good = (c2 == cnt) & ~split & (cnt > 1); first[good] = t; split |= good
    mean = (7 * n + int(cnt[cnt > 1].sum())) / n
    ok = sz[1] == 459298 and sz[2] == 35878 and sz[3] == 129 and len(sz) == 4 and bool(split[amb].all()) \
        and len(set(first[amb].tolist())) == 13 and abs(mean - 7.1357497822) < 1e-9
    line('seven-plus-one: (0,10,1346,716,147,1005,1218) leaves 459298/35878/129; an 8th phase in 0..14 (13 used) completes, mean %.5f' % mean, ok)
    cls = np.zeros(n, dtype=np.int64); used = 0
    while np.bincount(cls).max() > 1 and used < 9:
        C = int(cls.max()) + 1; best = np.full(C, n + 1); bp = np.zeros(C, dtype=np.int64)
        for t in range(N):
            m = np.bincount(cls * 7 + rd(t), minlength=C * 7).reshape(C, 7).max(axis=1); bt = m < best; best[bt] = m[bt]; bp[bt] = t
        sym = np.empty(n, dtype=np.int64); ch = bp[cls]
        for t in np.unique(ch): idx = np.flatnonzero(ch == t); sym[idx] = rd(int(t))[idx]
        _, cls = np.unique(cls * 7 + sym, return_inverse=True); used += 1
    line('adaptive-depth6: greedy minimax over all 1,944 phases separates W_6 in %d readings (bound 7)' % used, used == 7)
    print('TOWER NUMERIC SELFTEST: %s' % ('PASS' if all(R) else 'FAIL')); return all(R)

if __name__ == '__main__':
    if sys.argv[1:] == ['--selftest']: sys.exit(0 if selftest() else 1)
    print(__doc__); sys.exit(2)
