# Browser tests of both WEB-02 entries

**By:** Claude, for the Originator (ESC) and ChatGPT · **Date:** 25 November 2026

## Method

- **Pinned commits:** ChatGPT's entry `chatgpt-omega42-website` at 41db1c8 (`design-chatgpt/`, 7 pages). Claude's entry `claude-omega42-website`, the site built from the design tree with `tools/site_build.py`.
- **Viewports:** desktop 1440 × 900, and an iPhone 13 phone (390 × 844, its own device scale).
- **Each page was checked for:**
  - console errors and page errors;
  - failed local requests;
  - horizontal overflow;
  - anchors that point nowhere;
  - form controls with no label;
  - the number of h1 headings and the page language.
- **Interaction:** every visible button was pressed once.
- **Links:** every internal link of Claude's 290-page build was resolved.
- **Tools:** headless Chromium with Playwright. Screenshots were kept for the comparison.

## ChatGPT's entry (41db1c8)

| Page | Instruments | Desktop | Phone |
|---|---|---|---|
| index.html | homepage, emblem with pause | clean | clean |
| explore.html | Seven Veils, Arcana | clean | clean |
| worlds.html | Affinity, sixteen gateways | clean | clean |
| creative.html | Harmonia, Atelier | clean | clean |
| imagination.html | Scriptorium, Synesthesia | clean | clean |
| solve.html | SOLVE formulation studio | clean | clean |

"Clean" means all of the following held:
- no console or page errors;
- no overflow;
- no broken anchors;
- every control labeled;
- one h1;
- `lang="en"`;
- every button worked.

All 12 page loads passed (6 pages × 2 viewports). README.md is the seventh file in the folder.

**Mathematics checked in the source:**
- Seven Veils reads a mod 7 after t steps of N(a, b) = (b, a + b) mod 9, as in MF-194.
- Harmonia plays the (2, 5) orbit, period 24, at base · 2^(a/9).
- Synesthesia's 256.6 Hz for (2, 5) is 220 · 2^(2/9).

**Findings, for ChatGPT to weigh:**
1. **Phone header.** The navigation wraps to three rows and stays fixed, so it covers about a quarter of the phone screen. A collapsible menu would return that space.
2. **Arcana's checkboxes on the phone.** The boxes wrap so that a box can sit nearer the next number than its own. Wrapping each box with its number in one label element would fix that.
3. **Scope.** The entry is seven pages. It does not yet carry the library, the protocol, the derivations or the Co-Builder exchange; it links to the live site for those. The Originator should know this when comparing the two entries.
4. **Data.** All instruments run in the browser, store nothing, and play audio only on request. This meets CB-024's conditions.

## Claude's entry

| Page | Desktop | Phone |
|---|---|---|
| index, philosophy, observatory, mathematics, derivations, aperture, cobuilder, explore, vision | clean | clean |

All 290 pages built, with 0 broken internal links.

**Two things only appear when the pages are opened from disk (file://):**
- Google Fonts cannot be fetched in the test sandbox.
- `api/library.json` cannot be fetched over file://.

Over HTTP, the home page, the Observatory, Explore and the Playground loaded with no errors.

**One finding, fixed:** the Observatory's third observer-phase input had no accessible name. It now carries `aria-label="Observer 3 phase"`, on the design branch (6adc377) and in the release tree.

## When the website goes live

Main and the live site stay unchanged until the Originator chooses (CB-023). After the choice, going live takes three steps:
1. The chosen design is merged onto `release/2026-11-25`.
2. The full release pipeline runs: 69 steps, about 30 minutes, and every step must pass.
3. The result is pushed to main. GitHub Pages then publishes it, usually within minutes.

ChatGPT has not yet declared its entry final. The screenshot comparison at pinned commits follows that declaration.
