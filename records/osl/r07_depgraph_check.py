"""R-07 check: the dependency graph of the mathematical register, read from its own 'depends' fields.
Run from the repository root (main): python3 records/osl/r07_depgraph_check.py   (pure Python; under a second)
Edge u -> v means v depends on u. Checks: no dangling reference, no cycle, the structural closure properties (version-aware: the register grows),
and lists the entries whose status is stronger than a status they depend on."""
import json, re, sys
from collections import defaultdict, deque
R = []
def ok(name, c):
    R.append(bool(c)); print(('PASS ' if c else 'FAIL ') + name)
E = json.load(open('records/math/results.json'))['results']
ids = {e['id'] for e in E}; status = {e['id']: e.get('status') for e in E}
out = defaultdict(set); indeg = {i: 0 for i in ids}; refs = set()
for e in E:
    for u in set(re.findall(r'MF-\d+', e.get('depends') or '')):
        refs.add(u)
        if u in ids: out[u].add(e['id']); indeg[e['id']] += 1
ok(f'{len(E)} entries; every MF reference in a depends field names an entry', refs <= ids)
# Kahn: acyclic iff every node is removed
q = deque(i for i in ids if indeg[i] == 0); seen = 0; ind = dict(indeg); depth = {i: 0 for i in ids}
while q:
    u = q.popleft(); seen += 1
    for v in out[u]:
        depth[v] = max(depth[v], depth[u] + 1); ind[v] -= 1
        if ind[v] == 0: q.append(v)
ok('the register is acyclic (no circular derivation)', seen == len(ids))
def closure(n):
    s, st = set(), [n]
    while st:
        for v in out[st.pop()]:
            if v not in s: s.add(v); st.append(v)
    return s
c = {i: len(closure(i)) for i in ids}
top = sorted(ids, key=lambda i: -c[i])[:3]
print('  edges', sum(len(v) for v in out.values()), 'longest chain', max(depth.values()), 'largest closures', [(i, c[i]) for i in top])
ok('MF-01 has the largest closure, reaching most of the register (136 of 205 others when R-07 was written, 141 at 211 entries)', top[0] == 'MF-01' and c['MF-01'] >= 136 and 2 * c['MF-01'] > len(E) - 1)
weak = sorted((u, v) for u in ids for v in out[u] if status[v] == 'EXACT' and status[u] != 'EXACT')
print('  EXACT entries resting on a CONDITIONAL entry:', weak)
ok('exactly five such edges, all from MF-07 or MF-15 (the AP-SPACE readings)', len(weak) == 5 and {u for u, _ in weak} == {'MF-07', 'MF-15'})
print(f'{sum(R)} of {len(R)} checks passed')
sys.exit(0 if all(R) else 1)
