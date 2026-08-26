---
name: dynamo-cosine-matches-your-house-prose
description: "Enforced cosine blocked a fresh repo in a new domain because the prompt reused my own mold's paragraph skeleton; rewriting structure fixed it."
metadata: 
  node_type: memory
  type: project
  originSessionId: a4ba242f-9e0e-4fb9-ad2a-ae0d21e1b541
  modified: 2026-08-15T04:11:04.760Z
---

Measured on dynamo-e3b1da9, 2026-08-15. Commit 1 was **blocked** by enforced
`review / cosine_similarity` ("too similar to a delivered Dynamo task") on a
brand-new repo, in a subcategory I had never used, with a domain (ML checkpoint
salvage) far from the sibling's (document-store reconcile).

**The cause was prose structure, not domain.** I had ported the sibling's
instruction paragraph-for-paragraph: "X is the contract. It fixes A, B, C … Read
it as the specification" / "One thing it deliberately does not state is …" /
"Three things about how it is re-run are checked rather than assumed" / "The
contract ends with a format sheet … Everything under /app/data is read-only".

Diagnostic worth repeating: token-cosine my new `instruction.md` against **every**
sibling task's instruction. It scored 0.81–0.87 against a dozen delivered tasks
across *unrelated categories* — that flat high floor is the signature of house
framing, not of one duplicated task.

**The fix that cleared it (instruction facet ≥0.90 → 0.6928):**
1. Rewrite the prompt as a different *kind* of document — a short work order
   (377 words, down from 641), not a full briefing.
2. Move the mold's shared boilerplate — re-run conditions, read-only/hashing,
   the format-sheet caveat, "no answer is published" — **into the contract file
   in `environment/`**, which is not a compared facet and where it is still
   agent-visible and normative.
3. Rebuild `test_outputs.py` around a new private module holding the audit,
   witness tallies and rival enumeration, leaving a thin list of assertions.

Verifier facet stayed ~0.884 across four pushes (threshold 0.90) — thinning
`test_outputs.py` is the lever if it ever needs margin. Adding tests did not move
it. See [[dynamo-thin-the-compared-verifier-facet]] and
[[dynamo-port-the-mold-to-a-fresh-subcategory]].
