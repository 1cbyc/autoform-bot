# AutoformBot agent guidance

User instructions override this file. Use [CONTRIBUTING.md](CONTRIBUTING.md) for
setup, checks, style, and contributions. Use the
[development skill](skills/develop-plugin/SKILL.md) for product behavior and
consumer-example contracts.

## Repository work

- Treat current `main` as the product baseline; unmerged experiments do not
  supersede it.
- Start independent work from the latest `facebookresearch/main`; document the
  base when a pull request is intentionally stacked.
- Use a separate worktree and branch for each pull request. Inspect its status
  first and preserve unrelated or user-owned changes.
- Push only to `facebookresearch` or your own fork. Never develop on or rewrite
  another contributor's branch.
- Do not resolve feedback with destructive resets or force pushes. Restack
  deliberately and record replaced pull requests or branches.
- Keep risky or incomplete work draft. Before requesting review, make the pull
  request description match its exact head and run proportionate validation.
