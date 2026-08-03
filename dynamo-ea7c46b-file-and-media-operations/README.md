# Recover Design Task

This repository contains a Harbor task for Project Dynamo under `task/`. The agent must create a reusable Python program at `/app/recover_design.py` that repairs design-pack directories into a byte-exact PPM image and a strict JSON manifest.

The visible pack combines palette revisions, event replay, fragment checksums, masks, transforms, opacity math, channel bindings, clipping, and evidence consumption. The verifier also generates held-out packs to check the same disclosed rules against non-visible layouts, repaired source fragments, zero-opacity overpaint accounting, and channel-binding states.

Local validation performed before submission:

- `git diff --check`
- `bash references/check-base-image.sh task`
- `python3 -m py_compile task/solution/recover_design.py task/tests/test_outputs.py`
- direct pytest verifier smoke tests for oracle and no-op stages
- `harbor run -p task --agent oracle` with reward `1.000`
- `harbor run -p task --agent nop` with reward `0.000`
