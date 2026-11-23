# D4 — Introduction, Core Correspondence and Register Validation

**Status:** Isolated D4 harness implemented. The latest workflow is queued; no D4 pass is claimed.
**Prepared:** 23 November 2026
**Branch:** `proposal/path-b-release-packaging`
**Canonical implementation:** `tools/intro_output.py`
**Harness:** `tools/path_b_d4_introduction_test.py`
**Workflow:** `.github/workflows/path-b-d4-introduction.yml`
**Latest workflow:** [45163422397](https://github.com/The-Omega42-Initiative/Omega42/actions/runs/45163422397) — queued at last check

## 1. D4 scope

D4 validates the Introduction-to-Omega42 output and its declared textual correspondences with the Core and two supporting registers. It does not certify the truth of the philosophical, mathematical or legitimacy arguments.

The test deliberately separates:
- the Opening given on "Welcome Navigator";
- the full Introduction and Words Explained;
- exact correspondence between the Introduction and Core IN-OPEN / IN-00;
- the legitimacy register's argument-to-Core mapping;
- the Philosophical Register's passage-to-Core mapping.

## 2. Isolated package closure

The harness copies these six inputs into a temporary package:

- `tools/intro_output.py`
- `records/introduction/introduction.json`
- `records/introduction/legitimacy.json`
- `records/introduction/philosophy.json`
- `examples/introduction_opening.txt`
- `docs/Omega42_Core_Specification_V335_Rev450_STABLE.docx`

The renderer/checker uses Python standard-library modules, including `json`, `zipfile`, `html` and `re`. No third-party Python package is declared by this profile. The Core DOCX is read as a ZIP/XML document; it is not modified.

## 3. Validation commands

The harness executes:

1. `--selftest` — 13 internal cases covering render/check consistency, paragraph order, missing or summarized text, Friendly Notes placement, AI caveat placement and date boundary, close/signature, and vocabulary coverage.
2. `--terms` — Words Explained consistency.
3. `--check examples/introduction_opening.txt` — canonical Opening example.
4. `--core CORE.docx` — IN-OPEN / IN-00 correspondence, including the eight reasons and main reason.
5. `--legitimacy CORE.docx` — legitimacy register arguments against the Introduction and their grounds in the Core.
6. `--philosophy CORE.docx` — Philosophical Register passages and figures against Part 0 of the Core.
7. `--render` with an explicit Navigator, organisation, date (23 November 2026) and SCRIPT-CAPABLE execution label; then `--check` on the exact rendered output. It also round-trips `--first-render` through `--first` to validate the Friendly Notes and Navigator Identity Block close.

The render is written only inside the temporary package. The repository's canonical JSON, Core DOCX, example and registers are read-only inputs.

## 4. What the checks establish

If the workflow passes, it will establish that:
- the isolated renderer can load the Introduction source data;
- the Opening output matches the current declared text and order;
- the current Words Explained glossary covers the vocabulary used;
- the Core's IN-OPEN and IN-00 sections carry the corresponding Opening/Introduction text under the checker's exact comparison rules;
- the eight reasons and main reason are present as declared;
- the legitimacy and philosophical registers match the specified textual locations;
- a current-date rendered Opening passes the same checker.

It will not establish that the reasons are persuasive, the philosophical positions are true, the claims are empirically verified, or the Introduction's framing is universally accepted. Those are interpretive and substantive questions beyond this mechanical correspondence profile.

## 5. Scope limitations and future tests

The harness round-trips the renderer's first-navigation close template through `--first`. This checks the Friendly Notes and Navigator Identity Block structure. It is a template round-trip, not a check of a real first-navigation record from a live session.

The profile tests the Opening and its Core/register correspondence. It does not validate every website page, every Navigator output form, or every language adaptor.

## 6. Workflow and authority

The latest isolated workflow [45163422397](https://github.com/The-Omega42-Initiative/Omega42/actions/runs/45163422397) was queued at last check. No result is assumed.

- Path B remains a proposal.
- No canonical Introduction, JSON register, Core or Companion file has been changed by this harness.
- No release policy or L-493 requirement has been changed.
- No package has been released or certified.
- This report is a review artefact, not a message to Claude. No Claude communication has occurred.
