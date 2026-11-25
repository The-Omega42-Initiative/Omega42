#!/usr/bin/env python3
"""companion_compact.py -- the Companion Document in brief, for AI systems with small context windows.

The Companion's prose edition (ai/Omega42_Companion_V335_Rev450.md, rendered from the .docx by tools/ai_edition.py) runs to
about 500,000 tokens. This tool renders, from that edition and never by hand, a compact edition that fits a small window:

    ai/Omega42_Companion_Compact.md

It holds, in the Companion's own words:
  1. "How to read this Companion Document", whole;
  2. the Preamble's opening paragraphs, up to a share of the budget;
  3. for every Part, in order: its heading (with its status label), the size of the full Part in estimated tokens, and the
     opening sentences of the Part, cut at a sentence boundary;
  4. how to retrieve any Part in full (ai/manifest.json lists every section with its size and SHA-256).

Nothing is paraphrased: every line after the header is a verbatim excerpt. The compact edition is a guide to the Companion,
not a replacement for it; where it and the full text differ in force, the full text governs.

    python3 tools/companion_compact.py --build [--budget 24000]   # write the compact edition (default budget 24,000 tokens)
    python3 tools/companion_compact.py --check  [--budget 24000]  # the file is current and within its budget
    python3 tools/companion_compact.py --selftest

Tokens are estimated as characters / 4, the rule tools/ai_edition.py uses. Standard library only.
"""
import hashlib, os, re, sys
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(REPO, 'ai', 'Omega42_Companion_V335_Rev450.md')
OUT = os.path.join(REPO, 'ai', 'Omega42_Companion_Compact.md')
DEFAULT_BUDGET = 24000

def tok(s): return len(s) // 4

def sections(text):
    """[(heading, body)] split on Markdown headings."""
    parts, head, buf = [], '(front matter)', []
    for line in text.split('\n'):
        m = re.match(r'^#{1,6} (.*)$', line)
        if m:
            parts.append((head, '\n'.join(buf).strip())); head, buf = m.group(1).strip(), []
        else:
            buf.append(line)
    parts.append((head, '\n'.join(buf).strip()))
    return parts

SENT = re.compile(r'(?<=[.!?])\s+(?=[A-Z0-9"“(Ω])')

LABEL = re.compile(r'^\d+(?:\.\d+)*\s+(?:Scope|Index|What this part is|Status[^.]*|Purpose)\.\s*')

def lead(body, limit):
    """Opening sentences of the Part, at most `limit` characters, verbatim. A bare section label ("140.1 Scope.") is dropped;
    sentences are taken whole while they fit, and if fewer than half the limit is filled the next sentence is cut at a word
    boundary and marked with an ellipsis."""
    for para in body.split('\n'):
        p = para.strip()
        if len(p) < 40 or p.startswith(('|', '```', '---')):
            continue
        p = LABEL.sub('', p)
        if len(p) < 40:
            continue
        out = ''
        for s in SENT.split(p):
            if len(out) + len(s) + 1 > limit:
                if len(out) < limit // 2:
                    room = limit - len(out) - 2
                    cut = s[:room].rsplit(' ', 1)[0]
                    if cut:
                        out = (out + ' ' + cut).strip() + ' …'
                break
            out = (out + ' ' + s).strip()
        return out
    return ''

