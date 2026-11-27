#!/usr/bin/env python3
"""register_graph.py -- the mathematical register as a dependency graph (records/math/results.json; R-07).

An edge u -> v means that v depends on u (its "depends" field). Two release checks:
  (1) derivation acyclicity: no circular derivation, and every MF reference names an entry;
  (2) proposition-level status: an EXACT entry rests on a weaker entry only through a declared exact part
      (records/math/status_uses.json).
    python3 tools/register_graph.py --check       # both checks
    python3 tools/register_graph.py --closure MF-n  # the entries a change to MF-n reaches
    python3 tools/register_graph.py --selftest
Standard library only.
"""
import json, os, re, sys
from collections import defaultdict, deque
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def load():
    E = json.load(open(os.path.join(REPO, 'records', 'math', 'results.json'), encoding='utf-8'))['results']
    U = json.load(open(os.path.join(REPO, 'records', 'math', 'status_uses.json'), encoding='utf-8'))['edges']
    return E, U
def graph(E):
    ids = [e['id'] for e in E]; out = defaultdict(set); bad = []
    for e in E:
        for u in sorted(set(re.findall(r'MF-\d+', e.get('depends') or ''))):
            if u not in ids: bad.append('%s depends on %s, which is not an entry' % (e['id'], u))
            elif u == e['id']: bad.append('%s depends on itself' % u)
            else: out[u].add(e['id'])
    return ids, out, bad
def cycle(ids, out):
    indeg = {i: 0 for i in ids}
    for u in out:
        for v in out[u]: indeg[v] += 1
    q = deque(i for i in ids if indeg[i] == 0); n = 0
    while q:
        u = q.popleft(); n += 1
        for v in out[u]:
            indeg[v] -= 1
            if indeg[v] == 0: q.append(v)
    return sorted(i for i in ids if indeg[i] > 0)
def closure(out, n):
    s, st = set(), [n]
    while st:
        for v in out[st.pop()]:
            if v not in s: s.add(v); st.append(v)
    return s
def check(E=None, U=None):
    if E is None: E, U = load()
    ids, out, P = graph(E)
    c = cycle(ids, out)
    if c: P.append('circular derivation among %s' % ', '.join(c[:12]))
    st = {e['id']: e['status'] for e in E}; declared = {(d['from'], d['to']) for d in U if d.get('uses')}
    for u in out:
        for v in out[u]:
            if st[v] == 'EXACT' and st[u] != 'EXACT' and (u, v) not in declared:
                P.append('%s [EXACT] rests on %s [%s] with no declared exact part' % (v, u, st[u]))
    for d in U:
        if d['to'] not in out.get(d['from'], set()): P.append('declared use %s -> %s is not an edge of the register' % (d['from'], d['to']))
    return P, ids, out
def selftest():
    E = [{'id': 'MF-1', 'status': 'EXACT', 'depends': 'none'}, {'id': 'MF-2', 'status': 'CONDITIONAL on X', 'depends': 'MF-1'},
         {'id': 'MF-3', 'status': 'EXACT', 'depends': 'MF-2'}]
    cases = [('an undeclared EXACT-on-CONDITIONAL edge fails', any('MF-3' in p for p in check(E, [])[0])),
             ('a declared exact part passes', not check(E, [{'from': 'MF-2', 'to': 'MF-3', 'uses': 'the algebra'}])[0]),
             ('a cycle fails', any('circular' in p for p in check([{'id': 'MF-1', 'status': 'EXACT', 'depends': 'MF-2'}, {'id': 'MF-2', 'status': 'EXACT', 'depends': 'MF-1'}], [])[0])),
             ('a dangling reference fails', any('not an entry' in p for p in check([{'id': 'MF-1', 'status': 'EXACT', 'depends': 'MF-9'}], [])[0])),
             ('the register as it stands passes', not check()[0])]
    for n, ok in cases: print('%-58s %s' % (n, 'PASS' if ok else 'FAIL'))
    ok = all(o for _, o in cases); print('REGISTER GRAPH SELFTEST: %s' % ('PASS' if ok else 'FAIL')); return ok
if __name__ == '__main__':
    a = sys.argv[1:]
    if a == ['--selftest']: sys.exit(0 if selftest() else 1)
    if a == ['--check']:
        P, ids, out = check(); n = sum(len(v) for v in out.values())
        print('REGISTER GRAPH: %d entries, %d derivation edges, acyclic and status-consistent | %s' % (len(ids), n, 'PASS' if not P else 'FAIL (%d)' % len(P)))
        [print('  - ' + p) for p in P]; sys.exit(1 if P else 0)
    if len(a) == 2 and a[0] == '--closure':
        E, U = load(); ids, out, _ = graph(E); c = closure(out, a[1])
        print('%s reaches %d entries: %s' % (a[1], len(c), ', '.join(sorted(c, key=lambda s: int(s[3:]))))); sys.exit(0)
    print(__doc__); sys.exit(2)
