---
name: dynamo-heredoc-wedge-dominates-large-deliverables
description: "Terminus-2 wedges its terminal on big heredocs, so large single-file deliverables fail mechanically rather than on the crux."
metadata: 
  node_type: memory
  type: project
  originSessionId: c8eb28ff-48a8-46b1-9e30-a4edf5944bfa
  modified: 2026-08-11T22:00:05.627Z
---

On a Dynamo deliverable that is one 400–500 line script, expect most trials to fail for
a terminal reason rather than the intended one. On `dynamo/glint-profile` (2026-08-12),
six of seven trials across pass@2 and pass@5 wrote the file with a single
`cat > file << 'DELIM'` heredoc, the keystroke buffer truncated mid-body, bash dropped to
the `>` PS2 prompt, and every later command — closing delimiter, Ctrl-C, Ctrl-D — was
swallowed as heredoc text. Agents then burned 100–163 steps trying to escape. The only
solving trial wrote the script incrementally across several smaller heredocs.

**Why:** these score as *good valid fails* and the difficulty gate accepts them
(pass@5 1/5, avg 0.200, "Difficulty OK"), but every failing trajectory is marked
`difficulty_crux = FAIL` because the real problem is never reached. A human reviewer
sees mechanical rather than intellectual difficulty evidence.

**How to apply:** read the per-trajectory `difficulty_crux` column, not the pass fraction
— a green difficulty gate is not proof the crux is doing the work. Budget for it when
choosing a deliverable shape, and do not respond by adding difficulty; the wedge is
agent-side tooling, not task design. See [[dynamo-pass2-typo-is-not-difficulty]].

**Third confirmation (`dynamo-19c8cbd`, 2026-08-12), with the mechanism named.** Across three
pass@2 draws on a ~24KB single-file deliverable, five of six trials wedged. The trial analysis
identified two distinct proximate causes under one taxonomy: PTY input-buffering limits on a
~24KB single-keystroke paste, and a **10,000-byte terminal output cap** that made the closing
delimiter appear mid-stream in earlier output rather than as the heredoc terminator. Agents then
burned 40-46 minutes in escape loops. The gate still passed (2/2 valid fails, "Rerun Recommended:
NO") while every trajectory read `difficulty_crux = FAIL`.

**The lever is deliverable SHAPE, not the prompt.** Telling the agent how to write the file is
step-by-step procedure and fights `instruction_concision`. Instead relax the single-file contract:
let the program import helpers from a declared directory and have the replay harness copy that
directory alongside the entry point. That removes the operational failure surface without touching
difficulty, and it is a disclosed, fair contract change.

**Sequencing note:** do not push this fix while a pipeline is live — a push cancels the run. Bank
the tier1/QC verdict first, then act only if pass@5 also comes back all-wedge.

