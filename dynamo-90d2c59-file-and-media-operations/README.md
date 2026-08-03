# Vault Filter Dynamo Task

This Harbor task asks the agent to implement `/app/filter_vault.py`, a reusable file-search and filtering tool for a corrupted media vault. The tool validates manifest rows, rejects unsafe or corrupt files, applies override and renewal marker evidence, verifies receipt byte-window proofs, applies marker-backed media byte operations, activates bundle promotions, enforces per-profile caps, copies accepted media to canonical paths, and writes exact synchronized evidence views.

The verifier checks the shipped vault output and runs the submitted tool on hidden generated vaults that vary profile caps, override/renewal validity, receipt windows and proofs, chained media opcodes/ranges/retags, post-transform invalid ranges, bundle thresholds and retags, collision names, malformed rows, and symlink path traps. The goal is realistic file/media triage difficulty: multiple disclosed rules interact, and shallow visible-output hardcoding cannot pass.
