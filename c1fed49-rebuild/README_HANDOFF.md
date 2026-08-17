# dynamo-c1fed49 — salvage/repair rebuild, work in progress

The delivered PR (`nishant4731:submission`, HEAD `6e28a17`) holds
`dynamo/calderwell-review`, which is green on every gate except difficulty. This
folder holds the **replacement concept** started after four heads measured that
task's ceiling. Nothing here is in the git repo, so the PR stays clean.

## Why the rebuild

`dynamo/calderwell-review` is a recover-the-policy-from-a-log task. Measured on
the pipeline: pass@5 **5/5 solved, avg 1.000**; pass@2 solved 2/2 twice more
after two further ratchets. The reference pair solves the whole class in 15–50
minutes because everything it must do is stated (fairness requires stating it)
and everything it produces is checkable before submitting. Full evidence table:
memory `dynamo-reconstruction-mold-hit-its-ceiling`.

## What this rebuild is

`dynamo/chartvault-mend` — a Wardline chart vault that crashed mid-ingest. The
agent writes `/app/chart_mend.py <vault_dir>`, which mends the vault **in place**.
It is the salvage/repair mold (≈15 acceptances in the track record), whose crux
is work that **cannot be checked locally**:

| lever | how it appears |
|---|---|
| digest-driven assembly search | the crash lost receipt rows; those documents must be recovered by backtracking over loose spool fragments against the registry SHA-256 and byte length |
| evidence-mined parameters + decoys | per-station clock offsets, mined by differencing station receipts against trusted gateway anchors; `vault.json` *declares* offsets and is wrong for two stations in every vault |
| mined values decide outcomes | retention/disposal dates are computed from corrected stamps, so a wrong offset silently misfiles or misdisposes whole windows |
| byte-exact naming | case folding, last-dot extension split that must not fire on a leading dot, `~2`/`~3` collision ordinals in `doc_id` order within an encounter |
| exact-integer accounting | 18 counters sampled at distinct decision points, plus a per-document outcome array |
| evidence consumption | `spool/` and `receipts/` are removed once filing is done, so a buggy draft run on the live vault destroys the graded state |

## State: what works

`_vault_engine.py` (reference mender) and `_vault_gen.py` (fixture builder) are
written and validated together across a 10-vault corpus. Measured on the last
run, every trap fires and nothing is degenerate:

```
live-vault     filed=13 held= 0 disposed=19 quar= 2 search= 4 coll= 2 orphan= 6
held-wide      filed=24 held=10 disposed= 8 quar= 2 search= 6 coll= 4 orphan=10
held-old       filed=13 held= 2 disposed=13 quar= 2 search= 4 coll= 0 orphan= 7
sweep-probe    filed=14 held= 5 disposed= 5 quar= 2 search= 3 coll= 1 orphan= 6
   … 10 vaults total; mined station_offsets == true offsets on every one
```

Two contract gaps were found and fixed during that validation: searched
documents must be *anchored* (otherwise they have no instant and always dispose,
making the search pointless), and every station must keep one anchored document
whose receipts survive (otherwise its offset is not mineable).
`VAULT_HANDBOOK_TEMPLATE.md` is the agent-visible contract, written to match the
engine, with `<<REPORT>>` / `<<FILED>>` placeholders the build step fills.

## State: what is left

1. **`_vault_kit.py`** — port from the delivered task's `_desk_kit.py`
   (`/Users/utkarsha/Documents/Project 1/dynamo/c1fed49/task/tests/_desk_kit.py`,
   also copied to `/tmp/keep/kit_reference.py`). Reuse wholesale: `guard_path`,
   privilege drop to 65534, `_seal_tests`, `strict_load`, `type_strict_equal`,
   `run_mutant`, `scan_for_leaks`, the graded-run cache. Change the staging to
   copy a whole vault directory, and collect **the mended tree** (report bytes +
   the `filed/` manifest + proof the spool and receipts are gone) rather than
   three output files. Grade differentially against the reference on pristine
   copies, computed **before** the submitted tool runs.
2. **`test_outputs.py`** — fresh, thin; keep every reusable assertion family from
   the delivered suite.
3. **`_vault_proof.py`** — the fairness proofs this mold needs: each station's
   offset is uniquely determined by its anchors, and no two subsets of the loose
   fragments satisfy one document's (length, digest).
4. Build step: render the handbook example, freeze fixtures under `tests/vaults/`,
   write `reference_pins.json`, copy the engine to `solution/chart_mend.py`.
5. `instruction.md`, `task.toml` (artifacts, taxonomy, explanations), Dockerfile
   `COPY data`.
6. Mutation table (~60 anchors: retention days, the leading-dot rule, the
   collision ordinal, the offset mining, the search pruning, every counter) and
   the full local gate — sweep with build count and no-op control, oracle 1.0 /
   nop 0.0 in-container, plus the attack probes (lookup stub, planted conftest,
   symlink, `/tests` read).

## Gotchas already paid for on this repo

- `[agent].timeout_sec` must be **3600**; declaring 7200 makes pass@2 log a
  `low_timeout` FAIL because it caps the override at 3600.
- Do not narrate the trap: state each rule plainly and never contrast it with the
  naive reading.
- `git` cannot carry an empty directory — `filed/` therefore ships absent and the
  mend creates it.
- The staged vault directory must be chmod 0777 for the privilege-dropped tool to
  delete `spool/` and `receipts/`.
- Cosine passed 4/4 on this repo across same-concept pushes; an in-flight PR head
  is not in the corpus, so no reflexive reskin is needed.
