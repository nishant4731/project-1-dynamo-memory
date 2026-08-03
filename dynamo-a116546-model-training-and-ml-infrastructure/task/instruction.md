The tuning coordinator crashed during a resumable language-model sweep. Reconstruct the scheduler state from the files in `/app/data`, write the exact restart plan to `/app/resume_plan.json`, and leave a reusable program at `/app/rebuild_scheduler.py`.

Use `/app/data/policy.md` as the normative scheduler policy. The telemetry is in `/app/data/trials.jsonl` and `/app/data/metrics.jsonl`; candidate configurations are in `/app/data/candidates.json`. Events after the policy cutoff are not part of this restart.

`/app/rebuild_scheduler.py` must be runnable as `python3 /app/rebuild_scheduler.py --data-dir DATA_DIR --output OUTPUT_PATH` for any directory with the same four input files and policy schema. It must handle different policy slot counts and candidate-pool sizes under that schema, and must write the same JSON schema described below.

`/app/resume_plan.json` must be a UTF-8 JSON object with this exact schema:

`schema_version`: integer `1`.

`cutoff`: the cutoff timestamp copied from `/app/data/policy.md`.

`incumbent`: object with `trial_id`, `config_id`, `epoch`, and `score` for the best completed checkpoint under the policy. `score` is a JSON number rounded to 6 decimal places.

`promotions`: array of objects ordered by policy priority. Each object has `trial_id`, `config_id`, `from_epoch`, `to_epoch`, and `priority`.

`stops`: array of trial ids, sorted lexicographically, for active completed rung trials that must not continue.

`new_trials`: array of objects ordered by policy priority. Each object has `config_id`, `budget_epoch`, and `priority`.

Do not include any extra top-level keys.
