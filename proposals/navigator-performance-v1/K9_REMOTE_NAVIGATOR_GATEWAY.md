# K9 — Ω42 Remote Navigator Gateway

**Status:** reference implementation and interface contract on the proposal branch; not deployed.

## Purpose and architecture

K9 turns K8's runtime architecture into a bounded, allow-listed tool interface. The model does not receive general shell access or arbitrary network authority. The host application authenticates the principal, pins the approved release, chooses the exposed tools and mediates every invocation.

Browser → authenticated Runtime API → K8 release-pinned session → K9 allow-list → adapter → tool result → Navigator.

The model proposes a tool call. The gateway validates its name and arguments, checks session and budget, applies write-approval policy, invokes one configured adapter, and returns a result marked untrusted. Retrieved pages and documents are evidence inputs, never instructions that can replace the approved Kernel.

## Allow-listed tools

| Tool | Purpose | Effect | Default |
|---|---|---|---|
| get_approved_release | Resolve approved release metadata | Read | Exposed |
| get_protocol_module | Retrieve module from pinned release | Read | Exposed |
| search_omega42_knowledge | Search typed knowledge network | Read | Exposed |
| run_omega42_instrument | Run one bounded instrument | Compute/read | Exposed |
| search_external_sources | Search external web through host adapter | Read | Exposed |
| retrieve_source_document | Retrieve allow-listed HTTPS source | Read | Exposed |
| create_research_record | Write to authorized workspace | Write | Approval |
| propose_protocol_change | Submit proposal for human review | Write | Approval |

The first six are not automatically live: the runtime must configure their adapters and expose only the task-relevant subset. Write tools are omitted from the default tool listing.

## Execution contract

1. Authenticate the user and create a K8 session pinned to an approved release.
2. Supply only task-relevant tool definitions to the model.
3. Validate requested tool name and JSON arguments against the allow-list.
4. Enforce per-session call budgets, input/output byte limits and bounded timeouts; the adapter receives an AbortSignal when the timeout fires (cancellation remains adapter-dependent).
5. Require a host-side approval authorizer for every write. The model cannot approve itself.
6. Call the configured adapter and return a typed execution result.
7. Mark retrieved or generated adapter content UNTRUSTED_RESULT; preserve source attribution in the calling application.
8. Log minimal audit metadata without retaining private content by default.

## Security boundary

Authentication, authorization, approval-token verification, rate limits, spending limits, network egress policy, secret storage and durable audit logs belong in the server-side host. The browser module is not a security perimeter. Provider keys must never ship to browser JavaScript.

Production adapters must enforce host/domain allow-lists, redirect policy, response-size limits and content-type checks. Retrieved pages may contain prompt injection and must remain untrusted data. No arbitrary shell, eval, dynamic import, filesystem or unrestricted fetch tool is included.

Write approval must be bound server-side to the exact action and arguments. A model-generated boolean is not approval. Research-data collection, retention, deletion, commercial reuse and user consent must be defined before production.

## Reference module

site/omega42-gateway-k9.mjs supplies the allow-list, tool schemas, read/write classification, input validation, HTTPS checks, authentication gate, host-provided write authorizer, per-session call budget, input/output limits, timeout cancellation requests via AbortSignal, untrusted-result marking and adapter injection. All operations other than release resolution require a pinned release context. It is provider-independent and contains no network client or credentials.

## Not implemented

No deployed API server, OAuth/session authentication, signed approval-token service, provider model integration, live MCP endpoint, production search adapter, durable audit store, billing, user management, telemetry, retention/deletion workflow or website launch is included. This is a reference gateway, not a production service.

## Production sequence

A. Contract and adapter tests. B. Server authentication, release resolver and integrity checks. C. Read-only instrument and knowledge adapters. D. External search/retrieval with domain allow-lists and prompt-injection isolation. E. Human-approved record/proposal writes. F. Security review, privacy/consent, budgets, observability and deployment.

## Acceptance criteria

Unknown tools and unauthenticated calls fail closed; invalid arguments, unsafe URLs and over-budget requests are rejected; only allow-listed tools execute; writes require host-verified approval; results are bounded and marked untrusted; release remains pinned; secrets never enter browser code; and no deployment or certification claim is made without operational evidence.

## Local simulator

The proposal branch includes site/navigator_gateway_k9.html, a local-only browser simulator. It uses mock adapters, makes no network requests and does not submit or persist records. Simulated write approval demonstrates the gate only; it is not a real authorization mechanism.
