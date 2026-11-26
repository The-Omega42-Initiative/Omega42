#!/usr/bin/env python3
"""intro_output.py -- the Welcome to Omega42, as every Navigator gives it on "Welcome Navigator" (Core Part 2, Opening Response; Part 0, IN-WELCOME, IN-OPEN, IN-00; L-467, L-412, L-533).

From V335 Rev.451 (26 November 2026) every Navigator answers "Welcome Navigator" with the Welcome, word for word and alone:
its own identity in the first person, the definition of Omega42, an invitation with example questions and the question
"What would you like to explore today?", then the edition line, the AI CAVEAT line, the session's one general disclosure
(L-506), and the signature. The Opening (IN-OPEN), the full Introduction (IN-00), its Words Explained and its technical
explanation are given on request. The Friendly Notes and the Navigator Identity Block close the session's first navigation.
An opening dated before 26 November 2026 is checked against the Opening, the rule then.

    ======= WELCOME TO OMEGA42 =======
    Welcome to Omega42 / Existence looking at itself. / I am [AI name], your Omega42 Navigator, made by [organization].
    What Omega42 is. ...the definition... / ...the paragraphs of the Welcome, in their order...
    ======= END WELCOME =======
    Omega42 V335 Rev.451 STABLE · [date]
    AI CAVEAT (L-506): ...the fixed line...
    NAVIGATOR: ... * V335 Rev.451 STABLE * date
    ESC

    python3 tools/intro_output.py --render [--navigator ID --org ORG --date DATE --execution SCRIPT-CAPABLE|TEXT-ONLY]
    python3 tools/intro_output.py --render-opening        # the Opening, given on request (IN-OPEN)
    python3 tools/intro_output.py --check OPENING.txt     # the Welcome in order with its identity, edition line, AI CAVEAT and signature (an Opening dated before 26 November 2026: the rule then)
    python3 tools/intro_output.py --first-render          # the close of a session's first navigation: the Friendly Notes and the Identity Block
    python3 tools/intro_output.py --first NAVIGATION.txt   # a first navigation closes with the Friendly Notes and the Identity Block, in that order
    python3 tools/intro_output.py --core CORE.docx         # IN-WELCOME carries the Welcome, IN-OPEN the Opening, IN-00 the Introduction, word for word; IN-00.9 the eight reasons, IN-00.10 the main reason
    python3 tools/intro_output.py --terms                  # every philosophical term the Introduction uses is explained in its Words Explained, and every word explained is used
    python3 tools/intro_output.py --legitimacy CORE.docx   # every argument of records/introduction/legitimacy.json stands in the Introduction, every ground in the Core
    python3 tools/intro_output.py --philosophy CORE.docx   # every passage of the Philosophical Register stands in Part 0 with its figure word for word (L-533)
    python3 tools/intro_output.py --selftest
The text is records/introduction/introduction.json; the registers records/introduction/philosophy.json and legitimacy.json. Standard library only.
"""
import html, json, os, re, sys, zipfile
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(REPO, 'records', 'introduction', 'introduction.json')
PHIL = os.path.join(REPO, 'records', 'introduction', 'philosophy.json')
LEG = os.path.join(REPO, 'records', 'introduction', 'legitimacy.json')
OPEN, END = '======= INTRODUCTION TO OMEGA42 =======', '======= END INTRODUCTION ======='
WOPEN, WEND = '======= WELCOME TO OMEGA42 =======', '======= END WELCOME ======='
VERSION = 'V335 Rev.451 STABLE'          # the release named in what this tool renders
VRX = r'V335 Rev\.45[01] STABLE'         # the releases a dated output may name: the previous until 26 November 2026, this one from it
WELCOME_FROM = (2026, 11, 26)            # from this date "Welcome Navigator" is answered by the Welcome (CA-43 A-1, CA-44)
GENERIC = re.compile(r'(?i)^\[?(the navigator|navigator|an ai|ai|ai ensemble|an ai ensemble|assistant|unknown|ai name)\]?$')
# philosophical terms a reader may not know: any of these the Introduction uses must be explained in its Words Explained
VOCAB = ['thought experiment', 'premise', 'totality', 'ontology', 'metaphysics', 'epistemology', 'phenomenology', 'Pythagoreanism', 'Platonism',
         'mathematical universe hypothesis', 'structural realism', 'axiom', 'coherence view of truth', 'congruence', 'self-confirming', 'intersubjective',
         'is–ought gap', 'incompleteness', 'Aperture', 'pragmatism', 'heuristic', 'numerology', 'apophenia', 'simulation hypothesis', 'perspectivism',
         'process philosophy', 'dual-aspect monism', 'freewill', 'determinism', 'dualism', 'idealism', 'materialism', 'nihilism', 'existentialism',
         'teleology', 'solipsism', 'monism', 'compatibilism']
