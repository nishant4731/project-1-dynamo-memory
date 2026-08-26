---
name: dynamo-mutation-sweep-green-on-an-inert-rule
description: "A rule can be inert while its mutation sweep is green — mutants that perturb it fire, deleting it outright changes nothing. Always test the delete-the-rule direction."
metadata:
  type: feedback
---

Measured 2026-08-23 on `dynamo-a8b2707` (`dynamo/sentinel-trace`, head `1791e13`).

I added a rule that a bay's cohort cap drops by one on any day the bay is over its
crowding limit, floored at zero — five lines meant to re-key every conferred grade. The
sweep was green: `crowding_bound` (`>` → `>=`), `crowding_floor` (dropping the clamp),
`crowding_day`, `crowding_scope` and `crowding_counter` were all killed. I shipped it and
claimed the static-cap misreading was blind.

**It was not blind, it was inert.** Patching the reference to delete the reduction
entirely — `if over_limit: cap -= 1` → nothing — changed no graded byte on any of the six
protected packs. Every crowded landing happened to sit where the cap was not binding: the
anchor bay's cap was at or above `grade - 1`, and the relay bay's cap was already 0, so
`min(grade-1, cap)` and `min(grade-1, cap-1)` agreed. The mutants that *did* fire were the
ones reducing **more** than the rule does (`>=` reduces at the at-limit landing; removing
the floor sends a zero cap to -1). Those directions were witnessed; the rule's own
direction never was.

**The asymmetry to remember:** a single-clause mutation sweep perturbs a rule. It does not
ask whether the rule *does anything*. For any rule of the form "adjust X under condition
C", a witness must satisfy **both** C holds **and** the adjusted X changes the output —
for a `min(a, cap)` cap that means `0 < cap <= a`, not merely `cap` present and C true.

**How to apply.** For every rule you add, run one extra probe: delete the rule from the
reference and require a graded byte to move. Cheap, and it is the only check that
distinguishes decisive from inert. Then encode it — the generator here now asserts per
pack that crowding changes at least one conferred grade, so the geometry cannot drift back
to inert when the ward layout is retuned. Related: [[dynamo-inert-rules-are-c3-holes]]
(which says a stated rule whose value never reaches a graded byte survives mutation — this
is the sharper case where the sweep is *green* and the rule is still inert), and
[[dynamo-witness-must-be-the-selected-value]].
