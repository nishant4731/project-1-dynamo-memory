---
name: dynamo-starved-branches-need-algorithmic-depth
description: "Measured on dynamo-8ab540c: twelve disclosed-but-never-sampled branches still gave 2/2 solved in 7 minutes — starving the sample only works when the starved branch is hard to implement."
metadata: 
  node_type: memory
  type: project
  originSessionId: 83089d54-20bc-4295-882d-348f55fcb148
  modified: 2026-08-13T00:12:37.865Z
---

Built a DSP bring-up task (`dynamo/rate-chain-bringup`, 2026-08-13) explicitly around the
lever from [[dynamo-blind-sample-branch]]: the shipped chain ran at interpolation 1, phase 0,
differential delay 1, never wrapped a register, never clipped, never hit a rounding tie, never
capped or zeroed a shift and had whole-number delays, so **twelve** decisive rules were fully
specified in the contract and never observable in the agent's own testing. Grading was
byte-exact on ten protected chains plus a submission-salted one.

**pass@2: 2/2 solved, ~7 minutes per trial, zero valid fails.** Both agents read the contract,
wrote the whole model in one step, validated on the worked example, and finished. The analysis:
"the contract's prescriptive language was detailed enough to uniquely determine the
implementation without relying on unguided derivation."

**Why the lever failed here but worked on crosstalk-bench.** On `dynamo-44fbd85` the starved
branch was an *algorithm* (Hermite normal form over Z) — plausible implementations are subtly
wrong, so being unable to test it was fatal. Here every starved branch was a *stated rule* one
line long. A careful reader implements a stated rule correctly the first time, and starvation
adds nothing. The lever multiplies an existing per-rule error probability; against this
reference pair that probability is near zero for one-line rules.

**Three draws, one task, same answer.** After the first 2/2 I added a subsystem the
contract states as an objective rather than a procedure (design the decimating tail: enumerate
ordered factor sequences, score them with a disclosed multiply cost, tie-break lexicographically;
largest-factor-first is optimal on both visible briefs and wrong on six of ten protected ones) —
**2/2 again**. Then I added the binary32-style crux that measured 0/5 on `legacy-accum-port`:
coefficients written as exact decimal text, where `float(text)` before scaling is one word wrong
on 31 held-out coefficients and agrees on every visible one — **2/2 again**, and the analysis
records that both agents "used `decimal.Decimal` with `ROUND_HALF_EVEN`, explicitly matching the
contract's rule" and "rejected the naive largest-factor-first heuristic". Solve time rose 7 min →
21/31 min of a 60 min budget; the failure rate never moved.

**Fourth draw, and it refutes the obvious repair.** The hypothesis after three draws was that a
contract-driven task can still be hard when its core is "short to state, hard to implement". So I
added exactly that: each stage reports the **fewest adders** in a shift-add realisation of its
coefficients — a bounded reachability search no library computes, where the natural shortcut
(signed-digit recoding) overcharges 101 graded coefficients and is exact on every visible one
(45 factors into two adders where recoding wants three; 127 is one subtraction from 128 where
recoding wants six). **2/2 again**, 26 and 46 minutes. The analysis: both agents "built a two-adder
reachability table on odd-parts <= 4096" and the convergence "suggests these techniques are
well-established enough in training data that the model can reliably derive them from the contract
specification alone."

**Resolved on the fifth draw: the worked example was the oracle.** The contract quoted the
example case's full report and ledger, and the trial analysis showed both agents diffing every
intermediate against it — coefficient words, accumulators, register state, chosen shift, latency —
before submitting. So the starved branches were never facing a first draft; they faced an
implementation already debugged on every other axis. Shrinking the example to a sixteen-sample
format sheet (both row shapes, dash placeholders, digests, canonical JSON, and nothing else)
flipped the gate immediately: **0/2 solved, 2 valid failures, difficulty_crux PASS on both**, and
both agents failed on the *same* subsystem — the two-adder reachable set — in different ways. One
had the correct 722-value set and reasoned itself down to 224 at step 22, over-charging 498
odd-parts and cascading through the ledger digest into every held-out chain.

**The corrected generalisation:** with an oracle to debug against, this reference pair implements
anything the contract states. Without one, a bespoke search it cannot verify gets committed to
wrong. Both halves matter — the search has to be genuinely searchable (a stated rule stays easy
either way), and the shipped example must pin file conventions without confirming a single
computed value. Fairness (QC B1/B4) forces every graded rule into the contract, so a
contract-driven task can only be hard where the difficulty survives being stated — and four levers failed that test while the example still
carried a full answer: starved one-line rules, a combinatorial optimisation with a stated
objective and a wrong heuristic, an exact-decimal conversion whose float route is silently wrong,
and a bespoke bounded search with no library implementation. Depth of the stated computation is
not the axis; being stated at all is. Do not spend a second ratchet on a
contract-driven concept that draws 2/2; either it has that property from the start or it does not.

**How to apply:** before building, ask of each starved branch "would a competent implementation
plausibly get this wrong on the first try, with no way to check?" If the honest answer is no,
starving it buys nothing. Reserve the sample-starving trick for branches that carry real
implementation risk — canonical forms, search, exact rational/lattice work — and put the
difficulty budget into a subsystem that requires derivation (a small combinatorial optimisation
with a plausible-but-wrong heuristic, an inferred policy) rather than into more disclosed rules.
See [[dynamo-spec-mold-caps-at-80pct-solve]] and
[[dynamo-recovered-constants-are-still-transcription]] for the same conclusion from two other
shapes.
