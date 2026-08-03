# Vault Filter Dynamo Task

This repository contains a Harbor task for the File and Media Operations category, focused on file search and filtering.

The agent must implement `/app/filter_vault.py`, a reusable Python CLI that validates signed metadata records, applies renewal, suppression, review, bundle, retention, scoring, and filename rules, copies selected payloads, and writes a manifest plus accounting report. The visible fixture lives under `task/environment/data/vault`; hidden verifier fixtures are generated at test time from the same disclosed rules.

Local validation used:

```bash
PYTHONPYCACHEPREFIX=/tmp/dynamo-pycache python3 -m py_compile task/solution/filter_vault.py task/tests/test_outputs.py
git diff --check
bash references/check-base-image.sh task
harbor run -p task --agent oracle
harbor run -p task --agent nop
```