def build(budget=DEFAULT_BUDGET):
    text = open(SRC, encoding='utf-8').read()
    src_sha = hashlib.sha256(text.encode('utf-8')).hexdigest()
    secs = sections(text)
    get = lambda name: next((b for h, b in secs if h.startswith(name)), '')
    howto = get('HOW TO READ THIS COMPANION DOCUMENT')
    pre = get('PREAMBLE')
    # group sections by Part: a Part runs from its 'PART n' heading to the next one
    parts, cur = [], None
    for h, b in secs:
        if re.match(r'PART \d', h):
            cur = [h, b, tok(b)]; parts.append(cur)
        elif cur is not None and not re.match(r'(APPENDIX|Appendix)', h):
            cur[2] += tok(b)
            if not cur[1]:
                cur[1] = b
    header = ('# Ω42 Companion Document — compact edition for small context windows\n\n'
              'Rendered by tools/companion_compact.py from `ai/Omega42_Companion_V335_Rev450.md` (SHA-256 %s), itself rendered from '
              'docs/Omega42_Companion_Document_V335_Rev450_STABLE.docx. Paired release: read with the Core Specification V335 Rev.450 STABLE; '
              'for a navigation, the Navigator Pack (`ai/Omega42_Navigator_Pack.md`) is the essential reading.\n\n'
              'Every line below the rule is a verbatim excerpt; nothing is paraphrased. Each Part shows its heading with its status label, '
              'the size of the full Part, and its opening sentences. To read a Part in full, retrieve it by its heading from the full edition; '
              '`ai/manifest.json` lists every section with its size and SHA-256. Where this edition and the full text differ in force, the full '
              'text governs. Status labels: CDT-A discovered and verified, CDT-B constructed and chosen, CDT-C generated within the frame.\n\n---\n\n'
              % src_sha[:16])
    fixed = header + '## How to read this Companion Document\n\n' + howto + '\n\n'
    # Preamble: up to 12% of the budget
    pre_paras, used = [], 0
    for p in pre.split('\n'):
        if p.strip() and used + tok(p) <= budget * 0.12:
            pre_paras.append(p.strip()); used += tok(p)
    fixed += '## From the Preamble\n\n' + '\n\n'.join(pre_paras) + '\n\n## The Parts, in order\n\n'
    remaining = budget - tok(fixed) - 200
    # per-Part lead length chosen so every Part fits
    per = max(80, min(600, (remaining * 4) // max(1, len(parts)) - 120))
    while True:
        lines = []
        for h, b, n in parts:
            ld = lead(b, per)
            lines.append('**%s** (~%s tokens in full)\n%s\n' % (h, format(n, ','), ld))
        body = '\n'.join(lines)
        if tok(fixed + body) <= budget or per <= 80:
            break
        per -= 20
    out = fixed + body + '\n---\n%d Parts. Compact edition ~%s tokens (characters / 4), budget %s.\n' % (
        len(parts), format(tok(fixed + body), ','), format(budget, ','))
    return out, len(parts)

def main(a):
    budget = DEFAULT_BUDGET
    if '--budget' in a:
        budget = int(a[a.index('--budget') + 1])
    if '--build' in a:
        out, n = build(budget)
        open(OUT, 'w', encoding='utf-8').write(out)
        print('wrote %s: %d Parts, ~%d tokens (budget %d)' % (os.path.relpath(OUT, REPO), n, tok(out), budget)); return 0
    if '--check' in a:
        out, n = build(budget)
        cur = open(OUT, encoding='utf-8').read() if os.path.exists(OUT) else ''
        ok = cur == out and tok(out) <= budget + 100
        print('COMPANION COMPACT: %s (%d Parts, ~%d tokens, budget %d)' % ('PASS' if ok else 'NOT CURRENT', n, tok(cur), budget)); return 0 if ok else 1
    if '--selftest' in a:
        ok = True
        t = 'Alpha one is here. Beta two is quite a bit longer. Gamma.'
        ok &= lead(t, 30) == 'Alpha one is here.' and lead(t, 60) == t and lead(t, 44) == 'Alpha one is here. Beta two is quite a bit …'
        ok &= lead('140.1 Scope. ' + t, 30) == 'Alpha one is here.'
        ok &= [h for h, _ in sections('x\n### PART 1: A\nb\n### 1.1 B\nc')] == ['(front matter)', 'PART 1: A', '1.1 B']
        out, n = build(DEFAULT_BUDGET)
        ok &= tok(out) <= DEFAULT_BUDGET + 100 and n > 200 and '## How to read this Companion Document' in out
        src = open(SRC, encoding='utf-8').read()
        body = out.split('## The Parts, in order')[1]
        excerpts = [l for l in body.split('\n') if l and not l.startswith(('**', '---')) and not re.match(r'^\d+ Parts\.', l)]
        bad = [e for e in excerpts if any(seg.strip() and seg.strip() not in src for seg in e.rstrip(' …').split('. '))]
        ok &= not bad  # every excerpt is verbatim (checked sentence by sentence)
        if bad: print('not verbatim:', bad[:3])
        print('COMPANION COMPACT SELFTEST:', 'PASS' if ok else 'FAIL'); return 0 if ok else 1
    print(__doc__); return 2

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
