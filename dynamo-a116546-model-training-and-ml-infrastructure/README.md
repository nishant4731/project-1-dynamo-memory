# Resume Sweep Scheduler Task

This Harbor task asks an agent to reconstruct the restart plan for a crashed hyperparameter sweep and leave behind a reusable scheduler-rebuild CLI. The visible environment data under `task/environment/data/` contains scheduler policy, trial lineage, candidate configurations, and noisy metric telemetry with corrections and retractions.

The oracle in `task/solution/solve.py` canonicalizes metrics at the policy cutoff, scores checkpoints with validation loss plus overfit and cost penalties, applies successive-halving promotion rules, filters already-promoted lineages, and performs exact diversity-aware set selection for fresh candidate configurations.

Verification reads `/app/resume_plan.json` and executes `/app/rebuild_scheduler.py` on verifier-only fixtures. The pytest suite checks the schema, incumbent checkpoint, promotion order, stop list, fresh-trial selection, and generalization across hidden scheduler telemetry. Expected answers live only in `task/tests/`, which Harbor overlays at verify time.