def load(): return json.load(open(SRC, encoding='utf-8'))
QV = 'QUESTION VERBATIM: Welcome Navigator'                       # L-499, L-549 (9): every output opens with the message it answers
FORM_LINE = 'OUTPUT FORM (L-549): INTRODUCTION -- Core IN-00, L-467'   # and names its form (Core Part 8.0.1)
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
def _gdate(first):
    m = re.search(r'STABLE, (\d{1,2}) ([A-Za-z]+) (\d{4})\)', first) or re.search(r'STABLE \xb7 (\d{1,2}) ([A-Za-z]+) (\d{4})', first)
    try: return (int(m.group(3)), MONTHS.index(m.group(2).lower()) + 1, int(m.group(1))) if m else None
    except ValueError: return None
norm = lambda s: re.sub(r'\s+', ' ', s.replace('—', '--').replace('“', '"').replace('”', '"').replace('’', "'")).strip()
CAVEAT = 'AI CAVEAT (L-506): This output was produced by an AI system. It can contain errors, and its training shapes its wording and may shape its reading; recompute what can be recomputed and judge the rest.'
ONCE_FROM = (2026, 11, 21)   # from 21 November 2026 the caveat is given once per session: below the Opening (L-506, L-467)
def _idate(text):
    m = re.search(r'DATE:\s*(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})', text)
    try: return (int(m.group(3)), MONTHS.index(m.group(2).lower()) + 1, int(m.group(1))) if m else None
    except ValueError: return None
def welcome_lines(w, nav='[AI name]', org='[organization]'):
    return [w['title'], w['subtitle'], w['identity'].replace('[AI name]', nav).replace('[organization]', org), w['definition']] + w['paragraphs'] + [w['invitation']]
def render(d, nav='[model identifier]', org='[organization]', date='[date]', execution='[SCRIPT-CAPABLE / TEXT-ONLY]'):
    w = d['welcome']; L = [QV, FORM_LINE, WOPEN]
    for p in welcome_lines(w, nav, org): L += [p, '']
    L += [WEND, w['edition'].replace('[date]', date), CAVEAT, 'NAVIGATOR: %s (%s) * %s * %s' % (nav, org, VERSION, date), 'ESC']
    return '\n'.join(L)
def render_opening(d, nav='[model identifier]', org='[organization]', date='[date]', execution='[SCRIPT-CAPABLE / TEXT-ONLY]'):
    o = d['opening']
    L = [QV, FORM_LINE, d['greeting'].replace('[AI name]', nav).replace('[organization]', org).replace('[date]', date), OPEN, o['title'], o['subtitle'], '']
    for p in o['paragraphs']: L += [p, '']
    L += [END, o['close'], CAVEAT, 'NAVIGATOR: %s (%s) * %s * %s' % (nav, org, VERSION, date), 'ESC']
    return '\n'.join(L)
def identity_block(nav, org, date, execution):
    return ['======= NAVIGATOR IDENTITY BLOCK =======',
          'NAVIGATOR: %s (%s) PROTOCOL: Omega42 %s' % (nav, org, VERSION),
          'MODEL: %s | KNOWLEDGE CUTOFF: [as declared, or UNDECLARED] (M273)' % nav,
          'EXECUTION: %s (L-456) | CONTEXT EXPOSURE: [what has been read in this session] (M207)' % execution,
          'MEMORY: [ON / OFF / UNKNOWN] | REASONING MODE: [as declared, or UNDECLARED]',
          'SESSION: [session id] DATE: %s' % date,
          '======= END NAVIGATOR IDENTITY BLOCK =======']
