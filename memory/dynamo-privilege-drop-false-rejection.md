---
name: dynamo-privilege-drop-false-rejection
description: "A replay that pre-creates the output dir as root then drops privileges fails `shutil.rmtree` cleanup — a correct submission scores 0 and pass@2 records a task/verifier issue, not a valid fail."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: cdcd2dbe-3dc2-46a2-8b7b-9b15206e9e4b
  modified: 2026-08-13T05:19:14.262Z
---

Measured on `dynamo-f1e47b1` (shadecast-refit) pass@2, 2026-08-13: 1 solved / **0 valid-fail**
/ 1 task-verifier-issue. The failing trial had an algorithmically **correct** pipeline — all
eight shipped-frame delivery tests passed, 152 of 158 total — and died at
`shutil.rmtree(out_dir)` with `PermissionError`.

**Mechanism.** The replay harness created the staged output directory as root and then
`preexec_fn`-dropped to uid 65534. `rmtree` calls `os.rmdir` on the directory *node*, which
needs write permission on the **parent**, not the directory. Widening only the output dir
(`out.chmod(0o777)`) is not enough — the parent staging dir must be `0o777` too. The trial
analyser called it out precisely: "an undisclosed operational constraint is doing the work of
a test failure", and `decisive_rule_disclosed` FAILed.

**Why it matters beyond the bug:** an instruction that says "leave nothing else in it"
*affirmatively motivates* delete-and-recreate. Both readings — empty in place, or replace
outright — are legitimate, so both must grade identically. The reference solution's per-file
`os.remove` happened to dodge it, which is exactly why the oracle stayed green and only a real
agent found it.

**How to apply:** whenever a verifier replays a submission unprivileged into a directory the
harness made, chmod the **parent** as well, and ship a test that proves it — run a tiny probe
program through the same privilege-dropped path that does `rmtree` + `makedirs` + touch, and
assert the file appears. Note `mkdir(mode=...)` is masked by umask, so every widening needs an
explicit `chmod`. Related: [[dynamo-tempdir-0700-breaks-replay]], which is the same failure one
level up (a 0700 `mkdtemp` root the nobody-user cannot traverse).
