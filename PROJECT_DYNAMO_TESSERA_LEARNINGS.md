# Dynamo task learnings — tessera-decant (repo dynamo-7e6bfa7)

Everything here is measured on the pipeline, not inferred. Numbers are real runs.
Written so the next task can skip the cycles this one spent.

## 1. The gate arithmetic that decides everything

`trials` (pass@5) needs **>=3 failures that count, with >=1 "good valid fail"**.
The taxonomy is what matters, not the pass fraction:

| classification | counts? |
| --- | --- |
| solved | no (obviously) |
| **good-valid-fail** — finished, wrong answer, sound approach | **anchors the gate** |
| soft-timeout-fail — stuck/looping at cutoff | fills only, cannot anchor |
| in-progress-timeout — still making progress at cutoff | **counts for nothing** |
| task/verifier-issue | blocks; means the task is broken |

The single most important consequence: **an agent that runs out of clock is worth
nothing.** The goal is agents who *finish and are wrong*, not agents who are slow.
Adding difficulty that adds work pushes toward timeouts and makes the gate harder
to pass, not easier.

## 2. Measured regimes on near-identical heads

The same fixture moved through three regimes with small changes:

| configuration | pass@ result |
| --- | --- |
| 3 archive runs, all constants hidden | pass@2 1/2, **1 good valid fail** |
| 2 archive runs, constants hidden | pass@5 2/5 solved, 3 in-progress timeouts, 0 anchors |
| 2 runs, 4 constants disclosed | pass@2 **2/2 solved** (too easy) |
| 2 runs, 3 disclosed (cutoff re-hidden) | pass@2 pass, genuine failure |
| + two QC fixes added work | pass@2 **0/2, both timeouts** |
| + both step orders disclosed | pass@2 pass again |

**Read that table before touching difficulty.** The task sits on a knife edge at
the 3600s cap (hard cap — raising `[agent].timeout_sec` above it does nothing).
Two samples never settle where the edge is.

## 3. What actually discriminates (and what only costs time)

Costs the hour, sorts agents by patience, **give it away**:
- recovering flat constants readable off one straddling pair
- the order classification rules fire in; the order naming steps apply in
- which two stamped rows anchor a line; where collision ordinals start

Sorts agents by understanding, **withhold it**:
- a constant confounded with an artifact (the lane cutoff is not the hot lane's
  span, because eviction trims that lane from the old end — one trial missed it
  by 4.36x)
- **hinged** constants: two caps where a solver fitting one constant per knob
  matches most of the corpus and diverges on held-out data
- a rule the corpus does not witness at all (see §4)

## 4. Starve the sample, not the rule — the one lever that produced anchors

The only thing that reliably produced a *good valid fail* was a rule that is
**stated in the notes and absent from the worked corpus**:

> a stretch of a ticket log holding one stamped row fixes an origin but no slope,
> so it runs at the rate of the nearest earlier stretch holding two — or the
> nearest later one when it opens the catch.

Measured blindness table (graded cisterns vs the archive as control):

| misreading | graded | archive |
| --- | --- | --- |
| held flat at origin | fails 7/7 | reproduces exactly |
| borrows forwards first | fails 7/7 | reproduces exactly |
| takes the immediate neighbour | fails 7/7 | reproduces exactly |
| rated across the whole catch | fails 7/7 | reproduces exactly |
| truncated rounding (control) | fails 7/7 | **caught** |

The control row is the point: starve **one rule**, never the evidence. If the
corpus stops pinning a constant, that is ambiguity and QC blocks it as
hidden-knowledge.

**Do not narrate it.** A paragraph added to `instruction.md` saying "three runs
are not a catalogue of every situation, read the notes" took pass@5 from a
working head to **4/5 solved**. Removing the signpost restored it. The rule must
be stated plainly among the other format rules — no bold, no lead-in flagging it.

## 5. QC's recurring finding: a rule can be stated and still ungraded

Three consecutive blockers were the same species — the notes state a rule, and no
graded fixture exercises the point where readings diverge. Each needed a
constructed witness, and each was measured 0/7 before and 7/7 after:

