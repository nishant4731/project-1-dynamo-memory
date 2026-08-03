# Recover Atlas

Software Engineering task (`dynamo/recover-atlas`): implement a reusable Python recovery tool for a corrupted event-sourced atlas store. The visible corpus lives in `/app/atlas` (155 event rows, 87 calibration rows, ~42 KiB); deliverables are `/app/recover_atlas.py` and `/app/atlas_answer.json`.

The agent must infer each model adapter policy from calibration probes before repairing sparse event edges. Protected tests generate three hidden atlases (dimension 5–7, ≤211 event rows, ≤99 calibration rows, ≤54 KiB each) with distinct counter witnesses for all 14 report fields. The verifier checks the visible answer and runs the submitted tool on those hidden corpora. Ground truth is computed inside the verifier from protected fixtures, and the runtime image exposes only the visible atlas data.
