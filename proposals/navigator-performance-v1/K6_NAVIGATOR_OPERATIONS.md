# Ω42 K6 — Navigator Mathematical Operations Integration

**Status:** additive proposal on `navigator-performance-kernel-v1`; non-canonical pending Builder review.

## Objective

Connect the K2/K3/K5 mathematical instruments to a deterministic Navigator operations layer. The Navigator selects a task-specific instrument, executes only that instrument, returns a typed execution result, and can preserve the result in a provenance-bearing local research register.

K6 does not amend canonical Core rules, the question coordinate, M296, M327, four-arm navigation, the output skeleton, or Builder governance.

## Architecture

```
Question / task intent
        |
        v
Deterministic Instrument Router
        |
        +--> explicit task? ---- yes ----+
        |                                |
        +--> trigger match? --- yes -----+
        |                                v
        +--> ambiguous --> clarification
                                         |
                                         v
                              Selected instrument
                                         |
                 +-----------------------+----------------------+
                 |          |           |          |            |
               Orbit     Census       K1/K2    Temporal     Validators
                 |          |           |          |            |
                 +-----------------------+----------------------+
                                         |
                                         v
                              Typed execution record
                                         |
                                         v
                            Knowledge Register (local)
                                         |
                                         v
                              JSON export / review
```

## Six task-specific instruments

| Task | Instrument | Input | Output |
|---|---|---|---|
| `orbit` | Ω42 Orbit Engine | depth, state | period, cycle address, Λ |
| `census` | Orbit Census | depth | finite orbit and period census |
| `uniqueness` | K1/K2 checker | depth, optional seed | finite criterion reproduction |
| `temporal` | Temporal Difference Engine | values, optional lag | finite differences |
| `omegasl` | OmegaSL envelope validator | record | schema validity and errors |
| `researchGraph` | Knowledge Graph validator | graph | structural and dependency validity |

The router accepts an explicit task or deterministic intent trigger. If no trigger is unambiguous, it returns `NEEDS_CLARIFICATION` and does not execute anything. It does not run every instrument on every question.

## Execution and evidence discipline

The K6 record separates:
- `executionStatus: EXECUTED`: an instrument actually ran;
- `status: computed`: its output is a computation, not automatically a proof;
- mathematical proof review;
- source provenance;
- application validation.

K6 does not automatically promote a computed result to `proved`. A later proof-review workflow must link to a separately reviewed theorem or derivation record. Graph validation checks references and dependency cycles, not truth or source authenticity.

## Knowledge Register

The local register is an append-only-in-session collection with unique record IDs. Append is immutable in the module API. Records include:
- exact task and instrument name;
- protocol version;
- input and output;
- source label;
- explicit epistemic limitation.

The browser Workbench can export the register as JSON. This is a local convenience, not a secure hosted repository, access-control layer, or backup service. Do not enter personal or confidential data.

## Worked examples

### Example A — Orbit

Input:
```json
{"depth":1,"state":[2,5]}
```
Expected core output: modulus 9, period 24, generic exponent 2, canonical Ω42 depth 1, with a computed Λ record. The period is an executed finite orbit result; the general orbit theorem remains a separate mathematical proof claim.

### Example B — Census

Input:
```json
{"depth":1}
```
Expected census: 81 states, 5 orbits, with period distribution 1 orbit of period 1, 1 of period 8, and 3 of period 24. This is exhaustive for that finite state space only.

### Example C — Temporal differences

Input:
```json
{"values":[1,2,4,7,11,16],"lag":2}
```
The instrument computes differences of the supplied sequence. It does not infer causation or prove periodicity.

## Performance and implementation policy

1. Route only to the instrument required by the task.
2. Use BigInt for the finite modular arithmetic.
3. Keep bounded enumeration and make state-space limits explicit.
4. Preserve the full execution record; summarize only for display.
5. Keep deterministic computation separate from generative interpretation.
6. Treat unknown or ambiguous tasks as clarification, not a guess.
7. Preserve existing canonical and Construct X instruments unchanged.

## Security and privacy

The browser interface renders user-controlled values through `textContent`, not `innerHTML`. Register export is a user-initiated local JSON download. No network submission or telemetry is implemented. A future hosted register would require explicit consent, retention/deletion rules, authentication, authorization, licensing and privacy review before collection.

## Tests and Builder acceptance

Run:
```bash
node --test tests/navigator-operations-k6.test.mjs
```

Builder should review:
- trigger vocabulary and precedence;
- output record schema and evidence vocabulary;
- task input bounds and enumeration caps;
- integration with the canonical Knowledge Register;
- accessibility and browser security;
- privacy and retention policy before any hosted data service.

## Limitations

K6 is a task router and local operations workbench, not an autonomous agent that changes model weights or rewrites the protocol. Temporal calculations retain K2's floating-point limitation. OmegaSL validation remains a limited envelope check, not a full parser/compiler. Research graph validation is structural, not epistemic certification. No link is asserted between the 24-position question protocol and the 3-adic tower.
