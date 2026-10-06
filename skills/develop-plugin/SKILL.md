---
name: develop-plugin
description: Maintain AutoformBot's code, skills, tests, examples, and installation.
---

# Develop Autoform

Treat Autoform as an example-based plugin for an independent formalization
repository. Turn user nudges into product evidence: state a consumer
scenario/invariant and test insight, not the transcript, so
future agents need less steering.

Keep plugin and formalization roots distinct; keep Cabannes-specific facts in
examples. Agents can infer routine details; keep shared agent entrypoints concise
with on-demand references.

Per release, regenerate `production_module_roots` from Lake package configs.
Update private creation bundle, catalog identity, and complete `lake update` manifest
together; run `lake build`. A direct-Mathlib-only manifest is invalid.

Because repeated pathname reads are not a generation boundary, retain
descriptors. Read bounded outputs first; keep each marker schema in its owning
feature and require links to match the blob at the stable detected commit.

Workflow SHAs are compatibility locks, not update channels: they stay valid as
`main` advances but grow feature-stale. Updates use the canonical
`facebookresearch` source and full SHA together, update mirrors, and run the
example commands through that exact pin, never a branch, tag, or personal fork.

Normally run:

```bash
make lint
make test
make check-example
```

Validate skills/manifests with skill-creator/plugin-creator. Test
cachebuster/reinstall discovery only in a new thread.

Treat rewritten private declaration safety as fail-closed evidence: correlate
the official user name lexically by source coordinates.
