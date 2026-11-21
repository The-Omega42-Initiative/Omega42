# K7 — Ω42 Knowledge and Discovery Network

**Status:** proposal-branch implementation; not canonical adoption.

## Purpose
K7 connects definitions, axioms, lemmas, theorems, computations, instruments, interpretations, applications, open questions, conjectures and sources in a typed, provenance-bearing graph.

## Operations
- Validate node types, epistemic statuses, provenance and edge endpoints.
- Reject cycles only in dependency/proof relations (`depends_on`, `derives_from`, `proves`). Other relations may legitimately form cycles.
- Compute dependency closures.
- Find bounded graph paths from open questions to relevant mathematical and operational nodes.
- List explicitly registered contradiction edges.
- Normalize the existing K3 research graph into the K7 vocabulary.

## Epistemic limits
A graph path is a discovery lead, not a proof. A `contradicts` edge is a recorded candidate requiring review, not an automatically resolved semantic contradiction. Structural validation does not establish source authenticity, theorem correctness, or truth. K3 normalization is lossy in places and retains an import marker; review mappings before treating normalized records as canonical.

## Architecture
`Question → typed graph query → dependency/discovery paths → candidate instruments/results → human or formal review → provenance-bearing record`.

The 24-position question-navigation protocol is not asserted to be mathematically equivalent to, or derived from, the 3-adic Fibonacci tower. A formal bridge remains an open question.

## Next steps
1. Add a browser Knowledge Graph Explorer with safe DOM text rendering, graph import/export and accessible filters.
2. Integrate the K7 graph with the K6 local Knowledge Register.
3. Add formal subject/predicate/scope fields before attempting automated contradiction inference.
4. Add review workflow and signed provenance before hosting shared research records.
