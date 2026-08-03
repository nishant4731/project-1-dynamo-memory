Produce a Prism Relay optimizer for the pack mounted at `/app/data`.

Create these files in `/app`:

- `results.json`, containing the selected solution for the visible jobs.
- `relay_audit.json`, containing the compact audit report for the same visible selections.
- `prism_relay.py`, a reusable command-line tool invoked as `python3 /app/prism_relay.py INPUT_DIR OUTPUT_JSON AUDIT_JSON`.

The complete rules are shipped with the visible input in `/app/data/README.txt`. That README is part of the task contract, not a hint. It defines the legal domains, response-table semantics, slot enumeration, tick ordering, damper, relay, collector, switch, and gate state updates, frame/metric formulas, objective ranking, tie-breaks, event ordering, and exact JSON shape. Follow it for both the visible pack and any other pack passed to your CLI.

Important checker expectations: solve every legal assignment, sort output jobs by `job_id` instead of filename, output only valid JSON for both artifacts, and keep all numeric fields as integers. The verifier also runs your CLI on fresh packs with the same documented format, so hardcoded visible answers are insufficient.
