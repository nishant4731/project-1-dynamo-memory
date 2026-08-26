---
name: dynamo-stated-optimum-gets-solved
description: A stated global optimum whose greedy reading is wrong is NOT reliably hard — 7/7 agents solved a 64-subset one; only expensive-to-reach optima discriminate.
metadata: 
  node_type: memory
  type: project
  originSessionId: 6c48333f-56d9-4736-82fd-cc4088e05c61
  modified: 2026-08-13T04:09:21.406Z
---

On `dynamo-e88ef21` (`dynamo/cairn-pack`, 2026-08-13) the designed crux was the 19c8cbd recipe
ported to serialization: the contract asks for the **shortest legal container**, nine columns share
one varint-coded dictionary so the natural per-column choice is a greedy approximation, and the
shipped fixture was arranged so greedy and optimal coincide with no expected output anywhere. A
greedy packer built from the reference measured reward 0 locally while passing every shipped-pack
assertion — the trap worked exactly as designed.

**All seven evaluated trials solved it anyway** (two pass@2 draws + five pass@5): identical
`cairn_bytes` 1188, `column_tags`, `dict_entries` 32, and the pass@2 advisory says both trials
solved the joint 64-subset encoding outright.

**Why:** with only 64 subsets, naming the objective in the contract names the algorithm — you see
it is joint, you enumerate. 19c8cbd's 0/5 came from an optimum that was *expensive to reach*
(pruning argument over a large space), not from agents failing to notice jointness.

**How to apply:** before spending a task on "stated optimum, greedy-reachable wrong answer", ask
whether brute force over the whole choice space is feasible once noticed. If it is, the trap costs
one insight and buys no valid fails. Pair it with something else, or make the search itself the
wall. See [[dynamo-spec-mold-caps-at-80pct-solve]] and [[dynamo-ambiguity-is-the-only-valid-fail]].
