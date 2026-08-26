---
name: dynamo-plant-the-deep-knot-do-not-search-for-it
description: "Emergent structure (points ties, deep tie-break recursion) never appears by seed search; construct the entrants that produce it and protect them from every other plant."
metadata:
  node_type: memory
  type: feedback
---

On `dynamo-c31fb12` (`dynamo/trumpline-reckon`, Games / Board and card games) the
crux needed held-out instances whose tie-break recursion ran two levels deep.
Seed-searching for it measured **0 hits in 400 seeds** — with 26 entrants and
stakes spread over 2–8, points collide in pairs and never in threes, so every
knot separated at depth 1 and the three "no recursion" readings **survived every
circuit in the corpus**.

The fix was to **construct** it: five reserved entrants appended to the roster
but excluded from the table partition, playing a designed six-hand mini
tournament plus one outside hand each, chosen so all four share a points total,
restrict two-and-two inside the knot, one pair separates on the second
restriction and the other cannot be separated at all and locks. That took the
three readings from "survives everywhere" to caught on 19 of 19 protected
instances in one change.

**The expensive half is protecting the plant.** Four separate generator passes
independently corrupted it, each costing a debugging round:

1. the contending post copied `records[0]` *after* the plants were appended, so
   it duplicated a planted hand at a new table and moved one entrant's points;
2. the `repeat_rid` fault picked from `claimed`, which included planted ids —
   and because fault lines are inserted at random positions, the *original*
   sometimes became the refused one;
3. the "same instant, different players" plant sampled from the whole roster
   rather than the laned pool, dropping a reserved entrant into an ordinary hand;
4. holding records back as `post` operations still sliced them out of the sheet
   list when `pending_present` was false, so they vanished entirely.

The rule: keep a `protected` set of planted record ids, derive a `plain` list of
everything else, and make **every** later pass — bases for twins, edge records,
fault lines, the contending pair, the revise/strike pool, the stale index — draw
from `plain` only. Then assert the plant survived by surveying the reckoned
output, not by reading the generator.

See [[dynamo-starve-a-ranking-rule-with-graph-shape]] and
[[dynamo-blindness-table-before-pushing]] — the blindness table is what makes a
broken plant visible, because a corrupted plant shows up as a reading that
survives everywhere rather than as an error.
