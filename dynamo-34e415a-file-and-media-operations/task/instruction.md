Write a program that recovers artwork in legacy "DSP1" sprite-pack format and analyzes top-to-bottom paths. Apply it to `/app/data/design.dsp`.

Deliverables:
- `/app/solve.py` — Python 3 program invoked as `python3 /app/solve.py <input.dsp> <output.ppm> <answer.txt>`. Decodes a DSP1 file to binary PPM (P6) at the second path and writes the path analysis at the third. Must handle any valid DSP1 file.
- `/app/output.ppm` and `/app/answer.txt` — results for `/app/data/design.dsp`.

Grading runs `/app/solve.py` on held-out DSP1 files and checks decoded pixels (exactly) and path analysis. `/app/data/example.dsp` with `/app/data/example.ppm` and `/app/data/example.answer.txt` is a worked reference for self-checking. `/app/data/calib_a.dsp`, `/app/data/calib_b.dsp`, and `/app/data/calib_c.dsp`, with matching `.ppm`/`.answer.txt`, are calibration pairs for the undocumented opcode `0x04`. Their filters are None, so emitted residuals are directly visible as palette indices.

DSP1 format (big-endian unsigned integers):

Header (12 bytes):
- 0-3: magic `DSP1`
- 4: version, always `1`
- 5: flags. Bit 0 (`0x01`): set = 4-bit packed residuals; clear = 8-bit.
- 6-7: width W (>= 1)
- 8-9: height H (>= 1)
- 10-11: palette_count M (1..256; if 4-bit mode, M <= 16)

Palette: M entries of 3 bytes (R, G, B) immediately after header. Index i is palette entry i.

Filter table: next H bytes, one per row (row 0 first), filter type 0..4.

Residual stream: opcodes emitting W*H residual palette indices (0..M-1) in row-major order. Stops when W*H values are emitted. Opcode tags (1 byte):
- `0x00` LITERAL: byte count N (1..255), then N values. 8-bit: N bytes. 4-bit: packed ceil(N/2) bytes, MSB nibble first; odd N has 0 low nibble padding.
- `0x01` RUN: byte count N (1..255), then 1 value (4-bit: high nibble, 0 low nibble). Emits value N times.
- `0x02` COPY: length N (1..255), 2-byte distance D (1..65535, <= emitted count). Emits N values where k-th (k=0..N-1) is residual at (current_count - D) after previous k appends (self-overlapping if D < N). N and D are plain bytes.
- `0x03` AFFINE_COPY: length N, 2-byte distance D, byte A, byte B. For each k, read source residual at (current_count - D) after previous appends, emit `(source*A + B + k) mod M`. N/D rules match COPY.
- `0x04` CAL_COPY: undocumented legacy opcode. Its payload is length N, 2-byte distance D, then bytes A, B, C. Infer its emission rule from the calibration pairs; N/D and self-overlap rules match COPY.

Reconstruction: recover pixel index row by row. For pixel (x, y) with filter f, let `left` = index at (x-1, y), `up` = (x, y-1), `upleft` = (x-1, y-1); off-edge neighbors are 0. Predictor P:
- 0 None: P = 0
- 1 Sub: P = left
- 2 Up: P = up
- 3 Average: P = (left + up) // 2 (floor)
- 4 Paeth: p = left + up - upleft; pick left, up, or upleft closest to p (tie-break order: up, then upleft, then left).

Reconstructed index is `(residual + P) mod M` (only final sum reduces mod M). Pixel color is `palette[reconstructed_index]`.

Worked example — modular wrap (Sub, M=6): left=5, residual=3 -> index (3+5) mod 6 = 2.
Worked example — 4-bit packing: residuals [3, 10, 5] (N=3) stored as bytes `0x3A 0x50`.

Output PPM (P6): write bytes `P6\n<width> <height>\n255\n` followed by W*H*3 raw RGB bytes.

Path analysis: let g[y][x] be reconstructed index (0..M-1). Consider top-to-bottom paths picking cell (x_y, y) per row y (0..H-1) where:
1. Column step: |x_y - x_{y-1}| <= 1 for y >= 1.
2. Step modifier: straight steps (dx = 0) contribute g[y][x]; diagonal steps (|dx| = 1) contribute (g[y][x] + 1) mod M. Row 0 contributes g[0][x_0].
3. Path constraint: NO TWO CONSECUTIVE DIAGONAL STEPS. If step y-1 -> y is diagonal (|dx| = 1), step y -> y+1 MUST be straight (x_{y+1} = x_y).
4. Path score formula: Let S = (sum of cell contributions) mod M. Let P = max(g[y][x_y]) be peak index on path. Score is (S + P) mod M. (If H=1, each cell's (g + g) mod M is candidate).

Write `/app/answer.txt` as exactly three newline-terminated lines:
1. maximum score B, decimal integer in 0..M-1;
2. count of valid paths with score B, modulo 1000003;
3. lexicographically smallest optimal path columns as comma-separated zero-based integers `x_0,...,x_{H-1}`.

Worked example — path score (M=4): grid rows [3, 1] then [1, 3]. Straight paths 0->0 and 1->1 score 3; diagonal 0->1 scores 2. Max score B is 3, two paths achieve it, and the lexicographically smallest is `0,0`.
