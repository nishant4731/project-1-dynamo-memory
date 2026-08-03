Recover the Mercury-7 restricted custody export using only files under `/app/evidence/`.

The detailed, normative reconstruction rules are in `/app/evidence/vault_rules.md`. Follow that file exactly. It defines canonical source reconstruction, record eligibility, fingerprint supersession, export-ledger authorization, artifact share repair/recovery, release-ticket, cross-record batch, and reviewer-quorum authorization, audit and rejection proofs, manifest schema, and JSONL formatting.

Required outputs:
- `/app/results/manifest.json`
- `/app/results/audit_proofs.jsonl`
- `/app/results/rejections.jsonl`
- exact selected canonical sources under `/app/results/selected/`
- exact recovered media under `/app/results/artifacts/`

Create no other files under `/app/results/`.

The manifest must contain `{matches,proofs,rejections,summary}`. Accepted matches are sorted by `logical_id` and numbered from 1. Rejections cover every live in-force record rejected after fingerprint resolution, ordered by `logical_id`, with first failing reason among `ledger`, `artifact`, `ticket`, and `approval`; every ticket-passing group in this fixture has a valid batch gate. The two JSONL files must mirror `proofs` and `rejections` as compact JSON with lexicographically sorted keys.

The verifier also checks protected held-out coverage across the evidence families used by these rules:
both segmented source formats and parity repair, all share encodings, seeded and literal GF(257)
coordinates, every repair action, and varied ledger, ticket, batch, and approval algorithms/windows.
Do not solve by assuming one record shape or one authorization encoding; apply the rules to every
catalog row and every live in-force chain.
