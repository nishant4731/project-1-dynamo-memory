# Recovery Rules

The task instructions are authoritative; this file is the same agent-visible rule summary packaged inside the work environment for reference.

- Build `/app/restore_design.py`. It must accept exactly three arguments: input job directory, output PPM path, and output JSON report path.
- Input jobs contain a `manifest.json` with `canvas`, `palettes`, `fragments`, and optional `repair_groups`.
- Fragment paths, mask paths, and repair shard paths may be absolute or relative to the input job directory.
- PGM rasters use max values from `1` through `65535`; both text `P2` and binary `P5` encodings are valid, and comments may appear in the PGM header.
- If a PGM max value is not `255`, scale each stored sample into the task's 0-through-255 domain with `floor(sample * 255 / max_value + 0.5)` immediately after reading. Binary `P5` files with max value greater than `255` store two big-endian bytes per sample.
- Fragment scaled sample `255` is transparent. Fragment scaled sample `254` is a registration marker. Neither is painted.
- Mask samples are scaled coverage values from `0` through `255`. If a fragment sets `mask_polarity = "inverse"`, use `255 - mask_sample` after repair, scan normalization, orientation, and max-value scaling.
- A path written as `repair:<id>` is reconstructed by bitwise-XORing every listed shard sample at the same coordinate before scan normalization or orientation.
- For `scan = "serpentine"`, rows are numbered from zero. Reverse stored rows whose 0-based `y` index is odd (`y % 2 == 1`) before applying orientation.
- A fragment raster uses `scan` and `orientation`. A mask uses `mask_scan` and `mask_orientation` when present, otherwise it uses the fragment's `scan` and `orientation`.
- Orientations are `none`, `rot90`, `rot180`, `rot270`, `flip_x`, and `flip_y`. Rotations are clockwise; derive each rotation's pixel mapping from that clockwise convention. `flip_x` mirrors left-right by reversing each row; `flip_y` mirrors top-bottom by reversing row order.
- If a fragment has `source_window`, apply it after raster and mask repair, scan normalization, orientation, and mask polarity. The window is in transformed fragment coordinates and lies inside the transformed raster. Discard samples outside it, crop both raster and mask to the window, and rebase the kept top-left to `(0,0)` before registration or origin placement.
- If a fragment has `registration`, apply repair, scan normalization, orientation, and any `source_window` first. Then translate the transformed `254` marker coordinates so their set exactly equals the unordered `registration.canvas_points`; the unique translation is the fragment origin.
- Select the palette revision with the greatest `effective_at` value less than or equal to the fragment's `captured_at`.
- Palette revisions may be complete or partial. Build the usable color table and optional alias table by applying every same-name revision with `effective_at <= captured_at` in ascending `(effective_at, revision)` order; later `colors` and `aliases` entries replace earlier entries with the same key, and omitted keys keep their earlier values. The report still records the last applied revision id.
- A palette alias maps a stored sample index to another palette index after transparent/registration handling but before color lookup.
- Composite fragments in ascending `(z, captured_at, id)` order.
- Effective and captured timestamps are integer manifest values on the same timeline; compare them numerically.
- Missing `opacity` means `1.0`. A missing mask means full coverage `255` everywhere.
- For each nontransparent, non-marker sample, alpha is `fragment.opacity * mask_sample / 255`.
- In `mode = "over"`, source color is the alias-resolved indexed palette color. In `mode = "erase"`, source color is the canvas background color. In `mode = "atop-background"`, paint the alias-resolved indexed palette color only when the current destination pixel is still exactly the canvas background color; otherwise leave it unchanged.
- Composite source over destination in linear-light sRGB using the standard sRGB transfer curve. Round each encoded channel after every painted sample, not once at the end.
- Samples outside the canvas after orientation and source-window rebasing are ignored.
- Write `/app/recovered_sheet.ppm` as RGB PPM using the manifest canvas dimensions and max value `255`.
- Write `/app/recovery_report.json` with exactly: `width`, `height`, `applied_fragments`, `palette_revisions`, `rgb_sha256`, `opaque_pixel_count`, `background_pixel_count`, and `processing_audit`.
- `processing_audit` has exactly these integer counters: `palette_revision_count`, `repair_group_reads`, `repair_sample_xor_count`, `transparent_sample_count`, `registration_marker_count`, `clipped_paint_sample_count`, `zero_alpha_sample_count`, `painted_sample_count`, `erase_sample_count`, `blocked_atop_sample_count`, `remapped_sample_count`, and `window_discard_sample_count`.
- `palette_revision_count` is the total number of palette revision records applied across all fragments. `repair_group_reads` counts each read from a `repair:<id>` raster or mask path, and `repair_sample_xor_count` counts every shard sample XORed during those reads, including repeated reads.
- If `source_window` is present, `window_discard_sample_count` counts every transformed fragment-raster sample outside the window, and discarded samples are not counted in later audit buckets. After repair, scan normalization, orientation, and source-window cropping, count fragment-raster sample `255` as transparent and sample `254` as a registration marker before canvas clipping. For other samples, compute alpha before canvas clipping. Non-marker, nontransparent samples with alpha `<= 0` are zero-alpha samples. Positive-alpha samples whose palette alias changes the stored index are remapped samples before clipping. Positive-alpha samples outside the canvas are clipped paint samples. Positive-alpha `atop-background` samples inside the canvas whose destination is not background are blocked atop samples. Positive-alpha samples that are inside the canvas and allowed by their mode are painted samples; painted erase-mode samples are also erase samples.
