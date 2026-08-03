# dynamo/asof-fx-enrichment

Bitemporal, graph-based, point-in-time dataset preparation. The agent must
USD-normalize a transaction table from an append-only FX log of **directed
conversion edges** (many currencies are only quoted against other currencies,
and the rates are not arbitrage-free), reconstructing each rate as it was
authoritative **on the transaction's business date, as known at a fixed
knowledge cutoff**, and choosing the **least-cost conversion path** to USD.

## Overview

Inputs (`task/environment/data`, copied to `/app/data`):

- `transactions.csv` — `txn_id, txn_date, currency, amount`.
- `fx_rates.csv` — bitemporal edge log: `currency, rate_effective_date,
  recorded_at, rate, status` (`active` / `retracted`), `quote_currency` (`USD`
  or another currency), `tier` (conversion cost), `max_age_days` (freshness
  horizon), `daily_capacity` (max transactions per edge per day; two clearing
  edges are deliberately single-slot and interacting). Each row is a directed
  edge `currency -> quote_currency`.
- `config.json` — `{"knowledge_cutoff": "YYYY-MM-DD"}`.

Outputs (`/app/output`): `enriched_transactions.csv`,
`unresolved_transactions.csv`, `revenue_by_currency.json`,
`routing_audit.csv`, and a reusable `asof_resolve.py` exposing
`build_report(data_dir, out_dir)`.

## Approach

Per ordered `(currency, quote_currency)` pair, resolve the in-force edge on a
date with a strict order: filter by knowledge (`recorded_at <= cutoff`) → keep
the latest `recorded_at` per `rate_effective_date` → drop effective dates whose
authoritative row is `retracted` → take the greatest active
`rate_effective_date <= txn_date` → drop it if stale (`txn_date - effective >
max_age_days`). `rate_to_usd` is the product of rates along the **minimum-tier
simple path** to USD, tie-broken by least total tier → fewest hops →
lexicographically smallest currency-code sequence (rates are not arbitrage-free,
so the path choice determines the value). Then **all of a date's transactions are
routed together under per-edge `daily_capacity`** as a joint assignment: resolve
as many as possible, minimize total tier-cost, then prefer fewer distinct
non-USD intermediate currencies across the whole date. Paths can consume
capacity on multiple constrained edges, and each constrained edge on the path
must be debited and later reported in `routing_audit.csv` with deterministic
per-edge surge cost positions assigned by ascending `txn_id`. With interacting single-slot clearing edges, the cheapest routing can hand a scarce slot to a
*later* transaction and force an earlier one onto a dear fallback. The traps:
filtering `active` before resolving supersession; using post-cutoff data; treating
knowledge as-of the transaction date; single-quote-parent / first-path /
fewest-hops routing; missing cascade-to-unresolved; carrying a stale edge past its
horizon; and — the decisive crux — resolving transactions independently or
allocating scarce capacity greedily/per-edge instead of solving the joint optimum,
including on wider hidden same-day contention clusters where naive path-product
enumeration is not viable.

## Environment

Single Ubuntu image (`task/environment/Dockerfile`) with `pytest` baked in; the
solution and verifier are pure standard library.

## Verification

`task/tests/test_outputs.py` recomputes ground truth independently from a
protected copy of the dataset in `/tests/data`, checks the shipped outputs
(partition, per-row least-cost-path point-in-time rate, USD amounts, revenue
numeric totals, routing audit rows, ordering, half-up cent rounding, USD zero-hop handling, deterministic lexicographic path
selection, date-level intermediate consolidation, visible surge-position ordering, multi-edge capacity-path accounting, and equal-objective capacity tie-breaks), and runs the submitted
`asof_resolve.py` in a sandbox against eight fixed-seed generated hidden
datasets — each embedding the bitemporal traps, direct USD handling, every path
tie-break class, multi-edge constrained paths, edge-level surge audit costs, date-level intermediate consolidation, equal-cost joint-assignment tie-breaks, and a
cascade-to-unresolved pivot — so hardcoding or visible-instance tuning cannot
pass. The hidden datasets also include a wider capacity/surge contention
component to reject brute-force-only routing modules.
