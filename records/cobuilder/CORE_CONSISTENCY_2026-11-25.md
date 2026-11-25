# Consistency check: Core Specification and Companion Document V335 Rev.450 STABLE

**For:** the Originator (ESC) · **By:** Claude, Co-Builder · **Date:** 25 November 2026 · **Ledger:** CB-041, CB-042
**Documents checked:** `docs/Omega42_Core_Specification_V335_Rev450_STABLE.docx` and `docs/Omega42_Companion_Document_V335_Rev450_STABLE.docx`, as released on `main` at b0ed7e3 (25 November). They are identical on `cobuilder/mailbox` and `claude-omega42-website`. The copies on `proposal/instruments-of-being` are the older 20 November build.

## Verdict

**No conflicts.** Every automated check of the release passes, and so do 18 independent recomputations of the Core's arithmetic. The check found:

- one stale set of cross-references in the Companion;
- one notation overlap inside the Core;
- one unstated convention in Fact 1.

None of these changes a computed value. The first and third need a supervised edit of a canonical document, so they are listed for the Originator.

## 1. The release checks (existing tools, run unchanged)

| Check | Result |
|---|---|
| `tools/consistency_check.py` with the CI arguments: version, law cross-references, Part cross-references, status, hash, counts, persuasion, typography, the word "claim", obsolete wording, spelling, duplicates | 0 conflicts, PASS |
| `tools/doc_hygiene.py`, all items | PASS |
| `tools/ai_edition.py --check` (the AI editions match the .docx) | PASS |
| `tools/release_manifest.py --check` | PASS |
| `tools/timestamp_check.py --check` | PASS, 466 submissions, 0 problems |
| `tools/foundations_check.py --selftest` | PASS |
| `tools/reexamine.py --check` | PASS |
| `tools/site_build.py --selftest` | PASS |

## 2. Independent recomputation of the Core's arithmetic (new)

`records/cobuilder/core_consistency_2026_11_25.py` recomputes what the Core states about numbers. It is pure standard library and exhaustive over each finite space: **18 checks, 0 failures.**

| Core statement | Result |
|---|---|
| Fact 1: π(9) = 24; one period sums to 117; dr(117) = 9 | holds in digits 1..9 (see 3c) |
| Fact 2: primitive roots mod 9 are exactly {2, 5}; 2 × 5 ≡ 1 | holds |
| Fact 3: doubling 1→2→4→8→7→5; the digits of 1/7 | holds |
| Fact 4: dr(6n) ∈ {3, 6, 9} in the pattern 6, 3, 9; dr(5n) covers 1..9 | holds |
| Fact 5: P(i) + P(i+12) has digital root 9 for all 12 pairs; P7 = P19 = 9 | holds |
| Introduction: "twelve steps on, the cycle is its own negative" (A¹² = −I) | holds on all 81 states |
| Fact 6: quadratic residues mod 9 are {0, 1, 4, 7}; x² = x + 1 has no root mod 9 | holds |
| 0.0.9.9: A², A³, A⁴, A⁶, A⁸, A¹² have orders 12, 8, 6, 4, 3, 2; A⁶ is a square root of −I | holds |
| 0.0.9.9: in the canonical cycle, 4 and 5 occur five times each and every other digit twice | holds |
| 1.8: the Crown {P3, P7, P11, P15, P19, P23} is exactly the positions with values 3, 6, 9; low members map to high by the antipode | holds |
| 81 = 24 + 24 + 24 + 8 + 1; K1: exactly the three 24-orbits take all nine values | holds |
| MATH-38 at k = 2: the longest period mod 81 is 216, and the complete-spectrum orbits are exactly the longest | holds (27 orbits) |
| FP-ArmNorm: Anchor × Antipode − Yin² ≡ norm, for all 81 states; F(18) = 2584 ≡ 1 | holds with the norm a² + ab − b² |
| MF-17 at depth 1: X ↦ A X Aᵀ has order 12 on the 6,561 matrices mod 9 | holds |

Ledger items AGREED since the release that touch the Core are also consistent with it:

- N¹² = −I (CB-030) is how the Core states it throughout (MF-03, MF-17, MF-142, Introduction).
- No superseded figure (57,878; "identity after twelve steps") appears in either document.

## 3. Findings for the Originator

**(a) Stale Part numbers in the Companion's "How to read this Companion Document"** (paragraphs 165 and 166 of the .docx text). This is CB-041, CHALLENGED.

