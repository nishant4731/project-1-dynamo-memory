Lantern Labyrinth data notes

`training_transcripts.jsonl` contains one JSON object per line with:
- `case`: the game state and command tape before replay.
- `result`: the complete result after replaying that case.

`target_cases.jsonl` contains only case objects. It uses the same schema as `case`.

Case fields:
- `case_id`: stable string identifier.
- `start_room`, `energy`, `phase`, `charges`, `inventory`: initial player state.
- `rooms`: room dictionary. Each room has `terrain`, `glyph`, `hue`, `aura`, `echo`, `items`, `exits`, and optional `locks`.
- `item_bank`: item dictionary. Each item has `kind`, `hue`, `weight`, and `sig`.
- `commands`: replay tape. Legal verbs in the corpus are `go`, `take`, `drop`, `use`, `say`, and `wait`.

The labeled examples are the authority for the engine's transition rules and scoring rules.
The hidden engine is a compact arithmetic transition system with fixed integer tables for terrain, direction, hue, and item kind, plus verb-specific formulas over the current state and the case fields. Room and item ids are labels, not constants; future cases may use new room ids, item ids, maps, and non-empty initial `inventory`.
Calibration completeness guarantee: hidden grading does not introduce new terrain, direction, hue, aura, item-kind, verb, parser, status, modulus, or conditional-rule domains beyond the shipped training transcripts and this schema. Hidden cases only recombine the same finite feature domains and transition rules over renamed rooms/items, new graph topology, new locks, new command orderings, and new starting inventories. A runner that exactly matches every labeled training replay while honoring this schema has enough information to replay the salted hidden cases; there is no additional private convention in `tests/`.
For the recovered table report, `direction_bias` is anchored exactly as `{"N": -1, "E": 1, "S": 2, "W": 0, "U": 3, "D": -2}`. Infer and report `terrain_cost` against that anchor; do not report an additively shifted terrain/direction pair even if it reproduces the same movement-energy totals.
Commands are parsed as whitespace-separated tokens. Future command tapes may contain a non-empty command that is not exactly `go DIR`, `take ITEM`, `drop ITEM`, `use ITEM`, `say WORD`, or `wait`; that command is a failed `garbled` turn and uses the same failed-command energy convention visible in the training failures.
An unopened lock can be opened only by a held item with `kind` equal to `key`, matching `hue`, and `weight + current charges >= strength`; matching hue alone is insufficient. When multiple held keys could open a lock, the lexicographically first qualifying item name is used. A successful open records the lock as opened, then applies `charges = (charges + opener item sig + strength) % 17` and adds `inferred hue value for the lock hue * strength` to `score` before the usual movement arrival updates.
When the runner is called with `--tables-out`, it writes a JSON object with keys `charges_modulus`, `direction_bias`, `hue_value`, `item_kind_value`, `phase_modulus`, `syntax_status`, and `terrain_cost`. The table entries are the recovered integer tables. `syntax_status` is `{"malformed_non_empty": "garbled"}`.
