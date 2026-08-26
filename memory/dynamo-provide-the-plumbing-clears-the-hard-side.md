---
name: dynamo-provide-the-plumbing-clears-the-hard-side
description: "Measured on dynamo-379e527: five pass@2 draws blocked on in-progress timeouts; shipping a read-only I/O module turned the very next draw into a valid fail and pass@5 into 2 solved / 3 valid / 0 timeouts."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 78170f0c-ffe4-4520-83b2-fd6ece737755
  modified: 2026-08-14T21:15:07.282Z
---

`dynamo-379e527` (`dynamo/thornfield-warden`) missed the band from the **hard**
side for five consecutive pass@2 draws. Ten trials, and the split never moved:
2 solved, 2 countable fails, the rest cut off mid-derivation. Every draw said
`Rerun Recommended: YES`; the fifth identical draw proved that was a
distribution, not luck.

| head | change | pass@2 | pass@5 |
|---|---|---|---|
| 1 | 38 constants, 8 rungs, 20 report keys | 1 valid + 1 timeout | 1 solved, 1 valid, **3 timeouts** |
| 2 | score cut to 31 constants, 14 report keys | 1 solved + 1 timeout | — |
| 3 | +2nd straddle on every per-class boundary | 2 timeouts | — |
| 4 | ladder 8→6 rungs, 21 constants, agent 7200s | 2 timeouts | — |
| 5 | difficulty-neutral redraw | 2 timeouts | — |
| 6 | **read-only `/app/thornfield_io.py`** | **1 valid + 1 timeout — PASS** | **2 solved / 3 valid / 0 timeouts, avg 0.400, gate green** |

**What worked, and why the four cuts before it did not.** Cutting constants and
rungs (heads 2–4) reduced the crux and still left agents mid-derivation, because
the budget is spent on *total* work while difficulty lives only in the crux.
Providing the tedium removes budget without removing difficulty: a module that
implements the season reader and the whole byte layout (both table renderers, the
sorted-key space-free JSON, the trailing newline, the digest helper) and knows
nothing about the policy. Head 6 kept every constant and rung head 4 had.

**Do it this way.** Ship it read-only (`chmod 0444`, single file — the "no broad
recursive chmod" static check passes), and **stage the verifier's own copy into
every graded run** so extending it is harmless and rewriting it buys nothing.
Keep the normative byte layout in the spec anyway — `structured_data_schema`
wants it, and writing your own I/O must stay viable. Prove the wiring with a
submission that imports the module and must reproduce the reference bytes.

**Cross-check before cutting** (this is what tells volume from difficulty): list
every failure the trials have actually produced and require each to stay
reachable. Here wrong constants, wrong ladder order, a `standing` off-by-one, a
`relief_total` summed as a running total and a lambda arity crash all survived;
the only casualty was a trial that omitted a header column it had been handed
verbatim — clerical, not crux.

**The diagnostic signature (confirmed again on `dynamo-b296f2d`, 2026-08-15).**
Read the rubric aggregate, not the pass fraction. `difficulty_crux: PASS 2/2`
plus `approach_validity: PASS 2/2` plus `task_specification: PASS 2/2` plus
`low_timeout: FAIL 0/2` means the crux is real, the spec is fine, and the clock
decided — the hard side, every time. On b296f2d one trial recovered the withheld
policy *exactly* (0 mismatches on 1049 ledger rows), wrote a 334-line adjudicator
and was cut off 112 s later before it could run the script and delete a two-line
dead-code block it had itself flagged; the other spent all 49 steps on recovery
and never wrote a file. The analyser's own words: "no task or verifier fix is
indicated."

**Generalisation of the lever: when the contract has a written half and a
withheld half, ship the written half as a module that takes the withheld half as
a callable.** On b296f2d that meant `/app/tollgate_io.py` growing from
reader+writer into the full tick loop — screening ladder, seat lifetime, waiting
pool, all fourteen report counters, byte-exact writers — with the signature
`adjudicate(window, admit)` where `admit(candidates, opening)` returns the
ordered admissions. Nothing about the limits, the budget, the ordering or the
stop-vs-skip asymmetry is in it. Measured effect on the intended solution: 334
lines written from scratch → **147** lines, running in 0.37 s. Guard it with two
tests: the module must reproduce the reference byte-for-byte on every graded
window when driven by the true policy, and it must name no part of the policy
*and* have no default for its `admit` parameter (a blunt "constant N not in
source" check false-fires — `>= 2` contains `= 2`; assert on
`inspect.signature` instead).

Related: [[dynamo-volume-overshoots-the-band]] (same lever, independently measured
on dynamo-137a569), [[dynamo-pass2-overrides-the-agent-timeout]],
[[dynamo-timeouts-anchor-nothing]].
