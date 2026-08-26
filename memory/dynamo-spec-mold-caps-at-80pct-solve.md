---
name: dynamo-spec-mold-caps-at-80pct-solve
description: "Measured over three pass@5 runs — a fully-specified spec task solved ~80% regardless of rule volume; added volume converts failures into timeouts, not valid fails."
metadata: 
  node_type: memory
  type: project
  originSessionId: 1f50bdfb-64dc-492e-81b8-06b22ad799d3
  modified: 2026-08-12T19:57:48.521Z
---

Measured on `dynamo-56ae913` (2026-08-12/13), three consecutive pass@5 runs on the same
engine, each after a deliberate ratchet:

| version | solve time | pass@5 |
|---|---|---|
| documented spec, no oracle corpus | ~19–28 min | 3 solved · 2 valid fail |
| + bench-span voiding + weighted standings | ~19–28 min | 4 solved · 1 valid fail |
| + a fourth graded artifact (per-item digest) | **~45–47 min** | 4 solved · **0 valid fail** · 1 timeout |

**The volume lever moved the clock but not the solve rate.** Doubling implementation time
left 4/5 solving and converted the single non-solver from a countable failure into an
in-progress timeout, which does not anchor the gate. Two earlier ratchets that added *rules*
(rather than work) moved solve time barely at all — against a complete normative spec, more
rules buy typing, not thinking.

Two process mistakes worth not repeating:
- **Never ship a difficulty ratchet and a kill-removing fairness fix in one push.** Adding
  two rules while simultaneously clarifying the sorted-key mandate (which had been failing
  agents) netted out *easier*: 3/5 → 4/5 solved.
- Check similarity of the two compared facets *before* pushing, not after; and see
  [[dynamo-cosine-does-not-block-self]] — cosine did not actually block on self-match here.

**How to apply:** for the pass@5 band on this agent, the fully-specified-spec mold appears to
cap near 20% per-trial failure, matching the playbook's "fully-specified-spec ceiling" (fair,
self-contained, spec-driven tasks cap at ~20–40%). The oracle-corpus alternative caps
differently and worse — see [[dynamo-oracle-corpus-solve-or-timeout]]. Reaching 0–2/5 with
≥3 valid fails needs a different *concept*, not another ratchet on the same one: the levers
that historically worked were evidence-mined hidden parameters pinned by narrow evidence, and
operational irreversibility, applied from the first submission rather than bolted on.

**Third and fourth measurements (`dynamo-137a569`, `dynamo/rollup-evalrun`, 2026-08-13).** Same
conclusion from a much bigger ratchet. Head 1: a complete normative charter, 8 decisive branches
each *measured* byte-identical on the visible pack and caught on 3-5 of 9 held-out packs →
**2/2 solved in 9.5 and 15 min** of 60. Head 2 added three interacting subsystems — per-judge
adjudication constants deliberately absent from the charter and recovered by searching 87 gains
x 101 hinge positions per judge, suite revisions re-keying the shard identity, and a third graded
artifact — with 12 of 12 plausible misreadings measured blind on the visible pack →
**2/2 solved in 19 and 20 min**. Solve time roughly doubled; the failure rate stayed at zero.

The trial analysis named the mechanism precisely: "the golden approach [is] strongly implied by
the specification", and the platform's own difficulty suggestion said the recovery "reduces to a
mechanical brute-force enumeration over bounds the charter explicitly states". **Disclosing the
functional form and the parameter ranges turns inference back into transcription** — an
evidence-recovered constant is not a wall if the shape and the search space are written down.
The remaining lever the suggestion points at is *model selection*: leave one structural choice
(a second breakpoint, absolute vs proportional hinge, affine vs linear gain) to be inferred from
the calibration rows, with the visible pack's judges all taking the simple form, so a solver that
implements only that form is byte-identical on the sample and wrong on the held-out packs.

**Fifth measurement — the model-selection lever does not break the ceiling either
(`dynamo-137a569`, head 3, 2026-08-13).** After two 2/2 draws, the platform's own advisory said
to make the adjudication model's *shape* under-specified so recovery becomes model selection
rather than a parameter search. Implemented exactly that: the charter names a family (bias plus
**one or two** hinges, each with its own gain) and guarantees only that a pack's calibration rows
pin its judges uniquely, so the number of bands must be inferred before any constant is fitted.
Every judge in both visible packs has a single band, and a solver implementing only the one-hinge
family was *measured* byte-identical on the visible pack and rejected on 6 of 10 held-out packs.
**pass@2: 2/2 solved, 16 and 34 minutes.** Solve time finally moved (34 min is the longest of the
three heads) but the failure rate stayed at zero, and `difficulty_crux` was PASS on both trials —
the agents engaged the crux and beat it.

Three heads, three 2/2 draws, on one repo: 9.5+15 min, 19+20 min, 16+34 min. **Whatever is
derivable from a normative contract plus a uniquely-pinning evidence corpus, this reference pair
derives** — even when the thing to derive is which model generated the evidence. The remaining
untried levers are the ones the playbook lists as *different concepts*, not ratchets: operational
irreversibility (measured to fire 0/5 recently), or a policy induced from labelled outcomes with
no uniquely-pinning corpus at all — which collides with `qc_gate` B5 and with
[[dynamo-oracle-corpus-solve-or-timeout]]. Budget the decision before the build: three ratchets
cost a full day and three of six daily pass@2 runs.
