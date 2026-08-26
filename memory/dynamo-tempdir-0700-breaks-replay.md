---
name: dynamo-tempdir-0700-breaks-replay
description: "Privilege-dropped replay fails on two host-permission traps: mkdtemp roots are 0700, and /tests is chmod 0700 for the duration of the run."
metadata:
  type: feedback
---

Two failures that only appear inside the container, both hit on `dynamo-63f2f80`
and both invisible to a green local (root) test run:

1. **`tempfile.TemporaryDirectory` creates 0700.** Probe fixtures built under it
   are unreachable by the uid-65534 replay — `PermissionError` on the first
   `open()`, surfacing as dozens of fixture *errors*, not a clean failure. Call
   `root.chmod(0o755)` on every holder directory you build fixtures into.
2. **Never replay a stack that lives under `/tests`.** The sandbox chmods
   `/tests` to 0700 while the submission runs (that is the point), so pointing the
   run at `/tests/pristine_<fixture>` fails for the same reason. Copy the sealed
   fixture into the probe holder and replay from the copy; grade the untouched
   original by fingerprint.

**Why:** the verifier runs as root, so every path is readable during authoring and
during any host-side sweep. Only an in-container run as the unprivileged user
exercises the traversal.

**How to apply:** run oracle-in-Docker before believing any sweep. This is the same
class as the earlier `ReplayFleet` 0700 finding — treat "0700 by default" as the
expected state of anything `mkdtemp` returns.