- **eviction victim**: "the oldest row" never defined; a registered-first rival
  reproduced both archived runs exactly. Fixed by stating smallest hall tick
  *and* the tie-break.
- **collision ordinal**: only `~2` ever reached the register, so a decanter
  misplacing the ordinal from the third collision on graded as correct. Fixed
  with a third colliding name that outlives eviction.
- **rounding tie-break**: every drift probe rounds strictly up or down, so
  `2*rem >= den` and `2*rem > den` agreed everywhere. Fixed by constructing an
  exact-half ticket.

Still open at hand-off: the eviction **tie-break** (two rows sharing a hall tick)
is stated but ungraded. Seeding two same-tick rows does **not** work (measured
0/7) — both are oldest, both get evicted, the order never surfaces. The cut must
fall *between* them, which means placing them as the oldest rows remaining at the
*final* admission to that lane, not the oldest overall.

**Standing guard built for this:** a test pins the set of lesions the archive
cannot distinguish. Anything joining that set without a matching sentence in the
notes is a rule the agent is expected to guess. It caught a real regression and
corrected me twice.

## 6. Fixtures that do not survive the trip into the image

Two separate cycles lost to this, same root cause: **the local gate tests the
fixtures you generate, the pipeline tests the fixtures that ship.**

- **symlinks** flatten to empty files through the snapshot into the agent image
- **empty directories cannot be stored by git** — a blocked spill path arrived
  missing, reading as "never landed" instead of "blocked by a directory", and
  silently stopped witnessing that rule

Fix the *class*: a test now walks the committed archive and fails on any empty
directory under a spill path. Put a file inside any directory fixture.

## 7. The lane budget silently eats witnesses

Any new surviving row in a saturated lane evicts an old one — repeatedly the
naming, eclipse and long-stem witnesses. Symptoms appear as unrelated lesions
"slipping past". Rules that worked:

- give rows that only need to anchor a line a payload **defect**, so they cost no
  lane budget (a stretch whose marked payloads are damaged has damaged drift
  probes too)
- when a witness must survive, **raise the lane cap** rather than hoping
- freeing a filler slot *outside* the eviction cut frees nothing — check the
  register, do not reason about it

## 8. Arithmetic worth not re-deriving

Solving `(step * rise) % span == span/2` gives an offset of exactly
`span / (2 * gcd(rise, span))`. Therefore:
- an exact half sits at the stretch's **midpoint at best** — its position cannot
  be steered, only the **width of the carrying stretch** matters
- it exists only where `span` carries strictly more factors of two than `rise`;
  compute span as the next multiple of one extra power of two, do not search
- requiring `span` even *and* coprime with an even `rise` **never terminates**

## 9. Pipeline facts

- `[task].description` is **required** by the static gate even though the rubric
  does not enumerate it. Deleting it turned "Static checks OK" into failure with
  that deletion as the only change. The review eval flags it as extraneous —
  that finding is a false positive; keep the field.
- `difficulty_explanation` **must not cite pass@ results**; results-based claims
  fail criterion 17.
- PR bot comments are **edited in place**; sorting by `createdAt` returns stale
  bodies. Read the run log for the head you care about.
- Verifier must be **idempotent** and `solve.sh` re-runnable; reward file must
  never be chmod'd (Harbor reads it host-side).
- `/tmp` is shared with other sessions on this laptop — helper scripts were
  clobbered mid-run, one silently. Keep them in the session scratchpad. Never
  blanket `docker kill`; match your own container.

## 10. Recommended order for the next task

1. Design one archive-invisible, algorithmically deep rule first; everything else
   is transcription and will not produce anchors.
2. Keep total agent work well inside the hour — budget for finishing, not for
   maximum inference.
3. Build the blindness table and the archive-blind pinned set **before** the
   first push.
4. For every stated rule, construct the fixture where the readings diverge, and
   measure 0/7 -> 7/7. QC will find the ones you skip.
