---
name: dynamo-inprogress-timeouts-need-an-early-write-nudge
description: "pass@5 0/5 with 4 in-progress timeouts is a write-out problem, not a difficulty problem; ask for the deliverable early."
metadata: 
  node_type: memory
  type: project
  originSessionId: a4ba242f-9e0e-4fb9-ad2a-ae0d21e1b541
  modified: 2026-08-15T04:10:41.314Z
---

Measured on dynamo-e3b1da9 (cairn-salvage), 2026-08-15. pass@5 returned
**0 solved · 1 good-valid-fail · 4 in-progress-timeout · avg@5 0.000 — BLOCKED**
for want of counted failures, with `difficulty_crux`, `approach_validity`,
`task_specification` and `reward_hacking` PASS on all five trials.

All five trials were the same shape: recover the priority order and chain
semantics, plateau at 98–126 of 188 logged rounds on one remaining constant, get
cut off still analysing, and **never write the deliverable at all**. Every trial
held a usable candidate policy for most of the hour.

**Why:** an inferred-policy task invites "finish the inference, then code". That
strategy converts every failure into an in-progress timeout, which counts for
nothing at the gate. The pass@2 analyser named it twice before pass@5 did:
"neither agent treated code production as incremental".

**RESOLVED — the fix that worked was disclosing the function's SHAPE, not the
prompt nudge.** Asking for the artifact early (plain working-practice wording in
`instruction.md`) improved pass@2 but did NOT survive pass@5: a second draw came
back 0 solved / 1 good valid / **4 in-progress timeouts** again, because the
stronger reference pair pushes deeper into analysis before writing. What flipped
it was stating the *family* of the one constant every trial was stuck on — "a
fixed number of bytes plus a share of the allowance, neither figure written
here" — leaving the values, the five-part order and the two counts withheld.
Measured immediately: **0 solved · 4 good-valid-fail · 1 in-progress timeout ·
avg@5 0.000, gate PASS.** Four uncounted timeouts became four counted failures
and no trial solved. This is [[dynamo-provide-the-plumbing-clears-the-hard-side]]
applied to inference rather than typing: give away what only costs clock, keep
what costs understanding.

**How to apply:** when the taxonomy is mostly in-progress timeouts and the crux
criteria all PASS, do not touch the difficulty — adding to it and cutting it both
make it worse ([[dynamo-provide-the-plumbing-clears-the-hard-side]]). Ask for the
artifact early in `instruction.md`, in plain working-practice terms: get the
program emitting all four files as soon as any candidate exists and refine it
after. An agent that writes a policy matched to 126/188 emits well-formed, wrong,
gradable files — a good valid fail. The same agent silent at the buzzer is
nothing. It leaks no rule: being told to save early does not help anyone recover
the withheld policy.

Also confirmed here: **pass@2 does not predict pass@5 in either direction.** The
immediately preceding pass@2 was 0 solved / 2 valid-fail / **0 timeouts** — a
perfect draw — and the same head produced four in-progress timeouts over five
trials. See [[dynamo-timeouts-anchor-nothing]].
