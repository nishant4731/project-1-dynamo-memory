---
name: dynamo-unobservable-rule-is-not-a-starve
description: "A starve only holds while the shipped instance cannot discriminate the rival readings; reporting one extra identifier can expose a whole subsystem you meant to hide."
metadata:
  node_type: memory
  type: feedback
---

Measured on `dynamo-6459436` (`dynamo/gantry-cutover`, 2026-08-22) while building the
blindness table, before the first push.

The scheduler was designed as a starve: the shipped pipeline's runner roster has slots
to spare, so no rebuild ever queues and the priority rule never decides anything. The
first design gave every runner a **lane id** and reported it as a column of
`CUTOVER.tsv` and a key of `plan.ndjson`. Measured result: `lane_capacity_ignored`,
`priority_by_tid_only`, `priority_by_cost_only` and `highest_free_lane` were all
**DIFFERENT on the shipped pipeline** — because with no contention the pick *order*
still decides which lane id each job gets. The starve was worth nothing.

Replacing lane ids with a **per-suite slot count** (`RUNNERS.tsv: suite, slots`) and
reporting only `start` and `finish` made five misreadings blind in one edit:
ignoring the slot budget (13 of 22 protected pipelines wrong), reading it as one job
too many (13), reading it as a budget over all suites (14), and two priority
readings (11 and 16). Same rules, same corpus — only the observable surface changed.

**The rule:** a starve holds only while the shipped instance cannot discriminate the
rival readings. Before trusting one, ask what the graded output *reports*, not what
the rule *does*: an identifier that any implementation must allocate in pick order
leaks the pick order. Run the blindness table
([[dynamo-blindness-table-before-pushing]]) and treat every `DIFFERENT on shipped` row
as a design finding, not a footnote.

Corollary from the same session: the reverse mistake is an **inert** rule. Writing the
cached `crit` column as a literal `"0"` made the `crit[tid] = 0` assignment dead code,
so its mutation survived the sweep. Related: [[dynamo-inert-rules-are-c3-holes]].
