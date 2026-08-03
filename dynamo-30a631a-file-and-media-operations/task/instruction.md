The camera export in `/app/export` is a damaged grayscale video packet dump. Write a reusable Python 3 program at `/app/recover_clip.py` and use it to recover the supplied clip into `/app/recovered`.

Your program must accept exactly two arguments:

```bash
python3 /app/recover_clip.py INPUT_DIR OUTPUT_DIR
```

`INPUT_DIR` contains `manifest.json` and a `packets/` directory. The manifest has integer fields `width`, `height`, `frame_count`, and `base_pixel`. Before frame 0, the previous finalized frame is a `width` by `height` image filled with `base_pixel`.

Each file in `packets/` may contain multiple binary packet records concatenated together. A packet record is:

- bytes 0-3: magic `DMPV`
- byte 4: flags. Bit 0 set means XOR-delta, bit 0 clear means absolute. Bit 1 set means sparse-mask payload. Bit 2 set means serpentine tile scan order. Bit 3 set means run-length encoded payload. Bit 4 set means motion-copy payload. Other flag bits are ignored.
- bytes 5-6: frame index, unsigned big-endian
- byte 7: tile x coordinate
- byte 8: tile y coordinate
- byte 9: tile width
- byte 10: tile height
- bytes 11-12: revision, unsigned big-endian
- bytes 13-14: payload length, unsigned big-endian
- following bytes: payload

The two-byte frame index, revision, and payload length fields are full unsigned 16-bit big-endian values; do not treat either byte alone as the field value.

If bit 3 is set, first decompress the payload into its logical payload bytes. The RLE stream is a sequence of chunks. For a control byte below 128, copy the next `control + 1` literal bytes. For a control byte 128 or above, repeat the next byte `(control & 127) + 1` times. A packet with a truncated RLE chunk or an RLE stream that expands to the wrong logical length is malformed. For motion-copy packets, the three-byte motion header is part of this logical payload length.

For normal logical payloads, payload is exactly `tile_width * tile_height` grayscale bytes. For sparse-mask logical payloads, payload begins with `ceil(tile_width * tile_height / 8)` mask bytes, then one grayscale byte for each mask bit set to 1. Mask bits are read most-significant bit first in each byte; unused low bits in the final mask byte are ignored. A sparse packet proposes values only for pixels whose mask bit is 1.

For motion-copy logical payloads, payload begins with three bytes: `frame_back`, `source_dx`, and `source_dy`. `frame_back` is unsigned and must be at least 1; `source_dx` and `source_dy` are signed 8-bit integers. The source frame is `frame_index - frame_back`, which must already be finalized. For every proposed target pixel in the tile, copy the pixel at `(target_x + source_dx, target_y + source_dy)` from that source frame. If any proposed source pixel is outside the frame, the packet is malformed. A non-sparse motion-copy payload has only those three bytes. A sparse motion-copy payload has those three bytes followed by the mask bytes; it has no per-pixel value bytes because values come from the source frame.

Tile pixel order is row-major unless bit 2 is set. With serpentine order, even-numbered tile rows are read left-to-right and odd-numbered tile rows are read right-to-left. This order applies both to normal payload bytes and to sparse-mask bit positions/value bytes.

Packet files can contain junk bytes between records. Scan each file byte by byte for `DMPV`; after a valid packet, continue after that packet's payload. If a `DMPV` candidate is malformed, treat that candidate byte as junk and continue scanning from the next byte. Ignore packets whose payload does not match the normal, sparse-mask, or RLE encoding implied by the flags, whose frame index is outside the manifest range, or whose tile is not fully inside the frame. File order is not meaningful.

Finalize frames in increasing frame index. For each frame, start from the previous finalized frame. An absolute packet proposes its payload bytes as pixel values for its tile. An XOR-delta packet proposes `previous_finalized_pixel XOR payload_byte` for each pixel in its tile; use the previous finalized frame as a snapshot, not a frame being modified by other packets from the same frame. A motion-copy packet proposes copied source-frame bytes; if bit 0 is also set, the proposed value is `previous_finalized_pixel XOR copied_source_pixel`. If more than one packet proposes a value for the same pixel in the same frame, keep the proposal with the highest revision. If revisions tie, keep the proposal from the lexicographically earliest packet filename; if that still ties, keep the earlier byte offset within that file. Pixels with no accepted proposal keep their previous finalized value.

Write one frame image per frame under the chosen output directory's `frames` subdirectory. For the supplied clip, the required files are `/app/recovered/frames/frame_0000.pgm`, `/app/recovered/frames/frame_0001.pgm`, and so on through `/app/recovered/frames/frame_0007.pgm`. Each image must be binary PGM with header `P5\nWIDTH HEIGHT\n255\n` followed by the raw grayscale frame bytes in row-major order.

Also write `/app/recovered/summary.json` for the supplied clip. For any output directory, the summary file must use this schema:

```json
{
  "width": 0,
  "height": 0,
  "frames": [
    {"index": 0, "sha256": "...", "changed_pixels": 0}
  ],
  "clip_sha256": "..."
}
```

`sha256` is the SHA-256 hex digest of that frame's raw grayscale bytes. `changed_pixels` is the number of pixels whose value differs from the previous finalized frame, using the all-`base_pixel` frame before frame 0. `clip_sha256` is the SHA-256 hex digest of all raw finalized frames concatenated in order. The verifier will run your program on additional exports that follow the same format, so do not hardcode values from `/app/export`.
