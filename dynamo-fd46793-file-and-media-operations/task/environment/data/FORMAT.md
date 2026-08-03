Ledger format summary:

- Segment files matching `public_manifest.json` field `segment_glob` are parsed from `/app/video-ledger/segments`.
- Each `.lvseg` file starts with bytes `LVSEG1\n\0`, followed by repeated records: 4-byte little-endian payload length and that many UTF-8 JSON bytes.
- For duplicate `patch` values, keep one selected record by this exact order: highest `rev`, then highest authority where `relay < camera < repair`, then lexicographically largest `packet_id`.
- Reconstruct frames in increasing frame index. Frame 0 starts from zero luma. Any later frame with at least one selected `key` record also starts from zero luma; otherwise it starts from the previous reconstructed frame.
- Within one frame, apply selected records by ascending `(layer, packet_id)`.
- `key` and `set` write base64 `data`; `xor` XORs base64 `data`; `blend` alpha-composites base64 `data` using integer `alpha` as `(current * (255 - alpha) + data * alpha + 127) // 255`; `fill` writes integer `value`; `copy` reads `source_frame` and `source_rect`, applies optional `transform`, then optional signed `bias` modulo 256.
- Copy transform mappings: `identity` keeps `(col,row)`, `hflip` reads `(source_width-1-col,row)`, `vflip` reads `(col,source_height-1-row)`, `rot180` reads `(source_width-1-col,source_height-1-row)`, and `transpose` writes target `(col,row)` from source `(row,col)`.
- For `key`, `set`, `xor`, and `blend`, omitted `encoding` or `encoding: "raw"` means decoded `data` is row-major bytes. `encoding: "rle"` means decoded `data` is repeated runs of 2-byte little-endian `count` plus one byte `value`.
- Omitted `copy.transform` means `identity`; omitted `copy.bias` means `0`.
