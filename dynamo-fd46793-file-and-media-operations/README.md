# Ledger Video Recovery

This Harbor task asks the agent to recover a grayscale video stream from packetized ledger segment files. The visible corpus contains unordered segment files, superseded packet revisions, overlapping rectangle operations, and delta frames that depend on the previous reconstructed display frame.

The agent must implement `/app/recover_ledger_video.py`, run it on the public corpus, and write a PGM frame sequence plus `/app/recovered/manifest.json`. The verifier checks the public artifacts against protected expected hashes and also runs the submitted recovery program on verifier-generated hidden ledgers, which prevents public-output hardcoding.

The environment uses the approved Ubuntu 24.04 base image with Python, pytest, and pytest-json-ctrf baked in. Verification is fully local and does not install dependencies at runtime.
