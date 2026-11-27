"""Map Omega42 (the record) to its website (the built site) and measure, apart and never combined:
COHERENCE  the site's statements agree with the record (identifiers, statuses, counts, version);
CONGRUENCE each canonical component has a place on the site, and each page has a source in the record;
RESONANCE  the components are reachable from the Doorway, and how directly.
Usage: python3 sitemap_audit.py <built site> <repo>"""
import json, os, re, sys, html, collections
SITE, REPO = sys.argv[1], sys.argv[2]
J = lambda p: json.load(open(os.path.join(REPO, p)))
pages = {}
for d, _, fs in os.walk(SITE):
    for f in fs:
        if f.endswith('.html'):
            p = os.path.join(d, f); pages[os.path.relpath(p, SITE)] = open(p, encoding='utf-8').read()
text = {k: re.sub(r'<[^>]+>', ' ', html.unescape(re.sub(r'<script.*?</script>|<style.*?</style>', ' ', v, flags=re.S))) for k, v in pages.items()}
api = {f: open(os.path.join(SITE, 'api', f)).read() for f in os.listdir(os.path.join(SITE, 'api'))}
everything = ' '.join(text.values()) + ' '.join(api.values())
srcpages = {f[:-5] for f in os.listdir(os.path.join(REPO, 'site/pages')) if f.endswith('.html')}
# assets loaded by scripts (data the page fetches at run time counts as present)
assets = ''
for d, _, fs in os.walk(os.path.join(SITE, 'assets')):
    for f in fs:
        if f.endswith(('.js', '.json')): assets += open(os.path.join(d, f), encoding='utf-8', errors='ignore').read()
reach_text = everything + assets

R = J('records/math/results.json')['results']; MF = {e['id']: e for e in R}
LEX = J('records/lexicon/lexicon.json')['entries']
OPEN = J('records/open/register.json')['items']
DISC = J('records/discoveries/register.json'); DISC = DISC.get('entries', DISC.get('items', DISC)) if isinstance(DISC, dict) else DISC
paper = open(os.path.join(REPO, 'docs/OMEGA42_MATHEMATICAL_PAPER.md'), encoding='utf-8').read()
props = sorted(set(re.findall(r'\*\*((?:Theorem|Proposition|Lemma|Corollary) \d+\.\d+)', paper)))
cmp_ = sorted({int(m) for m in re.findall(r'companion-part-(\d+)\.html', ' '.join(pages))})

out = []
def row(*a): out.append(a)

# ---------------- CONGRUENCE: record -> site ----------------
def present(ids, hay): return [i for i in ids if re.search(r'(?<![\w-])' + re.escape(i) + r'(?![\w])', hay)]
mf_ids = sorted(MF, key=lambda s: int(s.split('-')[1]))
mf_on = present(mf_ids, reach_text)
lex_on = [e for e in LEX if e['term'].lower() in reach_text.lower()]
open_on = present([o['id'] for o in OPEN], reach_text)
disc_ids = [d['id'] for d in DISC] if isinstance(DISC, list) else []
disc_on = present(disc_ids, reach_text)
props_on = [p for p in props if p in reach_text]
row('CONGRUENCE record -> site', 'register entries MF', len(mf_on), len(mf_ids), [i for i in mf_ids if i not in mf_on][-12:])
row('CONGRUENCE record -> site', 'Lexicon terms', len(lex_on), len(LEX), [e['n'] for e in LEX if e not in lex_on][:12])
row('CONGRUENCE record -> site', 'open items', len(open_on), len(OPEN), [o['id'] for o in OPEN if o['id'] not in open_on][:12])
row('CONGRUENCE record -> site', 'discoveries D', len(disc_on), len(disc_ids), [i for i in disc_ids if i not in disc_on][:12])
row('CONGRUENCE record -> site', 'paper theorems and propositions', len(props_on), len(props), [p for p in props if p not in props_on][:12])
# instruments: register entries with a tool line, and whether an interactive instrument computes them
tools = collections.Counter(e.get('tool', '') for e in R if e.get('tool'))
row('CONGRUENCE record -> site', 'register entries with a recompute tool', sum(tools.values()), len(R), '')
# ---------------- CONGRUENCE: site -> record ----------------
nav_pages = set(re.findall(r'href="([a-z0-9-]+)\.html"', pages['index.html']))
generated = [k for k in pages if k[:-5] not in srcpages]
row('CONGRUENCE site -> record', 'pages generated from the record (Companion, Library, ...)', len(generated), len(pages), '')
row('CONGRUENCE site -> record', 'hand-written pages (site/pages)', len(pages) - len(generated), len(pages), '')

