---
name: dynamo-sample-starving-does-not-beat-a-general-implementer
description: "Starving the shipped sample only defeats solvers that generalise from the sample; Opus-4.8 reads the spec and implements the rule, so seven draws of sample-starves all solved."
metadata: 
  node_type: memory
  type: project
  originSessionId: e59d8a68-7870-4d5d-8ebf-3a89e06e8c82
  modified: 2026-08-17T08:06:21.580Z
---

Measured on dynamo-65cf2ab (residue-mill-salvage, 2026-08-17), seven pass@2 draws on one concept.

I built three independent sample-starves, each verified byte-identical on the shipped sample and
materially wrong on the graded mills:

1. **closure depth** — sample closes in one pass, graded mills need 2–9;
2. **lane turnover** — sample lanes all turn over on schedule, graded mills drift;
3. **per-band allowance** — `band_guards` empty on the sample, non-empty on graded mills.

All three were solved on first contact. The reason is simple and I should have seen it earlier:
**a sample-starve only catches an implementation that infers the rule from the sample.** This model
reads the charter and implements the stated rule generally, so what the sample happens to exercise
never enters its solution. The starve is invisible to it in exactly the way it is invisible to a
correct implementation.

What the draws actually measured:

| draw | result | cause of failure |
|---|---|---|
| 1 | 1 solved / 1 timeout | counter scope slip (`sealed_rows`) + `os.remove` on a directory |
| 2, 3 | 2 solved | — |
| 4 | 0 solved / 2 valid fails | undisclosed `margin`, undefined `spare` below k |
| 5 | 0 solved / 1 valid fail | undisclosed `margin` |
| 6, 7 | 2 solved | — (both gaps closed fairly) |

**Every valid failure came from a gap in the spec, not from the crux.** Closing each gap fairly
returned the task to 2/2 solved. Adding a fourth axis (four no-artefact scope counters) after that
changed nothing.

The operational conclusion: for a fully-specified deterministic spec over a visible instance, the
sample-starve is not a difficulty lever against this model at all — it is only a fairness property
(it stops a lookup table). The levers that remain are the ones the playbook already names:
irreversibility, evidence the spec cannot fully describe, or a different mold. Do not spend draws
building a fourth starve.

Supersedes the optimism in [[dynamo-mutual-closure-starved-by-anchor-density]] about that specific
concept: the mechanism there is real and byte-identical on the sample, but it did not produce
failures once the charter was fair. Related: [[dynamo-determined-exact-tasks-are-transcription]],
[[dynamo-stated-optimum-gets-solved]].
