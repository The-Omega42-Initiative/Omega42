"""mv.py -- the paragraph moves of the build kit, imported by embed_all.py: cut a range of paragraphs, insert XML after a paragraph, and write new paragraphs in the style of an existing one (tools/build/README.md)."""
import sys, re, html
sys.path.insert(0, '/home/claude')
from dx import Doc


def cut(D, s, e):
    """remove paragraphs s to e - 1 (indices of D.paras()), and everything that lies between them"""
    ps = D.paras()
    if e <= s: return
    a, b = ps[s][0], ps[e - 1][1]
    D.x = D.x[:a] + D.x[b:]


def insert_after(D, i, xml):
    """insert the XML text directly after paragraph i"""
    b = D.paras()[i][1]
    D.x = D.x[:b] + xml + D.x[b:]


def para_like(D, like, texts):
    """paragraphs carrying each text, in the paragraph and run style of the first paragraph that starts with like"""
    src = next((D.x[a:b] for a, b, t in D.all() if t.startswith(like)), None)
    if src is None: src = next(D.x[a:b] for a, b, t in D.all() if like in t)
    ppr = re.search(r'<w:pPr>.*?</w:pPr>', src, re.S)
    rpr = re.search(r'<w:rPr>.*?</w:rPr>', src[ppr.end() if ppr else 0:], re.S)
    return ''.join('<w:p>' + (ppr.group(0) if ppr else '') + '<w:r>' + (rpr.group(0) if rpr else '') +
                   '<w:t xml:space="preserve">' + html.escape(t, quote=False) + '</w:t></w:r></w:p>' for t in texts)
