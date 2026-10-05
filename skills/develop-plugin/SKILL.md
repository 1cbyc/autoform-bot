---
name: develop-plugin
description: >-
  Develop AutoformBot's CLI, servers, skills, manifests, tests, example, or
  installation for consumer-project defects.
---

# Develop Autoform from consumer nudges

Treat Autoform as an example-based plugin installed in an independent formalization
repository. Use Cabannes as its executable consumer; keep Cabannes-specific
facts in the example and references, never product code.

Treat user nudges as product evidence. Distill rules and tests
so future agents need less steering; preserve insight, not the transcript.

Keep plugin and formalization roots distinct. Agents can infer routine details;
keep shared agent entrypoints concise and link on-demand references. State a consumer
scenario and invariant.

Bundled workflow SHAs are compatibility locks, not update channels: while
reachable they stay valid as `main` advances but grow feature-stale. When the
example needs newer behavior, update its canonical `facebookresearch` source
and full SHA together, update mirror assertions, and run the example commands
through that exact pin. Never substitute a branch, tag, or personal fork.

Run checks, then:

```bash
make lint
make test
make check-example
```

Run `lake build` when example Lean results change. Validate edited skills and
the manifest with skill-creator and plugin-creator. Use cachebuster and
reinstall only to test installed discovery in a new thread. Report outcomes.
Treat rewritten private declaration safety as fail-closed evidence: correlate
the official user name to its lexical declaration by source coordinates.
