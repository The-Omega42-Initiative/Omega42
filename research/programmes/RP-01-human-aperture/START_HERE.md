# RP-01 · The Human Aperture: six observers at depth 5

**Pilot programme. Area: Mathematics of the ground. Maintainers: the Co-Builders (Claude, ChatGPT). Ledger: CB-008, CB-022.**

## The problem

The law is written A, as in the Core Specification. Work on the states (a, b) with a, b in 0 .. 242 (that is, Z/243 × Z/243, 59,049 states) under the native law

    A(a, b) = (b, a + b mod 243)

which has period 648 on this space. One aperture is shared by every observer:

    h(a, b) = a mod 7        (a read as an integer 0 .. 242)

A **team** is a set of six phases 0 ≤ d1 < ... < d6 < 648. Its **signature** of a state x is the tuple

    ( h(A^d1 x), ..., h(A^d6 x) ).

**Question.** Is there a team whose signatures are all distinct, that is, 59,049 different signatures? Six is the least number that could work, since 7^6 = 117,649 ≥ 59,049 > 7^5.

Teams that differ by a common shift of all phases (mod 648) have the same count, so you may take d1 = 0.

## What is already settled (with its check)

- Depth 2 (81 states): 24 anchored teams of three separate every state; (0, 2, 5) is the first.
- Depth 3 (729 states): 4,856 anchored teams of four; (0, 1, 4, 19) is the first.
- Depth 4 (6,561 states): the team (0, 94, 145, 152, 195) separates every state.

Script: `records/cobuilder/xobs02_search.py` and `records/cobuilder/cbx_2026_11_25_chatgpt_batch2.py`.

## How to contribute

A finding is accepted when anyone can rerun it. Send:

1. the team (six integers), and the count of distinct signatures you got;
2. the program that computed it (any language; a pure-Python version is preferred), and a seed if it searched at random;
3. if you argue impossibility: the argument, step by step, and any finite part of it as a program.

Submit through the *Propose research* form on GitHub (issue template 5-research.yml), area *Mathematics of the ground*, title starting `RP-01:`. Pull requests that add a file to `findings/` are also welcome.

Say which AI assisted you and with which settings; independent results found before reading others' are worth more, so say what you had read.

## Rules

- A count is checked by rerunning it, never by authority. "Not yet rerun" keeps a finding open; it never rejects it.
- A search that fails to find a team is not a proof that none exists. Keep the two apart.
- No private data in submissions.
