---
name: dynamo-search-the-fixture-for-its-own-edge-witness
description: "A measure-zero edge witness (a container landing exactly on a byte budget) should be found by a deterministic retry loop inside the builder, not pinned to a lucky seed that every later edit invalidates."
metadata:
  node_type: memory
  type: feedback
---

QC C3 wants an inclusive bound witnessed from both sides, and for a byte budget
that means a packed container whose total is **exactly** the budget. The odds are
about one in the mean record size per container — roughly 1 in 230 — so it is
found by seed search, not by construction.

On `dynamo-c31fb12` I pinned four slots to seeds that had it. **Every subsequent
generator edit reshuffled the packing and lost it**, three times: widening the
note distribution, varying the twin settle times, and fixing an unrelated roster
leak each silently dropped the witness, and the mutation sweep reported the
inclusive/exclusive probe as thin or surviving. Each round cost a full
re-search plus a re-freeze.

The fix is a `brim_search` flag on the shape and a loop in `build_store`:

```python
if spec.get("brim_search"):
    for step in range(600):
        plan = build_plan(seed + step, spec)
        if _packs_to_the_bound(plan):
            return plan
```

`_packs_to_the_bound` writes the plan to a temp directory, runs the reference,
and looks for a container whose size equals the budget. It is deterministic, so
the pins stay stable, it costs ~40 ms per slot, and it **self-heals** across every
later change to the generator. If it ever fails to find one, the mutation-sweep
test goes red loudly rather than the witness disappearing quietly.

Generalises to any measure-zero witness the corpus needs: search for it at build
time inside the builder, keyed off the reference's own output, instead of
freezing a seed that only happened to work.
