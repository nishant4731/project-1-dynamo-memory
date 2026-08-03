Create an executable Python 3 program at `/app/conform_reel.py`. The verifier runs:

`python3 /app/conform_reel.py <session_dir> <output_dir>`

Session dir has `session.json`, `clips.csv`, `edits.csv`, `looks.csv`, `motion.csv`, and `clips/`. Clip files are ASCII PPM `P3` contact sheets: frames left to right, width `frame_width * frame_count`, height `frame_height`. `session.json` gives `frame_width`, `frame_height`, and RGB `background`. `clips.csv` has `clip_id,path,frame_count,look_id`; `path` is relative to the session dir.

`looks.csv` has `look_id,channel,input_a,input_b,input_c,input_d,output_a,output_b,output_c,output_d,declared_gain,declared_lift`. Ignore declared gain/lift. Empty swatch cells are ignored. For each `look_id` and channel `0`/`1`/`2`, choose integer `gain` in `0..512` and `lift` in `-4096..4096` satisfying every present `input_*`/`output_*` pair under `output = max(0, min(255, (input * gain + lift + 128) // 256))`. If several pairs fit, keep smallest absolute `lift`; then smallest `gain`; then non-negative `lift`. Clip `look_id` `neutral` is absent from `looks.csv` and passes pixels through unchanged.

`edits.csv` has:

`event_id,revision,state,record_start,track,clip,source_start,source_len,out_len,direction,mirror_x,opacity,fade,blend`

Same `event_id` rows are revisions: keep highest integer `revision`; if that winner’s `state` is not `active`, drop the event. Active events cover `record_start` .. `record_start + out_len - 1`. For offset `k`: `fwd` uses `step = floor(k * source_len / out_len)` and source `source_start + step`; `rev` uses `step = ceil((k + 1) * source_len / out_len) - 1` and source `source_start + source_len - 1 - step`. If `mirror_x` is `1`, flip the source frame horizontally, then apply the clip look. Effective opacity at offset `k` is `opacity` when `fade` is `0`; when `fade` is `1` it is `(opacity * (k + 1) + out_len - 1) // out_len`. Effective opacity `0` still joins same-track suppression and non-empty-shift audit totals.

`motion.csv` has `event_id,offset,dx,dy`. Missing offsets are `(0, 0)`. Offsets are pre-mirror clip space. After mirror and look, place with `(eff_dx, dy)` where `eff_dx = -dx` if `mirror_x` is `1`, else `eff_dx = dx`: source `(x, y)` → `(x + eff_dx, y + dy)`. Out-of-frame pixels are transparent. `timeline.json` `motion` stores raw CSV `(dx, dy)`, not effective displacement.

Per output frame, start from background. On one track, only one covering event survives: greatest `record_start`, then lexically greatest `event_id`. Suppressed frames do not read clips or blend. Composite survivors in increasing `(track, event_id)` order. `opacity`/`fade` yield effective opacity `0..255`. `blend=over`: `(src * a + dst * (255 - a) + 127) // 255`. `blend=add`: `min(255, dst + (src * a + 127) // 255)`. `blend=screen`: `src_a = (src * a + 127) // 255`, then `255 - ((255 - dst) * (255 - src_a) + 127) // 255`. `blend=multiply`: `src_a = (src * a + 127) // 255`, then `(dst * src_a + 127) // 255`. Timeline length is max `record_start + out_len` among active events.

Write exactly these files in `<output_dir>`:

`final_reel.ppm`: ASCII `P3` contact sheet of output frames, same frame size, max `255`.

`timeline.json`: object with `frame_width`, `frame_height`, `segments`. One segment per active winning event, sorted by `(record_start, track, event_id)`, each with `event_id` (string), `record_start` (int), `record_end` (int, exclusive), `track` (int), `clip` (string), `look_id` (string), `source_indices` (int array), `motion` (`[dx, dy]` int pairs), `direction` (string), `mirror_x` (JSON boolean), `opacity` (int), `fade` (int), `blend` (string). `source_indices` and `motion` each have exactly `out_len` entries for every active segment, including offsets removed by same-track suppression.

`audit.json`: `output_frames`, `active_events`, `dropped_events`, `revised_events`, `tracks` (sorted ints), `clip_reads`, `look_counts`, `blend_counts`, `shifted_event_frames`, `empty_shift_frames`, `suppressed_event_frames` (all ints / objects as implied). `revised_events` counts distinct `event_id`s with more than one revision row, active or dropped. `tracks` lists tracks used by active events. For each surviving event frame: if every source pixel misses the frame after effective displacement, count one `empty_shift_frames` and do not increment `clip_reads`/`look_counts`/`blend_counts`; else increment those three once using the authored `blend` string. `shifted_event_frames` counts survivors whose effective displacement is not `(0, 0)`, including empty misses. `suppressed_event_frames` counts active frames removed by same-track suppression once each before cross-track overlap.
