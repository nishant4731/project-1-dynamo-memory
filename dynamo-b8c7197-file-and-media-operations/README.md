# RVF Ledger Rebuild

This Dynamo task asks the agent to recover a crashed grayscale video spool under `/app/session`.
The required deliverable is a visible repaired RVF movie, PGM contact sheet, frame-statistics CSV,
JSON report, TSV audit, output integrity index, and reusable executable CLI at
`/app/recover_spool.py`.

The spool combines encoded tile records, stateful tap rows that sample partially rendered video,
and a post-render patch ledger whose rows are guarded by hashes of the current frame bytes. The
verifier checks the shipped visible recovery, contact sheet, frame statistics, and audit against
protected expected outputs, then runs the submitted CLI on generated hidden spools with varied
dimensions, XOR-key periods, malformed rows, future taps, hash mismatches, clipping, patch
operations, saturation, and report counter cases.

The environment uses the approved pinned Ubuntu base image, bakes verifier dependencies at build
time, and copies only the visible session data into the agent image. Ground truth and hidden
fixture generation live in `task/tests/`. The contact sheet is a quick visual diagnostic, while the
statistics CSV deliberately checks each recovered frame from a different angle: it catches clipped
or missed blend/patch paths that can leave frame hashes wrong but hard to diagnose from raw bytes
alone. The audit TSV is intentionally redundant with the JSON report, and the output index records
exact byte counts and digests for every emitted artifact so cross-file serialization mistakes are
easy to isolate without parsing the binary RVF payload.
