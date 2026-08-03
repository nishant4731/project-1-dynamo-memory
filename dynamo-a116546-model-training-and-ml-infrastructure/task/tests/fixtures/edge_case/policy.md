Cutoff: 2026-07-18T12:00:00Z

The sweep uses successive halving with rungs at epochs 3, 6, and 12, eta = 3, and six available restart slots.

Metric log canonicalization:

- Use only metric rows whose `recorded_at` timestamp is at or before the cutoff.
- Ignore rows with `state` equal to `retracted`.
- For the same `(trial_id, epoch, split)`, keep the row with the largest integer `revision`; if there is still a tie, keep the row with the latest `recorded_at`.
- A checkpoint is usable only when the canonical rows include both `train` and `valid` splits for the same trial and epoch.
- A trial with `status` equal to `failed` in `/app/data/trials.jsonl` is never promoted or stopped, but its usable checkpoints still count when computing optimizer-family medians for new-trial selection.

Checkpoint score:

`valid_loss + 0.35 * max(0, valid_loss - train_loss - 0.035) + 0.00008 * gpu_seconds`

Lower score is better. Round only final values written to `/app/resume_plan.json`; do not round intermediate values.

Incumbent:

Choose the usable checkpoint with the lowest checkpoint score among all non-failed trials. Break ties by higher epoch, then lexicographically smaller trial id.

Promotion policy:

- For each rung except 12, rank all non-failed usable checkpoints at that rung by checkpoint score, then trial id.
- The promotable set at that rung is the first `ceil(n / eta)` ranked trials, where `n` is the number of ranked trials at that rung.
- A trial is active at a rung only if it has a usable checkpoint at that rung, has no usable checkpoint at a later rung in the same trial, and no child trial that started at or before the cutoff lists it as `parent_trial_id`.
- Promote active trials that are in the rung's promotable set. Promote from 6 to 12 before promoting from 3 to 6; within the same source rung, use checkpoint score then trial id. Assign priorities starting at 1.
- Stop every active, non-failed trial at a non-final rung that is not selected for promotion. Here "completed rung" means the trial has a usable checkpoint at that rung; it does not require the trial's top-level `status` to equal `completed`. Never stop trials whose only active checkpoint is at the final rung 12.

New-trial policy:

- Fill the remaining restart slots after promotions with fresh candidate configurations from `/app/data/candidates.json`.
- Exclude a candidate if any trial at or before the cutoff used the same fingerprint. A fingerprint is `(optimizer, lr, batch_size, dropout, weight_decay)`.
- For each optimizer, compute the median epoch-3 checkpoint score across all usable trials with that optimizer. Failed trials are included here if they have a usable epoch-3 checkpoint. If an optimizer has no usable epoch-3 checkpoint, use `1.0`.
- Score fresh candidates with:

`optimizer_median + 0.05 * abs(log10(lr) - log10(0.001)) + 0.02 * dropout - (0.015 if batch_size == 64 else 0)`

Lower is better. If `m` restart slots remain after promotions, choose exactly `min(m, number_of_fresh_candidates)` fresh candidates as a set. The set cost is the sum of candidate scores, plus `0.025` for each pair with the same optimizer, plus `0.006` for each pair with the same `batch_size`, plus `0.012` for each pair whose absolute `log10(lr)` difference is less than `0.12`, minus `0.010` for each distinct optimizer beyond the first in the set. Choose the set with the lowest set cost; break ties by the lexicographically smallest sorted list of `config_id` values. Order the selected candidates in `/app/resume_plan.json` by their individual fresh-candidate score, then `config_id`. Start each new trial with `budget_epoch` 3. New-trial priorities continue after promotion priorities.
