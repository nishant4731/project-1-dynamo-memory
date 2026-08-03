Rollcall packet format (RVPK1)

Every non-comment line in `/app/data/reel_packets.rvp` has this shape:

`RVPK1|seq|kind|capture_ms|revision|published_ms|row|col|crc32:payload`

The `payload` field is Base85 text for Python's `base64.b85decode` and may itself contain `|` characters, so parse the first eight `|` separators as fields and treat the remainder as `crc32:payload`.

Fields:
- `seq`: positive integer packet sequence number.
- `kind`: `TILE` or `PARITY`.
- `capture_ms`: frame capture timestamp in milliseconds.
- `revision`: positive integer revision for that captured frame.
- `published_ms`: time when that packet revision became authoritative.
- `row`: tile row, 0 through 3.
- `col`: tile column, 0 through 5 for `TILE`; `-1` for `PARITY`.
- `crc32`: eight lowercase hexadecimal digits for the uncompressed payload bytes.
- `payload`: Base85 text containing a zlib-compressed 64-byte payload.

A frame is 48 by 32 pixels. Each tile is 8 by 8 pixels, stored row-major as 64 grayscale byte values. A parity payload is also 64 bytes: byte `i` is the XOR of byte `i` from all six uncompressed tiles in that tile row for the same `capture_ms` and `revision`.

For recovery, each tile row's authoritative revision is the revision of the highest-revision in-window `PARITY` packet for that row whose decoded payload length and CRC-32 are valid; break ties by largest `seq`. Tile packets for that row must then be selected only at that authoritative parity revision, even if higher-revision `TILE` packets exist in the cutoff window. When more than one in-window `TILE` packet shares the same row, column, and authoritative revision, choose the largest `seq`; record that selected seq before applying CRC-32 rejection.

Contact-sheet layout for recovered frames uses four columns, one-pixel black gaps only between adjacent frames, and no outer border: width `4*48+3*1`, height `rows*32+(rows-1)*1`, with the first frame at pixel `(0,0)`.

Some reusable input directories may also include `clock_offsets.csv` with fields `band_start_seq,band_end_seq,offset_ms`. When present, add `offset_ms` to `published_ms` before comparing the packet to a cut-plan `cutoff_ms` for every packet whose `seq` is within that inclusive sequence band. Packets outside all listed bands use offset 0.
