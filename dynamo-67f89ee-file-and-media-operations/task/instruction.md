Recover the release atlas for the archived badge design package in `/app/design_bundle`. The package format and all rendering rules are normative in `/app/design_bundle/FORMAT.md`.

Create `/app/recovered/atlas.ppm` as an ASCII `P3` PPM containing the rendered release frames from `/app/design_bundle/releases.json` in listed order, left to right, with no padding between frames.

Create `/app/recovered/render_bundle.py` as a reusable Python 3 program that accepts exactly two arguments, `bundle_dir` and `output_dir`, and writes `atlas.ppm` and `report.json` for any bundle following `/app/design_bundle/FORMAT.md`.

Create `/app/recovered/report.json` as UTF-8 JSON with this exact top-level schema:

`{"atlas_sha256": string, "frames": [{"id": string, "raw_rgb_sha256": string, "non_background_pixels": integer, "clipped_mask_pixels": integer, "overpainted_mask_pixels": integer, "bbox": [integer, integer, integer, integer] or null}]}`

For every checksum, hash the row-major raw RGB bytes of the relevant image, not the textual PPM file. The `frames` array must follow the order of `/app/design_bundle/releases.json`; each bounding box is inclusive `[min_x, min_y, max_x, max_y]` over pixels that differ from that frame's resolved background color. `clipped_mask_pixels` counts, before blending, every nonzero transformed source-mask pixel that lands inside the 32 by 32 frame across all drawn placements; overlapping placements are counted each time they cover the same destination pixel. `overpainted_mask_pixels` counts the subset of those source-mask pixels whose destination pixel already differs from the resolved background immediately before that source pixel is blended.
