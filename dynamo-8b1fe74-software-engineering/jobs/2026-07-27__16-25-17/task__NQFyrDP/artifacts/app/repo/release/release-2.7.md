# Release 2.7 recovery note

The deploy branch was force-pushed during incident cleanup. Recreate the release branch
from release material, not from the newest ref. Validate each material candidate's exact
decision signature through the cutoff-reduced authority graph, then reduce each issue's
revisioned row in `.release/release-plan.tsv`. Repeatedly emit an active issue whose
dependencies have already been emitted; among eligible issues choose the earliest
`ready_at` instant, then the smaller numeric `schedule_seq`, then the smaller issue id.

All commits on the recovered branch must follow the audit convention where the subject starts
with `[<ISSUE_ID>]` (e.g. `[LX-1842] preserve cents during weighted allocation`) and the commit
body records `Source-Commit: <full source commit>`, `Evidence-Ref: <decision-log evidence_ref>`,
`Patch-ID: <stable patch-id>`, `Decision-Row: <1-based decision-log data row, excluding the header>`, and
`Release-Sequence: <two-digit ordinal>/12`. The manual-waived LX-2024 row also requires
`Waiver-State: approved`.

LX-1842 owns total-preserving weighted allocation and deterministic remainder
placement. LX-1926 owns refund direction for negative cent adjustments. If those two
pieces of evidence collide, allocate the absolute magnitude with LX-1842's remainder
rules and then restore the negative sign to each share.

LX-1855 owns local business-day settlement windows and entry-level merchant timezones
when an entry supplies `merchant_tz`. LX-1933 owns reversal-entry exclusion for those
same windows. If those two pieces of evidence collide, keep the LX-1855 timezone-aware
signature, use `merchant_tz` before the default timezone for each entry, and filter
reversal rows before comparing the local business date.

LX-2077 is release material even though its evidence ref in the decision log is only a
short object id left behind by `git fsck`; it was not preserved as a branch. It owns
`settlement_period_key(entry, tz_name="America/New_York")`: choose
`settlement_period_at` when present, otherwise `posted_at`, and return the local date
using `merchant_tz` before the default timezone.

LX-1870v2 owns the canonical SHA256 idempotency payload, sorted invoice lines, compact
JSON encoding, currency, and retry generation. LX-1906 owns the merchant namespace for
that same key. If those two pieces of evidence collide, the recovered release must keep
the LX-1870v2 SHA256 contract and include `merchant_id` in the payload. In `/app/repo/ledgerkit/config.py`,
include `REQUIRE_MERCHANT_ID`.

LX-1884 owns the retry-generation window calculation. LX-1917 owns the provider
deadline cap. If those two pieces of evidence collide, compute the LX-1884 retry window
first and then cap it at `deadline_cap` when that field is present. Resolve the LX-1917
trust event stream at the recovery cutoff before deciding which evidence is release
material; equal recorded instants use numeric `source_seq` rather than row order or text.

LX-2044 owns merchant reconciliation code validation. LX-2051 owns the nullable upstream
fallback for the same field. If those two pieces of evidence collide, return `UNKNOWN`
for `None`, reject an empty string by raising `ValueError`, and preserve every non-empty
raw code exactly as supplied. LX-2062 owns a bitemporal alias graph for non-empty merchant
codes and keeps the `knowledge_at` argument. At every graph hop, use the same requested
tenant, `as_of`, and `knowledge_at` cutoffs. Scope rows to the current code and tenant;
collapse rows sharing `alias_id` to the latest known revision by `recorded_at` instant and
numeric `source_seq`; then choose the latest retained `effective_at` not after `as_of`,
again using numeric sequence for an equal instant. Missing timestamps and sequences retain
the defaults in the conflict checklist. Follow the winning `canonical` as the next code.
If no row wins, return the current code. A winning `state: retired` row also returns the
current code, so downstream retirement suppresses only that hop; a later known active
revision may revive it. If traversal would revisit any code, return the original input
code rather than a partial path. Never cross tenant scope, use a future-known revision,
or use a later effective alias for an older invoice. Do not apply the PX-331 normalization
row or its rollback-only revert.

The 2.7 line must not contain 2.8 schema probes, the PX-331 merchant normalization, or
the legacy SHA1 idempotency variant.
