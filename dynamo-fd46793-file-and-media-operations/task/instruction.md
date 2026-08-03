Recover the grayscale video ledger in `/app/video-ledger`. Write a reusable Python 3 program at `/app/recover_ledger_video.py` and run it as:

`python3 /app/recover_ledger_video.py --manifest /app/video-ledger/public_manifest.json --segments /app/video-ledger/segments --out /app/recovered`

The program must also work with other manifests and segment directories that use the same format.

The manifest is JSON with `width`, `height`, `frame_count`, and `segment_glob`. Segment files are binary `.lvseg` files. The runtime corpus also includes `/app/video-ledger/FORMAT.md`, a plain-text summary of these rules. Each segment starts with the 8 bytes `LVSEG1\n\0`. After that, it contains zero or more records. Each record is a 4-byte little-endian unsigned payload length followed by that many UTF-8 JSON bytes.

Each record has `packet_id`, `patch`, `frame`, `rev`, `authority`, `layer`, `op`, and `rect`. `rect` is `[x, y, w, h]`, where `(x, y)` is the top-left pixel and `w * h` is the payload pixel count. `authority` is one of `relay`, `camera`, or `repair`, ranked from lowest to highest in that order. `op` is one of:

- `key`: absolute luma bytes for the rectangle, base64 encoded in `data`.
- `set`: absolute luma bytes for the rectangle, base64 encoded in `data`.
- `xor`: luma bytes to XOR into the current rectangle, base64 encoded in `data`.
- `blend`: luma bytes to alpha-composite into the current rectangle, base64 encoded in `data`, using integer `alpha` from 0 through 255. For each pixel, replace current byte `c` with `(c * (255 - alpha) + data_byte * alpha + 127) // 255`.
- `fill`: write the integer `value` from 0 through 255 into the rectangle.
- `copy`: copy pixels from `source_frame` and `source_rect`, optionally transformed by `transform`, then add signed integer `bias` modulo 256. `source_frame` must be no later than the target frame. `source_rect` is `[x, y, w, h]`. `transform` is one of `identity`, `hflip`, `vflip`, `rot180`, or `transpose`; omitted `transform` means `identity`, and omitted `bias` means `0`. `identity`, `hflip`, `vflip`, and `rot180` require `source_rect` and `rect` to have the same width and height. `transpose` swaps them, so `rect` width must equal `source_rect` height and `rect` height must equal `source_rect` width.

Copy transform coordinates are exact. For a source rectangle with local coordinates `(col, row)`, `identity` reads `(col, row)`, `hflip` reads `(source_width - 1 - col, row)`, `vflip` reads `(col, source_height - 1 - row)`, `rot180` reads `(source_width - 1 - col, source_height - 1 - row)`, and `transpose` writes target local `(col, row)` from source local `(row, col)`.

For `key`, `set`, `xor`, and `blend`, omitted `encoding` or `encoding: "raw"` means `data` decodes directly to `w * h` row-major bytes. `encoding: "rle"` means the base64 decoded `data` is repeated runs of 2-byte little-endian unsigned `count` followed by one byte `value`; expand runs across row boundaries until exactly `w * h` bytes are produced.

First decode every record from every matching segment. For records with the same `patch`, keep exactly one: highest `rev`; if tied, highest authority rank; if still tied, lexicographically largest `packet_id`. Do this supersession before reconstructing frames.

Reconstruct frames in index order. Frame 0 starts as all-zero luma. Each later frame starts as a copy of the previous reconstructed frame unless the current frame has at least one selected `key` record, in which case it starts as all-zero luma. For the selected records targeting a frame, apply them sorted by ascending `(layer, packet_id)`. `key` and `set` both write their decoded bytes into `rect`; `xor` XORs decoded bytes with the current rectangle; `blend` applies the alpha-composite formula above against the current rectangle; `fill` fills the rectangle with `value`. A `copy` record reads its source pixels from the final reconstructed `source_frame` when `source_frame` is earlier than the target frame. When `source_frame` equals the target frame, it reads from a snapshot of the current frame taken immediately before that `copy` record writes, so overlapping same-frame copies must not smear pixels written by the same copy. Pixel order inside a rectangle is row-major. Segment filename order must not affect the result except through the record fields above.

Write `/app/recovered/frame_0000.pgm` through `/app/recovered/frame_0006.pgm` for the public seven-frame corpus. Each PGM file must be binary P5 with exactly the header `P5\n<width> <height>\n255\n` followed by raw row-major luma bytes. Also write `/app/recovered/manifest.json` with exactly this schema:

`{"width": <int>, "height": <int>, "frame_count": <int>, "frames": [{"index": <int>, "sha256": <64 lowercase hex of raw luma bytes>, "mean_luma": <number rounded to 3 decimals>, "source_packets": [<packet_id strings in application order>]}, ...]}`

Use standard JSON formatting; field order is not important. Compute `mean_luma` as the arithmetic mean of the raw luma bytes and round it with round-half-to-even ties, equivalent to Python 3 `round(mean, 3)`. The `source_packets` list for a frame contains only the selected packet IDs applied to that frame after supersession, sorted in the same order they were applied.

Hidden ledgers may use frames up to 1200 by 900 pixels and hundreds of broad `fill`, `set`, `xor`, and transformed `copy` rectangle records. The output is still byte-exact, but a correct program should process broad row-aligned rectangles efficiently enough to finish within the verifier timeout.
