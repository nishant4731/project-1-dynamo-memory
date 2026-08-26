---
name: dynamo-witness-must-be-load-bearing-per-path
description: "QC C3-exec blocked on dynamo-2d0d4c3 because a bound's witness merely APPEARED in the output instead of deciding it; reproducing QC's method locally found 12 survivors of 107, six of them real."
metadata:
  type: feedback
---

`dynamo-2d0d4c3-security`, 2026-08-22, head `bba9eba` blocked by `qc_exec` with
`C3-exec`. The finding was real and narrow: mutate the reference so an inbox
`admit` no longer adds its fid to `taken`, and the whole graded corpus stays
byte-identical, because **every planted duplicate twinned a record the *segments*
already held** — nothing anywhere twinned an *earlier inbox admit*.

## The two mistakes worth remembering

**1. "The value appears in the output" is not "the bound decides something."**
`test_every_inclusive_bound_sits_on_a_planted_record` was green the whole time: it
scanned the restitched segments for `bytes == 1`, `pkts == 1`, `seq == 0` and
found them. But the planting moved an *existing* flow onto each edge, and the flow
it landed on was already refused for an earlier cause or merged away, so the
record with `bytes == 1` in the output arrived via an **amend**, and no *record*
was ever sifted at the floor. Tightening `< 1` to `<= 1` changed nothing.
**Assert the mutation flips, never the value's presence.**

**2. Every code path states its own copy of a bound.** `record_cause`,
`amend_cause` and `retract_cause` each carried their own `seq >= 0`; the engine
even words them differently (`if obj["bytes"] < 1 or obj["pkts"] < 1:` on one path,
all three joined on another). Probe anchors copied from the *solution* silently
matched the *amend* line in the engine, so three probes I believed covered the
record path were mutating something else and passing for the wrong reason.
**One probe per bound per path, and check the anchor is on the path you mean.**

## Reproduce QC's method, and grade it on QC's corpus

QC mutates the **submitted solution** and asks whether the shipped verifier still
returns reward 1. A local sweep of 107 single-token mutations (comparison
operators both ways, min/max swaps, every small integer +1), each graded over the
whole corpus, found **12 survivors**; six were real unwitnessed rules (the inbox
duplicate, three bound floors on two paths, the label alphabet's digit range, and
the byte budget + 1). After fixing: **0 survivors of 105**.

**The corpus matters as much as the sweep.** My first fix put the byte-budget
witness in the *sweep* dragnets, which only feed the verifier's internal probe
test. QC grades through the verifier, whose corpus is **HELD_OUT + live +
salted** — a sweep-only witness does not count. Both edges of a packing bound also
need separate homes: a **first** segment on the budget makes the initial `used`
load-bearing, a **later** one makes the per-segment reset load-bearing.

## The fixes that worked

- A `_plant_edges` pass appending **fresh flows with a reserved fid range**
  (`f-5xxxx`; the first attempt picked `f-7xxxx` and silently collided with the
  retract fids, so the witnesses were consumed — see
  [[dynamo-planted-witnesses-need-allocation-priority]]). Fresh, valid, therefore
  *accepted*, so tightening the bound refuses them and the output moves.
- One amend on the bytes/packet floor; one amend and one retract on the sequence
  floor; a second admit reclaiming a fid an earlier inbox admit took, filed at the
  end of the last inbox file so the genuine one is always read first.
- **Delete provably-equivalent mutation sites instead of witnessing them**:
  `rsplit(".", 1)[0]` → `rpartition(".")[0]` and a `sys.path.insert(0, …)` literal.
  No conforming input separates either reading, so they are unkillable mutants
  sitting in QC's search space. Extends
  [[dynamo-c3-needs-a-clause-sweep]] and [[dynamo-bounds-need-two-witnesses]].

Any corpus change moves every record, which breaks the measure-zero byte-budget
witnesses ([[dynamo-search-the-fixture-for-its-own-edge-witness]]) — budget seeds
had to be re-searched four times across this task. Search through the **rig's own
staging path**, not `forge.build_plan` directly, or the sizes disagree.
