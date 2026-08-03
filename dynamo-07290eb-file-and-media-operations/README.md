# Restore Metadata Dynamo Task

This repository contains a Harbor-format Project Dynamo task in `task/`.

The task asks an agent to build `/app/restore_metadata.py`, a reusable repair tool for archive packages whose object bytes survived but whose file paths, optional basename patches, permissions, and nanosecond mtimes must be reconstructed from signed ledger evidence. The shipped package is synthetic but models a realistic digital-preservation or media-archive recovery workflow.

Verification checks the repaired visible package and then runs the submitted tool against deterministic submission-salted hidden packages. The verifier compares file hashes, POSIX modes, mtimes, report schema/types, the JSONL audit manifest, the per-asset event trace, basename-patch accounting, collision handling, quarantine behavior, unexpected restored artifacts, and evidence consumption.
