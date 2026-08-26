---
name: dynamo-fixtures-must-survive-the-image
description: Symlinks flatten and empty directories vanish between git and the agent image, silently killing witnesses the local gate still sees.
metadata:
  type: feedback
---

Fixtures that live in the repo and are copied into the agent image can arrive
**different from what you generated**. Two measured cases on dynamo-7e6bfa7: a
symlink flattened to an empty regular file, and an **empty directory was not
stored by git at all** — a blocked spill path arrived missing, reading as "the
spill never landed" instead of "the path is blocked by a directory", which
silently stopped the corpus witnessing that rule.

**Why:** the local gate builds fixtures from the generator, so it stays green
forever; only the pipeline sees the committed-then-copied version. Both cases
cost a full cycle, and the second was caught only because an unrelated guard
happened to be sensitive to it.

**How to apply:** put a file inside any directory fixture. Add a test that walks
the **committed** tree and fails on any empty directory, and one that asserts the
built image still contains the fixture (`find /app -type l | wc -l`, count the
blocked dirs). Fix the class, not the instance.
