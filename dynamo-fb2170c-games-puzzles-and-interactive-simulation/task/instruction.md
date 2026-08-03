Reconstruct the missing Lantern Labyrinth replay engine from the public calibration package.

Normative inputs:

| Path | Role |
|---|---|
| `/app/data/training_transcripts.jsonl` | labeled examples; each line has a `case` and the engine's complete replay for that case |
| `/app/data/schema.md` | case schema plus required edge policies, including malformed commands, lock opening, and table-report keys |
| `/app/data/target_cases.jsonl` | unlabeled cases to replay for the visible output |

Deliverables:

| Path | Requirement |
|---|---|
| `/app/lantern_runner.py` | executable Python 3 CLI |
| `/app/visible_results.json` | replay array for `/app/data/target_cases.jsonl` |
| `/app/recovered_tables.json` | recovered constants emitted by the same CLI |

Runner interface:

`/app/lantern_runner.py --cases <jsonl_path> --out <json_path> [--tables-out <json_path>]`

The `--cases` file contains one case JSON object per line. Write one JSON array to `--out`, preserving line order. When `--tables-out` is present, also write the recovered table report described in `/app/data/schema.md`. Build `/app/visible_results.json` and `/app/recovered_tables.json` by running this interface on the visible target file.

Generalization rules:

- Recover rules from examples and `/app/data/schema.md`; do not hardcode visible case ids, room ids, item ids, or output rows.
- Hidden cases may use different room ids, item ids, maps, locks, command mixes, and starting inventories.
- The engine is deterministic and self-contained: no time, randomness, internet, or external game convention is part of the behavior.
- Treat room/item names as labels. Recover the arithmetic state machine over the fields and counters defined in the schema.
- The recovered table report is canonical, not defined only up to equivalent additive shifts. Use the exact direction-bias anchor stated in `/app/data/schema.md` when reporting `direction_bias` and the paired `terrain_cost` table.

Replay JSON contract:

| Object | Exact keys |
|---|---|
| case result | `case_id`, `final`, `turns` |
| `final` | `room`, `energy`, `phase`, `charges`, `score`, `inventory`, `opened`, `failed` |
| turn row | `turn`, `command`, `status`, `room`, `energy`, `phase`, `charges`, `score`, `bag_sig` |

Turn rows are post-command states and use 1-based `turn` numbers. Numeric fields must be JSON integers, not strings, floats, or booleans. Sort `inventory` lexicographically. Sort `opened` lexicographically as `room:direction`. Do not add keys beyond the tables above.
