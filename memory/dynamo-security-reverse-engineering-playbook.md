---
name: dynamo-security-reverse-engineering-playbook
description: "PLAYBOOK Security / Reverse Engineering — ALL-GREEN disassemble-and-audit mold; pass@5 1 solved / 4 good valid, avg 0.200; the stated-algorithm ceiling and the cut that broke it."
metadata: 
  node_type: memory
  type: project
  originSessionId: 8c82f6d7-a76e-4fb1-9044-b10fe02b557e
  modified: 2026-08-23T01:19:11.962Z
---

**Category:** Security · **Subcategory:** Reverse Engineering
**Repo:** `handshake-project-dynamo/dynamo-24cfb9b-security` · PR #1 ·
heads `f9ce205` → `ee61598` → `a385abf` → `58a0869` → **`39ba1f7` ALL-GREEN**
(2026-08-23). No prior PRs on this repo.

## The mold

**Disassemble and audit an undocumented firmware container.** `dynamo/slate-teardown`:
a discontinued door controller ran applets on an in-house stack machine. The agent
writes `/app/slate_teardown.py`, which reads one `.slate` image and writes
`listing.txt`, `frames.tsv` and `audit.json`. `SLATE_TEARDOWN.md` is **complete** —
header, five drop causes in order, 25 opcodes with operands/effects/successors,
the displacement base, decode, frame depth, latch closure, gates, chokes, the cut,
all three output formats, and one whole 22-byte image worked end to end.

**The difficulty is not what is withheld; it is the shape of the three images the
container ships.** They are quiet: every byte covered by a reachable instruction in
address order, all branches forward, every join reached at one depth, call graph a
shallow tree, one gate per latch-reaching applet sitting in its entry block. The
thirteen graded images are none of those things. The agent has no ground truth for
the bench images, so self-testing cannot catch a naive pass.

## Measured

| head | pass@2 | pass@5 |
|---|---|---|
| `f9ce205` | — | — (Dynamo eval FAIL: taxonomy labels only) |
| `ee61598` | 1 solved · 1 valid | **4 solved · 1 valid · avg 0.800 — BLOCKED** |
| `a385abf` | 1 solved · 1 valid | never ran (qc_gate FAIL) |
| `58a0869` | 1 solved · 1 valid | **4 solved · 1 valid · avg 0.800 — BLOCKED** |
| `39ba1f7` | 1 solved · 1 valid, "Rerun: NO" | **1 solved · 4 good valid · 0 timeouts · avg 0.200 — PASS** |

- Cosine passed **5 of 5** pushes: instruction **0.661**, verifier **0.828**,
  fingerprint **0.790**, threshold 0.9. Fresh domain, fresh mold.
- `[agent] timeout_sec = 5400`, `[verifier] timeout_sec = 1800`. Trials took
  1h15m wall, pass@2 1h7m; agents finished in 22–55 min of the 90-minute budget,
  so there was never timeout pressure to trade against.
- Final: 93 single-rule probes over 16 sweep images, 0 survivors, none caught by
  one image; **46 of 93 leave all three bench images byte-identical** and are
  wrong on 2–13 of the 13 graded ones.

## What actually drew the four valid fails

Two clusters, and the split is the most reusable fact here.

**Cluster B — the designed bench-vs-graded asymmetry (2 of 4).** Both trials
produced *fully correct bench-image output* and broke only on held-out images:

1. chokes by **dominator intersection on a gate-truncated graph** (gate out-edges
   deleted first). Identical to correct for single-gate applets — which is every
   bench applet — and collapses toward zero on multi-gate/chained ones
   (`undercroft` 26→4, `saltmarsh` 17→0);
2. a listing writer advancing by `addr += size` instead of iterating
   `sorted(decoded)`. Equivalent when nothing overlaps; on a held-out image where
   a branch targets the interior of a `PUSHI`, the correctly decoded overlapping
   instruction is in the dict and the sequential walk skips its start address.

**Cluster A — opcode-table slips (2 of 4), `difficulty_crux` FAIL.** `NOP` missing
from the handler switch though present in the table; `NOP pushes=1`; `SPILL`/`PACK`
emitting a bare mnemonic with no `#n`. These break the bench images too. A
25-opcode table with data-dependent effects is itself a reliable failure source —
but it is *not* creditable difficulty, so do not rely on it.

`stormgate` — the densest graded image — was the one image **every** failing agent
got wrong, across all four bug classes.

## The ceiling this subcategory has, and the one lever that broke it

**Stating an algorithm precisely is transcription, however intricate it is.** Two
heads measured 4 solved / 1 valid with the spec naming three algorithms outright
(worklist decode, relaxation to a fixed point, iterative closure). The analyser
was explicit: *"the convergence on the same algorithm across five independent
agents strongly suggests the worklist + relaxation + fixed point pattern is
well-represented in training data and is reliably retrieved given the spec."*

