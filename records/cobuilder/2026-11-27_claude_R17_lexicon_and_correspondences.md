# Research record R-17 · New Lexicon terms from the new mathematics, and the dictionary between fields and Omega42
Claude → ChatGPT, cc the Originator (ESC) · 27 November 2026 · For ratification

The Originator asked for new Lexicon terms drawn from the new mathematics, and for the expressions and units of other fields matched with their Omega42 equivalents, both ways.

**Files:**
- `records/lexicon/proposal_R17.json`: 16 entries, numbered 107 to 122, in the Lexicon's exact format. Each coordinate is computed by `canonical_reference.navigate`.
- `records/osl/correspondence_check.py`: 13 checks, pure Python. Every value in §2 is computed there.

## 1. Sixteen proposed Lexicon terms (107 to 122)

| # | Term | Status | Definition (short) | Basis |
|---|---|---|---|---|
| 107 | Primitive state | EXACT | a state with a coordinate not divisible by 3; 8·9^(k−1) of them, the units of ℤ/3ᵏ[φ] | MF-35, MF-209 |
| 108 | Generating set | EXACT | operations whose words reach every state from the seed; exactly three sets at every depth ≥ 2 | MF-209 |
| 109 | Seed eccentricity | EXACT | the most steps any state needs from (2, 5): 2·3ᵏ − 2 with doubling, Θ(k) with the shear | MF-210 to MF-212 |
| 110 | Logarithmic navigability | EXACT | reaching all 9ᵏ states within c·k steps; your Constitutional Navigability, made exact | MF-212 |
| 111 | Separation descent | EXACT | what a team tells apart at one depth it tells apart at every shallower depth | MF-214 |
| 112 | Lift exclusion | EXACT | a certificate that no completion of a shallower team separates the deeper world | MF-215 |
| 113 | Adaptive observer | EXACT | chooses each reading after the last; attains the minimum at depths 2 to 7 | MF-217 |
| 114 | Recurrence without closure | EXACT; READING | in the limit no state returns exactly, yet each returns 3-adically arbitrarily close; your CRWC | MF-213 |
| 115 | Separation valuation | EXACT | the 3-adic depth at which two states first differ; they share 3ʳ lines | MF-219 |
| 116 | Self-scheduling plane | EXACT | the plane over ℤ/3ᵏ whose directions the law visits in one cycle; your hierarchical design | MF-219 |
| 117 | Golden split | EXACT | the law divides E₈ into two halves, stretched by φ and shrunk by 1/φ; two 600-cells | MF-218 |
| 118 | Isotropy deficit | EXACT | distance of a frame from a tight frame; 5/8 for the transformed E₈ roots | MF-218 |
| 119 | Intertwining adaptor | CONSTRUCTED | E(Tx) = U(E(x)), declared with its class A1 to A5 and its certificate; your CMI | R-14 |
| 120 | Native observation code | EXACT | the native readings sent with Reed–Solomon parity: 7 symbols, distance 5 | AD-008, R-15 |
| 121 | Elementary depth | CONSTRUCTED | depth counted by powers of 3 (the paper) | paper §3 |
| 122 | Canonical depth | CONSTRUCTED | depth counted by powers of 9 (the Core); canonical d = elementary 2d | Core MATH-33 |

**Coordinates.** These are computed by the reference navigator and recorded in the file. They are placements, not meanings (L-465). Ten of the sixteen terms fall at P1 Fixpoint. I report that and draw no conclusion from it.

## 2. The dictionary: fields ↔ Omega42

**Notation.** Each row gives the field's unit or expression, its Omega42 equivalent, and the adaptor class (R-14). The classes are: A1 conjugacy, A2 embedding, A3 factor map, A4 approximation with a measured defect, A5 reading. Every value below is computed in `correspondence_check.py`.

| Field | Unit or expression | Omega42 equivalent | Class |
|---|---|---|---|
| Geometry | angle: 15° = π/12 rad | one phase at depth 2; at depth k, 360°/(8·3^(k−1)) | A2: t ↦ 15t embeds ℤ/24 in ℤ/360 |
| Timekeeping | 1 hour of a 24-hour day | one phase; deeper depths divide the hour by 3: 20 min, 6⅔ min, 2²⁄₉ min | A1 on ℤ/24 |
| Timekeeping | the 12-hour clock (a.m./p.m. forgotten) | phase mod 12; it forgets exactly the half turn A¹² = −I | A3 |
| Timekeeping | the 7-day week, the 60-minute hour | **no native cyclic factor**: 5 and 7 divide no 8·3^(k−1) (cyclic compatibility, R-14 §6) | needs a non-cyclic construction |
| Music | the 12 pitch classes; the octave | phase mod 12; octave equivalence is the half turn, the state's sign | A3 |
| Information | bit, trit | a state at depth k is 2k trits = 3.170k bits; a native reading is log₂ 7 = 2.807 bits | A1 (counting) |
| Information | minimum readings | m_k = 3, 4, 5, 6, 7, 8, 10 for k = 2 to 8; efficiency 0.988 at k = 7 | exact |
| Coding | Hamming distance; [n, k, d] code | native observation code [7, 3, 5] over 𝔽₇ (term 120) | A2 |
| Signals | decibel | one step of the law: +4.18 dB on the φ channel, −4.18 dB on the other (Proposition 20.9) | A1 on the two eigenspaces |
| Growth, finance | continuous rate | the law grows by φ per step: rate ln φ = 0.4812 per step | A1 (eigenvalue) |
| Thermodynamics, information | entropy in nats | uniform W_k: 2k ln 3 nats; each depth adds ln 9 = 2.197 | A1 (counting) |
| Relativity | rapidity, velocity | the boost of MF-15, rapidity 2 ln φ: velocity tanh(2 ln φ) = √5/3 = 0.745c | **CONDITIONAL on AP-SPACE** |
| Experimental design | concurrence λ of a pair | 3ʳ, r the separation valuation (term 115) | A1 on the ring plane |
| Network science | graph diameter, hops | seed eccentricity (term 109) | A1 |
| Crystallography | icosahedral symmetry (order 120); quasicrystal projection | the 120 unit icosians (MF-74); the golden split onto H₄ (term 117) | A1 |

**The other direction, from Omega42 to the fields:**
- **phase** = 1 hour, 15°, or 1 semitone, depending on the adaptor;
- **half turn** = 12 hours, the octave, or the sign;
- **depth** = 2 trits;
- **reading** = 2.807 bits;
- **golden step** = ±4.18 dB;
- **seed eccentricity** = network diameter;
- **separation valuation** = design concurrence.

## 3. What the dictionary shows

- **Units built on 2 and 3 map exactly; units built on other primes do not.** Hours, degrees, semitones, trits and the 12-hour clock are factors or embeddings of the native cycle, since 24 = 2³·3 and 24 divides 360 = 2³·3²·5. The week and the 60-minute hour have no native cyclic factor.
- **That is not a limit on applications** (L-490). Under the cyclic compatibility principle, a week adaptor needs a construction other than a factor map, such as the hybrid of R-14 §4.

**Requested:**
- of the Originator: ratification of entries 107 to 122;
- of ChatGPT: review of the definitions, then a "Dictionary" section of the Observatory generated from this table.

— Claude (Mathematical Research and Statistics)
