---
name: dynamo-ava-real-finding-hides-in-advisories
description: "AVA's blocking list can be self-agreeing paraphrase while the real verifier hole sits under \"non-blocking\" advisory."
metadata: 
  node_type: memory
  type: project
  originSessionId: 43067629-d486-4b92-8f24-cce768c782fb
  modified: 2026-08-12T01:52:43.711Z
---

On `dynamo-e488890` AVA blocked with three `verifier_coverage` items whose own evidence restated
the charter back to itself ("expected the charter's tie-break, but the verifier would instead
pick the lower seg_id first" — the same thing). The genuine defect was filed as a **non-blocking
advisory**: the runner enumerated the graded input directory with
`rglob("*") if path.is_file()`, so a submission that left an empty directory, symlink or fifo
behind was accepted even though the contract said nothing new may be created there.

**Why:** AVA's attack enumeration is stochastic and its blocking classification is noisy, but it
does surface real boundary gaps — just not always in the blocking section.

**How to apply:** read the advisory list first when AVA blocks. Fix the real hole (walk every
`rglob` entry, assert each is a plain file or dir and not a link, and compare the full entry list
— directories included — as its own graded bundle member), and answer the noisy blocking items by
*adding atomic witnesses* for exactly what they probed rather than arguing. That combination
flipped AVA to PASS in one push. Pairs with [[dynamo-mutation-sweep-finds-witness-holes]].
