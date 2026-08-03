Implement executable Python 3 command `/app/filter_vault.py`.

It must run exactly as:

`/app/filter_vault.py /app/vault /app/filtered`

The input vault contains the complete visible contract at `/app/vault/FORMAT.md`; follow that file as normative. It defines row validation, path safety, manifest selection, override and renewal marker handling, receipt proof validation, media byte operations, bundle promotion, bucket ranking, copy naming, JSON fields, TSV/NDJSON views, hashes, ordering, and rejection counters. The shipped `/app/vault/NOTES.txt` is fixture-local context, but `/app/vault/FORMAT.md` decides any rule conflict.

Create one synchronized evidence packet rooted at `/app/filtered`:

- `/app/filtered/report.json`
- `/app/filtered/audit.tsv`
- `/app/filtered/decision_trace.ndjson`
- `/app/filtered/bucket_rollup.tsv`
- accepted payload copies below `/app/filtered/accepted`

The four metadata views and payload tree must describe the same accepted and rejected records. A stale, missing, reordered, or internally inconsistent secondary view is incorrect even when copied bytes and the main report look plausible.

Do not modify `/app/vault`. Do not create symlinks anywhere below `/app/filtered`.
