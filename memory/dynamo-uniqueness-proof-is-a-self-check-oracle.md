---
name: dynamo-uniqueness-proof-is-a-self-check-oracle
description: "On dynamo-9a0adfd the identifiability proof QC demands also hands the agent a perfect self-check, so recovery costs time and never correctness; withholding a SECOND subsystem and deleting the worked example took it all-green at pass@5 2/5 with 3 good valid fails."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 8504a782-4d72-476d-a8d8-e85c0b0f3b22
  modified: 2026-08-14T23:15:19.503Z
---

The [[dynamo-reconstruction-beats-specification]] mold says: stop stating the
policy, make it recoverable from a large labelled log. QC B5 then demands you
*prove* the log pins it — every rival ordering, every perturbed constant, every
rival rule shape contradicted. On `dynamo-9a0adfd` (`dynamo/coppergate-deal`)
that proof is exactly what defused the task.

**The mechanism.** If the log uniquely determines the policy, then replaying a
candidate policy against the log to zero mismatches *proves it correct*. The
pass@2 analyser caught an agent doing precisely that: "confirmed 0 appetite
mismatches and 0 verdict mismatches across all 583 bid_log rows". Recovery can
therefore cost an agent time and can never make it wrong. What is left is a
volume-bound task, and [[dynamo-volume-bound-tasks-oscillate]] says those have no
fixed point — measured here in three heads:

| head | change | pass@2 |
|---|---|---|
| full board | 22 constants, log-recovered policy | 0/2, both in-progress timeouts, `difficulty_crux` PASS |
| board cut (spill + crest gone, `reach()` provided) | | 2/2 solved, 15 and 24 min |
| round made an assignment, starved on the shipped match | | 2/2 solved, 19 and 23 min |

**The diagnostic worth copying.** Run each mutant of your reference against the
*evidence corpus* and ask which ones it leaves label-identical. Here **41 of 76**
were undetectable from the bid log — every rule of the round loop and of
serialisation. The log verifies the policy and nothing else. That number tells
you where the remaining difficulty must live, and it is not where you think.

**Corollary that cost a head.** With the policy self-checkable, the *worked
example* becomes the only oracle for those 41. The trials showed both agents
writing real round-loop bugs — `STEP[cried_suit]` instead of the lot's own suit,
`spend_total` accumulated globally, a lexicographic sentinel of `"-"` instead of
one sorting after every id — and catching **every one** against the example
before submitting. Publishing a worked example in a reconstruction task is
handing over an answer key for exactly the half the evidence corpus cannot
check. Ship the byte layout as normative prose plus a read-only I/O module that
implements it, and publish no computed output at all; then a verifier test
asserts the rules quote no row and no report of any graded match.

**Also reconfirmed:** [[dynamo-stated-optimum-gets-solved]] beats
[[dynamo-withhold-an-algorithm-not-a-clause]] when the objective is spelled out.
Making the round a max-cardinality-then-max-appetite assignment, with the shipped
match built never to contend so a greedy pass is byte-identical there, did *not*
produce failures: both agents read the rule and "wrote coppergate_sim.py using
DFS assignment". Starving the sample only bites when the agent has no reason to
look for the rule; a stated objective is a reason.

**How it was finally won (ALL-GREEN, pass@5 2 solved / 3 good valid fails /
avg@5 0.400).** Withhold a *second* subsystem whose evidence mostly does not
discriminate — here which offer each surviving house takes, recoverable only
from 165 logged rounds, where the natural sequential reading fits every
non-contending round and the shipped instance is built never to contend. Then
delete the worked example so the reimplementation has no oracle at all. All five
trials recovered both withheld policies perfectly (543/543 bids, 165/165
rounds); every failure was a faithful-reimplementation slip cascading through
thirty rounds of state. **The withheld subsystem need not be the thing that
fails — it is the thing that consumes the analysis, so the reimplementation
happens under pressure and unchecked.**

Prove the withheld rule by *search*: replaying 101 rival objectives left 13
survivors, then 7 after requiring a survivor to also change a graded answer, all
differing only in where an unseated slot sorts; three purpose-built rounds closed
it. A curated rival list would have shipped a hole.

See [[dynamo-oracle-corpus-solve-or-timeout]], [[dynamo-calibration-ledger-not-an-oracle]].
