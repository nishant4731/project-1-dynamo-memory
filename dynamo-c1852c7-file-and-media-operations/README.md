# Recover Reel Dynamo Task

This repository contains a Harbor task for recovering a monochrome Y4M video reel from fragmented packet data.

The agent receives a visible packet log and manifest in `/app/data`. To solve the task, it must decode several tile codecs, discard recalled or checksum-invalid packets, choose authoritative revisions, repair missing tile replacements from ordered and sometimes chained parity packets, and write both the recovered video and an audit JSON file with reconstruction counters.

Verification is performed by pytest in `task/tests`. The tests reject missing or symlinked outputs, parse the Y4M container, compare the recovered video digest and frame statistics to protected expected values, and validate that the audit reports the parity repairs plus exact record, codec, and parity-branch accounting.

Note: pipeline redraw after a GitHub API timeout while posting the Dynamo eval sticky comment (eval itself had already passed).
