Recover video from `/app/data/clip.rvc`, then build a constrained delivery reel. Write reusable `/app/out/recover.py`; it reads `RVC_INPUT` (default `/app/data/clip.rvc`) and writes `clip.y4m`, `delivery.y4m`, `plan.json` into `RVC_OUTDIR` (default `/app/out`). With neither variable set, `python3 /app/out/recover.py` must produce those default outputs. The program is rerun on other RVC4 containers, so implement the general rules; do not special-case.

Container format (all integers unsigned little-endian):

Header: bytes 0–3 ASCII `RVC4`; then uint16 `width`, `height`, `frame_count` (N), `fps_num`, `fps_den`, `group_size` (G), `parity_count` (R).

If G>0 and R>0: an R×G byte matrix `C` (row-major; `C[r][j]` is byte `r*G+j`), holding GF(2^8) coefficients.

N frame records in decode order, each: byte `type` (0x49 `I`, 0x50 `P`, 0x42 `B`), byte `flags`, uint16 `display_index`, uint32 `payload_len` (= `width*height`), then payload bytes.

If R>0: parity records, for each group in order, R records of `width*height` bytes. Group g covers frame records `[g*G, g*G+G)`; the last group may be shorter. With group payloads `p_0..p_{m-1}` (j = within-group index), parity record r is byte-wise XOR over j of `gfmul(C[r][j], p_j)`, each `p_j` the post-ledger authoritative payload.

Correction ledger: uint16 `event_count` (L); then L file-order events: uint16 `target` (decode index), uint32 `seq`, uint8 `op` (0=SET, 1=CLEAR), and only for SET, `width*height` payload bytes.

Delivery section: uint16 `slot_count` (T), `modulus` (M), `target` (D); then T slots, each uint16 `cand_count` (c) then c candidates of uint16 `src_display_index`, `score`, `weight`.

Reconstruct (all bytes unsigned):

0. Ledger first. For each targeted frame, apply events by ascending `seq` (ties by file order) to a working payload starting as that frame's base: SET replaces it; CLEAR resets to base, not the previous SET. This authoritative payload is used below. Untargeted frames keep their record payload. No erased frame is targeted.

1. Recover erasures. A frame with `flags` bit 0 has unusable payload; a group has at most R erasures. Over GF(2^8) with polynomial 0x11B (`x^8+x^4+x^3+x+1`; addition XOR; `gfmul` field multiplication), each parity row gives `XOR over j of gfmul(C[r][j], p_j) == parity_r`. Move known terms across and solve for erased `p_j`; any independent subset of the R equations works (some subsets are singular) and the solution is unique. Recover before decoding.

2. Invert payload filters after recovery and before decoding; ledger/parity use stored filtered bytes. If `flags` bit 3 is set, first invert up-sub: row 0 unchanged; for y>0 `raw[y*w+x]=(stored[y*w+x]+raw[(y-1)*w+x]) mod 256`. If bit 1 is set, then invert row-sub per row: `raw[0]=stored[0]`, `raw[x]=(stored[x]+raw[x-1]) mod 256`.

3. Decode frames in decode order to `width*height` row-major 8-bit images:
   - `I`: image = payload; becomes the anchor.
   - `P`: `image[i] = (anchor[i] + payload[i]) mod 256`, where `anchor` is the latest `I`/`P`; becomes new anchor.
   - `B`: `image[i] = (pred[i] + payload[i]) mod 256`. If flags bit 2 is set, defer until all I/P anchors are decoded, then use `A0`/`A1` as nearest anchors with display_index below/above `display_index(B)` (future decode-order anchors may be used). Otherwise `A1` is latest anchor and `A0` the prior anchor. With `d0=|display_index(B)-display_index(A0)|` and `d1=|display_index(B)-display_index(A1)|`, `pred[i]=(d1*A0[i]+d0*A1[i]+(d0+d1)//2)//(d0+d1)`. A `B` is never an anchor.

4. `display_index` is a permutation of `0..N-1`. Write `/app/out/clip.y4m`: images in ascending `display_index` order, as the Y4M stream below.

Delivery reel. Pick one candidate per slot. A selection is valid if `(sum weights) mod M == D`, each chosen `src_display_index` differs from the previous two slots' sources, and no source appears over twice. Among valid selections pick greatest total score; ties use the lexicographically smallest sequence of chosen candidate indices (0-based within each slot). A valid selection always exists. Verifier spaces may be too large for full enumeration; each `recover.py` rerun must finish within 60 seconds. Then:

- `/app/out/plan.json`: `{"slots": [chosen candidate index per slot], "total_score": <int>, "weight_mod": <int>}`, with `weight_mod = (sum chosen weights) mod M` (=D).
- `/app/out/delivery.y4m`: for each slot, the image whose `display_index` equals the chosen candidate's `src_display_index` (T frames), as Y4M below.

Y4M stream (both `.y4m` files): header `YUV4MPEG2 W<width> H<height> F<fps_num>:<fps_den> Ip A1:1 Cmono\n` (ASCII, header values); then per image, bytes `FRAME\n` followed immediately by `width*height` raw luma bytes. No bytes before header or after last frame. `.y4m` files are byte-compared and `plan.json` value-compared.
