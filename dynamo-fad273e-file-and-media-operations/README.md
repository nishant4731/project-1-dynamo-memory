# Recover Audio Masters

Reviewer context: this submission is self-contained under `task/`; the root README is informational only. The task uses synthetic audio-session data generated for this repository and does not depend on external services or mutable network data.

The reference solution and verifier derive expected audio and metadata from the session manifests, packet payloads, and parity records during execution. The agent-visible environment contains the recoverable session inputs but no final WAVs, cue-sheet answers, tests, or solution code; the hidden verifier session is also an input session, not a clean answer copy.

Local validation used during development:

```bash
harbor run -p task --agent oracle
harbor run -p task --agent nop
```