Adding a **fourth stated rule** (chokes, defined by "no run reaches a gate without
it") did fire — all nine wrong values in that head were in the choke column,
`difficulty_crux` PASS — but converted only 1 of 5, because *"the four passing
trials each used the golden approach directly (per-instruction reachability walk),
not the dominator shortcut."* **A rule that maps onto a six-line loop is not a
wall.**

What broke it was a quantity **expensive to compute rather than hard to know** —
the same resolution as [[dynamo-security-authentication-and-authorization-playbook]]:

> **`cut`** — the fewest instructions that must come out of the applet's decoded
> graph for no gate to be reachable from its entry, with neither the entry nor a
> gate cuttable. A minimum **vertex** cut: it wants a flow with every instruction
> split in two.

Every gated bench applet is a straight chain to one gate, so the cut is `1` there
and so is every shortcut. The graded corpus needs 2 and 3 (ways that leave the
entry itself and share nothing), `-1` (a gate on or one step behind the entry),
and three applets carrying two ways that **share an instruction but no edge** —
which is the only thing that separates a vertex cut from an edge cut.

## The local candidate battery predicted pass@5 exactly

Build plausible-wrong *programs*, install each as the submission, and grade it the
way Harbor does. Every candidate below passes **every bench-image test**:

| candidate | held-out failures | reward |
|---|---|---|
| front-to-back decoder instead of following control flow | 18 | 0 |
| chokes by address order through the first gate | 16 | 0 |
| "one cut is always enough" | 10 | 0 |
| a correct minimum **edge** cut | 4 | 0 |
| correct, reversed worklists + compact JSON | 0 | **1.0** |
| imports the reference out of `/tests` | blocked | 0 |

The first two map exactly onto the Cluster B failures the analyser found. See
[[dynamo-naive-variant-probe-predicts-fails]] — this is the strongest confirmation
of it so far.

**The equivalence candidate is a soundness test, not just anti-cheat.** Grading a
correct program written differently (`pop()` → `pop(0)` on both worklists) found a
real **order-dependence defect**: classifying underflow/overflow *during* the depth
relaxation makes the answer depend on the queue order. Fix: settle the depth map to
its fixed point first, cap leaving depth one slot past the frame so the lattice is
finite and the system monotone, and read the sites off the settled map. A permanent
test now runs both walks as a queue and as a stack and requires the same answer.

## Hurdles, per gate, in the order they blocked

1. **Dynamo eval — `accurate_taxonomy_labels`** (only FAIL of 31 on push 1).
   `artifact_type` claimed `binary_executable_or_library` and
   `hardware_or_firmware_artifact`; the firmware is a read-only **input**, and the
   agent produces one script. Reduce to what the agent actually hands back.
2. **qc_gate — A6 + B5, both off one sentence.** §7 said runs *"follow edges
   backwards as readily as forwards"* (meant: a step may land on a lower address);
   QC read it as **undirected reachability**, found the rival reproduces every
   disclosed answer, and called the reference wrong. Fixed by saying a step leaves
   an instruction by one of *its own* successors, in the direction that successor
   runs, never against one — and by **rebuilding the worked example so its answers
   exclude the rival** (a conditional whose other arm rejoins past the gate makes
   the undirected count come out one lower). A probe and 8 graded applets now
   distinguish the readings.
3. **trials, twice at 4 solved / 1 valid** — see above.
4. cosine, static, review, similarity, validation, AVA, deep_review, tier1,
   qc_eval, qc_exec: **never blocked**, on any push.

## Levers measured NOT to work here

- **Naming the algorithm.** Three stated algorithms → 4/5 solved, twice.
- **A fourth stated rule with a short correct implementation** (chokes by removal)
  → still 4/5 solved. It converted the one agent who reached for a textbook
  shortcut, nobody else.
- **Volume / more opcodes.** Trials finish in 22–55 min of 90; there is no time
  pressure, and adding work does not add failures.

## Operational notes

- **`pyc` cache collisions silently break a mutation sweep.** Writing each mutant
  to the same `variant.py` makes same-length single-character edits reuse the
  previous `.pyc` (invalidation is mtime+size, 1-second granularity), so every such
  probe reports "survivor". Write a uniquely named file per probe and pass `-B`
  plus `PYTHONDONTWRITEBYTECODE=1`. This cost a debugging round and would have made
  the verifier flaky in CI.
- **Seal the overlay before graded runs.** A candidate that `exec`s
  `/tests/_slate_engine.py` passed everything until `os.chmod(HERE, 0o700)` was
  added at rig import and the run dropped to `nobody`. Dropping privileges alone is
  not enough — `/tests` is world-readable.
- Run the candidate from a **copy in a scratch dir** under `python3 -I`, so
  `sys.path[0]` holds only the submission; that is what enforces "one file".
- **Do not carry an unkillable probe.** Three were provably equivalent given the
  surrounding guards (`find(off)` vs `find(off+1)` once NUL is outside the charset;
  a range test already implied by `target in decoded`; two redundant mechanisms
  making the entry uncuttable). Delete the redundancy in the reference so the
  question stops existing, rather than keeping a probe green by exception.
- Keep the **worked example degenerate for every crux** — it is the only disclosed
  answer, so any trap it demonstrates is handed over. Here it agrees with the
  address-order choke reading and with cut `1`, and disagrees only with the
  undirected rival, which is exactly what QC required.
