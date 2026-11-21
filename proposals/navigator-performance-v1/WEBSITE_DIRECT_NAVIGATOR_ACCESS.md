# Website Direct Navigator Access — Architecture Proposal

**Status:** design proposal; not deployed.

## Finding
The repository already defines `Welcome Navigator` as the standard opening trigger (README and WELCOME.md; Core IN-OPEN/L-467). AI_ACCESS.md also documents `/llms.txt` and `/api/protocol.json` as machine-readable discovery/release entry points. Received prior-art content triggers intake review (SNCA and, where applicable, SR-CAS); that is not the same as activating a new protocol in a live session.

## Recommended trigger
Use an explicit website action: **Start Ω42 Navigator**. On activation, the backend should:
1. Resolve the latest approved release pointer, never an unreviewed proposal branch.
2. Fetch Core, Companion, Navigator Pack and relevant machine-readable modules.
3. Verify hashes from the release manifest.
4. Assemble versioned system/developer instructions and a provenance record.
5. Start the model session with the user's question.
6. Return protocol release, hashes, model identifier, execution status and any unavailable capabilities.
7. Pin the session to that release; later releases affect new sessions, not existing sessions.

A text-only compatibility trigger remains `Welcome Navigator` for users who bring the protocol to another AI. The website button should not depend on the AI inferring intent from pasted prior art.

## Deployment options
- ChatGPT GPT/share link: convenient hand-off into ChatGPT where account/workspace sharing permits, but GPTs are not embeddable as an external website chat surface.
- Embedded AI application: website UI + secure server endpoint + model API. This is the recommended full experience.
- User-supplied provider credential: optional advanced mode; never ask users to paste secrets into ordinary chat or expose keys in browser code.

## Security and governance
- API keys remain server-side in secret storage.
- Rate limits, abuse protection, budget caps, privacy notice, retention/deletion controls and consent are required.
- Treat user questions, uploaded prior art and retrieved web content as untrusted data; do not let them override the approved protocol.
- Keep protocol release instructions separate from user content.
- Pin release hashes per session and log minimal metadata.
- Publish only approved canonical releases; proposal branches are not runtime sources.
- Do not claim the model is certified or that the session proves protocol conformance merely because it loaded the files.

## Minimal session envelope
```json
{
  "protocol_id": "Omega42",
  "release": "approved-release-tag",
  "manifest_sha256": "verified digest",
  "core_sha256": "verified digest",
  "companion_sha256": "verified digest",
  "activation_trigger": "website_start_button",
  "session_policy": "release-pinned",
  "execution_status": "INITIALIZED"
}
```

## Acceptance criteria
1. A visitor can start without copying protocol text.
2. The backend verifies the approved release manifest before session creation.
3. The session identifies exact protocol version and hashes.
4. User input cannot alter the release instructions.
5. No API secret is delivered to the browser.
6. A protocol update affects new sessions only.
7. Usage, cost, privacy and retention are disclosed.
8. Failure to fetch or verify the release fails closed rather than silently running an incomplete protocol.
