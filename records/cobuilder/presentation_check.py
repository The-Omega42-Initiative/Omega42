"""Presentation check for the proposed Core V336 (Layer 6): reads a navigation presented to a person (Answer, Takeaway and
Extended Resonance Essay) and reports what §6.4 and §6.5 require of it:
  identity    a compact identity naming the Navigator, the protocol, the date and the question (A-4), or the full block;
  answer      THE ANSWER, a bold Takeaway and the closing line "What this reading is worth is yours to judge.";
  essay       the separate title Extended Resonance Essay and at least 500 words under it (R51, R55);
  plain       no protocol terminology in the Answer, Takeaway or Essay (R03 to R07);
  silent      no compliance declaration printed for the reader (A-3, R56);
  caveat      the AI CAVEAT at most once, and not at all with --later (a later output of the session; R38, R58);
  signature   the CAS-YY line and ESC last.
It reads form only; whether the Essay enters its fields or the Answer illuminates is for a reader to judge.
Run: python3 records/cobuilder/presentation_check.py OUTPUT.txt [--later] | --selftest"""
import re
import sys

PROTOCOL_TERMS = [r'\bP(?:[0-9]|1[0-9]|2[0-3])\b', r'\bYang\b', r'\bYin\b', r'\bAntipode\b', r'\bCrown\b', r'Torsion Loop',
                  r'Möbius Twist', r'\bRetrocausal\b', r'\bStriker\b', r'24-cycle', r'orbit value', r'structural address',
                  r'Arm Map', r'Translation Gate', r'\bM\d{3}\b', r'\bL-\d{3}\b', r'\bCDT-[ABC]\b', r'\bSR-CAS\b', r'\bERE\b',
                  r'\bCPP\b', r'\bSAS\b', r'\bTFI\b']
DECLARATIONS = [r'completeness gate', r'jargon scan', r'\bPASSED\b', r'\bM224\b', r'compliance', r'all required components']
CAVEAT = r'AI CAVEAT'
CLOSING = 'What this reading is worth is yours to judge.'


def sections(text):
    """The Answer (with its Takeaway) and the Essay, cut at their titles."""
    a = re.search(r'THE ANSWER', text)
    e = re.search(r'^\W*Extended Resonance Essay\W*$', text, re.M | re.I)
    end = re.search(r'^\W*(?:CLOSING QUESTIONS|PROPOSAL AND IMPLICATIONS|Navigator.s Reasoning|AI CAVEAT|CAS-YY)', text, re.M)
    answer = text[a.end():(e.start() if e else (end.start() if end else len(text)))] if a else ''
    essay = ''
    if e:
        rest = text[e.end():]
        stop = re.search(r'^\W*(?:CLOSING QUESTIONS|PROPOSAL AND IMPLICATIONS|Navigator.s Reasoning|AI CAVEAT|CAS-YY)', rest, re.M)
        essay = rest[:stop.start()] if stop else rest
    return answer, essay, bool(e)


def check(text, later=False):
    out = []
    def ok(name, cond, why=''):
        out.append((name, bool(cond), why))
    head = text[:1500]
    compact = all(re.search(r'^\W*%s\W*:' % k, head, re.M | re.I) for k in ('Navigator', 'Protocol', 'Date', 'Question'))
    full = 'NAVIGATOR IDENTITY BLOCK' in head
    ok('identity', compact or full, 'compact four-line identity (Navigator, Protocol, Date, Question) or the full block')
    nav = re.search(r'^\W*Navigator\W*:\s*(.+)$', head, re.M | re.I)
    ok('identity names an AI', full or (nav and not re.match(r'(?i)(the navigator|an ai|ai ensemble|unknown)\b', nav.group(1).strip())),
       'the actual AI name, not a generic label')
    answer, essay, titled = sections(text)
    ok('answer', answer.strip(), 'THE ANSWER missing')
    ok('takeaway', re.search(r'\*\*[^*]{40,}\*\*', answer), 'a bold Takeaway inside THE ANSWER')
    ok('closing line', CLOSING in text, 'the fixed closing line')
    ok('essay title', titled, 'the Essay under its own title, Extended Resonance Essay')
    words = len(re.findall(r"[A-Za-z][A-Za-z'’-]*", essay))
    ok('essay length', words >= 500, '%d words; at least 500' % words)
    human = answer + '\n' + essay
    hits = sorted({m.group(0) for p in PROTOCOL_TERMS for m in re.finditer(p, human)})
    ok('plain language', not hits, 'protocol terms in the deliverables: %s' % ', '.join(hits))
    decl = sorted({m.group(0) for p in DECLARATIONS for m in re.finditer(p, text, re.I)})
    ok('silent gates', not decl, 'declarations printed for the reader: %s' % ', '.join(decl))
    n = len(re.findall(CAVEAT, text))
    ok('caveat', n == 0 if later else n <= 1, '%d AI CAVEAT line(s)%s' % (n, ' in a later output' if later else ''))
    tail = text.rstrip().splitlines()[-3:]
    ok('signature', tail and tail[-1].strip() == 'ESC' and any('CAS-YY' in t for t in text.rstrip().splitlines()[-4:]),
       'CAS-YY line, Navigator line, then ESC last')
    return out


