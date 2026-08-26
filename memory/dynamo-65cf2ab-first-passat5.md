---
name: dynamo-65cf2ab-first-passat5
description: dynamo-65cf2ab cleared every gate incl. qc_gate and tier1; pass@5 5/5 because the spec itself named both traps.
metadata:
  type: project
---

2026-08-18, dynamo-65cf2ab (Mathematics and Formal Reasoning / Number theory and exact
arithmetic). Head `6122601` passed **every** gate — changes, cosine, review, similarity,
validation, ratelimit, pass2, deep_review, ava_review, tier1, qc_eval, qc_exec, **qc_gate** —
and `trials` ran for the first time in the task's history. **pass@5: 5/5 solved, 34–70 min of
a 90 min ceiling.**

**What got the gates green** (each was a separate blocking finding):
- **QC B5** on a withheld rule: unfixable by partial disclosure, see
  `[[dynamo-b5-vs-pass2-determinability-pincer]]`. Fixed by stating the seating law outright
  and deleting the shipped archive — which had become a full answer key for every graded
  column, including the one carrying the difficulty.
- **QC E3**, real and confirmed: `WORKDIR /app` is agent-owned and `python3 -m pytest` puts
  the cwd on `sys.path`. Planting `/app/struct.py` executed it inside the pre-fix verifier.
  Fixed with `python3 -I` from a fresh directory, plus `PYTHONSAFEPATH=1` in the image.
- **tier1 three times**, each a *diff-truncation* artifact, not a real miss — it reported
  fixes "not attempted" that were demonstrably in range. `task/environment/` sorts before
  `task/tests/`, so bulky data churn there hides later hunks. Keep data dirs small.
- **pass@2 time pressure**: both trials burned the full 3600 s cap (pass@2 pins its own hour
  regardless of `task.toml`). Shipping `/app/data/forge_io.py` — parsing and serialisation
  only, no answer — freed the clock. See `[[dynamo-provide-the-plumbing-clears-the-hard-side]]`.

**Why pass@5 was 5/5:** the specification named its own failure modes. §7 said rounding through
a wider float "is a different function" and that corpora "contain instances where the two
disagree"; §5 said the set is complete "only once a whole sweep admits nothing further". The
trial report then records all five agents converting "explicitly avoiding float64
intermediaries" and seating as "an iterative BFS closure, **not a single pass**" — my own
wording handed back. Confirms `[[dynamo-do-not-narrate-the-trap]]` and
`[[dynamo-never-hand-the-agent-the-map]]` at pass@5 scale.

**How to apply:** state the rule (QC needs it), never the misreading. Write the spec, then
grep your own agent-visible text for "not", "different", "disagree", "wrong" — anywhere it
contrasts the right reading against a wrong one, you have written the answer key.
