# Recover Design Master

This Harbor task is self-contained under `task/` and uses a synthetic layered design package generated for the repository. The agent-visible input is `/app/data/package`; it contains the manifest, release ledger, fragment payloads, and parity payloads needed to recover the approved design. It does not contain the final PPM, report, tests, or solution code.

The core challenge is reconstructing a point-in-time approved design master from stateful release/revoke rows, validating and repairing indexed-image fragments, decoding multiple compact codecs, and rendering exact integer alpha compositing. The required reusable program is verified on hidden generated packages so a visible-output-only solution does not pass.

Local validation target:

```bash
harbor run -p task --agent oracle
harbor run -p task --agent nop
```
