Create `/app/orbit_solver.py`. It must be a Python 3 program that reads one JSON instance from standard input and writes exactly one JSON object to standard output.

The instance describes a rooted tree whose nodes are numbered `0` through `n - 1`. The field `parents` has length `n`; exactly one entry is `-1`, marking the root, and every other entry is the parent node id. Parent ids are not guaranteed to appear before their children. The field `options` has length `n`; `options[i]` is a nonempty list of choices for node `i`. Each choice has integer fields `cost`, `residue`, `residue2`, `residue3`, and `load`. The field `residue` is interpreted modulo `modulus`; `residue2` is interpreted modulo `modulus2`; `residue3` is interpreted modulo `modulus3`.

A feasible plan chooses exactly one option index for every node. Its primary residue is the sum of the chosen `residue` values modulo `modulus`. Its secondary residue is the sum of the chosen `residue2` values modulo `modulus2`. Its tertiary residue is the sum of the chosen `residue3` values modulo `modulus3`. Its base cost is the sum of chosen costs. For each root-to-leaf path, compute the sum of chosen loads on that path; `peak_load` is the maximum of those path sums and `valley_load` is the minimum of those path sums. The plan score is:

`base_cost + peak_weight * peak_load + spread_weight * (peak_load - valley_load)`

Find a feasible plan whose primary residue equals `target`, whose secondary residue equals `target2`, and whose tertiary residue equals `target3`, with all targets compared modulo their corresponding modulus, and whose score is minimum. Instances are guaranteed to have at least one feasible plan. Hidden instances may have up to 14 nodes, up to 4 options per node, and moduli as large as 13, 11, and 7, so exhaustive enumeration of option assignments is not viable.

Your program's output object must contain exactly these keys:

`minimum_score`: the minimum score as an integer.
`peak_load`: the peak load of your reported plan as an integer.
`valley_load`: the valley load of your reported plan as an integer.
`residue`: the residue of your reported plan as an integer from `0` to `modulus - 1`.
`residue2`: the secondary residue of your reported plan as an integer from `0` to `modulus2 - 1`.
`residue3`: the tertiary residue of your reported plan as an integer from `0` to `modulus3 - 1`.
`choices`: a list of `n` integers where `choices[i]` is the selected option index for node `i`.

The sample file `/app/data/public_cases.json` contains small public instances and one optimum output for each, using this same input and output schema.
