---
name: dynamo-operational-passat-failures
description: pass@ can clear on failures that never touch the crux — read difficulty_crux, and don't redraw an all-green head to fix the taxonomy.
metadata:
  type: feedback
---

On `dynamo-0a072a0` every failing trial across two heads (2 pass@2 + 4 pass@5)
died the same way: the agent wrote its ~500-line program in one
`cat > file << 'EOF'` heredoc, the terminal's output-truncation limit swallowed
the closing delimiter, and the shell sat in PS2 for ~140 further steps. The
platform counted them as **good valid fails**, pass@5 read 1/5 with avg@5 0.200,
and the final gate passed — while `difficulty_crux` was FAIL on every one of
them. The single solving trial wrote the file incrementally over ~50 appends.

**Why:** the gate's taxonomy (valid fail vs timeout vs infra) is coarser than the
per-trial rubric. A task can clear the difficulty bar on evidence that says
nothing about its reasoning, and a human reviewer reading the trajectory panel
may see that.

**How to apply:** read the per-trial rubric and Fail Reasons, not the headline
fraction, and say so plainly when reporting. But do **not** push a corrective
commit onto a cosine-green, all-green head just to improve the failure taxonomy:
the redraw can land in the 3–5/5 reject band, and every push after a cosine PASS
needs its own fresh identity reskin. The lever that would help — a smaller
required program — is the same lever that lowers difficulty.

Related: [[dynamo-pass2-typo-is-not-difficulty]], [[dynamo-cosine-change-the-question]].
