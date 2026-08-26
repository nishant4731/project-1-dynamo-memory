---
name: dynamo-data-querying-and-databases-sql-querying-playbook
description: "PLAYBOOK Data Querying and Databases / SQL querying — ALL-GREEN settle-a-season-from-a-SQLite-ledger mold; pass@5 1 solved / 4 good valid, avg 0.200."
metadata:
  type: project
---

**Category:** Data Querying and Databases · **Subcategory:** SQL querying
**Repo:** `handshake-project-dynamo/dynamo-0a86356-data-querying-and-databases` ·
PR #1 · heads `b75b6d4` → `75e86fa` → **`ebeebbd` ALL-GREEN** (2026-08-23).

## The mold

**Analyzer-tool over a read-only SQLite ledger, complete contract, difficulty
entirely in the shape of the shipped instance.** `dynamo/headgate-settle`: the
agent writes `/app/headgate_settle.py <season_dir>`, which closes an irrigation
district's water season out of a 13-table ledger and writes `carriage.tsv`,
`statements.tsv`, `headgate.tsv`, `disputes.tsv` and `settle_report.json` back
into that directory, leaving the ledger untouched. `DITCH_BYLAWS.md` states all
16 sections — which is why qc_eval/qc_exec/**qc_gate passed clean on every
push** and B5 never came up.

## Measured

| head | pass@2 | pass@5 |
|---|---|---|
| `b75b6d4` | 0 solved · 2 valid · 0 timeouts · "Rerun: NO" | **4 solved · 1 good valid · avg 0.800 — BLOCKED** |
| `75e86fa` | 1 solved · 0 valid · **1 in-progress timeout** · "Rerun: YES" | never ran |
| `ebeebbd` | **0 solved · 2 valid · 0 timeouts** · "Rerun: NO" | **1 solved · 4 good valid · 0 timeouts · avg 0.200 — PASS** |

Cosine passed 3/3: instruction **0.707 → 0.706**, verifier **0.824 → 0.814**,
fingerprint **0.805 → 0.792**, threshold 0.9. Dynamo eval 31/31 on push 1.
Duplicate UNIQUE (closest TB2 lexical 0.089). AVA PASS (one advisory),
deep_review PASS with **zero** blocking issues, tier1 PASS.

## What drew the valid fails — the single most reusable fact

**3 of the 4 pass@5 failures were the carriage factor**, quoted from the
analysis: *"a network traversal for carriage factors that is correct on
Bellcourt's branching-only (tree-shaped) topology but wrong on held districts
with rejoining laterals … DFS-with-backtracking, backward column-propagation on
all flowpath edges, or an undisclosed walk variant. Bellcourt masks the defect
entirely."* The rule — `factor(R,S)` is the **sum over every route** of the
product of the per-link losses — is stated in full in §4. It converts anybody
because the *natural code* (a DFS that marks nodes seen) coincides with the
correct answer on a tree and only on a tree.

The 4th failure was `keystone`, and it is **a genuine ambiguity I left in**: §11
says keystone leaves out reaches the member drew from and is `-` "when no reach
is left to choose from", but never says the pool is restricted to reaches with
**non-zero** reach weight. The reference restricts it. The trial's sub-analysis
marks `decisive_rule_disclosed = FAIL` / `spec_consistency = FAIL` and calls the
agent's literal reading defensible; the gating `task_specification` column was
PASS on all five, so it did not block. One sentence would fix it — held back
only because the head was already all-green and a redraw is a coin flip.

## The ratchet that broke the 4/5 ceiling

Head 1 was a complete, hard spec — 8 ordered rejection causes, mixed
inclusive/exclusive interval conventions, exact rationals, half-even cents, a
minimum vertex cut, scoped credits — and still solved **4/5**. What flipped it
to 1/5 was **three subsystems that re-key the whole computation, each degenerate
on the shipped season**:

1. **Dated outages.** An `outage` takes a reach out between two dates, so the
   network *and every carriage factor* become functions of the day, and a reach
   can be cut off because something upstream was out. Shipped season: no
   outages, so computing the network once is right there.
2. **A daily headgate capacity.** Each order costs `volume ÷ its day's factor
   from the headgate`, rounded up; a day's orders fill in water-right seniority
   order until capacity runs out, and an order that does not fit is **passed
   over, not the end of the walk**. Shipped season: never short.
3. **Dated works attribution.** A charge is carried only by water taken on or
   after `incurred_on`, re-keying `carriage.tsv` from (member, reach) to
   (member, charge). Shipped season: every repair predates the first order.

Blindness table went 19/29 → **33/40** misreadings byte-identical on the shipped
season. `works_dating_ignored` was wrong on **21 of 21** held-out seasons;
`outages_ignored` 15/21; `capacity_never_bites` 12/21; `stop-at-first-refusal`
9/21.

## Levers measured NOT to work here

- **A complete, intricate spec on its own.** Head 1's whole rule set solved 4/5.
  Confirms [[dynamo-stated-algorithms-are-transcription-too]] and
  [[dynamo-widening-implementation-surface-measures-zero]].
- **Counters as difficulty.** 45 counters drew zero attributed failures across
  10 trials; cutting the 7 bare `len(table)` ones cost nothing.
- **Credits (scope, expiry, issue order)** — 4 stated rules, never once named in
  a fail analysis.

## Hurdles, per gate, in the order they blocked

1. **pass@5 4/5 solved (avg 0.800).** Fixed by the three subsystems above, not
   by volume. Trials had 45 min of spare budget, so adding work was safe.
2. **pass@2 in-progress timeout.** The failing trial spent 45 min in ONE API
   call, self-diagnosed both crux bugs at step 11, and lost the rest to a JSON
   parse error. Fixed by cutting 7 pure row-count counters and adding one line
   asking for a runnable tool to be left behind whatever state the run reaches —
   [[dynamo-inprogress-timeouts-need-an-early-write-nudge]] applied verbatim.
   **No rule, bound or crux was touched**, exactly as the difficulty suggestion
   advised.
3. Cosine, static, eval, duplicate, validation, AVA, deep_review, tier1, qc_*:
   **never blocked, on any push.**

## Operational findings specific to a database task

- **Rebuilding SQLite fixtures per mutation probe dominates the verifier.** The
  first in-container oracle took **634 s**; caching one built ledger per slot and
  `shutil.copyfile`-ing it per probe, plus dropping the never-modified ledger
  digest from the probe comparison, took it to **21 s**. Do this first.
- **Never grade a `.sqlite3` by its bytes.** Compare it by its rows (a canonical
  dump) so page layout cannot decide a verdict, and exclude `ledger.sqlite3*`
  from the tree digest.
- **A prefix cap is order-independent.** "Spend the allotment in `(taken_on,
  tie-break)` order" makes the tie-break provably inert — total within is
  `min(total, cap)` whatever the order. Ordering only becomes load-bearing once
  the *rate* moves mid-season; splitting rate cards mid-season took the
  don't-sort-at-all misreading from wrong on 2 of 19 seasons to 16 of 21.
- **An exact-equality bound needs integer units.** `head <= spare` was
  unwitnessable while heads were fractions (measure zero). Rounding the head
  requirement up to whole units, and then setting one season's `day_capacity` to
  an exact prefix sum of the busiest day's queue, made the inclusive bound bite
  on 10 of 21.
- **Equal-weight ties need a reason to exist.** Keystone ties never arise when
  every link loses something; giving lined reaches a carry of `12/12` created
  them and closed a C3 hole.
- **Index witness cohorts from the base member count, not the roster length.**
  Closed-turnout and no-allotment cohorts indexed from `len(members)` landed on
  the two synthetic half-cent members and silently destroyed their witnesses.
- **pass@2 pins `override_timeout_sec=3600` whatever `task.toml` says**;
  pass@5 honours the file. Keep `[agent].timeout_sec = 5400` so pass@5 has room
  to produce *finished and wrong* rather than uncounted timeouts, and calibrate
  the deliverable to fit 3600.

## Gate tensions

The usual B1/B5-versus-pass@2 pincer never fired, because nothing is withheld:
every rule is stated and the difficulty lives in the degeneracy of the shipped
instance. The cost of that choice showed up exactly once — the `keystone`
candidate pool, where "stated completely" quietly wasn't.
