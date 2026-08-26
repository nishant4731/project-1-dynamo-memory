---
name: dynamo-never-hand-the-agent-the-map
description: "Measured across four heads of dynamo-63f2f80: agents get right every blind clause the prompt or a scope section enumerates, and wrong the one it omits. Disclose that the sample is narrow; never list which rules it skips."
metadata:
  type: feedback
---

Four evaluated heads of one task, same engine throughout:

| head | prompt / scope disclosure | pass@2 | pass@5 |
|---|---|---|---|
| 016e716 | pitfall tour in prompt; §12 listed 7 unexercised clauses — **root-opaque not among them** | 0/2, 2 valid fails | — (AVA blocked) |
| 9a8c57a | root-opaque stated in §4.1 **and added to §12's list** | 1/2 | **5/5 solved** |
| 37f656b | + a chunker whose 3 branches §12 announced as never firing | **2/2 solved** | — |
| edd6d99 | prompt reduced to a neutral brief; §12 no longer enumerates | 1/2, 1 valid fail | in flight |

**The correlation is one-to-one: every clause the disclosure named got implemented
correctly; the one it omitted killed both trials.** Head 3 is the sharpest case —
a rolling-window chunker with a minimum, a maximum and a per-cut window reset,
none of which the shipped stack exercises, and both agents got all three right
because §12 said in as many words that those three never fire there.

**Two mistakes to avoid, both mine.**
1. A prompt section explaining *where the difficulty sits* is a study guide. Dynamo
   eval graded mine "borderline PASS — flirts with trap-hinting" and I read a pass
   as endorsement. Take that wording as a finding.
2. A scope section is required for fairness (the sample really is narrow, and
   saying so pre-empts a "misleading data" rejection) — but it must say *that* the
   stack is narrow, not *which* rules it skips. The itemised version is the test
   plan for the held-out probes.

**Also measured:** a blind sample buys nothing when the contract states the
algorithm imperatively. The chunker was specified step by step ("rotate left by
one; when p - start >= 48, exclusive-or …"), so it was transcription regardless of
what the fixture exercised. Blindness bites only where the correct behaviour needs
derivation the agent could plausibly get wrong —
see [[dynamo-blind-sample-branch]], and prove it the way
[[dynamo-blind-branch-shipped-fixture-proof]] describes.

**Free extra:** give paired counters *different* values across probe stacks. A
trial lost to a transposed `(forced, suppressed)` return tuple — invisible on the
probe where both equalled 1, caught by the probe where they were 2 and 1.
Related: [[dynamo-ambiguity-fix-needs-a-paired-algorithmic-trap]].
