# dynamo/pack-texture-budget

Fit textures into a fixed GPU memory page by choosing one compression variant
per texture — a multi-constraint exact optimization with coupled global
penalties where the obvious approaches are provably wrong.

## Overview

The agent writes a reusable, self-contained solver `/app/solve.py`, invoked as
`python3 -S /app/solve.py <instance.json> <out.json>` so site-packages are
disabled at grading time. Each instance lists textures, each with several
variants `(cost, loss, tier, residue, upload)`.
Pick exactly one variant per texture so that the chosen sizes sum to
**exactly** `budget`, **exactly** `tier1_count` picks are tier-1, and the
chosen variants preserve legacy streaming-manifest compatibility registers:
the page-table bucket, a rolling manifest checksum whose multiplier depends on
the chosen variant, an adjacent-texture seam bucket, and a second-order
adjacent-window bucket. The objective minimizes effective `loss` and also
penalizes the longest contiguous tier-1 streak, the busiest cyclic upload slot,
and the cumulative in-order spread between the busiest and emptiest upload
slots after every texture assignment. The verifier runs the program on the
visible instance in
`/app/data` **plus several hidden instances**.
The hidden cases vary texture count, variant count, manifest moduli, and upload
period; their numeric ranges keep exact dynamic programming reproducible, but
full DFS or meet-in-the-middle enumeration is intentionally the wrong shape.
The scale case uses a wider upload period, so a solver has to carry a richer
upload-load tuple rather than depending on a fixed three-slot shape; the ramp
case makes transient upload balancing decisive, so optimizing only the final
peak load is not sufficient. The wide case uses flat loss/cost choices across
many textures, so suffix-loss branch-and-bound cannot stop after the first
feasible selection.

The difficulty is a coupling trap: greedy (lowest-loss per texture) misses the
exact constraints, a natural budget/tier DP ignores the path-dependent streak
penalty, and sweeping over max-streak still fails unless the manifest bucket,
rolling manifest checksum, seam/window buckets, and upload-load distribution are
carried through the search. A correct solver needs a joint state such as
`(tier-1 count, filled budget, residue, checksum, current streak, max streak, upload loads)`
with dominance pruning and transition costs for transient upload spread, while
the full-product search space is far too large to brute force. Installed
constraint solvers are not available to the submitted program during
verification because it is run with `python3 -S`.

## Approach (reference solution)

`solution/optimize.py` is the joint-state DP; `solution/solve.sh` installs it as
`/app/solve.py` and solves `/app/data`. `solution/generate.py`
deterministically (seeded) builds every instance — the visible `main` and the
hidden `tight` / `greedytrap` / `scale` / `period5` / `zerohero` / `plateau` / `ramp` / `wide`
cases — each with a known feasible point so an optimum exists. Each
`expected.json` optimum is derived by running the reference DP, not
hand-authored. The hidden set includes a no-tier-1 edge case, a scale
case with an active upload load tuple, and a flat-loss five-slot plateau case
where loss ordering is not enough to prune the exact search, plus a ramp case
where cumulative upload spread dominates the final peak shortcut.
The wide case is intentionally larger (34 textures) and flat-valued to force
state merging rather than feasible-solution search.

## Environment

Single image (`environment/Dockerfile`) from the approved `python:3.13-slim`
base with `pytest` + `pytest-json-ctrf` baked in (pinned); the solver is pure
Python. Only the visible instance (`environment/data/`) is copied to `/app/data`;
`solution/` and `tests/` are never copied into the image.

## Verification

`tests/test_outputs.py` checks `/app/solve.py` is a real file, then (per hidden
case) copies only `instance.json` to a temp dir, runs the program with
`python3 -S`, and
independently recomputes cost/tier-count/residue/checksum/upload-load/loss from
the instance, asserting: one valid variant per texture, cost == budget, tier
count == tier1_count, manifest page-table bucket == residue_target, rolling
manifest checksum == checksum_target, adjacent seam bucket == neighbor_target,
second-order adjacent-window bucket == window_target, and total loss == the
protected optimum — all-or-nothing across cases, exact integer comparison (no
tolerances). Provable shortcuts fail: greedy lands outside the exact
constraints, budget/tier-only DP returns a suboptimal streak pattern, and linear
residue/solver reductions miss the choice-dependent checksum and upload-load
coupling; final-peak-only upload balancing misses the ramp case's transient
spread cost. Ground truth lives only in `tests/`, overlaid at verify time.
