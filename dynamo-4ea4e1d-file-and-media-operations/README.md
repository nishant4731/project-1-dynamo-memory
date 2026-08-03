# Video Band Recovery Task

This Harbor task asks the agent to produce `/app/recover_video.py`, a reusable Python script that rebuilds grayscale video frames from a damaged clip ledger.

The visible input under `task/environment/data/cam_roll_17` contains a synthetic but realistic media recovery workspace: a `ledger.tsv` file points to fragmented frame-band payloads, some of which are stale, corrupt, expired, superseded, RLE-compressed, or delta-coded against the previous recovered frame. The instructions define the point-in-time selection rule, payload codecs, PGM output format, and exact manifest schema.

Verification runs the submitted script against the shipped clip plus deterministic hidden clip workspaces generated at verify time. The tests compare the recovered `manifest.json` semantically and every produced PGM frame byte-for-byte, while rejecting missing, extra, or symlinked outputs.
