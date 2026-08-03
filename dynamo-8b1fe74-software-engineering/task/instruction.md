A damaged Git repository is at `/app/repo`. A release branch for LedgerKit 2.7 was force-pushed during incident cleanup, and the current `release/2.7` ref is not authoritative. The recovery console files under `/app/repo/.release/`, `/app/repo/release/`, and `/app/repo/ci/` are the source of truth for deciding which release evidence is authoritative. In particular, `/app/repo/.release/trust-overrides.tsv` records cutoff-bounded trust state transitions that can revoke or restore otherwise signed evidence; the decision-signature, authority-event, and authority-witness-limit ledgers determine whether the release has a globally valid scoped authorization proof; and the release plan is itself a cutoff-reduced revision ledger. `/app/repo/.release/conflict-contracts.md` is an authoritative checklist for the recovered behavior of overlapping release-material rows; use it instead of spending time dumping every topic branch body once source commits and patch ids are recorded.

Recreate the release branch named by `recovered_branch` in `/app/repo/.release/branch-map.txt`. The recovered branch must start at the `release_base` commit from that file, must contain one auditable commit for each row classified as release material by `/app/repo/.release/recovery-rules.md`, and must derive commit order from `/app/repo/.release/release-plan.tsv` using the scheduler defined by the recovery rules and `/app/repo/release/release-2.7.md`. Some evidence refs may be short object ids left behind in the object database rather than branch or tag names; they are still authoritative if they resolve to a commit. Each recovered commit must preserve the source commit's author and committer names, emails, and timestamps exactly, even when the recovered patch is manually resolved, and its net diff must reconstruct that issue's own source evidence rather than deferring the issue's behavior into another recovered commit. Each commit subject on the recovered branch must start with `[<ISSUE_ID>]` (e.g. `[LX-1855] ...`) and each commit body must include exact `Source-Commit: <full source commit>`, `Evidence-Ref: <decision-log evidence_ref>`, `Patch-ID: <stable patch-id>`, `Decision-Row: <1-based decision-log data row, excluding the header>`, and `Release-Sequence: <two-digit ordinal>/8` trailers; approved manual-waiver commits must also include `Waiver-State: approved`. Rows classified as superseded or rejected must have no net effect. When release-material evidence overlaps, implement the combined behaviors in `/app/repo/.release/conflict-contracts.md` and the release order note. The branch must not contain 2.8-only files or schema probes, and `/app/repo` must be left with a clean working tree: no untracked helper scripts, caches, or generated debris. Stable Git patch identity is the authority for duplicate evidence.

Leave the recovered branch in `/app/repo` and write `/app/recovery_manifest.json`. The manifest schema is normative:

```
{
  "recovered_branch": "branch name",
  "base_commit": "40 hex commit id",
  "final_commit": "40 hex commit id at recovered_branch",
  "final_tree": "40 hex tree id at recovered_branch",
  "included": [
    {
      "issue": "issue id from a release-material row",
      "commit": "40 hex source evidence commit id",
      "patch_id": "stable git patch-id for that source commit",
      "rationale": "short reason",
      "authority_witnesses": [
        {
          "capability": "required gate capability",
          "signature_id": "selected decision-signature id",
          "signer": "selected distinct signer",
          "delegation_path": ["ordered root-to-signer delegation ids"]
        }
      ]
    }
  ],
  "excluded": [
    {
      "issue": "issue id from an audit-reportable rejected or superseded row",
      "commit": "40 hex source evidence commit id",
      "decision": "reject or superseded",
      "patch_id": "stable git patch-id for that source commit",
      "rationale": "short reason"
    }
  ]
}
```

The `included` array must contain exactly the release-material rows in release order, including each row's canonical authorization witness assignment defined by the recovery rules. The `excluded` array must contain at least the audit-reportable rejected or superseded rows named by the recovery rules, with `decision` set to `reject` or `superseded`; other rejected rows still must have no net effect on the recovered branch but need not be listed in the manifest. All commit ids in the manifest must be full 40-character object names, and the manifest's final commit and tree must match the recovered branch.
