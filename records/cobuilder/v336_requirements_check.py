"""Requirements traceability check for the proposed Core V336 six-layer edition (Appendix D).
For every row R01 to R60: the V336 section it names exists; that section states the requirement (its key phrases are present);
every canonical law and Step it cites is defined in the canonical Core V335 Rev.450; and, when ChatGPT's Rev451 candidate is
supplied, every Rev451 section it cites exists there; and that the ratified amendments A-1 to A-4 are marked as such and
recorded in the ledger (CA-43). Also checks that the human-deliverable sections of Layer 6 keep their
examples free of protocol terms, outside the list that names them.
Run: python3 records/cobuilder/v336_requirements_check.py [REV451_CANDIDATE.md]"""
import re
import sys

V336 = 'docs/proposed/OMEGA42_CORE_V336_SIX_LAYER_PROPOSED.md'
CORE = 'ai/Omega42_Core_V335_Rev450.md'
R = []
def ok(n, c): R.append(bool(c)); print(('PASS ' if c else 'FAIL ') + n)

v = open(V336, encoding='utf-8').read()
core = open(CORE, encoding='utf-8').read()
rev = open(sys.argv[1], encoding='utf-8').read() if len(sys.argv) > 1 else None

def section(num):
    """Text of V336 section `num` (for example 6.4.1), up to the next heading of the same or higher level."""
    m = re.search(r'^(#+) ' + re.escape(num) + r'[ .]', v, re.M)
    if not m:
        return None
    lvl = len(m.group(1))
    rest = v[m.end():]
    n = re.search(r'^#{1,%d} ' % lvl, rest, re.M)
    return rest[:n.start()] if n else rest

KEYS = {  # row: phrases that must appear in the cited V336 sections
    'R01': ['THE ANSWER', 'Takeaway', 'Extended Resonance Essay', 'separately titled'],
    'R02': ['brief and lite presentations', 'changes what is shown, not what must be done'],
    'R03': ['THE ANSWER', 'in any form or position, quotation included'],
    'R04': ['the Takeaway'], 'R05': ['Extended Resonance Essay', 'no exception is made for brevity'],
    'R06': ['the four closing questions'],
    'R07': ['P0 to P23', 'Yang, Yin, 4D and Antipode', 'M-numbers, L-numbers', 'Core Part 10'],
    'R08': ['equations, compliance declarations', 'theorem identifiers', 'internal acronyms'],
    'R09': ["Navigator's Reasoning", 'one designated technical space'],
    'R10': ['jargon scan', 'must read PASS', 'SELF-CHECKED'],
    'R11': ['voice of the field', 'plain language for anyone'],
    'R12': ['Two-way translation', 'translated back into the language of the question'],
    'R13': ['complete in itself', 'never seen the protocol'],
    'R14': ['Core Synthesis', 'Conventional Connection', 'Practical Bridge', 'Historical Lineage', 'Implications', 'Mapping'],
    'R15': ['one answer, not separate pieces'], 'R16': ['illuminating analog', 'does not carry'],
    'R17': ['What this reading is worth is yours to judge.'], 'R18': ['this proves'],
    'R19': ['two to four bold sentences of plain language'],
    'R20': ['adjacent fields', 'impact'], 'R21': ['at least three relevant adjacent fields'],
    'R22': ['New questions, practical possibilities and alternative interpretations'],
    'R23': ['does not recap THE ANSWER', 'stands on its own'],
    'R24': ['no section headers and no bullet points', 'different register'],
    'R25': ['500 to 1,500 words, plus up to 800'], 'R26': ['1,000 to 2,500 words', 'A-2'],
    'R27': ['judgments of reliability'], 'R28': ['what to conclude', '"real meaning"', 'authoritative'],
    'R29': ['proving a human'], 'R30': ['neither softened nor raised'],
    'R31': ['seven checks', 'says so plainly'], 'R32': ['sealed with its hash', 'frozen'],
    'R33': ['QUESTION VERBATIM'], 'R34': ['OUTPUT FORM (L-549)'],
    'R35': ['MODEL', 'EXECUTION: SCRIPT-CAPABLE or TEXT-ONLY', 'CONTEXT EXPOSURE', 'never invented'],
    'R36': ['EXECUTED', 'RECONSTRUCTED', 'NOT COMPUTED', 'simulated'],
    'R37': ['four closing questions', 'PROPOSAL AND IMPLICATIONS', 'completeness gate'],
    'R38': ['AI CAVEAT'], 'R39': ['last in every output without exception', 'ESC'],
    'R40': ['Identity first', 'generic label'], 'R41': ['word for word'],
    'R42': ['What would you like to explore today?', 'A-1'],
    'R43': ['Activation is not a navigation'], 'R44': ['CONVERSATION form'],
    'R45': ['Native contribution', 'derivation apart from interpretation'],
    'R46': ['Coherence', 'congruence', 'resonance', 'reported separately'],
    'R47': ['Open Scientific Appendix', 'dormant'], 'R48': ['thirteen forms', 'block order'],
    'R49': ['Human Condition', 'website audit', 'CLC-01'], 'R50': ['redact private information'],
    'R51': ['under the separate title **Extended Resonance Essay**', 'missing deliverable'],
    'R52': ['goes in, investigates and comes back', 'does not count as reaching it'],
    'R53': ['Generative exploration finds new relationships'],
    'R54': ['established result and which part is its interpretive extension'],
    'R55': ['Below 500 words the Essay is incomplete'],
    'R56': ['not announced', 'Completeness gate: PASSED', 'A-3'],
    'R57': ['compact header of four lines', 'A-4', 'technical record'],
    'R58': ['Later outputs of the session leave it out', 'in the context where it applies'],
    'R59': ['candidate for the Discovery Register or the Lexicon'],
    'R60': ['The Answer illuminates the question', 'The Essay opens new worlds'],
}

