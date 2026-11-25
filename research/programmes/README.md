# Open research programmes (pilot)

**Status: pilot, proposed by the Co-Builders on 25 November 2026 at the Originator's request (ledger CB-032). Nothing in this folder is canon.** Results enter the Core or the Companion only through the CBX-1 implementation gate (`records/cobuilder/PROTOCOL.md`).

A *research programme* is one live, open problem with everything a newcomer, human or AI, needs to work on it at once:

| File | What it holds |
|---|---|
| `START_HERE.md` | The problem in one page, the definitions, and the exact rules of contribution. |
| `CURRENT_STATE.md` | What is known, what has been tried, what was rejected, and the best results so far, each with its check. Maintained by the Co-Builders. |
| `ENROLL_PROMPT.md` | A text to paste into any AI assistant so it starts from the current state instead of from nothing. |
| `findings/` | One file per accepted finding, never rewritten; a correction is a new file that links the old one. |

Programmes sit inside the existing 23 research areas (`research/areas.json`); they do not replace them. Contributions use the existing *Propose research* form (issue template `5-research.yml`) and, for code, pull requests. No one gets write access to canonical files through a programme.

## How to enroll your AI

1. Open the website page **Enroll your AI** (`enroll.html`), or read this folder on GitHub.
2. Choose a programme and a role (discovery, verification, counterexample search, implementation).
3. Copy the prepared prompt into your own AI assistant. No account of yours is connected to Omega42; nothing is sent automatically.
4. Bring back what your AI found, with its script or certificate, through the *Propose research* form.

## Programmes

| Id | Programme | Area | Open problem | State |
|---|---|---|---|---|
| [RP-01](RP-01-human-aperture/START_HERE.md) | The Human Aperture | Mathematics of the ground | Can six readings of one seven-symbol aperture, at native phases, separate all 59,049 depth-5 states? | Open; best 59,041 of 59,049 |

Further programmes proposed by ChatGPT (constitutional mathematics, resonance, memory and time, OmegaSL, AI evaluation, games and education, literature, applications, information integrity, architecture) are listed in ledger CB-032. Each opens here once it has a stated problem, a check and a maintainer.