# ---------------- COHERENCE: site statements vs record ----------------
bad_mf = sorted({m for m in re.findall(r'\bMF-(\d+)\b', everything) if 'MF-' + m not in MF}, key=int)
row('COHERENCE', 'MF identifiers on the site that the register lacks', len(bad_mf), '', bad_mf[:15])
stat_bad = []
for k, t in text.items():
    for m in re.finditer(r'\b(MF-\d+)\b[^.;\n]{0,40}?\b(EXACT|CONDITIONAL|VALIDATED|SPECULATIVE|OPEN|PROVED)\b', t):
        e = MF.get(m.group(1))
        if e and m.group(2) in ('EXACT', 'CONDITIONAL', 'VALIDATED', 'SPECULATIVE') and m.group(2) != e['status']:
            stat_bad.append((k, m.group(1), m.group(2), e['status']))
row('COHERENCE', 'MF status words that differ from the register', len(stat_bad), '', stat_bad[:8])
vers = collections.Counter(re.findall(r'V\d{3} Rev\.\d+ [A-Z]+', everything))
row('COHERENCE', 'version strings', dict(vers.most_common(4)), '', '')
counts = []
pat = [(r'\b(\d{2,3}) (?:Lexicon )?(?:terms|entries) (?:in the Lexicon)?', 'lexicon', len(LEX)),
       (r'\b(\d{2,3}) open items\b', 'open items', len(OPEN)),
       (r'\b(\d{3}) register entries\b', 'register', len(R))]
for k, t in text.items():
    for rx, what, truth in pat:
        for m in re.finditer(rx, t):
            n = int(m.group(1))
            if what == 'lexicon' and 'exicon' not in t[max(0, m.start() - 80):m.end() + 40]: continue
            if n != truth: counts.append((k, what, n, truth))
row('COHERENCE', 'stated counts that differ from the record', len(counts), '', counts[:10])
closed = [k for k, t in text.items() if re.search(r'O-35[^.]{0,60}\bOPEN\b', t)]
row('COHERENCE', 'pages still calling O-35 open', len(closed), '', closed[:5])
old = [k for k, v in pages.items() if 'github.com/omega42/' in v]
row('COHERENCE', 'links to the retired personal repository', len(old), '', old[:5])

# ---------------- RESONANCE: reachability from the Doorway ----------------
links = {k: {os.path.normpath(os.path.join(os.path.dirname(k), u)) for u in re.findall(r'href="([^"#?:]+\.html)', v)} for k, v in pages.items()}
dist = {'index.html': 0}; q = ['index.html']
while q:
    x = q.pop(0)
    for y in links.get(x, ()):
        if y in pages and y not in dist: dist[y] = dist[x] + 1; q.append(y)
hist = collections.Counter(dist.values())
orph = sorted(k for k in pages if k not in dist)
row('RESONANCE', 'pages reachable from the Doorway', len(dist), len(pages), orph[:10])
row('RESONANCE', 'clicks from the Doorway: pages at 0,1,2,3,4,5+', [hist.get(i, 0) for i in range(5)] + [sum(v for d, v in hist.items() if d >= 5)], '', '')
key = ['paper.html', 'paper-register.html', 'lexicon.html', 'research-suite.html', 'open-mathematics.html', 'adaptor-lab.html',
       'observatory.html', 'discovery-register.html', 'protocol.html', 'omegasl.html', 'companion.html', 'derivations.html', 'cobuilder.html']
row('RESONANCE', 'clicks to the mathematical hubs', {k[:-5]: dist.get(k, 'unreachable') for k in key if k in pages}, '', '')
inbound = collections.Counter(y for x in links for y in links[x] if y in pages and y != x)
row('RESONANCE', 'pages linked from only one other page', sum(1 for k in pages if inbound[k] == 1), len(pages), '')
row('RESONANCE', 'hubs and their inbound links', {k[:-5]: inbound[k] for k in key if k in pages}, '', '')

for r in out:
    print(' | '.join(str(x) for x in r))
