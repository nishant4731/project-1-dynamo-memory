# Release Recovery Dynamo Task

This task asks an agent to recover a damaged Git release branch for a small LedgerKit
codebase. The agent starts with `/app/repo` on an operations branch containing recovery
records, stale release refs, a dangling short-object evidence commit, trust-revoked
signed evidence, patch-equivalent duplicates, superseded commits, and rejected incident work.

The intended solution is to reconstruct `recovered/release-2.7` from the recorded release
base and the accepted shiproom decisions, using stable Git patch identity to avoid duplicate
or misleading evidence. The agent also writes `/app/recovery_manifest.json` describing the
branch, source commits, excluded decisions, and final tree.

The verifier checks the manifest schema, recovered branch topology, exact canonical tree,
required patch-id sequence, absence of rejected and superseded patches, and LedgerKit behavior
from an archived copy of the recovered branch.
