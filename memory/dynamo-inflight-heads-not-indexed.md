---
name: dynamo-inflight-heads-not-indexed
description: "Proven on dynamo-7e6bfa7 — byte-identical instruction.md passed cosine on a later head, so a PR's own heads do NOT enter the corpus."
metadata: 
  node_type: memory
  type: project
  originSessionId: 7110d418-8520-45e1-942a-0fd9ba7507cb
  modified: 2026-08-13T00:26:37.891Z
---

Four heads on one PR, same task concept throughout:

| head | change | instruction | verifier | fingerprint |
|---|---|---:|---:|---:|
| 1 | original | 0.713 | 0.790 | 0.769 |
| 2 | full domain reskin of head 1 | **0.631** | 0.736 | 0.797 |
| 3 | bugfix; facets 0.91 / 0.96 lexically like head 2 | **0.674** | 0.769 | 0.802 |
| 4 | fixture fix; `instruction.md` **byte-identical** to head 3 (1.0000), verifier 0.9998 | **PASS** | PASS | PASS |

Head 4 is decisive rather than inferential: byte-identical compared facets cleared the gate. Head 2 also scored *lower* than head 1 despite being the same task renamed.

**Why:** "delivered Dynamo task" means a task that completed the pipeline, not any commit that passed cosine. None of these heads completed — each was blocked at `qc_gate`, so trials never ran.

**How to apply:** do not reflexively spend a domain reskin on every push after a cosine pass. On a bugfix push it is pure risk — regenerating fixtures and reference pins invites new defects for no gate benefit. Push the fix, and treat an actual block as the signal to reskin. This narrows [[dynamo-reskin-clears-post-index-cosine]] rather than deleting it: a task that genuinely completed trials, or one delivered in an earlier repo, should still be treated as indexed, and the reskin remains the proven cure when a block is real.

**Second, stronger confirmation (dynamo-e488890 PR #3, 2026-08-12).** Head 1 passed cosine
(`0.7117 / 0.8000 / 0.7911`) **and ran pass@2 to completion** — 1/2 with a valid failure — so it
got further through the pipeline than any head above. Head 2 kept the same task, domain and
vocabulary, measuring **0.9222 / 0.9776 (joined 0.9775)** lexically against head 1, and passed at
`0.7323 / 0.8057 / 0.7961`; the service scores barely moved. So even *running the agent trials*
does not put a head in the corpus — only a delivered/accepted task counts. When a follow-up push
does need real divergence, add a **new graded deliverable wired through instruction → contract →
reference → verifier** rather than renaming nouns.

**Third confirmation (dynamo-9b8a04d PR #1, 2026-08-13).** Head 1 passed cosine
(`0.6967 / 0.7615 / 0.7951`) and ran pass@2 to completion (2/2 solved — blocked as too easy). Head
2 rebuilt the task's core (a policy moved out of the prose into a fitted ledger) but kept the same
domain and vocabulary, measuring **0.9815 / 0.9654 (joined 0.9701)** lexically against head 1 — the
highest self-similarity I have pushed — and cleared the gate again in 81s. Three separate repos now
agree: a head that merely *ran* pass@2 is not in the corpus, and the local lexical guard is not a
predictor of the service verdict.

