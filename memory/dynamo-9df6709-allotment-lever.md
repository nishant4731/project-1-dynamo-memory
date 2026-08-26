---
name: dynamo-9df6709-allotment-lever
description: On dynamo-9df6709 a contended-evidence allotment cleared pass@2 and every review gate but measured 4/5 on pass@5 — because section 6 named the naive approach it was trying to punish.
metadata: 
  node_type: memory
  type: project
  originSessionId: e19fae0e-682c-4934-9e95-c982d525ac98
  modified: 2026-08-13T13:50:01.032Z
---

Replaced the withheld naming clause (see [[dynamo-withheld-clause-gets-induced]]) with a
contended-evidence rule: one file can answer several pending rows, and the mend must take the
allotment filing the most rows, ties to the earlier row then the smaller offer. Greedy
first-fit is **byte-identical to the reference on the shipped vault** and wrong on all 12
held-out ones (11 of 30 checks fail).

**Measured, `2a3eec0`:** cosine, review, similarity, validation, ratelimit, pass2,
deep_review, ava_review, tier1, qc_eval, qc_exec, qc_gate all green — the first head here to
clear pass@2 *and* the whole review stack. pass@2 was 1 solved / 1 valid fail with
`difficulty_crux` PASS. **pass@5 was 4/5 solved, 1 valid fail, avg@5 0.800 — blocked, not hard
enough** (needs ≥3 fails).

**The allotment caused neither failure.** The pass@5 failure was a two-line bug in the
out-of-order tracker (`previous_max = max(...)` written before the comparison read it). The
pass@2 failure was a *correct* allotment implemented as a bitmask DFS over `2^n_files × n_rows`
that got SIGKILLed on 8 of 12 vaults; the solvers found that contention is local and the
problem decomposes into independent groups. Across 7 trials the rule produced one failure, and
that one was efficiency, not misreading.

**Why: I narrated the trap.** Section 6 had a paragraph saying rows do not take the first
offer that fits, that a seq-order mender can spend on an early row the chunk a later row
needed, and that the vault does not accept that. That is the naive approach named with its
consequence — the exact edit [[dynamo-do-not-narrate-the-trap]] measured as 3 solved/2 valid →
5 solved/0. Section 13 compounded it with a checklist of eight mistakes, six restating rules
already normative elsewhere ([[dynamo-never-hand-the-agent-the-map]]).

**How to apply:** building the trap and describing it are separate decisions, and the second
one silently undoes the first. After writing any new rule, grep the spec for sentences that
name the wrong reading or explain why it is wrong, and delete them — the rule stays exactly as
precise, and nothing becomes ambiguous. Keep only hazards no rule can protect against
(destructive single run, untrustworthy timestamps) and state that the rules are narrow in
places *without* saying which.
