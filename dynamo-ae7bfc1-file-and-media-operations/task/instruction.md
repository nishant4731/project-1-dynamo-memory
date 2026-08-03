Create executable `/app/filter_vault.py`; it must accept a vault directory and an output directory as its two arguments.

Use `/app/vault/FORMAT.md` as the exact contract for parsing records, marker side effects, ranking, filename normalization, copying, and every exported artifact. Follow its canonical JSON/JSONL byte format and review-point cap rule exactly. Infer the vault-specific scoring profile from `/app/vault/score_calibration.tsv`; verifier-built vaults use the same profile family but different calibration evidence.

Before finishing, run the program for `/app/vault` and populate `/app/filtered` with `manifest.jsonl`, `audit.tsv`, `report.json`, `receipt.json`, and the selected payload tree below `files/`.
