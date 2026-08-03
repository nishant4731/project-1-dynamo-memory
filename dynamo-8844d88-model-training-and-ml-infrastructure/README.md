# Revisioned Hyperband Promotion Planner

This Harbor task asks the agent to finish a Python promotion planner for an asynchronous Hyperband-style tuning ledger. The planner must reconstruct the current state of trial metrics from revisioned event logs, discard stopped or incomplete trials, rank candidates with a risk-adjusted validation-loss score, solve a compute-budget-constrained survivor selection, and emit a deterministic next-budget allocation plan.

The visible task data is in `task/environment/data/visible_ledger.json`. The verifier executes `/app/tuner.py` on the visible ledger and on protected hidden ledgers with the same schema, so hardcoded visible answers and shortcut rankers fail.

Verification is programmatic through `task/tests/test_outputs.py`. It checks artifact integrity, JSON schema, visible output correctness, hidden cases with stale revisions and checkpoint traps, and a larger deterministic ledger that catches greedy top-k, local-only, and brute-force combination assumptions.
