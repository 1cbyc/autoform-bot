# AutoformBot

A plugin for Claude Code and Codex that helps turn mathematical papers and
notes into Lean 4 formalizations: plan the work, write proofs, and review
progress from your coding assistant.

## Installation

Requires Python 3.10+, [`uv`](https://docs.astral.sh/uv/), Git, and Lean 4
with Lake.

**Claude Code**

```bash
claude plugin marketplace add facebookresearch/autoform-bot
claude plugin install autoform@autoform
```

**Codex**

```bash
codex plugin marketplace add facebookresearch/autoform-bot --ref main
codex plugin add autoform@autoform
```

After installing, start a new session in your Lean project.

## Usage

Run these commands in your Claude Code or Codex conversation:

| Task | Claude Code | Codex |
| --- | --- | --- |
| Set up the project | `/autoform:setup` | `$setup` |
| Plan from a paper or notes | `/autoform:roadmap` | `$roadmap` |
| Write Lean definitions and proofs | `/autoform:formalize` | `$formalize` |
| Review the roadmap and progress | `/autoform:human-review` | `$human-review` |
| Request an independent AI review | `/autoform:agent-review` | `$agent-review` |

Start with `setup`, then use `roadmap` to plan your formalization and
`formalize` to work through it. Use either review command to inspect the plan
or the resulting formalization.

For example, invoke `roadmap` and ask:

> Build a complete roadmap for Sections 2–4 of `paper.pdf`.

Keep the source file in your project or provide an accessible path.

## License

[MIT](LICENSE).
