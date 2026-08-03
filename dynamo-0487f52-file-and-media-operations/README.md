# Stenciled Luma Journal Task

This Harbor task asks agents to recover a crashed grayscale luma journal from authenticated anchor rows, packet logs, byte-repair sidecars, authenticated packet gates, packet lease windows, frame operation sidecars, current-bus feedback taps, and post-render threshold stencils. The recovered output also includes a tab-separated audit ledger, a PGM contact sheet for visual inspection, and a per-frame TSV scan of final luma statistics.

The required deliverables are:

- `/app/recovered/movie.y4m`
- `/app/recovered/contact.pgm`
- `/app/recovered/report.json`
- `/app/recovered/ledger.tsv`
- `/app/recovered/scan.tsv`
- `/app/recover_spool.py`

The visible fixture lives in `task/environment/data/session`. The verifier checks the visible recovered clip, typed report, ordered ledger, PGM contact sheet, TSV frame scan, and report digest bindings, then runs the submitted reusable CLI on protected generated journal fixtures with varied geometry, source offsets, repair rows, gate and lease windows, packet revisions, operation choices, tap writes, stencil passes, and scan statistics.

The fixture-local notes are part of the normative contract alongside `task/instruction.md`.

The task is designed as a realistic media repair workflow: solvers must build a reusable recovery program, not just reconstruct the shipped clip. Ground truth and hidden fixture generation remain in `task/tests/`, which Harbor overlays only at verification time.
