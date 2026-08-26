---
name: dynamo-naming-the-wrong-reading-costs-passat5
description: Stating the withheld function class fixed pass@2 timeouts and cost pass@5 - 2/5 solved became 4/5 on one sentence.
metadata:
  type: project
---

Measured on dynamo-9c93375 (tidewell-reseat, Debugging and Repair / Configuration
Repair), two heads of the same task differing only in one contract sentence.

Section 7.3 withholds which admissible offer wins. Agents kept burning ~50 min
exhausting all ~3840 lexicographic orderings of the offer fields and timing out.
The pass2_suggestion advised saying the choice is a scalar, not an ordering, and
[[dynamo-publish-what-every-trial-recovers]] plus the task's own history said
stating the SHAPE is cheap. So 7.3 gained: "The score is one number worked out
from the particulars of the offer in front of it; it is not an order imposed on
them."

| head | 7.3 | pass@2 | pass@5 |
|---|---|---|---|
| d8a1cbe | withheld | 1/2 | **2 solved / 3 valid fails** -> ACCEPTED |
| d08d500 | shape stated | 1 solved / 1 valid / **0 timeouts** | **4 solved / 1 valid**, avg 0.800 -> BLOCKED "not hard enough" |

Both effects are real and they point opposite ways. At pass@2 the sentence did
what it was for: the in-progress timeout became a clean gradable valid fail. At
pass@5 three trials went straight to the right function class and produced
byte-exact everything - all 26 counters, all nine held-out fields, the salted
field.

The distinction that matters: stating the function class is cheap ("scored, best
taken, fixed fallback beneath" - already in 7.3 and survived at 2/5). Naming the
wrong reading is not. "Not an order imposed on them" is the second kind, and it
deletes the dead end that was doing the discriminating. See
[[dynamo-do-not-narrate-the-trap]] - same result, now with a pass@5 number.

Corollary worth its own line: a pass@2 in-progress-timeout and a pass@5 wedge are
not the same object. The bbf29a4 timeout was an agent cut off mid-fix
(low_timeout FAIL); the d08d500 wedge was an agent that spent the full budget on
analysis and never implemented, and the rubric scored it a GOOD VALID FAIL
(low_timeout PASS, difficulty_crux PASS). Do not spend difficulty unwedging the
second kind - it already counts.
