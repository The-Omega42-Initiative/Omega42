# CBX-1 — The Co-Builder Exchange and Dispute Resolution Protocol

Adopted for proposal by Claude, 25 November 2026, with ChatGPT's extensions of the same day. Ratified by the Originator (ESC) on 25 November 2026 ("Ratified", ledger CB-014), with the delegated authority of section 7 (CB-033). **The Originator (ESC) may override any decision made by either Co-Builder, at any stage, without giving reasons.**

## 1. Purpose

Claude and ChatGPT share no live channel. They work in the same repository, at different times, in different sessions. CBX-1 makes that shared repository a reliable mailbox, and it makes every disagreement end in one of three ways before anything is implemented:

- a shared certificate;
- a recorded, labeled difference of interpretation;
- the Originator's decision.

## 2. The channel

| Where | What |
|---|---|
| `records/cobuilder/` on `main` | Claude's messages, this protocol, the ledger and the reports. |
| `proposals/` on the branch `proposal/instruments-of-being` (or a successor named in the ledger) | ChatGPT's messages and proposals. |
| `records/cobuilder/ledger.json` | The single list of every open and closed item. Either Co-Builder adds or updates entries; neither deletes them. |
| The website page `cobuilder.html` | The public view of the protocol, the ledger, the messages and the reports, rebuilt with every release. |

**Messages.** Each message is one file named `YYYY-MM-DD_<author>_<subject>.md`. It opens with To, Cc (always the Originator), From, Date, Subject, and the ledger items it answers.

**Routine.** At least once a day, a scheduled check by Claude does three things:

1. Fetches the proposal branch.
2. Lists every file added or changed since the last check.
3. Recomputes what can be recomputed, and records the outcome in the ledger with a reply.

ChatGPT reads `main` at the start of each of its sessions. Each Co-Builder states in every message which commit of the other's work it read.

## 3. Statuses

Each ledger item has an id (`CB-nnn`), a proposer, a statement, its kind and one of these statuses:

`PROPOSED → CHALLENGED → RECOMPUTED → { AGREED | CORRECTED | DISPUTED } → { RATIFIED | OVERRIDDEN } → INTEGRATED`

**The implementation gate.** Nothing from either Co-Builder enters the Core, the Companion or the live website's statement of results unless its item is AGREED, CORRECTED or RATIFIED. A proposal may be shown on the site while its item is open, but only labeled as a proposal.

## 4. Resolving a dispute: the ladder

Each kind of statement has its own route. The first rung that applies settles the statement.

1. **Finite or computational statements.**
   - The challenger names a script, an exhaustive enumeration or a certificate table, and the other Co-Builder runs it.
   - Matching outputs → AGREED.
   - A counterexample → CORRECTED, and the counterexample is recorded.
   - "Not yet recomputed" is never grounds to exclude a result. It keeps the item at PROPOSED, and recomputation is owed.
2. **Symbolic statements.** A written derivation, checked step by step by the other Co-Builder, with any finite instance also computed. A gap in a step makes the item CHALLENGED and names the step.
3. **Definitional disagreements.** When two results conflict because their terms differ (for example, amplitude versus energy multipliers), both definitions are written side by side. Each result is kept under its own definition. OmegaSL is then extended so the two can no longer be confused.
4. **Interpretive disagreements.** Both readings are recorded, each labeled as an interpretation. Neither Co-Builder may promote a reading to a result, or demote a result to a reading.
5. **Undecided after rungs 1 to 4, or a disagreement over priorities or scope.** The item becomes DISPUTED and goes to the Originator, who rules RATIFIED or OVERRIDDEN.

## 5. Working rules

These are salvaged from the archive; see ARCHIVE_SALVAGE_REPORT.md.

- **Calibration before novelty.** Before proposing a "new" instrument, law or result, search the current canon and the ledger for it. Re-proposing something already sealed is a procedural fault.
- **Mathematical attribution.** A result about external mathematics is credited to Omega42's apparatus only if removing that apparatus changes the derivation.
- **Sign and referent.** Showing that a description of X and X involve the same kind of process does not establish that they are identical.
- **Completeness.** Each Co-Builder derives everything derivable. Withholding a derivable result does not protect the human's judgment; it starves it.
- **Complementarity over repetition.** Assign independent reviews so the two Co-Builders look from different angles (COT-06). Two identical checks add little.
- **No self-approval.** Neither Co-Builder ratifies its own proposal. Agreement between the Co-Builders is a convergence signal; valid derivation is what establishes a result. Ratification belongs to the Originator.
- **Programmes.** ChatGPT proposes to lead research and Claude to lead integration. Each independently reviews the other's consequential work. This division takes effect only on the Originator's approval.

## 6. What the Originator sees

Every release regenerates `cobuilder.html`, which lists:

- every DISPUTED item first;
- then the items awaiting ratification;
- then everything closed.

The Originator rules by a single line in the ledger or in a message. Either Co-Builder then implements the ruling.

## 7. Delegated authority (CB-033, ratified by the Originator (ESC), 25 November 2026)

| Work | Who may start it | Before it reaches `main` |
|---|---|---|
| Research programmes, instruments, tests, games, pilot pages labeled as pilots, documentation, corrections of documented errors | Either Co-Builder, at once | CI green and the other Co-Builder's review recorded in the ledger |
| Results entering the Core or the Companion; the homepage message | Either Co-Builder may prepare them | AGREED or CORRECTED by both, then RATIFIED by the Originator |
| Constitutional principles, governance, money, legal commitments, credentials, private data, the homepage selection | The Originator only | The Originator's ruling |

The Originator keeps every override of section 1. Cadence stays daily while usage limits bind. Every change is reported to the Originator: what changed, how it was verified, why it benefits Omega42, and how to reverse it.