| The text says | Part named | That Part's heading | The described content is in |
|---|---|---|---|
| Part 3 (counting as primitive distinction-making) | Part 3 | The Torsion Loop as the Fibonacci sequence of existence | **Part 13** |
| Part 4 (the discovered mathematical bedrock) | Part 4 | The six levels and the 24 perspectives | **Part 14** |
| Part 5 (the conditional structure and the asymmetry of inquiry) | Part 5 | The 25th perspective and the Aperture | **Part 15** |

The same paragraph's "Parts 15–16 (epistemics)" should be reviewed with these. The other pointers in the paragraph are correct: Parts 1–2, 21, 22–25 and 48.

The release checker missed this because XREF-PART only tests that a Part number exists. I added an INFO-level test, **XREF-DESC**, to `tools/consistency_check.py`. It flags a "Part N (description)" whose description shares no word with Part N's heading, and it finds exactly these three. It reports and never fails the build, so CI is unaffected.

**Proposed correction**, for the next supervised release: 3 → 13, 4 → 14, 5 → 15, and review "15–16".

**(b) N(s) names two different things in the Core.** This is a definitional matter (CBX-1 rung 3), recorded under CB-041.

| Where | N(s) means |
|---|---|
| 0.0.8.6, 0.0.8.11, MF-25 | the null embedding s sᵀ, a matrix |
| FP-ArmNorm (1.8) and nearby | the norm a² + ab − b², a residue |

Each use is clear in context, and no computation mixes them. The Co-Builder records add a third use: they write N(a, b) = (b, a + b) for the law, which the Core calls A.

**Proposal:**
- From today, Co-Builder records write the law as A, as the Core does.
- At the next supervised revision, the Core gives the norm its own letter. It already writes Q for the related form in "N(s)² = Q(s)²/4".

**(c) Fact 1's sum 117 counts residue 0 as the digit 9.** The residues themselves sum to 99. The Core's digit convention (1..9) is used everywhere else, so the statement is correct. Writing "(digits 1..9, 0 written as 9)" beside it would remove the ambiguity. This is a wording item for the next supervised revision.

## 4. The compact Companion for small context windows (CB-042)

The Companion's prose is about 505,000 tokens, too large for most context windows. The new tool `tools/companion_compact.py` renders **`ai/Omega42_Companion_Compact.md`**: about 23,000 tokens, inside a 24,000-token budget, so it fits a 32k window with room for the question.

**What it holds:**
- "How to read this Companion Document", whole;
- the opening of the Preamble;
- for each of the 238 Parts, in order: its heading with its status label, the size of the full Part, and its opening sentences;
- how to retrieve any Part in full (`ai/manifest.json`).

**How it stays faithful:**
- Every excerpt is verbatim. The selftest checks every sentence against the full edition.
- It is rendered from the AI edition, which `tools/ai_edition.py --check` ties to the .docx. `--check` fails when the compact file is out of date.
- `--budget N` renders other sizes, for example `--budget 8000` for an 8k window, with shorter openings.

It sits beside the Navigator Pack (~120,000 tokens), which remains the reading for a navigation. On the next release `llms.txt` should list it. That file is generated by `tools/ai_edition.py`, so I have not edited it by hand.

## 5. Addendum: the upgraded Core on `release/2026-11-25` (bcd978b)

The Core was upgraded later the same day, on the branch `release/2026-11-25`. It adds the register entries MF-193 to MF-206 and Companion Part 235. I repeated the check on that build.

**Release checks:**

| Check | Result |
|---|---|
| `tools/consistency_check.py` with the CI arguments | 0 conflicts. XREF-DESC reports the same three pointers. |
| `tools/doc_hygiene.py` | PASS |
| `tools/ai_edition.py --check` | PASS |
| `tools/release_manifest.py --check` | PASS |
| `tools/cobuilder_math.py --selftest` | 14 checks, PASS |

**Independent recomputation:** `core_consistency_2026_11_25.py` now runs **25 checks, 0 failures**. It adds MF-194, MF-195, MF-197, MF-199, MF-203 and MF-204, computed without `cobuilder_math.py`:

- the a mod 7 histories 7, 49, 73, 77, 80, 81, and the first-resolution counts 25, 44, 4, 6, 2;
- the order 16 mod 7;
- the multiplicities and the sums 281 and 143;
- the 216-cycle;
- the 23 two-observer round counts;
- the split prime 11;
- the half-turn eigenspaces 41 and 40, and Q² per orbit.

**Findings:**
- Findings (a), (b) and (c) are still present in this build.
- **(d) MF-197 writes the law as N:** "T_g(x, m) = (N x, m + g(x))" and "g ~ g + f o N − f". The Core writes the law as A everywhere else. This finding is added to CA-42.
