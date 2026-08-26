---
name: dynamo-publish-what-every-trial-recovers
description: "When low_timeout FAILs while difficulty_crux PASSes, publish the parameters every trial recovered identically and keep only the one they all died on."
metadata: 
  node_type: memory
  type: project
  originSessionId: 858c7146-cad6-4d04-a6cb-b2b908e4341d
  modified: 2026-08-15T00:09:44.178Z
---

Measured on dynamo-9c93375 (`dynamo/tidewell-reseat`), two evaluated heads:

| head | withheld | pass@2 | pass@5 |
| --- | --- | --- | --- |
| 1 | the whole policy — 5 freshness limits, scope limit, grade floor, corroboration minima, refusal order **and** the score | 0 solved · 0 valid · **2 in-progress-timeout** | — |
| 2 | only the score, with its *shape* stated | 1 solved · 1 valid | **2 solved · 3 valid · 0 timeouts, avg 0.400, ALL-GREEN** |

Head 1 missed on the **hard side**: `difficulty_crux` PASS, `approach_validity`
PASS, `low_timeout` FAIL on both trials, neither agent writing a line of the
deliverable. Both had independently recovered every threshold by the same method
and both died on the score — so the parameters that ate the hour discriminated
nobody.

**The rule:** read the per-trial rubric, not the pass fraction. `low_timeout`
FAIL + `difficulty_crux` PASS means publish what the trials recovered identically
and keep only what they all died on. This is
[[dynamo-provide-the-plumbing-clears-the-hard-side]] applied to *disclosure*
rather than to code — what you hand over is sometimes half the spec, not a module.

**Corollary that cost nothing: state the FAMILY of the withheld quantity.** The
pass@2 advisory observed both agents hunting a lexicographic ordering over fields
rather than a quantity computed from them; the contract then said "scored, best
taken, fixed fallback beneath" without naming a term or a weight. At pass@5 **two
of five agents still wedged the full hour in that same wrong hypothesis space.**
Disclosing the function class is what QC B5 demands anyway and it converts far
fewer wedges into finishers than the fear suggests — never pay difficulty to
withhold a function class.

Related: [[dynamo-reconstruction-beats-specification]], [[dynamo-timeouts-anchor-nothing]],
[[dynamo-operational-passat-failures]], [[dynamo-weights-need-behavioural-identifiability]].
