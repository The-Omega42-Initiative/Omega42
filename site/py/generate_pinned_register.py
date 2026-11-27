#!/usr/bin/env python3
"""Generate a pinned Observatory page from an explicitly selected Git revision.
No certificate execution, ratification or deployment is performed.
"""
import argparse, html, json, re, subprocess
from pathlib import Path

FIELDS = ("id","statement","domain","derivation","tool","check","depends","does_not_follow","status")
BASE = "https://github.com/The-Omega42-Initiative/Omega42/blob/"
def render(rows, revision):
    if not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise ValueError("Full immutable commit SHA required")
    if not rows:
        raise ValueError("Empty register")
    seen = set()
    e = html.escape
    blocks = []
    for row in rows:
        if any(not isinstance(row.get(k), str) or not row[k].strip() for k in FIELDS):
            raise ValueError("Missing or invalid record field")
        ident = row["id"]
        if not re.fullmatch(r"MF-\d+", ident) or ident in seen:
            raise ValueError("Invalid or duplicate ID: " + ident)
        seen.add(ident)
        if not re.fullmatch(r"tools/[a-zA-Z0-9_/-]+\.py", row["tool"]):
            raise ValueError("Unexpected certificate path")
        if not (row["status"] == "EXACT" or row["status"].startswith("CONDITIONAL on ")):
            raise ValueError("Unrecognized inherited status")
        detail = "".join("<dt>"+label+"</dt><dd>"+e(row[key])+"</dd>" for label,key in [
            ("Domain","domain"),("Derivation","derivation"),("Dependencies","depends"),
            ("Does not follow","does_not_follow"),("Expected check marker","check")])
        link = BASE+revision+"/"+row["tool"]
        blocks.append(f'<details id="{ident}"><summary>{ident} — {e(row["status"])} — {e(row["statement"])}</summary><dl>{detail}<dt>Certificate source (not executed)</dt><dd><a href="{link}">{e(row["tool"])}</a></dd></dl></details>')
    return ('<!--{"title":"Pinned mathematical register","desc":"Exact source records and audit references","nav":"mathematics"}-->\n'
        '<section class="stack"><h1>Pinned mathematical register</h1>'
        f'<p>Snapshot {revision}. {len(rows)} records. Status is inherited verbatim; no certificates were executed by this generator.</p>'
        f'<p><a href="{BASE}{revision}/records/math/results.json">Machine-readable source</a> · <a href="open-mathematics.html">Audit protocol</a></p>'
        '<label for="mf-search">Search mathematical records</label><input id="mf-search" type="search"><p id="mf-count" role="status"></p><div id="mf-records">'
        + "\n".join(blocks) + '</div></section><script>(()=>{const q=document.getElementById("mf-search"),r=[...document.querySelectorAll("#mf-records details")],c=document.getElementById("mf-count");function update(){let n=0;for(const x of r){x.hidden=!x.textContent.toLowerCase().includes(q.value.trim().toLowerCase());if(!x.hidden)n++;}c.textContent=n+" of "+r.length+" records";}q.addEventListener("input",update);update();})();</script>\n')

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("revision",help="Explicitly reviewed ratified Git revision")
    p.add_argument("--output",default="site/pages/pinned-register.html")
    p.add_argument("--check",action="store_true")
    a=p.parse_args()
    if not re.fullmatch(r"[0-9a-f]{40}",a.revision): p.error("Full SHA required")
    raw=subprocess.check_output(["git","show",a.revision+":records/math/results.json"])
    rows=json.loads(raw)["results"]
    result=render(rows,a.revision)
    target=Path(a.output)
    if a.check:
        if target.read_text(encoding="utf-8")!=result: raise SystemExit("FAIL: stale or altered page")
        print(f"PASS: {len(rows)} pinned records")
    else:
        target.write_text(result,encoding="utf-8")
        print(f"Generated {len(rows)} records; certificates NOT EXECUTED")
if __name__=="__main__": main()
