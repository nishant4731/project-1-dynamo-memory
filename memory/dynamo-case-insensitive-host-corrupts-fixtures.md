---
name: dynamo-case-insensitive-host-corrupts-fixtures
description: A fixture whose filenames differ only by case is silently merged when frozen on macOS and split again in the container, so the shipped bytes never match the regeneration.
metadata:
  type: feedback
---

Building dynamo-65cf2ab (2026-08-17) I planted a decoy seat file named `3.SEAT` beside the real
`3.seat` to witness a suffix rule. On the macOS host the filesystem is case-insensitive, so
freezing the fixture **overwrote** the real seat with the decoy's contents; inside the container
(case-sensitive overlayfs) the verifier's regeneration produced both files. The shipped vault and
the regenerated vault then disagreed by exactly one refused seat, and the oracle failed its own
verifier with a one-field diff that looked like an engine bug.

**How to apply:** never let two shipped fixture paths differ only by case — pick a decoy that
differs by more than casing (`3.sea1`, not `3.SEAT`). More generally, any fixture property that
survives ext4 but not APFS/HFS+ will pass every in-container check and still ship wrong, because
the freeze happens on the host. Same family as [[dynamo-fixtures-must-survive-the-image]]
(symlinks flatten, empty dirs vanish): the local gate tests what you generate, not what ships.

Cheap guard: after freezing, regenerate into a temp dir on the same host and diff the two trees —
a case collision shows up immediately as a missing file rather than as a puzzling counter.
