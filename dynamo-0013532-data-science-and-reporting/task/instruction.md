Prepare a USD-normalized transaction table from an append-only FX edge log with
late, retroactive corrections. Many currencies are quoted through other
currencies, and rates are not globally arbitrage-free.

Inputs in `/app/data`:

- `/app/data/transactions.csv` — columns `txn_id` (unique integer), `txn_date`
  (`YYYY-MM-DD` business date), `currency`, `amount` (decimal, local currency).
- `/app/data/fx_rates.csv` — bitemporal directed edges `currency ->
  quote_currency`, with columns `currency`, `rate_effective_date` (`YYYY-MM-DD`),
  `recorded_at` (`YYYY-MM-DD`), `rate` (one unit of `currency` equals `rate`
  units of `quote_currency`), `status` (`active` or `retracted`),
  `quote_currency`, `tier` (positive integer base cost), `max_age_days`
  (positive freshness horizon), `daily_capacity` (positive per-date transaction
  limit), `surge_threshold` (positive base-tier usage count), and
  `surge_penalty` (non-negative extra cost for each use beyond that threshold).
  Rows for the same `currency`, `quote_currency`, and `rate_effective_date` have
  distinct `recorded_at` values.
- `/app/data/config.json` — an object with a single key `knowledge_cutoff`
  (`YYYY-MM-DD`).

For each transaction attach `rate_to_usd`, the USD value of one unit of its
currency on its business date, reconstructed as of cutoff `K`.

First determine which edge, if any, is in force for an ordered pair
`(currency, quote_currency)` on a date `D`:

- Use only that pair's rows with `recorded_at <= K`; ignore later rows. A
  correction recorded by `K` applies to all transactions, including earlier ones.
- Per `rate_effective_date`, the latest `recorded_at` row is authoritative. If it
  is `retracted`, that effective date has no edge; superseded rows do not return.
- Choose the greatest `rate_effective_date <= D` whose authoritative row is
  `active`. Its `rate`, `tier`, `surge_threshold`, and `surge_penalty` apply on
  `D`.
- That edge is usable only if fresh: `D - rate_effective_date <= max_age_days`.
  If stale, no earlier effective date for that pair applies.

Then convert to USD by routing with daily capacity. For currency `C` on date
`D`, candidate paths are simple directed paths `C -> USD` over edges in force on
`D`; path base cost is the sum of base `tier` values, and `rate_to_usd` is the
product of edge `rate` values (`USD` is `1`). Rank paths by (1) least total base
tier, (2) fewest hops, (3) lexicographically smallest currency-code sequence.
Because rates are not arbitrage-free, the chosen path determines the value.

All transactions sharing a date are routed together; each edge carries at most
`daily_capacity` transactions that date. A path may consume capacity on more than
one edge; every constrained edge on the chosen path must be debited. Edge tier
cost is dynamic: for `N` uses on date `D`, the first `min(N, surge_threshold)`
uses incur base `tier`, and each extra use incurs `tier + surge_penalty`. Choose
the routing that first
**resolves as many transactions as possible**, then **minimizes total tier-cost**
(base tiers plus all edge surge penalties), then minimizes the count of distinct
non-USD intermediate currencies used by resolved paths on that date; break
remaining ties by the sequence, in ascending `txn_id`, of each transaction's path
key `(total base tier, hops, currency-code sequence)`, where unresolved sorts
after resolved. A transaction is
unresolved if it has no path to `USD` on `D` because of gaps or staleness, or if
capacity forces it out under that objective. Scarce and surge-pricing edges
interact, so the cheapest whole-day routing is a joint assignment over dynamic
tier costs. Hidden datasets may include dozens of same-day transactions sharing
constrained edges; `build_report` must avoid full-day path-product brute force.
A high `daily_capacity` is still a limit; it is nonbinding only when it is at
least the same-day transaction count.

Keep intermediate rates at full precision; only `amount_usd` is rounded.
`amount_usd` is `amount * rate_to_usd` rounded to two decimals (round half up)
and must be written with exactly two digits after the decimal point.

Produce exactly these files:

- `/app/output/enriched_transactions.csv` — one row per resolved transaction,
  header `txn_id,txn_date,currency,amount,rate_to_usd,amount_usd`, sorted by
  `txn_id` ascending.
- `/app/output/unresolved_transactions.csv` — one row per unresolved
  transaction, header `txn_id,txn_date,currency,amount`, sorted by `txn_id`
  ascending.
- `/app/output/revenue_by_currency.json` — a JSON object mapping each currency
  with at least one resolved transaction to the sum of its resolved `amount_usd`
  values, rounded to two decimals (round half up).
- `/app/output/routing_audit.csv` — one row per edge traversed by a resolved
  transaction, header `txn_id,txn_date,edge_position,edge_currency,edge_quote_currency,edge_tier_cost`,
  sorted by `txn_id` then `edge_position`. `edge_position` is 1-based within the
  chosen path. For reporting only, order same-date uses of an edge by ascending
  `txn_id`; this is the deterministic mapping for which transactions receive
  the first base-tier uses when `surge_threshold` binds. Uses beyond
  `surge_threshold` report `tier + surge_penalty`; earlier uses report `tier`.
  Zero-hop USD transactions have no audit rows.
- `/app/output/asof_resolve.py` — reusable module exposing
  `build_report(data_dir, out_dir)`. Given `transactions.csv`, `fx_rates.csv`,
  and `config.json` with these schemas, it writes the four report files into
  `out_dir`, requires no network, writes only inside `out_dir`, and will be run
  on additional datasets.
