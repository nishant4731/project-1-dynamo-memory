Tune `/app/data/scene.json` for a deterministic 16-bit microcore. Produce exactly `/app/out/plan.json`, `/app/out/run_report.json`, and `/app/out/solver.py`.

The scene has `mem_size`, `max_steps`, `window`, optional `peak_bonus` (default 0), optional `store_latency` (default 0), optional `mod` (default 1000003), `place_exactly`, and `banks`. Each bank has integer `id`, optional `init_mem` (`[addr, value]` pairs), `program` (`[op, arg]` instructions), and `slots`. Each slot has `id`, `at` (program index), and `choices` (`[op, arg]` fillers). All arithmetic is modulo 65536.

Each bank runs on a fresh core: `acc`, `idx`, `R0..R3`, and cycle counter start at 0; `Z` starts set; `pc` starts at 0; `mem` is `mem_size` zero words, then each `init_mem` pair sets `mem[addr % mem_size] = value & 0xFFFF`. Execute until `HLT`, `pc` leaves `[0, len(program))`, or `max_steps` instructions execute; that core state is final. Before each instruction record load `base_load * (1 + (acc & 7))` using pre-instruction `acc`, then apply the instruction.

Opcodes — `effect` | `cycles` | `base_load`:
- `LDI k`: `acc = k & 0xFFFF` | 1 | 2
- `ADI k`: `acc = (acc + k) & 0xFFFF` | 1 | 3
- `XOR k`: `acc = (acc ^ k) & 0xFFFF` | 1 | 2
- `MUL k`: `acc = (acc * k) & 0xFFFF` | 3 | 6
- `ROL k`: rotate `acc` left by `k & 15` bits (no change if 0) | 1 | 2
- `LD r`: `acc = R[r & 3]` | 1 | 2
- `ST r`: `R[r & 3] = acc` | 1 | 2
- `LDM`: `acc = mem[idx % mem_size]` | 2 | 4
- `STM`: `mem[idx % mem_size] = acc` | 2 | 4
- `INX k`: `idx = (idx + k) & 0xFFFF` | 1 | 2
- `BNZ t`: if `Z` is clear, set `pc = t` (this costs 2 cycles); otherwise fall through (1 cycle) | see effect | 3
- `HLT`: stop | 1 | 1

Every non-branch instruction advances `pc` by 1. `Z` is updated to `(acc == 0)` only by `LDI`, `ADI`, `XOR`, `MUL`, `ROL`, and `LD`. `LDM` writes `acc` but does not change `Z`; `ST`, `STM`, `INX`, `BNZ`, and `HLT` never change `Z`.

Memory writes pass through a store buffer. `STM` captures address (`idx % mem_size`) and value (`acc`) when it executes, but the write becomes visible only more than `store_latency` executed instructions later: `LDM` sees an earlier `STM` only if at least `store_latency + 1` executed instructions separate them (`store_latency = 0` means visible to every later instruction). `LDM` never forwards from the buffer; it reads committed memory and can read stale data. Buffered writes commit in issue order; any still in flight when the bank stops are then flushed in issue order.

For a completed bank run, `peak` is the largest sum of `load` over any `window` consecutive executed instructions in execution order (if fewer than `window` instructions executed, the sum of them all). Its `raw` value is `31*acc + 37*idx + sum((a+1)*mem[a] for a in range(mem_size)) + sum((r+7)*R[r] for r in range(4))`, its `checksum` is `raw % mod`, `live_words` is the count of nonzero `mem` words, and `cycles` is the final cycle counter.

A configuration turns each slot either off (the bank keeps `program[at]` unchanged) or on (replace `program[at]` with one entry from that slot's `choices`). Exactly `place_exactly` slots across all banks must be on. Banks are independent. For a configuration, `live = sum of per-bank live_words`, `checksum = (sum of per-bank raw) % mod`, `peak = max of per-bank peak`, and `cycles = sum of per-bank cycles`. Maximize `score = 1000003*live + checksum + peak_bonus*peak` (the `1000003` multiplier is fixed regardless of `mod`). Break ties by the lexicographically smallest `picks` list (defined below).

Your reusable solver must handle larger conforming scenes than `/app/data/scene.json`: hidden grading may include tens of banks and hundreds of billions or more global configurations. Naive product enumeration is not sufficient; `solve(scene_path, output_dir)` must still return the exact optimum within about 45 seconds on those scale scenes.

Write `/app/out/plan.json` as `{"picks": [{"arg": int, "bank": int, "op": str, "slot": int}], "score": int}`, where `picks` lists the on slots (bank `id`, slot `id`, and the chosen `op`/`arg`) sorted ascending by `(bank, slot)`; tie-breaking compares `picks` lists element-wise by `(bank, slot, op, arg)`.

Write `/app/out/run_report.json` for the chosen optimal configuration as `{"checksum": int, "cycles": int, "live_words": int, "peak": int, "per_bank": [{"acc": int, "bank": int, "checksum": int, "cycles": int, "halted": bool, "idx": int, "live_words": int, "peak": int}]}`, where `per_bank` is sorted ascending by `bank`, `halted` is true iff that bank's run stopped on `HLT`, and `acc`/`idx` are that bank's final values.

Also write `/app/out/solver.py`, an import-safe module exposing `solve(scene_path, output_dir)` that loads `scene_path`, applies these rules, and writes `plan.json` and `run_report.json` into `output_dir` for any conforming scene.
