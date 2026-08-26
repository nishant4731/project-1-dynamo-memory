---
name: dynamo-8ab540c-rate-chain-all-green
description: Dynamo 8ab540c (DSP rate chain) landed ALL-GREEN on head 13; pass@5 1/5 with 4 valid fails all on one crux.
metadata: 
  node_type: memory
  type: project
  originSessionId: 83089d54-20bc-4295-882d-348f55fcb148
  modified: 2026-08-13T17:45:38.294Z
---

`dynamo-8ab540c-hardware-embedded-and-low-level-systems` PR #1 went ALL-GREEN on
2026-08-13 at commit `6b5df4c` (13th head). Final band: **pass@5 = 1/5 solved, 4
good-valid-fail, avg@5 0.200**, and all four failures shared *one* root cause —
a flawed BFS for the two-adder reachable set (treating every one-adder value as
simultaneously available rather than sequentially held). pass@2 cleared six
consecutive independent draws.

**Why it took 13 heads.** The blocker for the first five draws was not the rules
— it was that §10 of the contract quoted the worked example's full
`chain_report.json` and `stage_ledger.tsv` byte-for-byte. Agents used it as a
step-by-step debugging oracle, verifying every intermediate quantity before
submitting, so no starved branch could trap them. Shrinking §10 to a 16-sample
"format sheet" that explicitly says reproducing it proves nothing flipped the
gate. See [[dynamo-oracle-corpus-solve-or-timeout]] and
[[dynamo-do-not-narrate-the-trap]].

**Why it survived once it was hard.** The surviving crux was *algorithmic*, not
a clause: a stated rule that is expensive to implement correctly, not one that
is hidden. Matches [[dynamo-withhold-an-algorithm-not-a-clause]] and
[[dynamo-starved-branches-need-algorithmic-depth]]. The reviewer explicitly
noted `decisive_answer_discoverable` = PASS — every decisive rule was in the
agent-visible contract.

**How to apply:** on a fully-specified spec task the ceiling is set by
implementation cost, not by information withheld. Spend the difficulty budget on
one algorithm agents get subtly wrong (here: sequential-hold vs
simultaneous-availability in a reachable-set search), and make sure the graded
corpus spans the whole range every numeric constant partitions — see
[[dynamo-mutation-sweep-finds-witness-holes]] for the ceiling hole QC caught
here after my own 83-anchor sweep reported zero survivors.
