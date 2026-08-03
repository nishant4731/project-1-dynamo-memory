# Rescue Mix Dynamo Task

This repository contains a Harbor task under `task/` for repairing a crashed audio packet spool. The agent must implement `/app/rescue_mix.py`, reconstruct a byte-exact raw PCM mixdown, write a JSON audit report, and consume the ledger/packet evidence after a successful repair.

The verifier checks the shipped visible session and runs the submitted tool on protected generated sessions that exercise clock-anchor recovery, packet integrity checks, duplicate precedence, three packet codecs, signed gain arithmetic, saturating audio assembly, bounds clipping, and exact report accounting.
