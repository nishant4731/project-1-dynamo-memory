# Release recovery rules

The release branch named in the shiproom log is canonical only when its patch set
matches the release material implied by `.release/decision-log.tsv` and
`release/release-2.7.md`. Treat tags whose names contain `qa-green` as evidence about
a CI run, not as release authority.

The ledger is not a cherry-pick script. A row is release material only when it is on
lane `2.7`, its gate is `signed` or `dependency-cleared`, it has no successor, and its
phase is `shiproom` or `merge-required`, and its exact issue/evidence pair has a signature
authorized by the delegation rules below. A row whose gate is `manual-waived` is release
material only when it is on lane `2.7`, has no successor, has phase `waiver-required`,
`ci/release-2.7-runs.json` lists an approved waiver for the same issue and evidence_ref,
and its exact issue/evidence pair also has an authorized signature.
Rows with a successor are superseded by that successor.
Rows on any other lane, rows with gate other than `signed` or `dependency-cleared`, rows with
phase `rollback-only`, `withdrawn`, or `experimental`, and rows under `risk-hold` must have
no net effect in the recovered release.
Decision labels follow classification, not similarity: a `duplicate` / `shadow` row with an
empty successor is `reject`, never `superseded`, even when its stable patch id equals an
included source patch. Only a nonblank successor produces the `superseded` decision.
The manifest's `excluded` array is an audit index, not a complete dump of every rejected
row. It must list rejected/superseded rows that can be mistaken for release material because
they are duplicate/shadow evidence, successor-superseded evidence, rollback-only evidence,
2.8 lane probes, trusted-looking rows rejected by authorization or trust state, or the PX-331
normalization incident pair. Other withdrawn, delayed, risk-hold, or follow-up rows must still
have no net effect in the recovered release, but they do not need manifest entries.

Join decision rows to all rows in `.release/decision-signatures.tsv` with the exact
`issue` and `evidence_ref`. A `signed` gate requires capability `release`; a
`dependency-cleared` gate requires both `release` and `dependency`; and a
`manual-waived` gate requires both `release` and `waiver`. Required capabilities must
come from distinct signers, and their authorization paths must be edge-disjoint by
`delegation_id`. Extra, duplicate, unauthorized, wrong-capability, or edge-sharing
signatures do not satisfy a requirement. Reduce `.release/authority-events.tsv` independently for each
`delegation_id`: ignore events recorded after `authority_cutoff`, then choose the latest
`recorded_at` instant, breaking an equal instant by the larger numeric `source_seq` and
treating a missing sequence as `0`. Only a winning `granted` event creates an edge. At the
signature's `signed_at` instant, every edge in an authorization path must match the issue:
`*` matches all issues, a scope ending in `*` is a prefix match, and any other scope is exact.
Every edge must also have either the signature's exact `capability` or capability `*`.
The instant must be at or after `valid_from` and strictly before a nonblank `valid_until`.
A signature is authorized only if a path of such edges exists from `authority_root` to its
signer without repeating a principal. Authority does not transfer between issue scopes,
outside validity intervals, or through a revoked/cyclic path.

Every included manifest row must record its part of the canonical global authorization proof
in `authority_witnesses`, ordered by capability. Each witness records `capability`,
`signature_id`, `signer`, and the root-to-signer `delegation_path` as ordered delegation ids.
First enumerate every distinct-signer, edge-disjoint assignment for each material row.
`.release/authority-witness-limits.tsv` caps how many witnesses across the entire recovered
release may contain each listed delegation id; unlisted ids are unlimited. After deriving
release order, dependency-capability witnesses must also rotate root corridors: among
dependency-cleared rows in release order, the first delegation id of the dependency witness
must differ from the preceding dependency-cleared row's first delegation id. Non-dependency
rows do not reset that comparison. The preceding dependency corridor is also cooling down:
it must not occur in any witness path of the next dependency-cleared row, including that
row's release witness. Choose one assignment per included row so rotation, cooldown, and all
global limits hold. Compare full
release assignments in release order; within a row compare witnesses by capability, then
shorter path, delegation-id path lexicographically, signer, and signature id. Record the
smallest complete release assignment, not independently smallest per-row assignments.

After classification, reduce `.release/release-plan.tsv` independently for every issue.
Ignore rows recorded after `plan_cutoff`; among the rest choose the latest `recorded_at`
instant, breaking an equal instant by the larger numeric `revision_seq` and treating a
missing sequence as `0`. Every material issue must have exactly one winning `active` row.
Then repeatedly emit an eligible issue whose comma-separated `depends_on` issues have all
been emitted. Among eligible issues choose the earliest `ready_at` instant; for an equal
instant choose the smaller numeric `schedule_seq`, treating a missing sequence as `0`; if
both still tie, choose the lexicographically smaller issue id. A missing, retired, cyclic,
or stalled material plan is invalid. Do not use file order or timestamp/sequence strings.

`.release/trust-overrides.tsv` is an append-only event ledger. For each exact `issue` and
`evidence_ref` pair, ignore events recorded after `recovery_cutoff` in `branch-map.txt`,
compare `recorded_at` as timestamp instants, and choose the latest event. If two events
have the same recorded instant, choose the larger numeric `source_seq`, treating a missing
sequence as `0`; do not compare timestamp or sequence strings lexicographically. A winning
`revoked` event rejects an otherwise signed or dependency-cleared row, while a winning
`trusted` event restores that exact pair. An override never affects other evidence for the
same issue.

For duplicate evidence, use stable patch identity to avoid applying the same fix twice.
The recovered branch should start at the recorded release base and contain no 2.8-only files.

Auditing Standard:
Each commit on the recovered branch MUST have a subject beginning with `[<ISSUE_ID>]`, plus
`Source-Commit: <full source commit>`, `Evidence-Ref: <decision-log evidence_ref>`,
`Patch-ID: <stable patch-id>`, `Decision-Row: <1-based decision-log data row, excluding the header>`, and
`Release-Sequence: <two-digit ordinal>/10` trailers. A manually waived release row also
requires `Waiver-State: approved`.
