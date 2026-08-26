---
name: dynamo-green-checks-do-not-audit-your-proof
description: The identifiability search that proves a reconstruction task fair can itself be unsound; on dynamo-b296f2d its cap floors excluded a whole policy family and every gate still passed.
metadata:
  type: feedback
---

`dynamo-b296f2d` shipped `test_each_ledger_admits_exactly_one_policy`, an
exhaustive search asserting the evidence pins exactly one policy — the load-bearing
fairness claim, and the one QC B5 and deep review both leaned on by name.

It had a hole. `lower_bounds()` derived the capacity floors from **live**
occupancy (a candidate was admitted at occupancy N, therefore the cap is > N).
That inference is only valid when the limits read live occupancy. For the rival
family whose limits read the round's **opening** counts, occupancy can exceed the
cap within a round, so the true limit could sit *below* the computed floor —
outside the searched grid, never found. "Exactly one policy fits" was partly an
artefact of where the grid started.

Nothing caught it: static checks, Dynamo eval 31/31, deep review, AVA, qc_eval,
qc_exec and qc_gate all passed with it present. It surfaced only because an
unrelated experiment — searching for an alternate policy to give a held-out
window — returned **zero** consistent policies for a policy known to be correct
by construction. That impossible result was the tell.

**How to apply.** When a task's fairness rests on a search, the search is
load-bearing code and needs its own adversarial test: feed it a policy you
constructed and demand it find *that* policy. Run this for policies spanning
every branch of the family, not just the shipped one — a floor, prune or early
exit derived under one branch's assumptions silently excludes the others. Treat
"0 survivors for a known-good input" as a proof bug, never as a data quirk.

Related: [[dynamo-generator-dedupe-unwitnesses-rules]] (same species: the check
you rely on cannot see the assumption underneath it),
[[dynamo-widen-the-hypothesis-space-not-the-evidence]].
