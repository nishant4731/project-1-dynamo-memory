# Repair Video Reels

This Harbor task asks the agent to recover approved RGB video takes from a damaged post-production session in `/app/data/session`.

The agent must produce exact binary PPM contact strips, JSON recovery metadata and stats, an edited broadcast contact strip, and a reusable Python recovery tool at `/app/recovered_video/recover_reel.py`. The task exercises point-in-time release ledger handling, mixed RGB24 frame encodings with non-uniform frame counts, encoded-payload hash validation, XOR and GF(256) parity repair, lexicographic modular edit-plan selection, clipped integer RGB compositing, recovery accounting, and irreversible payload/parity evidence consumption.

Verification regenerates pristine sessions, reruns the submitted reusable tool on the visible session and hidden verifier-generated sessions under an isolated subprocess, then compares exact JSON schemas and byte-identical PPM media outputs against an independent reference while confirming evidence deletion.

<!-- infra redraw 2026-07-28T05:07Z: pass@2 AgentSetupTimeoutError on Daytona; re-trigger pipeline -->
