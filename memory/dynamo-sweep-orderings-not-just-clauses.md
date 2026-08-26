---
name: dynamo-sweep-orderings-not-just-clauses
description: "QC C3-exec hit twice on the same task — first on admission clauses, then on sort keys; sweep every decision category, and expect witnesses that only work by luck."
metadata:
  type: feedback
---

On `dynamo-56ae913`, `qc_exec` blocked twice in a row with C3-exec, on two different
categories of decision:

1. **admission conditions** — which rows/marks/chits are refused (18 holes).
2. **ordering rules** — sort keys, tie-breaks, traversal order (5 holes).

Fixing category 1 and pushing cost a full ~2h pipeline cycle before category 2 surfaced.
The sweep technique transfers exactly; only the list of things to sweep changed. Before
pushing, enumerate **every** decision the contract documents and weaken each one:
admission clauses, sort keys, tie-breaks, boundary comparisons (`<` vs `<=`), traversal
order, and the point in the run at which a counter is read.

Three failure shapes, each needing a different fix:

- **No witness** → plant a fixture. For a tie-break this means engineering an actual tie;
  the cheapest source is a value that is zero *by construction* (a system with nothing
  rated has total 0 whatever the weights), not a value solved for. Solving item weights to
  force a tie fails: gaps run to thousands and the spec caps weights at "small".
- **Provably unreachable** → delete the distinction and fix the prose. A leading `/`
  always yields an empty path segment; a digest binding model *and* judge can never match
  two slots; reading rows in any order cannot change a grouped-then-maxed result.
- **Witnessed only by luck** → make it deterministic. A model-id tie-break is invisible
  when the tied pair happens to sit in alphabetical order, because a *stable* sort
  reproduces it for free — seat them in the opposite order on purpose. Likewise a
  supersession pair must share a stamp AND an attempt before `record_id` decides anything.

**How to apply:** run the mutant for every rule against *every* graded seed, not just the
sweep pair — a rule witnessed on one seed still leaves the sweep pair green and survives.
See [[dynamo-c3-needs-a-clause-sweep]] for the first half of this and
[[dynamo-witness-must-be-the-selected-value]] for why a planted witness often changes no
output byte.
