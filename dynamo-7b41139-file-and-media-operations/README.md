# Conform Reel

This task asks the agent to implement `/app/conform_reel.py`, a reusable Python conformer for small video edit sessions represented as ASCII PPM frame-strip contact sheets plus CSV edit decisions.

The task is in the `File and Media Operations` category and `Video Processing` subcategory. The submitted program must parse clip sheets, apply edit revisions, retime source frames with integer floor mapping, mirror frames when requested, composite overlapping tracks with exact alpha/additive rules, and write a rendered reel plus timeline and audit JSON artifacts.

Verification runs the submitted script on the shipped `/app/session` data and on deterministic held-out sessions generated during grading. The tests compare rendered PPM pixels and parsed JSON structures against an independent reference renderer, while also rejecting missing, empty, or symlinked submitted scripts.
