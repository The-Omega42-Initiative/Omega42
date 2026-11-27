#!/usr/bin/env python3
"""theory_foundations.py -- the mathematical foundations of the Living Theory of Existence, rendered from the register.

Reads records/theory/foundations.json (which territory cites which register entry) and records/math/results.json (the
entries themselves), and writes a page in which every statement, status and recompute command comes from the register.
Each cited entry also gets its INHERITED status: the weakest status among the entries it rests on, through its depends
chain, except along the edges declared in records/math/status_uses.json as using an exact part only.

    python3 records/theory/theory_foundations.py            # print the page (Markdown)
    python3 records/theory/theory_foundations.py --check    # every citation resolves; prints the status counts
Run from the repository root (main or the mailbox branch with main's records). Standard library only.
"""
import json, os, re, sys
ROOT = os.getcwd()
def load(p): return json.load(open(os.path.join(ROOT, p), encoding='utf-8'))
F = load('records/theory/foundations.json')
E = {e['id']: e for e in load('records/math/results.json')['results']}
try: U = {(d['from'], d['to']) for d in load('records/math/status_uses.json')['edges']}
except FileNotFoundError: U = set()
def parents(i): return sorted(set(re.findall(r'MF-\d+', E[i].get('depends') or '')))
def inherited(i, seen=None):
    seen = seen or set(); worst = E[i]['status']
    for p in parents(i):
        if p in seen or p not in E: continue
        seen.add(p)
        if (p, i) in U: continue                    # uses an exact part of p only
        w = inherited(p, seen)
        if w != 'EXACT': worst = w if worst == 'EXACT' else worst
    return worst
def page():
    L = ['# The Living Theory of Existence: mathematical foundations', '',
         'Generated from the register by records/theory/theory_foundations.py. Each territory lists the exact results its chapter may cite. '
         'A reading built on them is marked GENERATED-Omega42 (Core L-551 (5)); a correspondence with the observable world is PENDING, FOR APPLICATION (L-490).', '']
    for t in F['territories']:
        L += ['## %s' % t['name'], '', '*%s*' % t['question'], '', '| Result | What the chapter may cite | Status | Inherited | Recompute |', '|---|---|---|---|---|']
        for c in t['cites']:
            if 'mf' in c:
                e = E[c['mf']]
                L.append('| %s | %s. *%s* | %s | %s | `python3 %s --selftest` ("%s") |' % (c['mf'], c['role'][0].upper() + c['role'][1:], ' '.join(e['statement'].split())[:220], e['status'], inherited(c['mf']), e['tool'], e['check']))
            else:
                L.append('| %s | %s | EXACT | EXACT | `python3 %s` |' % (c['ref'], c['role'][0].upper() + c['role'][1:], c['tool']))
        L.append('')
    L += ['## Not yet grounded', '']
    for n in F['not_yet']: L.append('- **%s.** %s.' % (n['name'], n['note'][0].upper() + n['note'][1:]))
    return '\n'.join(L) + '\n'
def check():
    P = []
    for t in F['territories']:
        for c in t['cites']:
            if 'mf' in c and c['mf'] not in E: P.append('%s cites %s, which is not in the register' % (t['name'], c['mf']))
            if 'tool' in c and not os.path.exists(os.path.join(ROOT, c['tool'])): P.append('%s cites %s, which does not exist' % (t['name'], c['tool']))
    cnt = {}
    for t in F['territories']:
        for c in t['cites']:
            if 'mf' in c and c['mf'] in E: cnt[inherited(c['mf'])] = cnt.get(inherited(c['mf']), 0) + 1
    print('THEORY FOUNDATIONS: %d territories, %d citations, inherited statuses %s | %s' % (len(F['territories']), sum(len(t['cites']) for t in F['territories']), cnt, 'PASS' if not P else 'FAIL'))
    [print('  - ' + p) for p in P]; return not P
if __name__ == '__main__':
    if sys.argv[1:] == ['--check']: sys.exit(0 if check() else 1)
    sys.stdout.write(page())
