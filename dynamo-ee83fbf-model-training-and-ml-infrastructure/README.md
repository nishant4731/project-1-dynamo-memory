# LoRA Replay Dynamo Task

This repository contains a single Harbor task in `task/`. The task asks an agent to implement a reusable deterministic LoRA fine-tuning replay utility for a tiny classifier bundle.

The agent must produce `/app/replay_lora.py`, run it on the visible bundle in `/app/data`, and leave `/app/final_adapter.json`, `/app/training_report.json`, `/app/influence_report.json`, and `/app/replay_audit.json`. The utility must also generalize to any bundle with the same schema.

Difficulty combines point-in-time corrected records, bitemporal policy revisions, freeze-membership Adam moment scrubbing, scheduled Adam LR decay shared by the Adam step and decoupled weight decay, exact optimizer/clip/tail behavior, and a counterfactual influence audit with upper-triangular pairwise skips plus exact Shapley subset valuation.

Verification recomputes expected adapters, audits, and influence reports from the task contract and runs the submitted utility on hidden fixtures that exercise correction handling, scheduled policy changes, LR decay, freeze transitions, sparse features, clipping, tail accumulation, leave-one-out replay, pairwise interactions, and subset Shapley values.