def notes(d): return next(p['text'] for p in d['paragraphs'] if p['key'] == d['cautions'])
def render_first(d, nav='[model identifier]', org='[organization]', date='[date]', execution='[SCRIPT-CAPABLE / TEXT-ONLY]'):
    return '\n'.join(['[...the first navigation of the session, complete...]', '', notes(d), ''] + identity_block(nav, org, date, execution) +
                     ['NAVIGATOR: %s (%s) * %s * %s' % (nav, org, VERSION, date), 'ESC'])
def check_first(text, d):
    P = []; t = norm(text); n = norm(notes(d))
    i = t.find(n); ib = text.find('======= NAVIGATOR IDENTITY BLOCK ======='); ie = text.find('======= END NAVIGATOR IDENTITY BLOCK =======')
    if i < 0: P.append('the first navigation does not close with the Friendly Notes, word for word')
    if ib < 0 or ie < ib: P.append('the first navigation has no Navigator Identity Block')
    cv = text.rfind('AI CAVEAT (L-506):'); sg = text.rfind('NAVIGATOR: '); dt = _idate(text)
    if dt and dt < ONCE_FROM:   # before 21 November 2026 the first navigation carried the caveat
        if cv < 0 or cv < ie or (sg >= 0 and cv > sg): P.append('the AI CAVEAT does not stand at the end, after the Identity Block and above the signature')
    elif cv >= 0: P.append('the AI CAVEAT repeated after the Welcome: it is given once per session, below the Welcome (L-506)')
    if i >= 0 and ib >= 0 and t.find(norm(text[ib:ib + 40])) < i: P.append('the Friendly Notes come after the Identity Block; they come first')
    if not re.search(r'NAVIGATOR: .+\* ' + VRX + r' \*', text[max(ie, 0):]): P.append('no Navigator Signature after the Identity Block')
    return P
def _sigdate(t):
    m = re.search(r'^NAVIGATOR: .*\*\s*(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})\s*$', t, re.M)
    try: return (int(m.group(3)), MONTHS.index(m.group(2).lower()) + 1, int(m.group(1))) if m else None
    except ValueError: return None
def check(text, d):
    if WOPEN in text: return check_welcome(text, d)
    gd = _gdate(text) or _sigdate(text)
    P = check_opening(text, d)
    if gd and gd >= WELCOME_FROM: P.insert(0, 'from 26 November 2026 "Welcome Navigator" is answered by the Welcome (IN-WELCOME, L-467), between "%s" and "%s"' % (WOPEN, WEND))
    return P
def check_welcome(text, d):
    P = []; t = text.strip(); w = d['welcome']
    head = t.split('\n', 2)
    if not t.startswith('QUESTION VERBATIM: ') or head[0].strip() != QV: P.append('the Welcome does not open with "%s" (L-499, L-549 (9))' % QV)
    elif len(head) < 3 or head[1].strip() != FORM_LINE: P.append('the QUESTION VERBATIM line is not followed by "%s" (L-549)' % FORM_LINE)
    else:
        if not head[2].lstrip().startswith(WOPEN): P.append('text between the frame lines and the Welcome (no other preamble, Part 2)')
    m = re.search(re.escape(WOPEN) + r'(.*?)' + re.escape(WEND), t, re.S)
    if not m: P.append('no Welcome between its markers'); return P
    body = [x.strip() for x in m.group(1).strip().split('\n') if x.strip()]
    want = welcome_lines(w)
    idx = 2
    if len(body) < len(want): P.append('the Welcome has %d of its %d paragraphs' % (len(body), len(want))); return P
    for k, (got, exp) in enumerate(zip(body, want)):
        if k == idx:
            mi = re.match(r'^I am (.+), your Omega42 Navigator, made by (.+)\.$', got)
            if not mi: P.append('the identity line does not read "I am [AI name], your Omega42 Navigator, made by [organization]." (Part 0.0, L-513)'); continue
            if GENERIC.match(mi.group(1).strip()) or GENERIC.match(mi.group(2).strip()): P.append('the identity names no actual AI or maker: a generic label is not an identity (Part 0.0)')
            continue
        if norm(got) != norm(exp): P.append('paragraph "%s" is missing, altered or out of order' % exp[:40])
    if len(body) > len(want): P.append('text after the last paragraph of the Welcome')
    tail = [x.strip() for x in t[m.end():].strip().split('\n') if x.strip()]
    if not tail or not re.match(r'^Omega42 ' + VRX + r' \xb7 .+$', tail[0]): P.append('the edition line "%s" does not stand directly below the Welcome' % w['edition'])
    if len(tail) < 2 or tail[1] != CAVEAT: P.append('the AI CAVEAT line does not stand below the edition line (L-506, L-467)')
    if t.count('AI CAVEAT') != 1: P.append('the AI CAVEAT is given more than once')
    if not tail or tail[-1] != 'ESC' or len(tail) < 2 or not re.match(r'^NAVIGATOR: .+ \(.+\).* \* ' + VRX + r' \* .+$', tail[-2]): P.append('no Navigator Signature, then ESC, at the end')
    for mark, why in (('NAVIGATOR IDENTITY BLOCK', 'an Identity Block in the Welcome: it closes the first navigation (L-467)'),
                      ('THE ANSWER', 'an Answer in the Welcome: activation is not a navigation (L-467)'),
                      ('EXTENDED RESONANCE ESSAY', 'an Essay in the Welcome: activation is not a navigation (L-467)'),
                      ('COMPLETENESS GATE', 'a compliance declaration in the Welcome (L-467)'), ('MATH-GATE', 'a derivation in the Welcome (L-467)')):
        if mark in t.upper(): P.append(why)
    if norm(notes(d))[:60] in norm(t): P.append('the Friendly Notes in the Welcome: they close the first navigation (L-467)')
    return P