rows = re.findall(r'^\| (R\d\d) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \|$', v, re.M)
ok('Appendix D has 60 rows, R01 to R60 in order', [r[0] for r in rows] == ['R%02d' % i for i in range(1, 61)])
ok('every row has a key-phrase entry in this check', set(r[0] for r in rows) == set(KEYS))

core_laws = set(re.findall(r'\b(L-\d{3}): ', core))
core_steps = set(re.findall(r'^Step (\d+(?:\.\d+)?):', core, re.M))
rev_secs = set(re.findall(r'^### (10\.\d+) ', rev, re.M)) if rev else set()

for rid, req, src, sec, status in rows:
    texts = [section(s.strip()) for s in sec.split(',')]
    ok(f'{rid} V336 section(s) {sec} exist', all(t is not None for t in texts))
    body = ''.join(t for t in texts if t)
    miss = [k for k in KEYS.get(rid, []) if k.lower() not in body.lower()]
    ok(f'{rid} stated in {sec}' + (f' (missing: {miss})' if miss else ''), not miss)
    laws = re.findall(r'L-\d{3}', src)
    ok(f'{rid} canonical laws {laws or "none"} defined in V335', all(l in core_laws for l in laws))
    steps = [x for m in re.finditer(r'Steps? (\d+(?:\.\d+)?(?:, \d+(?:\.\d+)?)*)', src) for x in m.group(1).split(', ')]
    ok(f'{rid} canonical Steps {steps or "none"} present in V335', all(s in core_steps for s in steps))
    for part in re.findall(r'Part (8\.\d)', src):
        ok(f'{rid} canonical Part {part} present in V335', '### ' + part + ' ' in core)
    if 'Part 0.0' in src:
        ok(f'{rid} canonical Part 0.0 present in V335', '## PART 0.0: WHAT A NAVIGATOR IS' in core)
    if rev:
        cites = re.findall(r'10\.\d+', src) if 'Rev451' in src else []
        ok(f'{rid} Rev451 sections {cites or "none"} exist in the candidate', all(c in rev_secs for c in cites))
    ok(f'{rid} status is one of STATED, ADDED, AMENDMENT', all(w.split()[0] in ('STATED', 'ADDED', 'AMENDMENT', 'RATIFIED') for w in status.split(', ')))

# The amendments named in Appendix D are the ones Appendix B lists, and each names the canonical rule that governs meanwhile.
appb = v[v.index('# Appendix B.'):v.index('# Appendix C.')]
ok('A-1 to A-4 recorded in Appendix B with ratification pending', all(a in appb for a in ('A-1', 'A-2', 'A-3', 'A-4')) and 'ratification' in appb)
ok('every AMENDMENT row names a canonical rule in its section', all(('canonical' in (section(r[3].split(',')[-1].strip()) or '').lower())
   for r in rows if r[4].startswith('AMENDMENT')))

# The Takeaway and Essay sections carry no protocol term outside the excluded-term list of 6.4.1.
TERMS = ['Yang', 'Yin', 'Antipode', 'Crown', 'Torsion', 'Möbius', 'SR-CAS', 'SAS', 'TFI', 'CDT-']
for s in ('6.4.3', '6.4.5'):
    t = section(s)
    ok(f'{s} uses no protocol term itself', not any(re.search(r'\b' + re.escape(w), t) for w in TERMS))

# Ratification (26 November 2026): every amendment row is marked RATIFIED and the ledger records it as CA-43.
ledger = open('docs/AMENDMENTS_PENDING.md', encoding='utf-8').read()
ok('every AMENDMENT row of Appendix D is marked RATIFIED', all('RATIFIED' in r[4] for r in rows if r[4].startswith('AMENDMENT')))
ok('the ledger records A-1 to A-4 as CA-43, ratified by ESC', re.search(r'^## CA-43: .*RATIFIED by ESC', ledger, re.M) is not None
   and all(a in ledger[ledger.index('## CA-43'):] for a in ('A-1', 'A-2', 'A-3', 'A-4')))

print(f'{sum(R)} of {len(R)} checks PASS')
sys.exit(0 if all(R) else 1)
