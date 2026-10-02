---
name: agent-review
description: >-
  Judge an Autoform mathematical roadmap or Lean formalization with explicit,
  evidence-based rubrics. Use for an independent agent audit of source coverage,
  DAG quality, statement faithfulness, proof integrity, axioms, sorries, or
  Mathlib contribution quality; do not use merely to prepare a visualization for
  a human reviewer.
---

# Judge Autoform work as an agent

Select the rubric from the artifact under review.

- For a roadmap or blueprint, read [roadmap quality](references/roadmap-quality.md),
  inspect its declared sources and coverage boundary, and validate the Markdown
  DAG.
- For Lean code, read [faithfulness](references/faithfulness.md),
  [proof integrity](references/proof-integrity.md), [code quality](references/code-quality.md),
  and [Mathlib style](references/mathlib-style.md). Compile the relevant target,
  inspect the proof chain, and compare the complete public statement with the
  original source.
- For a read-back, an auditor's English account of what Lean declarations
  assert, read [read-back faithfulness](references/readback-faithfulness.md).
  Judge it against the cited source passage, without the Lean.

Keep objective evidence separate from judgment. Never claim compilation,
declaration resolution, axiom cleanliness, source coverage, or dependency
correctness without showing how it was checked. If required sources are absent,
return insufficient evidence rather than guessing.

Regenerate skeleton evidence from the exact candidate after its Lean build, and
only in a trusted checkout or an operating-system sandbox: extraction runs Lake
configuration and project metaprograms, which can forge its report. Treat a
stale-build refusal as insufficient evidence; never pair current source with an
older build. Record the skeleton hash as a drift checksum, the evidence hash for
the packet read, and, for a faithfulness verdict, the article review hash. These
are advisory provenance, not reviewer authentication or an approval key.

Report findings first, ordered by severity and tied to files or nodes. Then give
the rubric scores, weighted verdict, commands run, unresolved questions, and a
short remediation list. Do not edit the reviewed work unless the user separately
asks for fixes.

Use the short [Cabannes thesis review case](references/thesis-review-case.md)
when a concrete Lean example helps distinguish faithfulness from integrity.
