---
name: dynamo-b5-vs-pass2-determinability-pincer
description: Four measured heads show any disclosure sufficient for QC B5 is also sufficient for the agent; recovery-of-a-rule difficulty cannot survive B5.
metadata:
  type: feedback
---

On dynamo-65cf2ab I measured the disclosure axis end to end, holding everything else fixed.
The graded rule was a seating law: which instances get a ledger line, as a least fixed point.

| head | disclosure | pass@2 | QC |
|---|---|---|---|
| 0c73281 | law stated in full | 2 solved, 0 valid-fail | — |
| 1305698 | law withheld, 3 archive corpora | 0/2, **1 valid-fail** | **B5 Major** |
| 60dd373 | law withheld, 3 corpora, shrunk | 0/2, **2 valid-fails** | **B5 Major** |
| f06a7a2 | form stated, only `R(N,q)` left to 6 corpora | 2 solved, 0 valid-fail | (B5 addressed) |

**The pincer:** QC B5 ("Underdetermined / Hidden-Knowledge Mapping") blocks any graded output
that turns on a rule the agent cannot determine from what it can see. Its two remedies are
"document the rule" or "give enough to determine the mapping". Documenting it is head 1; the
second remedy, done properly, is head 4 — I declared the law's shape (anchors, closure, and that
the relation is a predicate of exactly two numbers and nothing else) and proved 125 candidate
laws left exactly one survivor. Both ends solve 2/2.

**Why:** once the signature is declared, the agent does not search a space — it reads the
relation pointwise off the archive (which pairs must have been admitted, which must not) and
generalises. Declaring the signature *is* handing over the answer, one step removed. And nothing
weaker satisfies B5, because B5 is exactly the complaint that the agent cannot derive it.

**How to apply:** do not spend heads tuning *how much* of a rule to disclose — the two endpoints
are both solved and everything between inherits one or the other. Recovery-of-a-rule difficulty
is not viable under B5 on a fully-specified deliverable. Move difficulty into a **stated**
computation that is hard to implement correctly and whose errors are invisible without an oracle
(`[[dynamo-starve-execution-not-rules]]`), e.g. one where the naive algorithm is infeasible at
the shipped scale and the correct one is a non-obvious descent. Beware the failure mode there:
agents who cannot find the algorithm time out, and timeouts anchor nothing
(`[[dynamo-timeouts-anchor-nothing]]`, `[[dynamo-in-progress-timeouts-need-plumbing]]`).

Related: `[[dynamo-stated-algorithms-are-transcription-too]]`,
`[[dynamo-determined-exact-tasks-are-transcription]]`, `[[dynamo-tier1-vs-cosine-pincer]]`.