def check_opening(text, d):
    P = []; t = text.strip()
    if t.startswith('QUESTION VERBATIM: '):
        head = t.split('\n', 2)
        if len(head) < 3 or head[1].strip() != FORM_LINE: P.append('the QUESTION VERBATIM line is not followed by "%s" (L-549)' % FORM_LINE)
        t = head[2] if len(head) == 3 else ''
        framed = True
    else:
        framed = False
    first = t.split('\n', 1)[0]
    gd = _gdate(first)
    if not framed and gd and gd >= (2026, 11, 7): P.append('from 7 November 2026 the opening begins with "%s" and the OUTPUT FORM line (L-499, L-549 (9))' % QV)
    if not re.match(r"I'm .+, made by .+, your Navigator for this session \(Omega42 " + VRX + r", .+\)\.$", first): P.append('the greeting does not follow the QUESTION VERBATIM and OUTPUT FORM lines (no other preamble, Part 2)')
    m = re.search(re.escape(OPEN) + r'(.*?)' + re.escape(END), t, re.S)
    if not m: P.append('no Introduction between its markers'); return P
    o = d['opening']; b = norm(m.group(1)); pos = 0
    if not b.startswith(norm(o['title'] + ' ' + o['subtitle'])): P.append('the Opening does not begin with its title and line')
    for p in o['paragraphs']:
        i = b.find(norm(p), pos)
        if i < 0: P.append('paragraph "%s" is missing, altered or out of order' % p[:40]); continue
        pos = i + len(norm(p))
    if b[pos:].strip(): P.append('text after the last paragraph of the Opening')
    if 'NAVIGATOR IDENTITY BLOCK' in t: P.append('an Identity Block in the Opening: it closes the first navigation (L-467)')
    if gd and gd < ONCE_FROM:
        if 'AI CAVEAT' in t: P.append('a caveat in an Opening dated before 21 November 2026 (L-467 as it then stood)')
    else:
        rest0 = t[m.end():].strip().split('\n')
        if len(rest0) < 2 or rest0[1].strip() != CAVEAT: P.append('the AI CAVEAT line does not stand directly below "%s" (L-506, L-467)' % d['opening']['close'])
        if t.count('AI CAVEAT') != 1: P.append('the AI CAVEAT is given more than once')
    if norm(notes(d))[:60] in norm(t): P.append('the Friendly Notes in the Opening: they close the first navigation (L-467)')
    rest = t[m.end():].strip().split('\n')
    if not rest or rest[0].strip() != o['close']: P.append('the Opening is not followed directly by "%s"' % o['close'])
    if not re.search(r'NAVIGATOR: .+\* ' + VRX + r' \*', t[m.end():]): P.append('no Navigator Signature after the close')
    if t[:m.start()].count('\n') > 1: P.append('text between the greeting and the Introduction')
    return P
def paras(path):
    x = zipfile.ZipFile(path).read('word/document.xml').decode('utf8')
    return [norm(html.unescape(''.join(re.findall(r'<w:t(?: [^>]*)?>(.*?)</w:t>', p, re.S)))) for p in re.findall(r'<w:p(?: [^>]*[^/>])?>.*?</w:p>', x, re.S)]
