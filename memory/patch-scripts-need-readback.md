---
name: patch-scripts-need-readback
description: "A multi-edit patch script that asserts mid-way writes nothing — verify spec/doc edits by reading back, not by trusting the assert."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e19fae0e-682c-4934-9e95-c982d525ac98
  modified: 2026-08-12T07:59:36.083Z
---

When patching a spec or contract with a Python script that does several `assert old in s; s = s.replace(...)` steps and one `open(p,"w").write(s)` at the end, a failed assertion on a *later* hunk discards every earlier edit silently. On dynamo-9df6709 this dropped the rewrite of the normative ordering rule *and* a new totals field, so the charter told the reader one rule while the verifier graded another — caught a full CI cycle later by `structured_data_schema`.

**Why:** the script prints nothing on the hunks that did apply, and the exception looks like "that one hunk didn't match", not "nothing was saved".

**How to apply:** write each hunk in its own call, or write the file before asserting the next hunk. Then verify mechanically rather than by eye: parse the spec's schema blocks and compare them member-for-member against what the oracle actually emits, and assert the emitted table header appears verbatim in the spec. Fold that comparison into the graded suite so drift cannot come back — see [[dynamo-reskin-doc-drift]].
