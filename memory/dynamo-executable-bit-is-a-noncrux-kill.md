---
name: dynamo-executable-bit-is-a-noncrux-kill
description: "An \"executable file\" deliverable requirement becomes a recurring difficulty_crux=FAIL kill — agents heredoc the file at 0644 and self-test with python3."
metadata: 
  node_type: memory
  type: project
  originSessionId: 43067629-d486-4b92-8f24-cce768c782fb
  modified: 2026-08-12T05:26:26.750Z
---

On `dynamo-e488890` the verifier asserted `os.access(PROGRAM, os.X_OK)` before collection.
Agents wrote the deliverable with `cat > file << 'EOF'` (mode 0644) and self-tested with
`python3 /app/tool.py …`, which never needs the exec bit — so they never noticed. It aborted
collection with **0 tests run** in two separate pass@2 draws and in 2 of the 3 valid fails of the
pass@5 draw that was accepted, every time with `difficulty_crux=FAIL` and no recoverable values.

**Why it cuts both ways:** it is disclosed in the prompt, so it is fair and it was load-bearing —
without it that accepted 2/5 draw would have been 4/5 solved and blocked. But it is exactly the
shape a human reviewer discounts ("failing tests are only file existence, naming or permissions").

**How to apply:** decide deliberately which side you want. To keep it, make sure the prompt says
"executable" *and* shows direct `/app/tool.py …` invocation. To remove it, drop the `X_OK`
assertion and state the invocation as `python3 /app/tool.py …` so the prompt matches the runner
exactly — and budget a real ratchet in the same push to replace the difficulty it was carrying.
Related: [[dynamo-operational-passat-failures]], [[dynamo-blind-sample-branch]].
