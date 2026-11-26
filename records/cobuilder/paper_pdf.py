"""Typeset a Markdown document of docs/ as PDF (A4) with the site's Markdown renderer and Chromium: by default the mathematical paper.
Needs Playwright. Run from the repository root: python3 records/cobuilder/paper_pdf.py [docs/NAME.md]"""
import os, re, sys, tempfile
sys.path.insert(0, 'tools')
import site_build as sb
from playwright.sync_api import sync_playwright
CSS = '''body{font-family:"DejaVu Serif",Georgia,serif;font-size:10.5pt;line-height:1.5;color:#111}
h1{font-size:20pt;text-align:center;margin:0 0 4pt} .sub{font-size:12.5pt;text-align:center;font-style:italic;margin:0 0 10pt}
h2.part{font-size:14pt;text-align:center;margin:22pt 0 6pt;break-before:page;letter-spacing:.03em}
h2{font-size:13pt} h3{font-size:12.5pt;margin:16pt 0 4pt;break-after:avoid} h4{font-size:11pt;margin:10pt 0 3pt;break-after:avoid}
p{margin:5pt 0;text-align:justify;hyphens:auto} ul{margin:4pt 0;padding-left:16pt} li{margin:2pt 0}
code{font-family:"DejaVu Sans Mono",monospace;font-size:8.5pt} table{border-collapse:collapse;margin:6pt auto;font-size:9.5pt;break-inside:avoid}
th,td{border:0.6pt solid #888;padding:3pt 7pt;text-align:left} th{background:#f1ece0} .byline{text-align:center;font-size:9.5pt;color:#333}'''
SRC = sys.argv[1] if len(sys.argv) > 1 else 'docs/OMEGA42_MATHEMATICAL_PAPER.md'; OUT = SRC[:-3] + '.pdf'
src = open(SRC, encoding='utf-8').read()
title, body = src.split('\n', 1)
h = re.sub(r'<h2 id="(part-[^"]*)">', r'<h2 class="part" id="\1">', sb.md_html(body)).split('\n')
h[0] = re.sub(r'<p><b>(.*)</b></p>', r'<p class="sub">\1</p>', h[0]); h[1] = h[1].replace('<p>', '<p class="byline">')
tmp = os.path.join(tempfile.mkdtemp(), 'paper.html')
open(tmp, 'w', encoding='utf-8').write('<!doctype html><meta charset="utf-8"><title>%s</title><style>%s</style><h1>%s</h1>%s' % (title[2:], CSS, title[2:], '\n'.join(h)))
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(); pg.goto('file://' + tmp)
    pg.pdf(path=OUT, format='A4', margin=dict(top='22mm', bottom='22mm', left='20mm', right='20mm'), display_header_footer=True,
           header_template='<span></span>', footer_template='<div style="font-size:8pt;width:100%;text-align:center;color:#555">' + title[2:] + ' · <span class="pageNumber"></span> / <span class="totalPages"></span></div>')
    b.close()
print('wrote', OUT)