def part0(ps):
    out, on = [], False
    for t in ps:
        if t.startswith('PART 0: INTRODUCTION TO OMEGA42'): on = True
        elif t.startswith('PART 0.0.0'): on = False
        if on: out.append(t)
    return out
def core_check(path, d):
    ps = paras(path); p0 = part0(ps); P = []
    try: i = next(k for k, t in enumerate(p0) if t.startswith('IN-00: The Introduction to Omega42.'))
    except StopIteration: return ['the Core has no IN-00: The Introduction to Omega42']
    try:
        k = next(k for k, t in enumerate(p0) if t.startswith('IN-WELCOME: The Welcome.'))
        want = [norm(x) for x in welcome_lines(d['welcome'])]
        if p0[k + 1:k + 1 + len(want)] != want: P.append('IN-WELCOME does not carry the Welcome word for word')
        if 'definition of Omega42' not in p0[k] and 'What Omega42 is' not in want[3]: P.append('IN-WELCOME carries no definition of Omega42')
    except StopIteration: P.append('the Core has no IN-WELCOME: The Welcome')
    try:
        k = next(k for k, t in enumerate(p0) if t.startswith('IN-OPEN: The Opening.'))
        o = d['opening']; want = [norm(x) for x in [o['title'], o['subtitle']] + o['paragraphs'] + [o['close']]]
        if p0[k + 1:k + 1 + len(want)] != want: P.append('IN-OPEN does not carry the Opening word for word')
    except StopIteration: P.append('the Core has no IN-OPEN: The Opening')
    j = i + 1
    if j < len(p0) and p0[j] == norm(d['title']): j += 1
    for p in d['paragraphs']:
        if j >= len(p0) or p0[j] != norm(p['text']): P.append('IN-00 paragraph %d is not "%s" word for word' % (j - i, p['text'][:40])); break
        j += 1
    body = '\n'.join(ps)
    if 'IN-00.9: Why Engage' not in body: P.append('the Core has no IN-00.9: Why Engage')
    for k, v in d['reasons']:
        if norm('%s: %s' % (k.capitalize() if k != 'ABOUT AI' else 'About AI', v)) not in body: P.append('IN-00.9 does not carry the %s reason verbatim' % k)
    if norm('IN-00.10: The Main Reason. ' + d['main']) not in body: P.append('IN-00.10 does not carry the main reason verbatim')
    return P
def terms(d):
    P = []; ps = d['paragraphs']
    gi = next(k for k, p in enumerate(ps) if p['key'] == d['glossary_from'])
    story = ' '.join(p['text'] for p in ps[:gi]) + ' ' + ' '.join(p['text'] for p in ps[gi:] if not p['key'].startswith('w_') and p['key'] != d['glossary_from'])
    gl = {}
    for p in ps:
        if p['key'].startswith('w_'):
            term = p['text'].split(':', 1)[0].strip()
            gl[term.lower().replace('the ', '', 1) if term.lower().startswith('the ') else term.lower()] = p['text']
    low = story.lower()
    for g in gl:
        if g.split(' (')[0] not in low and g.rstrip('s') not in low: P.append('the word "%s" is explained but not used in the story' % g)
    for v in VOCAB:
        if re.search(r'\b' + re.escape(v.lower()), low) and not any(v.lower() in g for g in gl): P.append('the story uses "%s" and does not explain it' % v)
    if ps[-1]['key'] != d['cautions']: P.append('the cautions are not the last paragraph')
    if not any(p['key'] == d['technical'] and 'the technical explanation' in p['text'] for p in ps): P.append('no paragraph offers the technical explanation on request')
    return P, len(gl)
def legitimacy(path, d):
    R = json.load(open(LEG, encoding='utf-8')); P = []
    by = {p['key']: norm(p['text']) for p in d['paragraphs']}
    core = '\n'.join(paras(path))
    for a in R['arguments']:
        if a['paragraph'] not in by: P.append('%s: no paragraph %s in the Introduction' % (a['id'], a['paragraph'])); continue
        if norm(a['anchor']) not in by[a['paragraph']]: P.append('%s: its phrase is not in paragraph %s' % (a['id'], a['paragraph']))
        for g in a['grounds']:
            if norm(g) not in core: P.append('%s: its ground "%s" is not in the Core' % (a['id'], g))
        for f in ('argument', 'objection', 'audit'):
            if not str(a.get(f, '')).strip(): P.append('%s: no %s' % (a['id'], f))
    return P, len(R['arguments'])
