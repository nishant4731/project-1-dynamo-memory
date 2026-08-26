---
name: dynamo-verifier-must-not-import-agent-paths
description: Digest-pinning one agent-writable module does not make importing it safe — its siblings shadow the stdlib; copy the verified bytes to a scratch dir and run python3 -I.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 26baa8a5-9e75-43c9-b21a-1b948f75e740
  modified: 2026-08-15T01:45:41.512Z
---

QC E3 ("Reward / Harness Plumbing Exploit") blocked dynamo-4242b2d on this,
correctly. The task ships a read-only I/O helper at `/app/data/sca/bench_io.py`
and the verifier proved it agrees with the reference by running it in a child
with `sys.path.insert(0, "/app/data/sca")`. The helper itself was digest-pinned
and the check ran before the import — and it was still exploitable: the pin
covers `bench_io.py`, not its **siblings**. A planted
`/app/data/sca/json.py`, `os.py` or `hashlib.py` is imported first, as the
verifier user, which is not privilege-dropped.

**Why:** putting any agent-writable directory on `sys.path` hands over the
whole import namespace, not just the one file you vetted. "I check the digest
first" defends the named file and nothing else.

**How to apply:** never execute agent-writable code where it sits. Read it
through the symlink guard, compare to the pin, copy the verified bytes into a
scratch directory, and run the child with `python3 -I` from there, dropped to
uid 65534 with a scrubbed env. Note that `-I` implies `-P`, so the script's own
directory is *not* added — the driver has to do
`sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))` itself or the
import fails.

Two companions worth shipping in the same push: pin **every** file under the
read-only tree, not the interesting four (QC raises the mismatch between "all of
`/app/data` is read-only" and a four-file pin as a separate E2 item), and skip
`__pycache__`/`*.pyc` in that comparison — if you invite the agent to import a
module, the byte cache it leaves is not a modified input and failing on it is a
false rejection. See [[dynamo-in-progress-timeouts-need-plumbing]] for why the
helper exists at all.
