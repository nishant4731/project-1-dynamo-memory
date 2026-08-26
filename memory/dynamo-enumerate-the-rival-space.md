---
name: dynamo-enumerate-the-rival-space
description: "On a policy-reconstruction task the hand-written rival list said the log pinned the policy; enumerating the full ranking space found four survivors it had missed, all involving a field the policy ignores."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d555551c-8ce6-4f22-9ff0-31ffdbae2e56
  modified: 2026-08-14T19:20:44.331Z
---

Measured 2026-08-15 on `dynamo-25a45c7` (`dynamo/atlas-curate`). The task withholds a
curator's admission policy and requires it to be recovered from a 1261-row decision
log, so the whole fairness case rests on the log pinning the policy uniquely.

**The curated audit was clean and wrong.** A hand-written rival family — every limit
perturbed both ways, every component of the ranking dropped, reversed, or transposed,
plus structural variants — reported 0 survivors over 419 rivals. Then I stood in for
the solver and brute-forced the space an agent would actually search: every ordering
over every subset of the rankable quantities, both directions, at every saturation.
**Four survivors**, all of them keys that also rank on `cells`, a field the real
policy ignores entirely. The log never happened to contain two candidates that tie on
everything above `cells` while differing in it, so ranking on cost explained every
row and would have produced different answers on the graded bundles. That is a B5
ambiguity that the curated list structurally could not see, because I only enumerated
perturbations *of my own policy* and never a field my policy does not use.

**The rule: enumerate the rival space, do not curate it.** A hand-written rival list
tests what the author thought of; the point of the audit is what they did not. Include
every quantity the contract admits into the decision, including the ones the answer
ignores — "the policy does not use it" is the claim under test, not a reason to skip
it. Ship the enumeration itself as a verifier test so the property survives later
fixture edits.

**Fixing it is a calibration pool, not a weaker check.** Two pairs, each alike on
every ranked field and differing only in the ignored quantity, with the pairs arranged
in opposite directions so ranking on it ascending contradicts one pair and descending
contradicts the other. After that, 31,599 enumerated rankings left zero survivors.

**Watch the second-order break.** Adding the calibration pool fixed the log but broke
the graded side: the new rivals had to change a graded artifact too, and the fixture's
planted pairs all carried equal `cells`, so four of them changed nothing on any
bundle. The two questions are separate and both need asking — *does the evidence
contradict this reading* and *does this reading fail the verifier*. A reading that the
log rules out but the grader accepts is not a fairness bug, it is a C3 hole.

Related: [[dynamo-reconstruction-beats-specification]],
[[dynamo-blindness-table-before-pushing]], [[dynamo-c3-needs-a-clause-sweep]].