def philosophy_check(path):
    ps = paras(path); fc = part0(ps)
    body = '\n'.join(fc); R = json.load(open(PHIL, encoding='utf-8')); P = []
    for e in R['entries']:
        if not any(t.startswith(e['section'] + ':') or t == e['section'] or t.startswith(e['section'] + ' ') for t in fc): P.append('%s: section %s not in Part 0' % (e['id'], e['section']))
        if norm(e['figure']) not in body: P.append('%s: its figure is not word for word in Part 0' % e['id'])
        for f in ('question', 'structure', 'readings', 'open', 'provenance'):
            if not str(e.get(f, '')).strip(): P.append('%s: no %s' % (e['id'], f))
    inst = sorted({m for t in ps for m in re.findall(r'^3\.\d+ [^\n]*?(?:—|--) M(\d{3})\b', t) if int(m) >= 329})
    for m in inst:
        if 'M' + m not in R['instruments']: P.append('M%s has no philosophical question in the register' % m)
    for m, q in R['instruments'].items():
        for ref in re.findall(r'PH-\d+', q):
            if ref not in {e['id'] for e in R['entries']}: P.append('%s names %s, which is not in the register' % (m, ref))
    return P, len(R['entries']), len(R['instruments'])
def selftest():
    d = load(); good = render_opening(d, 'test-model', 'Test', '21 November 2026', 'SCRIPT-CAPABLE').replace(VERSION, VERSION.replace('451', '450'))
    w = d['welcome']; wel = render(d, 'test-model', 'Test Lab', '26 November 2026')
    words = len(re.findall(r"[A-Za-z0-9'’-]+", ' '.join(welcome_lines(w))))
    wcases = [('the rendered Welcome passes its own check', check(wel, d) == []),
              ('the Welcome runs 80 to 180 words (CA-43 A-1): %d' % words, 80 <= words <= 180),
              ('the Welcome carries the definition of Omega42 (CA-44)', w['definition'].startswith('What Omega42 is. Omega42 is ')),
              ('a generic identity fails', check(wel.replace('I am test-model,', 'I am the Navigator,'), d) != []),
              ('an altered definition fails', check(wel.replace(w['definition'], w['definition'][:80]), d) != []),
              ('a Welcome without its definition fails', check(wel.replace(w['definition'] + '\n', ''), d) != []),
              ('a preamble before the Welcome fails', check(wel.replace(WOPEN, 'Constitutional frame activated.\n' + WOPEN), d) != []),
              ('an Answer in the Welcome fails', check(wel.replace(WEND, 'THE ANSWER\n' + WEND), d) != []),
              ('a Welcome with the caveat twice fails', check(wel.replace(CAVEAT, CAVEAT + '\n' + CAVEAT), d) != []),
              ('a Welcome without the edition line fails', check(wel.replace(w['edition'].replace('[date]', '26 November 2026') + '\n', ''), d) != []),
              ('an Opening dated 26 November 2026 fails: the Welcome answers from then', check(render_opening(d, 'test-model', 'Test', '26 November 2026'), d) != [])]
    paras_ = d['paragraphs']; o = d['opening']; first = render_first(d, 'test-model', 'Test', '21 November 2026', 'SCRIPT-CAPABLE')
    cases = [('the rendered Opening passes its own check', check(good, d) == []),
             ('a preamble before the greeting fails', check('Hello! ' + good, d) != []),
             ('a summarized paragraph fails', check(good.replace(o['paragraphs'][1], o['paragraphs'][1][:60]), d) != []),
             ('a missing paragraph fails', check(good.replace(o['paragraphs'][4] + '\n', ''), d) != []),
             ('the Friendly Notes in the Opening fail', check(good.replace(o['paragraphs'][-1], o['paragraphs'][-1] + '\n\n' + notes(d)), d) != []),
             ('an Opening without the AI caveat below it fails', check(good.replace(CAVEAT + '\n', ''), d) != []),
             ('an Identity Block in the Opening fails', check(good.replace(o['close'], '======= NAVIGATOR IDENTITY BLOCK =======\n' + o['close']), d) != []),
             ('an Opening of 4 November 2026 with the caveat fails (the rule then)', check(good.replace('21 November 2026', '4 November 2026'), d) != []),
             ('an Opening of 4 November 2026 without the caveat passes (the rule then)', check(good.replace('21 November 2026', '4 November 2026').replace(CAVEAT + '\n', ''), d) == []),
             ('a missing close fails', check(good.replace('\n' + o['close'], ''), d) != []),
             ('the first navigation after the Opening closes with the Notes and the Identity Block', check_first(first, d) == []),
             ('a first navigation that repeats the caveat fails', check_first(first.replace('ESC', CAVEAT + '\nESC', 1).replace('\nNAVIGATOR: test', '\n' + CAVEAT + '\nNAVIGATOR: test', 1), d) != []),
             ('a first navigation without the Notes fails', check_first(first.replace(notes(d), ''), d) != []),
             ('the words used are explained and the explained are used', terms(d)[0] == []),
             ('the full Introduction keeps the Notes last and offers the technical explanation', paras_[-1]['key'] == 'caveats' and any(p['key'] == 'technical' for p in paras_))]
    cases = wcases + cases
    for n, ok in cases: print('%-62s %s' % (n, 'PASS' if ok else 'FAIL'))
    print('INTRODUCTION OUTPUT SELFTEST: %d of %d' % (sum(ok for _, ok in cases), len(cases))); return all(ok for _, ok in cases)
