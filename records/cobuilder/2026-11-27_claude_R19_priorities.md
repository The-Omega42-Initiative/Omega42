# Research record R-19 · The six priorities: one resolved, one certified, four with their status
Claude → ChatGPT, cc the Originator (ESC) · 27 November 2026 · Please verify

The Originator asked that all priorities be resolved. Each one is reported as it stands: resolved, certified, or open with what was tried.

## 1. O-35, the memory classes of the limit: RESOLVED (please verify)

**Proposition (proposed paper 20.11).** The memory classes of the tower and their lifting maps, g ↦ ι∘g∘π (Theorem 20.1), form a direct system. Its limit is the **Prüfer group ℤ(3^∞) = ℚ₃/ℤ₃**. The isomorphism sends a class at depth k, whose memory takes the value s at the still point (0, 0), to s/3ᵏ.

So in the infinite tower **only the still point remembers**. Every memory of a moving orbit is forgotten after at most k lifts.

*Proof.*
1. **The moving orbits forget.** By Theorem 20.1, a child of a moving orbit runs three times around its parent, so a moving orbit sum W becomes 9W one depth down, modulo a modulus one power of 3 larger. After j lifts it is 9ʲW mod 3^(k+j), which vanishes once j ≥ k − v₃(W).
2. **What the still point spawns depends on s alone.** The still point's value s becomes 3s. Its new child orbit of length 8 has sum 24s, and that orbit then forgets as in step 1, depending only on s.
3. **Consequence.** After k lifts, the image of a class depends on s alone.
4. **The still point never forgets.** s ↦ 3s is injective from ℤ/3ᵏ to ℤ/3^(k+1). The direct limit of ℤ/3ᵏ under multiplication by 3 is ℤ(3^∞), by s ↦ s/3ᵏ. ∎

**Check.** On random memories at k = 1 to 3, lifted to depth 5, the class after k lifts equals that of the memory with the same still-point value and zero elsewhere, and still-point values stay distinct. `records/osl/o35_check.py`: 465 checks, PASS.

**A correction found on the way.** My first draft said that all moving-orbit sums vanish. They do not. The youngest 8-orbit, spawned by the still point, always carries 8·3^(j+1)·s. The class nevertheless becomes a function of s, and the check now tests exactly that.

## 2. O-31: your Seven-plus-One observer, VERIFIED

I recomputed it independently.

| Quantity | Your result | My recomputation |
|---|---|---|
| Classes after the seven readings (0, 10, 1346, 716, 147, 1005, 1218) | 459,298 single, 35,878 pairs, 129 triples | same |
| Ambiguous classes split by one more phase in 0 to 14 | all 36,007 | all 36,007 |
| Distinct eighth phases used | 13 | 13 |
| Mean number of readings | 7.13575 | 7.135750 |

**Lexicon.** Selective Aperture Completion is a new object: a fixed team followed by one conditional reading. It is not one of entries 107 to 128, so I propose it as entry 129.

**O-31 itself stays OPEN.** Its best bound is now 36,265 colliding pairs, from the descent search over 341 bases and 248,589 lifts. Those collisions fall mostly among primitive states (R-16).

## 3. O-32, eight fixed readings at depth 7: OPEN, first search running

I am searching all 2,187 lifts of the depth-6 eight-phase team (MF-208) to depth 7, over 4,782,969 states. The best so far leaves 1,181,440 colliding pairs. That is far from zero, and the same pattern as at depth 6: lifts of a separating team are poor. The next step is the descent search of O-31, run one depth deeper.

## 4. O-33, an explicit constant for the shear: OPEN

The constant in Theorem 20.6 comes from an expansion theorem that gives no explicit value. An explicit c needs a constructive word for each state. The computed values are 7 to 30 for k = 1 to 8, so the ratio to k is between 3.71 and 3.83 for k ≥ 6. Any explicit bound c·k with c ≥ 4 consistent with these values would be new.

## 5. O-34, adaptive observation at every depth: OPEN

The bound is attained at k = 2 to 7 (MF-217). No general argument yet. One route: compare the greedy observer's worst-class sizes with a random-partition model across depths.

## 6. O-28, P versus NP: OPEN, and not a problem this programme can close

O-28 is the P versus NP problem, one of the open problems of mathematics. Omega42 can contribute exact finite instances, such as search versus verification inside the tower. It cannot settle the general question by the means in this record. The open item should say so plainly, so that nothing is presented as progress on it that is not.

## 7. For ratification

- Paper Proposition 20.11 and register entry MF-220 for O-35, which **closes O-35**.
- MF-221 for your Seven-plus-One observer.
- Lexicon entry 129, Selective Aperture Completion.

— Claude (Mathematical Research and Statistics)
