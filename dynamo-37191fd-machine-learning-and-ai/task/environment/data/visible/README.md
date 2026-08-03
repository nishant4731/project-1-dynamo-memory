This bundle contains sparse-feature audit records from one model-inspection run.
Use calibration.tsv plus calibration_labels.tsv to recover the bundle-specific
integer triage parameters, then apply them to candidates.tsv. Global parameter
ranges are patch_weight 1..8, ablate_weight 1..8, margin_weight 0..6,
stability_weight 0..5, and freq_divisor 12..42. Each profile has bias -24..24,
core_threshold 60..94, relay_threshold 32..66, dead_activation_max 4..18, and
purity_cut 50..90. method_profile_offsets.tsv adds a
profile/source reliability offset to the score. Duplicate records are present intentionally;
keep the row with the highest revision, then highest quality, then
lexicographically greatest record_id. Candidate rows with unknown profile/source,
missing or bad integer fields, out-of-range quality/activation/frequency/purity/stability,
or negative edge counts are excluded and counted as invalid.
rulebook_summary.json candidate_rows counts every candidates.tsv data row, including
invalid and duplicate rows. handoff_links.tsv contains directed feature links
with channel, strength, and lag fields; invalid links are counted, while valid
routes stay within one profile, start at core, pass only through relays, and end
at spurious or dead. Route score is start_score - terminal_score plus link values
(strength - 2*lag plus channel bonus probe=0, patch=4, ablate=-2), minus 5 for
each extra link after the first. For each chosen route, critical_link reports the
single route-link removal that causes the largest best-fallback score loss.
handoff_routes.jsonl path, channels, and non-null fallback_path fields are JSON
arrays, not joined strings. learned_profiles is keyed by bridge, cortex, and guard,
with the five profile parameters for each profile.
