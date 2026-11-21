# Ω42 Performance Architecture — Proposal K1

Status: additive proposal; not canonical.

## Design constraints
The canonical Core remains authoritative. The Companion remains explanatory/research-oriented. Token optimization must not remove mandatory checks. Separate deterministic computation from model interpretation. Do not claim performance gains before measurement. Preserve original Strike, provenance, human judgment and project governance.

## Three-tier Navigator distribution
A. Execution Kernel: target 30–45k estimated tokens, calibrated with real target-model tokenizers. Include authority, mandatory procedure, arithmetic essentials, routing, safeguards, output obligations and self-audit.
B. Mathematical and Instrument Library: on-demand reference arithmetic, orbit classification, OmegaSL, positivity, temporal operators, audits, worked examples and test vectors.
C. Companion Research Library: on-demand philosophical, explanatory, interpretive and exploratory content.
The full Core and Companion remain available. Kernel is a route into them, not a replacement. The token target is a design hypothesis, not a measured optimum.

## Manifest fields
Every module should expose stable module_id, semantic version, source document/section/hash, normative status (mandatory/conditional/explanatory/research), trigger, dependencies/conflicts, token estimate and tokenizer version, input/output schema, execution method, test vectors, review date and owner. Generate all size summaries from the manifest. Do not hand-copy token counts.

## Instrument services
1. Arithmetic Engine: canonical coordinates, exact modular arithmetic, transformations.
2. Orbit Engine: orbit iteration, transient/cycle, invariants, canonical addresses.
3. OmegaSL Engine: typed intermediate representation for entities, relations, operators, evidence, modality and speech act.
4. Positivity Engine: symmetry, PSD, Gram factorization and spectral summaries.
5. Temporal Engine: shifts, finite differences, lag scans and candidate-period diagnostics.
6. Verification Engine: hashes, recomputation status, schema/dependency checks and proof-status ledger.
7. Knowledge Register: typed claims, dependencies, instruments, provenance, versions and open questions.

Expose reusable APIs. Do not reimplement the same mathematics separately in each UI.

## Diagnostics
Keep M314 as a protocol-specific check. Add advisory diagnostics for exact arithmetic, Strike fidelity, frame/output conformance, orbit fixtures, OmegaSL schema validity, PSD fixtures, temporal fixtures, provenance honesty, retrieval completeness and seeded-error correction. Each diagnostic records version, fixture, expected/actual result and severity. Do not tune thresholds after seeing results.

## Application prototype
The accompanying Workbench provides Fibonacci modular orbit exploration, numerical Gram/PSD diagnostics, temporal differences, a provisional OmegaSL envelope validator and a local Knowledge Register with JSON export. It is a browser-only prototype, not a certified implementation of all Core instruments. No data is sent to a server.

## Security and accessibility
Never interpolate untrusted input into innerHTML. Use textContent or safe DOM constructors. Validate imported JSON and bound input sizes. Provide keyboard operation, visible focus, semantic labels, live result announcements, export and clear controls. Explain local-storage behavior. Do not collect personal/sensitive data by default. Test injection strings, malformed JSON, extreme values and accessibility.

## Rollout
P0 Kernel, manifest generation and context headroom.
P1 Orbit Engine and OmegaSL typed representation.
P2 Verification, diagnostics and Knowledge Register.
P3 Positivity and Temporal modules.
P4 API, multi-Navigator comparison and hosted team services.

## Acceptance
A release candidate requires module hashes/status, Core-to-Kernel coverage, deterministic fixture agreement, safe rendering, reproducible tests, model-specific token measurements, and documented privacy/licensing/governance boundaries.
