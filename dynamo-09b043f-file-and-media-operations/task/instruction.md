The design export in `/app/design_drop` was interrupted while a multi-board SVG atlas was being assembled. Create an executable Python 3 program at `/app/recover_design.py` with this interface:

`python3 /app/recover_design.py INPUT_DIR OUTPUT_DIR`

The program must read the four JSONL files named `boards.jsonl`, `layer_events.jsonl`, `tokens.jsonl`, and `fragments.jsonl` from the input directory, create the output directory if needed, then write exactly two files inside it: `atlas.svg` and `report.json`. Also run the program on `/app/design_drop` and write the requested visible outputs to `/app/restored/atlas.svg` and `/app/restored/report.json`.

Use these reconstruction rules. JSONL row order is not authoritative. First discard every board row whose `status` is `"deleted"` — deleted rows never win and never hide an older active revision. Among the remaining rows for each `board_id`, keep the row with the largest `(revision, recorded_at, record_id)` tuple. If no non-deleted row remains for a `board_id`, omit that board entirely. Render kept boards in ascending `board_id` order, packed horizontally. The atlas width is the sum of kept board widths; its height is the maximum kept board height. Board widths and heights are numeric values and use the same numeric formatting rule as layer values.

For each kept board, consider only layer events with the same `board_id` and `effective_at <= board.exported_at`; count later layer events in `late_layer_records_ignored`. For each `layer_id`, keep the event with the largest `(effective_at, recorded_at, event_id)` tuple. If that kept event has `op: "delete"`, do not render the layer and count it in `tombstones_applied`. Otherwise render it. Within a board, render layers by ascending numeric `z`, breaking ties by ascending `layer_id`.

Token colors are point-in-time. For a layer's `fill_token` or `stroke_token`, find token rows with the same `token` and `effective_at <= layer.effective_at`, keep the largest `(effective_at, recorded_at, token_id)` tuple, and use its `value` only when `status` is `"active"`. If no such active state exists, use the layer's `fallback_fill` or `fallback_stroke` and count one `token_fallbacks` entry for that layer color.

Path layers list `segment_hashes`. For each hash, choose the `fragments.jsonl` row whose stripped `d` string has that SHA-256 digest; the row's own `digest` field is not authoritative and must not be used to accept or reject a row. If several rows validate for the same digest, use the smallest `(serial, fragment_id)` tuple. The SVG path `d` attribute is the chosen stripped segment strings joined by one space in the order listed by `segment_hashes`. `fragment_records_ignored` is the total number of fragment rows minus the number of distinct fragment rows actually used.

Write `atlas.svg` exactly as UTF-8 text with a final newline. Use this structure and attribute order:
`<svg xmlns="http://www.w3.org/2000/svg" width="W" height="H" viewBox="0 0 W H">`
then one board group per kept board:
`  <g id="board-BOARD_ID" transform="translate(X 0)">`
`    <title>BOARD_NAME</title>`
then layer elements, then `  </g>`, then `</svg>`.

A rect layer is:
`    <rect id="LAYER_ID" x="X" y="Y" width="W" height="H" fill="COLOR" opacity="OPACITY" />`
If a rect omits `opacity`, treat it as `1`. A text layer is:
`    <text id="LAYER_ID" x="X" y="Y" font-size="SIZE" fill="COLOR" font-family="Inter, Arial, sans-serif">TEXT</text>`
A path layer is:
`    <path id="LAYER_ID" d="D" fill="none" stroke="COLOR" stroke-width="WIDTH" stroke-linecap="round" stroke-linejoin="round" />`

Escape XML special characters in attributes and text. Format numeric values from their exact JSON decimal text (not from binary float approximations): integers stay as integers; otherwise round half to even to three decimal places using decimal arithmetic, then trim trailing zeroes and a trailing decimal point.

Write `report.json` as UTF-8 JSON with two-space indentation, sorted keys, and a final newline. It must contain exactly these keys: `atlas_sha256` (SHA-256 hex digest of `atlas.svg` bytes), `boards` (integer count of kept boards rendered in the atlas), `fragment_records_ignored`, `late_layer_records_ignored`, `layer_order` (object mapping each board id to its rendered layer ids in render order), `layers_rendered`, `token_fallbacks`, and `tombstones_applied`.
