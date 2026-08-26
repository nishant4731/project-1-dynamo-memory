---
name: dynamo-support-definitions-admit-padding
description: "QC B1/B5 on dynamo-568d798: 'every element's precondition is met by an earlier element' lets any always-satisfiable element be parked at the front, so the stated set is strictly larger than the one the reference computes."
metadata:
  type: feedback
---

Writing a derivation/reachability set as *"a sequence in which every element's
precondition is met by an earlier element"* is the natural phrasing and it is
**wrong** whenever some element's precondition is satisfiable outright.

Measured on `dynamo-568d798` (`dynamo/lanternfall-restage`), qc_gate B1 **and**
B5, both Major. Section 8 defined a *run* to a scene as a sequence of open
passages in which every passage's `head` is "an act's opening or the `tail` of an
earlier passage in the sequence". A passage whose head **is** an act's opening
meets that at **any** position — so `[p_from_act_B, p1(s-001→s-002)]` is a
literally valid run reaching `s-002`, dragging act B's scenes into the graded
`route` count. The reference computed the least fixed point, which unions only
what the last passage rests on. The canon therefore described a **strictly
larger** answer than the verifier graded, and nothing agent-visible chose
between them.

**The fix is a minimality clause, not more prose.** State it as numbered parts
and add: *every element other than the last is one a later element needs* —
spelled out in the domain's own terms (here: its `tail` is a later passage's
`head`, or its `drop` is one of a later passage's `keys`). That is exactly
equivalent to the least fixed point: rule 4 forces each element to be
transitively needed by the last one, and any derivation DAG linearises into such
a sequence.

**Then check it, don't assert it.** `dev/runcheck.py` enumerated **every
subset** of the open passages of two small hand-built instances — one braided
with a key detour, a back-walk and a locked wing, one where two sources share a
token pool — tested each subset against the four numbered rules, and compared
the resulting scene-union to the reference's column. 0 mismatches. Cheap, and it
converts "the prose probably matches the code" into a fact. Any definition you
state as an enumeration deserves this.

See [[dynamo-games-puzzles-interactive-text-games-playbook]] and
[[dynamo-b5-vs-pass2-determinability-pincer]].
