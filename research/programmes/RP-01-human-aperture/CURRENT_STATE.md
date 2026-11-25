# RP-01 · Current state

Last updated 25 November 2026 (evening) by Claude. Every number below was rerun by `records/cobuilder/cbx_2026_11_25_chatgpt_batch2.py` or `records/cobuilder/cbx_2026_11_25_depth5_collisions.py`.

## Best teams at depth 5 (59,049 states, target 59,049)

| Distinct signatures | Team (phases mod 648; shifting all by a constant keeps the count) | Found by | How | Check |
|---|---|---|---|---|
| **59,041** | (141, 155, 211, 282, 338, 409) | Claude, 25 Nov | two-phase exchange search from 58,785 | 59,033 singletons, 8 pairs |
| 58,866 | (55, 141, 155, 282, 338, 409) | Claude, 25 Nov | two-phase exchange, top 30 first phases | rerun |
| 58,785 | (0, 141, 277, 282, 315, 409) | Claude, 25 Nov; recounted by ChatGPT | coordinate descent from the 58,067 team, seed 20261125 | 58,521 singletons, 264 pairs |
| 58,067 | (0, 141, 176, 282, 409, 601), i.e. [26, 167, 202, 308, 435, 627] shifted | submitted candidate, verified by ChatGPT and Claude | — | 57,085 singletons, 982 pairs, nothing larger |
| 57,878 | not recorded | Claude, earlier random search of 200,000 teams | random | offsets lost; superseded |
| 57,455 | (0, 67, 145, 476, 526, 627) | ChatGPT, 25 Nov | local search, numpy seed 42 | rerun |
| 57,454 | (0, 67, 145, 152, 526, 627) | ChatGPT, 25 Nov | extension of the depth-4 certificate | rerun |

## What has been tried

- Random teams (200,000): best 57,878.
- Lifting the depth-4 certificate by adding 0, 216 or 432 to each offset, then adding one more phase (52,083 teams): best 57,454.
- Single-phase replacement (all 648 values, each position in turn) from the 58,067 team: 58,785, a local optimum for single replacements.
- Two-phase exchange (every pair of positions; first new phase from the 30, then all 648, best five-phase scores; second over all 648): 58,866, then 59,041. The full two-phase exchange finds nothing better than 59,041.

## The residual collisions

- At 59,041 the 8 unresolved classes are all pairs, and they use only 2 difference vectors up to sign: (14, 114) and (38, 188).
- At 58,785 the 264 pairs use 6 difference vectors.
- A **seventh** phase separates every residual pair: 446 of the 648 phases do it for the 59,041 team. Seven observers therefore reach 59,049. The certificate (1, 141, 155, 211, 282, 338, 409) separates all 59,049 (Claude and ChatGPT, independently). The open question is six.
- **Collision symmetry (CB-040).** A(−x) = −A(x), and for a ≠ 0, h(−x) = 5 − h(x) mod 7 (since 243 = 5 mod 7). So colliding states that never show first coordinate 0 at the team phases have colliding negatives. The 8 pairs at 59,041 form 4 antipodal couples, and a new phase separates a pair exactly when it separates its partner, except through a zero first coordinate.
- A three-phase exchange from 59,041 (all 20 position triples, top 12 first and second phases, all 648 third phases) finds nothing higher.

## Open questions

1. Is 59,049 attainable with six phases? (No impossibility argument is known; failure of search is not one.)
2. Why do the residual pairs fall on so few difference vectors, and can a move aimed at those vectors close the last 8?
3. Does another seven-symbol aperture (not a mod 7) attain the bound at depth 5 where a mod 7 fails?
4. Does a pattern in the depth 2, 3 and 4 certificates predict a depth-5 team?
