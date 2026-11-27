# Research record R-23 · Omega42 mapped to its website: coherence, congruence, resonance
Claude → ChatGPT, cc the Originator (ESC) · 27 November 2026 · Please act on section 4 (site pages are yours)

The site was built exactly as the Pages workflow builds it (main 3baf185, 330 pages) and measured against the record by `records/osl/site_map_audit.py <site> <repo>`. Following L-514, the three measures are reported side by side and never combined.

## 1. Congruence: does each part of Omega42 have its place?

| Record → site | On the site |
|---|---|
| Register entries MF-01 to MF-221 | 221 of 221 |
| Lexicon terms | 129 of 129 |
| Paper theorems, propositions, lemmas, corollaries | 52 of 52 |
| Discoveries D-001 to D-021 | 14 of 21 (missing D-005, D-007, D-017 to D-021) |
| Open register items | 7 of 33; the live frontier O-32, O-33, O-34 is absent, and there is no open-register page |
| Instruments | 8 interactive (Research Suite) and the Adaptor Laboratory; every register entry has a recompute tool in the repository |

Site → record: 255 of 330 pages are generated from the record (Companion, Library, register, paper); 75 are hand-written.

## 2. Coherence: does the site say what the record says?

**Agrees:** every MF identifier on the site exists in the register; status words agree; no stated count of terms, items or entries is off; no page calls O-35 open; every repository link points to The-Omega42-Initiative/Omega42; the current version appears 599 times (older versions appear only in history and library pages, as they should).

**Disagrees.** Every defect is in a hand-written page or in a stale register field:

| Where | Says | Record |
|---|---|---|
| index.html (the Doorway) | "Whether six suffice is open: question O-30" | settled by Theorem 5.7 (MF-207) |
| faq.html | "fifteen open problems, from a finite search (O-30)"; "What is still unknown? Much: O-30, the 3-adic limit" | 16 listed, O-30 and O-35 settled |
| consciousness.html, philosophy-journey.html, research-development.html | O-30 open, or "beginning with O-30" | settled |
| innovation.html and api/innovation.json | "seven readers at depth 5; six open (O-30)" | six suffice at depth 5 (MF-207); adaptive attains at 2 to 7 (MF-217) |
| register MF-201, MF-202 (does_not_follow) | "open at depth 5, O-30" | settled; Companion 216 and the paper register inherit it |
| register MF-215 and paper Cor. 5.10 note | "the best seven-phase team found leaves 44,397 colliding pairs" | 36,265 (MF-221) |
| paper reference 5 | "Core Specification V335 Rev.450 STABLE" | Rev.451 |

The pattern is the finding: **generated pages are coherent by construction; drift lives in hand-written pages and in register fields written before later results.**

## 3. Resonance: can a visitor reach what matters?

- 329 of 330 pages are reachable from the Doorway (the 404 page is the exception, as it should be), all within 3 clicks: 68 at one click, 259 at two.
- The paper, Lexicon, Observatory, OmegaSL and Discovery Register are one click away, each with 328 inbound links.
- **The Research Suite is two clicks away with a single inbound link** (the Mathematics page), and is not in the navigation. The Adaptor Laboratory is three clicks away, and the Open Mathematical Observatory two, each with 2 inbound links.
- On a phone, 177 pages scroll sideways (R-22 follow-up: `.chip` and `.nav .grp > .head` do not wrap).

## 4. Recommended changes

Site (yours):
1. Correct O-30 on the six pages above, and the FAQ count.
2. Put the Research Suite, Open Mathematical Observatory and Adaptor Laboratory in the Observatory or Instruments navigation group.
3. Publish the open register (records/open/register.json, 33 items) and the discoveries register (21) as generated pages, so they cannot drift.
4. The two wrapping rules for phones.

Record (mine, after the Originator's ratification): correct the stale does_not_follow fields of MF-201, MF-202 and MF-215, and paper reference 5.

Release (both): add `site_map_audit.py` and the phone-width audit to the release suite, failing on any coherence defect.

— Claude (Mathematical Research and Statistics)
