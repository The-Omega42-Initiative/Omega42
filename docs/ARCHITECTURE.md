# Repository architecture

How the Omega42 repository is organized, built, checked and released. Written for Co-Builders, contributors and AI systems working on the repository.

## The two documents are the release

Omega42 is defined by two Word documents in `docs/`:

- the **Core Specification** (normative);
- the **Companion Document** (explanatory).

Under the self-containment law L-493, **every file in the repository is embedded in them**: the scripts and records in the Companion's appendices, and the site sources and tools alongside them. A release is valid only if anyone can rebuild the whole repository from the two documents alone. That is why every change, however small, passes through the release pipeline before it reaches `main`.

## The map

| Path | What it holds |
|---|---|
| `docs/` | The two release documents; the founding vision (`VISION.md`); the Constitution (`CONSTITUTION.md`); policies and reviews |
| `ai/` | Plain-text editions for AI systems: the Core, the Companion, the Navigator Pack and a token manifest |
| `site/` | The website sources: `pages/*.html` (each opens with a JSON header giving title, description, nav key and any scripts), `assets/` (style, scripts) and the layout |
| `tools/` | Python tools: `site_build.py` (builds the website and its data files), `release_manifest.py`, the protocol and mathematics tools, and `build/` (the release pipeline) |
| `records/` | The record: registers, investigations, recomputation scripts and their outputs. `records/cobuilder/` holds the Co-Builder exchange. |
| `research/` | Research areas and the Speculative Foundations program |
| `library/` | Library editions of historical documents, with recomputation notes |
| `agents/` | Specifications for scheduled Navigators, such as the Frontier Navigator of the Discovery Bulletin |
| `governance/`, `community/`, `submissions/`, `examples/` | Governance records, community material, submissions and worked examples |

## Building the website

```
python3 tools/site_build.py --out /path/to/site    # builds every page and data file
python3 tools/site_build.py --selftest               # checks the build
```

How a page is built:

1. The build places each page's body into the layout.
2. It fills the `{{PLACEHOLDERS}}`: version, repository, download links and sizes, the lead discovery, the questions, the Co-Builder ledger and messages, and others.
3. It fails if any `{{` is left over.

The navigation groups are defined in `NAV` in `site_build.py`. GitHub Pages publishes the `main` branch.

## The release pipeline

```
python3 tools/release_manifest.py --build
bash tools/build/pipe.sh > pipe.txt 2>&1      # about 30 minutes
grep -E "STEPS|^FAIL|SUMS" pipe.txt           # must read: STEPS 69, FAILED 0 · SUMS OK
```

The pipeline does four things:

1. Re-embeds every file in both documents (`tools/build/embed_all.py`).
2. Regenerates the AI editions.
3. Runs every self-test, including:
   - the re-examination check (`tools/reexamine.py`);
   - extraction and verification of the embedded files;
   - the site build.
4. Writes `SHA256SUMS`.

Two rules for new files:

- **New record folders** need a line in `tools/reexamine.py`, either as an investigation or as exempt reference data.
- **New recomputation scripts** belong under `records/<area>/`, where they are embedded in the Companion's Appendix C.

## Branches

| Branch | Use |
|---|---|
| `main` | The release; published as the website |
| `cobuilder/mailbox` | Claude's daily Co-Builder replies awaiting the next release |
| `proposal/instruments-of-being` | ChatGPT's research proposals |
| `claude-omega42-website`, `chatgpt-omega42-website` | The two website designs in the WEB-02 comparison; the Originator chooses |
| `frontier/DF-nnn` | Staged Discovery Bulletin entries from the Frontier Navigator |

## Rules that apply to every change

- **No personal information.** The Originator is named only as "the Originator (ESC)". No personal names, e-mail addresses, Drive links or file IDs appear anywhere.
- **American spelling,** and the house word list in the Constitution's spirit: no hedging and no inflation.
- **Canonical changes** need the Originator's ratification or agreement under CBX-1 (`records/cobuilder/PROTOCOL.md`).
- **Commits** are authored as `Omega42 Navigator <navigator@omega42.invalid>`.
