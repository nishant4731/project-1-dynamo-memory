Implement the Lumen Circuit board replayer for the files already staged in `/app/data`.

Your submission has four responsibilities:

1. Render `/app/data/scene.json` into `/app/output/final.ppm`.
2. Emit the parsed replay summary for that same scene as `/app/output/report.json`.
3. Emit the intervention forecast for that same scene as `/app/output/forecast.json`.
4. Install a reusable program at `/app/renderer.py`.

The reusable program must be invokable as:

```bash
python3 /app/renderer.py SCENE_JSON OUTPUT_DIR
```

It must load the requested scene, create the output directory if necessary, and replace any existing `final.ppm`, `report.json`, or `forecast.json` in that directory with newly computed artifacts. The grader will intentionally reuse output directories, so a renderer that leaves stale files in place is incorrect.

Treat `/app/data/FORMAT_NOTES.md` as the complete specification for the replay format. It defines the ordering of same-tick events, actor stepping, wall bounces, slash/backslash mirrors, digit tiles and portal-pair selection, prism-cell phase changes, zero-based collision group indexing, scheduled flare pulses, heat accumulation, intervention forecast replay, cell-to-pixel expansion, actor overlays, checksums, counter names, sort order, and exact JSON primitive types.

Part of the work is recovering the rendering profile. `/app/data/FORMAT_NOTES.md` gives the hue RGB table directly. The remaining fixed profile data, including non-digit tile base colors and the four 3-by-3 actor masks, is recoverable from the calibration folders under `/app/data/calibration/case_*/`. Every calibration folder includes the input `scene.json` plus the engine-produced `final.ppm` and `report.json` for that probe. The probes combine heat, tile decoration, flares, and actor overlays, so recover the profile through the documented integer rendering equations rather than assuming blank zero-heat examples.

All math in the replay is integer math. Clamp only where the rulebook says to clamp. The image must be binary P6 PPM with header `P6\n<canvas_width> <canvas_height>\n255\n`, where `canvas_width = scene width * 3` and `canvas_height = scene height * 3`, followed immediately by raw RGB bytes. JSON whitespace is irrelevant, but the loaded object must exactly match the schema and values described in the rulebook.

Do not solve only the bundled scene. Hidden checks run `/app/renderer.py` against fresh scenes with different board sizes, tick counts, portal labels, flare anchors and periods, forecast probe ticks and stamp amounts, event schedules, wall stamps, actor populations, and collision layouts. Build the replay engine from the documented format and recovered profile instead of copying visible outputs.