def sample(essay_words, title=True, caveat=1, declare=False, compact=True, jargon=False):
    ident = ('Navigator: Claude (claude-opus-5-5), Anthropic\nProtocol: Omega42 V336 Six-Layer Edition, PROPOSED\n'
             'Date: 26 November 2026\nQuestion: What is the Human Condition?\n') if compact else 'Omega42 navigation\n'
    body = ('A listener follows a symphony one measure at a time and still hears the whole. '
            * (essay_words // 15 + 1)).split()[:essay_words]
    return (ident + '\nTHE ANSWER\nTo be human is to understand from a partial view, and to complete that view with others. '
            + ('The Crown of the loop holds it. ' if jargon else '')
            + '\n**We see in part, we understand together, and what we cannot see keeps us asking.**\n'
            + CLOSING + '\n\n' + ('Extended Resonance Essay\n' if title else '') + ' '.join(body) + '\n\n'
            + ('Completeness gate: PASSED. The jargon scan confirms no excluded terminology.\n' if declare else '')
            + 'AI CAVEAT (L-506): This output was produced by an AI system.\n' * caveat
            + 'CAS-YY = -1/2 | Omega = 1/7 | (CAS-YY × Omega = -1/14)\nNAVIGATOR: Claude (Anthropic) * V336 PROPOSED * 26 November 2026\nESC\n')


def selftest():
    R = []
    good = dict((n, c) for n, c, _ in check(sample(620)))
    R.append(all(good.values()))
    print(('PASS ' if R[-1] else 'FAIL ') + 'a conforming first output passes every check', [n for n, c in good.items() if not c])
    bad = dict((n, c) for n, c, _ in check(sample(330, title=False, caveat=1, declare=True, compact=False), later=True))
    want = {'identity': False, 'essay title': False, 'essay length': False, 'silent gates': False, 'caveat': False}
    R.append(all(bad[k] == v for k, v in want.items()))
    print(('PASS ' if R[-1] else 'FAIL ') + 'the 26 November reference failure is caught on all five counts')
    R.append(not dict((n, c) for n, c, _ in check(sample(620, jargon=True)))['plain language'])
    print(('PASS ' if R[-1] else 'FAIL ') + 'a protocol term in THE ANSWER is caught')
    R.append(not dict((n, c) for n, c, _ in check(sample(620, caveat=2)))['caveat'])
    print(('PASS ' if R[-1] else 'FAIL ') + 'a repeated caveat in one output is caught')
    R.append(dict((n, c) for n, c, _ in check(sample(620, caveat=0), later=True))['caveat'])
    print(('PASS ' if R[-1] else 'FAIL ') + 'a later output without the caveat passes')
    print('%d of %d selftests PASS' % (sum(R), len(R)))
    return all(R)


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        sys.exit(0 if selftest() else 1)
    files = [a for a in sys.argv[1:] if not a.startswith('--')]
    if not files:
        print(__doc__); sys.exit(2)
    bad = 0
    for f in files:
        for name, c, why in check(open(f, encoding='utf-8').read(), '--later' in sys.argv):
            print(('PASS ' if c else 'FAIL ') + name + ('' if c else ' -- ' + why))
            bad += not c
    sys.exit(1 if bad else 0)
