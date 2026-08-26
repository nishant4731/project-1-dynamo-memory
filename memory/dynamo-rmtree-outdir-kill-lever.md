---
name: dynamo-rmtree-outdir-kill-lever
description: "A \"clear the output directory\" rule kills agents who rmtree+makedirs it — 4 of 5 pass@5 fails, but difficulty_crux FAIL on all of them."
metadata: 
  node_type: memory
  type: project
  originSessionId: 6c48333f-56d9-4736-82fd-cc4088e05c61
  modified: 2026-08-13T04:11:26.236Z
---

On `dynamo-e88ef21` (`dynamo/cairn-pack`, 2026-08-13) pass@5 was 1/5 with 4 good-valid fails, and
**all four shared one root cause**: the agent called `shutil.rmtree(out_dir)` then
`os.makedirs(out_dir)` to satisfy "delete every file already in `<out_dir>`". Removing the
directory entry needs write permission on its *parent*; the probe harness gives the landing dir
0777 inside a 0755 room the demoted uid does not own, so `os.rmdir` raises `PermissionError`
before any output exists. The one passing trial cleared the contents instead.

All four had already solved the whole algorithm — the shipped container was byte-correct in every
trial.

**Why:** the requirement is disclosed ("deletes every *file* already in `<out_dir>`", "writes only
inside `<out_dir>`") and realistic — an output directory handed to you by a caller may be a mount
point. The analyser marked `task_specification` and `approach_validity` PASS on all four, so they
count as valid failures.

**How to apply:** it is a cheap, strong kill lever on any reusable-CLI task with a clear-the-output
rule, and it costs nothing to include. But `difficulty_crux` reads FAIL on every such trial, so the
difficulty evidence is a peripheral idiom, not the modelling problem — a human R1 can push back.
Keep the wording explicit (files, not the directory) and expect the question. Do **not** "fix" the
harness on an all-green head: here it would have removed 4 of 5 failures from agents who had solved
everything else, turning an accepted 1/5 into a likely 4-5/5 reject. Same family as
[[dynamo-executable-bit-is-a-noncrux-kill]] and [[dynamo-operational-passat-failures]].