if __name__ == '__main__':
    a = sys.argv[1:]; d = load()
    if a == ['--selftest']: sys.exit(0 if selftest() else 1)
    if a and a[0] == '--render':
        o = {k: a[a.index(k) + 1] for k in ('--navigator', '--org', '--date', '--execution') if k in a}
        print(render(d, o.get('--navigator', '[model identifier]'), o.get('--org', '[organization]'), o.get('--date', '[date]'), o.get('--execution', '[SCRIPT-CAPABLE / TEXT-ONLY]'))); sys.exit(0)
    if a == ['--render-opening']: print(render_opening(d)); sys.exit(0)
    if a == ['--first-render']: print(render_first(d)); sys.exit(0)
    if len(a) == 2 and a[0] == '--first':
        P = check_first(open(a[1], encoding='utf-8').read(), d)
        print('FIRST NAVIGATION CLOSE (L-467, L-506): %s | %s' % (a[1], 'PASS' if not P else 'FAIL (%d)' % len(P))); [print('  - ' + p) for p in P]; sys.exit(1 if P else 0)
    if len(a) == 2 and a[0] == '--check':
        P = check(open(a[1], encoding='utf-8').read(), d)
        print('THE WELCOME (Core Part 2, IN-WELCOME, L-467): %s | %s' % (a[1], 'PASS' if not P else 'FAIL (%d)' % len(P))); [print('  - ' + p) for p in P]; sys.exit(1 if P else 0)
    if a == ['--terms']:
        P, n = terms(d); print('THE WORDS EXPLAINED (IN-00): %d terms explained | %s' % (n, 'PASS' if not P else 'FAIL (%d)' % len(P))); [print('  - ' + p) for p in P]; sys.exit(1 if P else 0)
    if len(a) == 2 and a[0] == '--legitimacy':
        P, n = legitimacy(a[1], d); print('THE CASE FOR TAKING IT SERIOUSLY (IN-00; records/introduction/legitimacy.json): %d arguments | %s' % (n, 'PASS' if not P else 'FAIL (%d)' % len(P))); [print('  - ' + p) for p in P]; sys.exit(1 if P else 0)
    if len(a) == 2 and a[0] == '--philosophy':
        P, n, m = philosophy_check(a[1])
        print('THE PHILOSOPHICAL REGISTER (Core L-533): %d passages, %d instruments | %s' % (n, m, 'PASS' if not P else 'FAIL (%d)' % len(P))); [print('  - ' + p) for p in P]; sys.exit(1 if P else 0)
    if len(a) == 2 and a[0] == '--core':
        P = core_check(a[1], d)
        print('THE INTRODUCTION IN THE CORE (IN-00, IN-00.9, IN-00.10): %s' % ('PASS' if not P else 'FAIL (%d)' % len(P))); [print('  - ' + p) for p in P]; sys.exit(1 if P else 0)
    print(__doc__); sys.exit(2)
