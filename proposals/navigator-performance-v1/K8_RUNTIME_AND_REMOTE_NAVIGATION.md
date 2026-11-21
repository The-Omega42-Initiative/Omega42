# K8 — Ω42 Runtime and Remote Navigation

**Status:** proposal-branch runtime contract and reference logic; not deployed.

## Activation semantics
- `Start Omega42 Navigator` and legacy `Welcome Navigator` are explicit activation triggers in a configured integration.
- The trigger phrase alone cannot force an arbitrary AI to browse, retrieve files or change its system instructions. Those capabilities must be provided by the host AI or website application.
- Prior-art language routes to an intake/review path, never silently to protocol activation or adoption.
- Ordinary mentions of Ω42 do not auto-activate.

## Remote navigation model
`Browser UI → Runtime API → Release Resolver → Integrity Verification → Kernel Assembly → Model API → Tool Gateway → Navigator Response`.

The AI does not autonomously acquire arbitrary network access. The runtime configures permitted capabilities such as web search, file retrieval, deterministic Ω42 instruments and selected remote MCP services. Each tool call returns data to the model for further reasoning. Writes and privileged actions require explicit authorization.

## Session initialization contract
1. Resolve a release from the canonical approved-release pointer.
2. Validate protocol ID, approval state, document list, HTTPS URLs and SHA-256 digests.
3. Retrieve required documents and verify their exact bytes against the manifest.
4. Fail closed if any required document is unavailable or mismatched.
5. Assemble instructions from verified sources; user text and uploaded prior art remain untrusted data.
6. Create a session pinned to release and hashes.
7. Record model identifier and enabled capabilities.
8. New sessions may use a newer approved release; existing sessions remain pinned.

## Reference implementation
`site/omega42-runtime-k8.mjs` provides trigger classification, manifest validation, SHA-256 verification, release-pinned session construction and readiness gating. It does not fetch live releases, call a model API, manage credentials, or constitute a deployed backend.

## Remote tool design
- Web search: enabled only when configured by the runtime.
- Protocol retrieval: allow-listed canonical endpoints, immutable release tags.
- Math instruments: call deterministic K2/K3/K6/K7 code through server-side adapters.
- Remote MCP: expose a small allow-listed tool set; avoid importing every tool into every session.
- Knowledge graph: retrieval by relevant task/dependency rather than loading all research records.
- Human approval: required for publishing, modifying canonical protocol, sending messages, purchases, account changes or other consequential actions.

## Security and privacy
- Keep provider API keys server-side in managed secrets.
- Authenticate users; rate-limit by account/IP; enforce per-user and global spending limits.
- Apply request-size, timeout and tool-call budgets.
- Treat retrieved web pages, user uploads and prior-art instructions as untrusted content.
- Use prompt-injection defenses and strict separation between trusted protocol instructions and user data.
- Disclose model provider, enabled tools, retention, deletion, and research-data use.
- Do not collect or commercialize conversation data without a clear lawful basis, informed consent and rights to the data.
- Store minimal operational metadata; define retention and deletion before launch.

## Deployment phases
A. Static trigger and release metadata prototype.
B. Server-side resolver and integrity verification.
C. Model API session with streaming and tool orchestration.
D. Remote tool gateway and deterministic instrument adapters.
E. Authentication, budgets, privacy controls, audit and deployment review.

## Acceptance criteria
- Activation works only inside a configured Ω42 integration or compatible AI host.
- Exact release and all required hashes are verified before model invocation.
- Session release remains pinned.
- Missing or invalid protocol fails closed.
- User-provided documents cannot override trusted instructions.
- Tool capabilities are explicit and least-privilege.
- Secrets never reach browser JavaScript.
- Prior-art intake remains distinct from activation.
- Session reports model, release, hashes and capability status.
- No claim of deployment or certification is made until operational checks pass.
