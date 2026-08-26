---
name: dynamo-ambiguity-fix-needs-a-paired-algorithmic-trap
description: "Measured on dynamo-63f2f80: stating the boundary that killed both pass@2 trials sent pass@5 to 5/5; only an algorithmically subtle blind branch replaced it, not another disclosed subsystem."
metadata:
  type: project
---

Three evaluated heads of one task (`dynamo/squash-layer-stack`, Container Builds):

| head | change | pass@2 | pass@5 |
|---|---|---|---|
| 016e716 | 9 blind rule families, root-opaque boundary **unstated** | 0/2, 2 valid fails | not reached (AVA blocked) |
| 9a8c57a | root-opaque **stated** + provenance ratchet (new manifest column, new counter, third tally) | 1/2 | **5/5 solved, avg 1.000** |
| 37f656b | + content-defined chunker whose 3 decisive branches the shipped stack cannot reach | pending | pending |

**The mechanism.** Both 016e716 failures were the same boundary: an opaque marker
whose canonical path is a single component names the root (empty-string parent),
and a flat-dict implementation never matches it. Deep review rated it
*derivable but unstated* — Advisory 1, non-blocking. Stating it fixed every
agent's code. Solve times: 31 min, then 17–42 min of 60. Flat. The provenance
ratchet (origin beside layer, `bytes_by_origin` splitting one total along a
different line) is a textbook "value source differs" kill and still bought
nothing.

**What replaced it.** One requirement that is hard to *implement*, not hard to
*read*: a rolling-window chunker with a minimum that suppresses early boundaries,
a maximum that forces late ones, and a window reset per cut. The shipped stream
never puts the mask on zero, so it yields one chunk and all three branches are
dead code during the agent's own testing. Proof before pushing: a chunker
dropping all three passes 236 of 246 checks and every shipped-stack comparison.

**How to apply.** A prose clarification a reviewer merely *recommends* can still
cost the whole difficulty budget — before making one, ask what kill remains and
budget the replacement in the same push. And prefer a branch whose *correct
implementation* is non-obvious over another stated rule: see
[[dynamo-blind-sample-branch]] and [[dynamo-blind-branch-shipped-fixture-proof]].
Related: [[dynamo-spec-mold-caps-at-80pct-solve]],
[[dynamo-recovered-constants-are-still-transcription]].
