You are planning execution for a pipeline-parallel training job with skip connections between residual blocks. The model is split into shards, and each shard can run under one of several candidate execution plans (differing in precision, activation recomputation, and communication strategy). Each plan for a shard has an integer `memory` (device memory it consumes), `comm_units` (collective-communication bucket units it contributes), `route_delta` (router-state contribution), `bandwidth` (peak interconnect bandwidth it requires), `throughput_loss` (throughput penalty, lower is better), and `precision_id` (an integer precision mode identifier).

Read the instance from `/app/data/problem.json`. Its fields:
- `num_shards`, `plans_per_shard`
- `memory_budget` (integer)
- `comm_alignment`, `comm_target_residue`, `route_modulus`, `route_target_residue`, `current_plan_index_modulus`, `current_plan_index_bias` (integers; `current_plan_index_modulus` is positive)
- `priority_plan_index_tiebreak_shards`: a list of shard indices used only for the final tie-break
- `precision_route_multipliers`: a list indexed by `precision_id`
- `peak_penalty`, `cast_penalty`, `adjacent_bandwidth_tier_penalty`, `skip_cast_penalty`, `skip_bandwidth_tier_threshold`, `skip_bandwidth_tier_penalty`, `previous_bandwidth_tier_bias` (integers)
- `skip_connections`: a list of 2-element lists `[[src, dst], ...]`, representing residual skip connections between non-adjacent shards `src` and `dst`. Skip connections may overlap, so more than one earlier source shard can be pending when a later shard is chosen. The same source shard may appear in more than one skip connection; keep that source shard's precision and bandwidth tier pending until its last listed destination, and charge every listed skip connection independently. The list is not a set: if the same `[src, dst]` row appears more than once, each row is charged independently.
- `shards`: a list of `num_shards` objects, each `{"shard_id": i, "plans": [ {"memory", "comm_units", "route_delta", "bandwidth", "throughput_loss", "precision_id"}, ... ]}`. Plans are indexed by their position in this list, starting at 0.
Solve from the actual lists in the input file: do not assume a fixed number of precision modes, a fixed set of `precision_id` values, or a fixed number of plans per shard beyond what that input declares.

Choose exactly one plan for every shard so as to MINIMIZE the total cost, defined as:

    total_cost = (sum of throughput_loss over the chosen plans)
                 + (cast_penalty * count of adjacent shard transitions i -> i+1 with precision_id[i] != precision_id[i+1])
                 + (adjacent_bandwidth_tier_penalty * count of adjacent shard transitions i -> i+1 whose bandwidth tiers differ)
                 + (skip_cast_penalty * count of skip connections [src, dst] with precision_id[src] != precision_id[dst])
                 + (skip_bandwidth_tier_penalty * count of skip connections [src, dst] whose source and destination bandwidth tiers differ)
                 + peak_penalty * (maximum bandwidth over the chosen plans)

subject to all global constraints:
1. the sum of `memory` over the chosen plans is `<= memory_budget`;
2. the sum of `comm_units` over the chosen plans satisfies `sum % comm_alignment == comm_target_residue`.
3. the router state starts at 0 and updates from shard 0 through shard `num_shards - 1` as `state = (state * precision_route_multipliers[current_precision_id] + route_delta + previous_precision_bias + previous_bandwidth_tier_bias * previous_bandwidth_tier + current_plan_index_bias * (current_plan_index % current_plan_index_modulus)) % route_modulus`, where both previous-shard terms are 0 for shard 0, and for later shards `previous_precision_bias` is `previous_precision_id + 1` and `previous_bandwidth_tier` is the bandwidth tier of shard `i-1`; the final state must equal `route_target_residue`.

The single largest `bandwidth` among the chosen plans sets the peak term for the whole job. Each chosen plan has residual transport bandwidth tier 0 when its `bandwidth <= skip_bandwidth_tier_threshold`, and tier 1 otherwise. When adjacent shards `i` and `i+1` (for `i` from `0` to `num_shards - 2`) have different `precision_id` values, a requantization boundary overhead `cast_penalty` is added; when their bandwidth tiers differ, an adjacent staging overhead `adjacent_bandwidth_tier_penalty` is also added. For each listed residual skip connection `[src, dst]`, if `precision_id[src] != precision_id[dst]`, one extra requantization overhead `skip_cast_penalty` is added for that connection; if the source and destination bandwidth tiers differ, one extra staging overhead `skip_bandwidth_tier_penalty` is also added for that connection. Charge each adjacent transition and each skip connection independently, so a transition can incur neither, either, or both relevant overheads, and multiple connections sharing one source each charge separately at their own destinations. An assignment is feasible only if it satisfies all three constraints; the instance is guaranteed to have at least one feasible assignment. Report the minimum achievable `total_cost` over all feasible assignments, and one feasible assignment that achieves it. If multiple feasible assignments achieve the same minimum `total_cost`, choose one whose maximum `bandwidth` is as small as possible among those minimum-cost assignments. If assignments still tie after that peak-bandwidth rule, choose one with the smallest sum of selected plan indices. If assignments still tie, compare the selected plan indices at the shards listed in `priority_plan_index_tiebreak_shards`, in that list order, and choose the assignment with the lexicographically smallest such sequence.

Write the result for `/app/data/problem.json` to `/app/output/plan.json` as a single JSON object with exactly:
- `"min_total_cost"`: an integer, the minimum achievable `total_cost` over all feasible assignments.
- `"assignment"`: a list of `num_shards` integers; element i is the chosen plan index for shard i (the shard at position i in `shards`). It must be feasible and its `total_cost` must equal `min_total_cost`.

Also write `/app/output/plan_solver.py`, a Python 3 script that accepts exactly two command-line arguments: an input problem JSON path and an output JSON path. When run as `python3 /app/output/plan_solver.py INPUT.json OUTPUT.json`, it must solve the problem at `INPUT.json` using the same rules and write the same two-key JSON schema to `OUTPUT.json`.

Output only those two files. All values are integers; do not emit floats, NaN, or infinity.
