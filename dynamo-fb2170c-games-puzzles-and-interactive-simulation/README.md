# Lantern Labyrinth

This Harbor task asks the agent to infer a deterministic interactive text-game replay engine from labeled Lantern Labyrinth transcripts and implement a reusable Python runner.

The agent receives training transcripts and visible target command tapes under `/app/data`. The required artifacts are `/app/lantern_runner.py` and `/app/visible_results.json`.

Verification pins the visible data, checks the visible output exactly, and runs the submitted runner on protected hidden labyrinths generated inside the verifier.
