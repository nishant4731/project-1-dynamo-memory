Finish `/app/tuner.py`, a CLI promotion planner for revisioned hyperparameter-tuning ledgers. It must run as `python3 /app/tuner.py INPUT_JSON OUTPUT_JSON`. Also create `/app/plan.json` by running it on `/app/data/visible_ledger.json`. A copy of this specification is available in the container at `/app/SPEC.md`.

Each input JSON has `promotion_round`, `trials`, and `events`. `promotion_round` has integer `from_budget`, `to_budget`, `slots`, `compute_budget`, and `folds`. Each trial has `trial_id` and `params`. Events are processed as a ledger, not as already-clean summaries:

- `metric` events have `seq`, `trial_id`, `budget`, `fold`, `revision`, `val_loss`, `train_loss`, and `wall_time_sec`.
- `invalidate` events have `target_seq`; the targeted metric must be ignored.
- `checkpoint` events have `seq`, `trial_id`, `budget`, and `path`.
- `stop` events have `trial_id` and `budget`; if the stop budget is at or below `from_budget`, that trial is not eligible for promotion.

For each trial, use only metrics at exactly `from_budget`. For each required fold, keep the non-invalidated metric with the largest `(revision, seq)`. A trial is eligible only if it has one selected metric for every required fold, has at least one checkpoint at exactly `from_budget`, and is not stopped. Use the checkpoint at exactly `from_budget` with the largest `seq`.

For every selected metric compute:

`adjusted_loss = val_loss + 0.4 * max(0, val_loss - train_loss) + 0.015 * log2(1 + wall_time_sec / from_budget)`

For an eligible trial, compute the mean adjusted loss and the population standard deviation across required folds. Its promotion score is:

`score = mean_adjusted_loss + 0.6 * population_stdev`

Rank eligible trials by ascending unrounded `score`, then ascending unrounded mean adjusted loss, then ascending `depth * width` from `params`, then ascending `trial_id`.

Survivors are not simply the first ranked trials. Each eligible trial has cost `depth * width`. Select exactly `slots` survivors whose total cost is at most `compute_budget`; inputs guarantee at least one feasible set. Among feasible sets, choose the set with the smallest total unrounded `score`, then smallest worst individual unrounded `score`, then smallest total unrounded mean adjusted loss, then smallest total cost, then lexicographically smallest survivor ID list after sorting that set by the candidate ranking above. For these survivor-set objective comparisons, treat numeric differences at or below `1e-12` as equal before moving to the next tie-break. List survivors and allocations in candidate-rank order.

`OUTPUT_JSON` and `/app/plan.json` must be UTF-8 JSON objects with exactly these top-level keys:

- `round`: string formatted as `"{from_budget}_to_{to_budget}"`.
- `survivors`: promoted trial IDs in rank order.
- `ranked_candidates`: one object per eligible trial in rank order. Each object has `trial_id`, `score`, `mean_adjusted_loss`, and `folds_used`. Round `score` and `mean_adjusted_loss` to 6 decimal places. `folds_used` is the required fold list.
- `allocations`: one object per survivor in rank order. Each object has `trial_id`, `next_budget`, `checkpoint`, and `params`. `next_budget` is `to_budget`. `params` is the original trial params except `learning_rate` is multiplied by `sqrt(from_budget / to_budget)` and rounded to 8 decimal places.
- `discarded`: object mapping every ineligible trial ID to one of `stopped`, `missing_metric`, or `missing_checkpoint`. If more than one reason applies, use that priority order. Sort discarded IDs lexicographically.

The same CLI must work on other ledgers with the same schema; do not special-case `/app/data/visible_ledger.json`.
