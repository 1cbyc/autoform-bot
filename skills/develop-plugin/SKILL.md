---
name: develop-plugin
description: >-
  Develop AutoformBot's CLI, servers, skills, manifests, tests, example, or
  installation for consumer-project defects.
---

# Develop Autoform from consumer nudges

Treat Autoform as an example-based plugin installed in independent Lean
repositories. Use the Cabannes thesis only as an executable consumer.

Inspect the worktree and consumer behavior; name a refactor's invariant.

Distill consumer nudges into owning-skill decision rules and focused acceptance
tests. Preserve reusable insight, not the transcript or one-off choice.

Implement reusable behavior; keep Cabannes-specific facts in its example and
references.

Keep plugin and formalization roots distinct. Keep shared agent entrypoints
concise and link command/schema details as on-demand references.

Bundled workflow SHAs are compatibility locks, not update channels: while
reachable they stay valid as `main` advances but grow feature-stale. When the
example needs newer behavior, update its canonical `facebookresearch` source
and full SHA together, update mirror assertions, and run the example commands
through that exact pin. Never substitute a branch, tag, or personal fork.

Run focused checks, then normally run:

```bash
make lint
make test
make check-example
```

Run `lake build` when example Lean results change. Validate edited skills and
the manifest with skill-creator and plugin-creator. Report outcomes and checks.
Treat rewritten private declaration safety as fail-closed evidence: correlate
the official user name to its lexical declaration by source coordinates.
