# Recover Press Proof

This Harbor task is self-contained under `task/` and uses a synthetic prepress package generated for this repository. The agent-visible input is `/app/data/proof_package`; it contains a manifest, approval ledger, indexed-image fragment payloads, and XOR parity payloads needed to recover the approved press proof. It does not contain final outputs, tests, or solution code.

The challenge is reconstructing point-in-time approved artwork from stateful approve/withdraw rows, validating and repairing damaged indexed-image fragments, decoding several compact codecs, solving modular registration offsets, and rendering exact integer alpha/overprint compositing. The required reusable program is verified on hidden generated packages so a visible-output-only solution does not pass.

Local validation target:

```bash
harbor run -p task --agent oracle
harbor run -p task --agent nop
```
