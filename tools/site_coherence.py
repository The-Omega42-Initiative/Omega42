#!/usr/bin/env python3
"""site_coherence.py -- the website measured against the record (R-23, CA-53): congruence, coherence and resonance,
reported side by side and never combined (L-514).

    python3 tools/site_coherence.py --check SITE_DIR      # SITE_DIR built by tools/site_build.py --out SITE_DIR

Fails (exit 1) when the site loses a part of the record or contradicts it:
  CONGRUENCE  every register entry MF, Lexicon term, paper theorem, discovery D and open item O appears on the site;
  COHERENCE   no MF identifier the register lacks; no closed open item called open; no repository link to a
              retired location; the current version on the Doorway;
  RESONANCE   every page but 404 reachable from the Doorway within 3 links; the Research Suite, Open Research
              Register and Mathematical Atlas in the navigation.
Standard library only."""
import collections, html, json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
J = lambda *p: json.load(open(os.path.join(ROOT, *p), encoding='utf-8'))


def audit(site):
    pages = {}
    for d, _, fs in os.walk(site):
        for f in fs:
            if f.endswith('.html'): pages[os.path.relpath(os.path.join(d, f), site)] = open(os.path.join(d, f), encoding='utf-8').read()
    strip = lambda v: re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', re.sub(r'<script.*?</script>|<style.*?</style>', ' ', v, flags=re.S))))
    text = {k: strip(v) for k, v in pages.items()}
    extra = ''
    for sub in ('api', 'assets'):
        for d, _, fs in os.walk(os.path.join(site, sub)):
            for f in fs:
                if f.endswith(('.js', '.json')): extra += open(os.path.join(d, f), encoding='utf-8', errors='ignore').read()
    hay = ' '.join(text.values()) + extra
    has = lambda i: re.search(r'(?<![\w-])' + re.escape(i) + r'(?![\w])', hay) is not None
    R = {e['id']: e for e in J('records', 'math', 'results.json')['results']}
    lex = J('records', 'lexicon', 'lexicon.json')['entries']
    opn = [o['id'] for o in J('records', 'open', 'register.json')['items']]
    disc = [x['id'] for x in J('records', 'discoveries', 'register.json')['discoveries']]
    paper = open(os.path.join(ROOT, 'docs', 'OMEGA42_MATHEMATICAL_PAPER.md'), encoding='utf-8').read()
    props = sorted(set(re.findall(r'\*\*((?:Theorem|Proposition|Lemma|Corollary) \d+\.\d+)', paper)))
    res = []
    def line(group, name, ok, detail=''): res.append((group, name, ok, detail))
    for name, ids in (('register entries', list(R)), ('open items', opn), ('discoveries', disc)):
        miss = [i for i in ids if not has(i)]
        line('CONGRUENCE', '%s on the site: %d of %d' % (name, len(ids) - len(miss), len(ids)), not miss, miss[:8])
    miss = [e['term'] for e in lex if e['term'].lower() not in hay.lower()]
    line('CONGRUENCE', 'Lexicon terms on the site: %d of %d' % (len(lex) - len(miss), len(lex)), not miss, miss[:8])
    miss = [p for p in props if p not in hay]
    line('CONGRUENCE', 'paper results on the site: %d of %d' % (len(props) - len(miss), len(props)), not miss, miss[:8])
    unknown = sorted({m for m in re.findall(r'\bMF-(\d{2,})\b', hay) if 'MF-%s' % m not in R}, key=int)
    line('COHERENCE', 'MF identifiers the register lacks: %d' % len(unknown), not unknown, unknown[:8])
    closed = sorted({m for m in re.findall(r'\bO-(\d\d)\b', hay)} - {o[2:] for o in opn}, key=int)
    called_open = []
    for k, t in text.items():
        if k.startswith(('history', 'library-', 'companion-appendix-c', 'core-proposed', 'cobuilder', 'research-integration')): continue
        for c in closed:
            for m in re.finditer(r'O-%s\b' % c, t):
                w = t[max(0, m.start() - 90):m.end() + 60]
                if re.search(r'\b(is open|that is open|open at depth|remains open|still open|Open: O-%s|six open)\b' % c, w) and not re.search(r'\b(closed|settled|resolved|closes|settles)\b', w):
                    called_open.append('%s: O-%s' % (k, c))
    line('COHERENCE', 'closed open items called open: %d' % len(called_open), not called_open, called_open[:8])
    retired = [k for k, v in pages.items() if 'github.com/omega42/' in v]
    line('COHERENCE', 'links to a retired repository location: %d' % len(retired), not retired, retired[:5])
    ver = re.search(r'V\d{3} Rev\.\d+ [A-Z]+', open(os.path.join(ROOT, 'site', 'layout.html'), encoding='utf-8').read() + pages.get('index.html', ''))
    line('COHERENCE', 'version on the Doorway: %s' % (ver.group(0) if ver else 'none'), bool(ver))
    links = {k: {os.path.normpath(os.path.join(os.path.dirname(k), u)) for u in re.findall(r'href="([^"#?:]+\.html)', v)} for k, v in pages.items()}
    dist = {'index.html': 0}; q = ['index.html']
    while q:
        x = q.pop(0)
        for y in links.get(x, ()):
            if y in pages and y not in dist: dist[y] = dist[x] + 1; q.append(y)
    far = sorted(k for k in pages if k != '404.html' and dist.get(k, 99) > 3)
    hist = collections.Counter(dist.values())
    line('RESONANCE', 'pages within 3 links of the Doorway: %d of %d (at 1, 2, 3: %d, %d, %d)' % (len(pages) - 1 - len(far), len(pages) - 1, hist[1], hist[2], hist[3]), not far, far[:8])
    navkeys = ('research-suite.html', 'open-register.html', 'mathematical-atlas.html')
    nav = re.search(r'<nav[^>]*class="[^"]*nav[^"]*"[^>]*>(.*?)</nav>', pages.get('paper.html', ''), re.S)
    navtext = nav.group(1) if nav else pages.get('paper.html', '')
    miss = [k for k in navkeys if 'href="%s"' % k not in navtext]
    line('RESONANCE', 'Research Suite, Open Research Register and Atlas in the navigation', not miss, miss)
    return res


if __name__ == '__main__':
    if len(sys.argv) != 3 or sys.argv[1] != '--check': print(__doc__); sys.exit(2)
    res = audit(sys.argv[2]); ok = all(r[2] for r in res)
    for g, n, o, d in res: print('%-11s %-92s %s%s' % (g, n, 'PASS' if o else 'FAIL', '' if o or not d else '  ' + str(d)))
    print('SITE COHERENCE: %s' % ('PASS' if ok else 'FAIL')); sys.exit(0 if ok else 1)
