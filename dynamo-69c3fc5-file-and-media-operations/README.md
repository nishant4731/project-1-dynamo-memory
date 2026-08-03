# Splice Restore

This Harbor task asks the agent to implement `/app/restore_masters.py`, a reusable audio-session restoration program. The program reads session ledgers, decodes binary PCM splice fragments, applies recall/cutoff authority rules, discards trim-exhausted winners, infers a non-linear asymmetric crossfade convention from visible calibration examples, applies fragment gain plus a final master gain, restores mono WAV masters, and emits a JSON repair manifest with stage-specific accounting.

The task lives entirely under `task/`. The agent-visible fixture is in `task/environment/data/session_bank` and is structurally milder than the hidden banks. Hidden verification cases are generated deterministically at test time. The verifier executes the submitted program on those hidden banks, compares exact PCM bytes for every WAV, and checks the full manifest schema and accounting fields.

Local checks:

```bash
git diff --check
PYTHONPYCACHEPREFIX=/tmp/dynamo69_pycache python3 -m py_compile task/solution/solve.py task/solution/restore_masters.py task/tests/audio_cases.py task/tests/test_outputs.py
bash references/check-base-image.sh task
harbor run -p task --agent oracle
harbor run -p task --agent nop
```
