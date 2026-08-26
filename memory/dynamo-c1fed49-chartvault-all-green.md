---
name: dynamo-c1fed49-chartvault-all-green
description: "dynamo/chartvault-mend went ALL-GREEN at pass@5 1/5 with 4 good valid fails; the single biggest lever was deleting the worked example's answer key, which took pass@2 from 2/2 solved to 0 solved."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 8e848bdb-69db-4125-b540-9956c1880b3f
  modified: 2026-08-16T01:56:24.224Z
---

`dynamo-c1fed49` (`dynamo/chartvault-mend`, 2026-08-16, head `fc392dc`):
**pass@5 1 solved · 4 good-valid-fail · 0 timeouts · avg@5 0.200 · gate green.**
The salvage/repair mold — a crashed clinical chart vault mended in place — after
four heads of a recover-the-policy-from-a-log task on the same repo capped out at
5/5 solved ([[dynamo-reconstruction-mold-hit-its-ceiling]]).

**The lever that actually moved it, measured on consecutive heads:**

| head | pass@2 | note |
|---|---|---|
| full worked example published in the handbook | **2/2 solved, ~14 min** | both agents diffed their output against §7 and patched until byte-identical |
| same task, §7 cut to three convention fragments | **0 solved, valid fails** | nothing else changed |

The trial analyser said it outright: *"the worked example acted as the key
debugging signal, not first-principles derivation alone."* The two bugs agents
self-corrected against it — hold-only-on-due-disposal, and counting a rebuild
before its digest check — became the failure surface the moment the key was gone.
This is [[dynamo-oracle-corpus-solve-or-timeout]]: publish enough of the example
to pin byte conventions (one `station_offsets` entry for the `[before, after]`
shape, two `outcomes` rows for entry shape and collision-ordinal placement) and
nothing that lets a solver verify its whole answer.

**What the difficulty is made of**, all fair and all disclosed: two clock offsets
per station split at a serviced instant (mine one and you date half the vault
wrong, silently); receipts that belong only to the station the registry names, so
an abandoned ingest's rows and fragments are not evidence; digest-driven search
for documents the crash orphaned; retention/hold/quarantine outcomes; byte-exact
naming; 18 counters; and consumption of the spool and receipts at the end.

**Timeout calibration:** `[agent].timeout_sec` 3600 → **7200**. pass@2 caps at
3600 whatever task.toml says, but pass@5 honours it, so this converted
in-progress timeouts (worth nothing) into conceptual failures. The CI difficulty
suggestion recommended precisely this — read it, it is often right.

**The one defect species the gates kept finding:** a counter defined by what
*parsed* instead of by what the mend *kept*. `fragments_used` (QC B5, twice) and
`rebuilt_from_receipts` (caught by the pass@2 analyser, which classed that trial
as a task issue rather than an agent error). Define report counters by outcome.

**Noise to ignore without changing grading:** AVA returned seven self-agreeing
"blockers" once (each stating expectation and behaviour identically) and an empty
finding set pointing at a passing deep_review another time; both cleared on a
benign redraw. Its one real item was `importlib.spec_from_file_location` in the
mutation probe — fixed by running candidates as programs, exactly as
[[dynamo-ava-blocking-items-can-be-all-noise]] records.

**tier1 gotcha:** `base_sha` never advances, so a fix landing *before* the pinned
base is invisible to it. Symlink guards existed; E5 only cleared once realpath
resolution appeared in the cumulative diff.
