# AutoformBot agent guidance

User instructions override this file. These rules describe repository-specific
practice; use `CONTRIBUTING.md` for the public contribution process and the
owning skill for product behavior.

## Scope and sources of truth

- Develop the plugin in this repository and test behavior in an independent
  Lean consumer checkout. Keep plugin and formalization roots separate.
- The bundled Cabannes thesis project is an executable compatibility example,
  not a place for product-specific exceptions.
- Markdown under `blueprint/` is the authored roadmap and dependency graph.
  Rendered sites, Mermaid graphs, dashboards, and runtime projections are
  derived views; do not introduce a second durable scheduler or graph.
- Treat current `main` as the product baseline. Experimental replacement PRs do
  not supersede merged servers or workflows until their stated gates pass.

## Branches, forks, and worktrees

- Start new work from the latest `facebookresearch/main` unless the PR is an
  explicitly documented stack.
- Push to `facebookresearch` or your own fork. Never develop on another
  contributor's fork or rewrite their branch.
- Use a separate worktree and branch for each PR. Before editing, inspect its
  status and preserve unrelated or user-owned changes.
- Do not use destructive resets or force pushes to resolve review feedback.
  Restack deliberately and record replaced PRs or branches.
- Keep risky or incomplete work draft. Mark it ready only after exact-head CI,
  an accurate PR description, and proportionate human review.

## Implementation boundaries

- Prefer small changes with a named invariant. Split lifecycle, protocol,
  packaging, and test-only hardening when they can be reviewed independently.
- Follow `pyproject.toml`, Ruff, and neighboring code for Python style (four
  spaces and the configured 120-column limit); generic contribution prose is
  not the executable formatting contract.
- Public CLI and JSON shapes are contracts. Version schema changes, reject
  ambiguous input, escape human output, and keep diagnostics path-safe.
- Lean server operations require an explicit project root, bounded time and
  output, verified descendant cleanup, and no retry after dispatch has an
  unknown outcome. A project root routes work; it is not an OS sandbox.
- Keep live worker/claim information local-only. Loopback services still need
  request-level Host/Origin checks and must not expose secrets or local paths.
- Outward-facing actions—pushing claim refs, publishing Pages, posting messages,
  or changing repository settings—require the authority supplied by the user.

## Templates, mirrors, and immutable pins

- Files under `autoform_cli/templates/` are product templates. When a generated
  workflow, audit helper, ignore rule, or site configuration changes, update its
  bundled-example mirror and the equivalence test in the same PR.
- Pin Actions, Elan, Autoform, and consumer dependencies immutably. Use the
  canonical `https://github.com/facebookresearch/autoform-bot.git` source and a
  full commit SHA, never a branch, tag, abbreviated SHA, or personal fork.
- An immutable Autoform SHA is a compatibility lock, not an update channel. It
  remains reproducible as `main` advances but becomes feature-stale. Bump it
  whenever the example starts relying on newer CLI, schema, template, or skill
  behavior.
- When bumping the example pin, run the workflow command through that exact
  Git URL and SHA—not merely through the current checkout—and confirm the
  example still checks and renders. Update pin assertions with the mirror.

## Validation

- Add the narrow regression first and run focused checks while iterating.
- Before handoff, normally run:

  ```bash
  make lint
  make test
  make check-example
  ```

- Run `lake build` when Lean sources, toolchains, Lake configuration, or the
  example's Lean dependency pins change.
- Validate every edited `SKILL.md` with the skill-creator validator and validate
  edited plugin manifests. Build and inspect the wheel when packaging changes.
- Exercise Python 3.10/3.13, Windows, real Lean, or real REPL paths when the
  change touches their platform boundary. Never dismiss an exact-head failure
  as environmental without reproducing it against the unchanged baseline.
- Report commands and outcomes accurately. Keep known limitations and deferred
  work in issues with concrete acceptance criteria.
