# Read-back faithfulness rubric

Judge whether a read-back asserts what the source passage asserts. Both sides
are English. You never see Lean, and that is the point: a judge shown code can
read a suggestive identifier as a promise, and every rubric that shows code has
to warn against it. Here there is nothing to pattern-match on.

This rubric is the other half of [faithfulness](faithfulness.md). That one
asks whether the Lean says what the source says. This one asks whether the
read-back, which an auditor wrote from the Lean alone, says what the source
says. A discrepancy here means either the formalization drifted or the auditor
misread it, and the reviewer decides which.

## Evidence

You receive exactly two things, and nothing else may be consulted.

1. **The source passage**, verbatim, at the locator the article cites.
   `autoform skeleton --packets DIR --passages DIR` writes it.
2. **The read-back**: a rendering in mathematical English of what one or more
   Lean declarations *literally assert*, written by an auditor who was shown
   only their blind packets, never the article, the source, or any statement
   of intent.

Do not open any other file, and do not search for any name. If the read-back
covers several declarations, judge them together against the passage: a source
theorem is often an existence half and a uniqueness half, and each alone is
honestly incomplete.

Read the read-back as raw text, exactly as the auditor wrote it, never as
rendered output. A renderer shows what the text asks it to show, and a
read-back can ask it to hide part of what it says.

## The read-back says more, on purpose

A read-back is deliberately pedantic. It accounts for every binder, names
typeclass assumptions, and surfaces degenerate cases the passage never
discusses: what a definition means on the empty set, what a total function
returns on junk input, whether a hypothesis silently forces nonemptiness.

**None of that is a discrepancy.** The passage is prose for a human who
supplies context; the read-back is a transcript of what a machine was told.
Extra precision about the *same* claim is `elaboration`, and it is not
penalized. Only a difference in what is *claimed* counts.

## Procedure

Work in three steps and show each.

1. **Card the passage.** Its objects with their kinds, its hypotheses
   numbered, its conclusion, its quantifier structure. Mark a hypothesis
   *implicit* when the passage uses it without stating it.
2. **Card the read-back** the same way, from its prose alone.
3. **List discrepancies**, each with one category below and one line of
   detail, then read the decision off the list. Never adjust it by impression.

## Discrepancy vocabulary

| Category | Meaning |
|---|---|
| `elaboration` | The read-back is more precise about the same claim: a degenerate case, a convention, a binder the passage leaves implicit. Not penalized. |
| `hypothesis-missing` | A hypothesis the passage states has no counterpart, and the conclusion needs it. |
| `hypothesis-missing: generalizes` | A hypothesis has no counterpart, yet every instance of the passage's setting is an instance of the read-back's. Say why in the detail line. |
| `hypothesis-added` | The read-back assumes something the passage proves or constructs. |
| `conclusion-weaker` / `conclusion-stronger` / `conclusion-different` | The conclusion says less, more, or something else. Existence in place of unique existence is `conclusion-weaker`. |
| `quantifier` | Order, strength, or dependence of a quantifier changed. |
| `strictness` | Strict against non-strict, open against closed, positive against nonnegative. |
| `domain` | Type, domain, finiteness, or locality changed. |
| `object-substituted` | A passage object is replaced by a proxy the read-back does not connect to it. |
| `scope` | The read-back covers part of what the passage claims and is silent on the rest. Say which parts are covered. |
| `vacuous` | The read-back says the hypotheses cannot all hold, or that the claim holds trivially. |
| `unreadable` | The read-back does not state a mathematical claim you can card, or hides part of what it says from whoever reads it rendered. |
| `none` | The cards agree. |

## Decision

Three outcomes, bound to the list. A read-back takes the worst outcome any of
its discrepancies binds it to.

| Decision | Bound to |
|---|---|
| `agrees` | Only `none`, `elaboration`, or `hypothesis-missing: generalizes`. |
| `review` | A difference you believe is only apparent — a cleared denominator, an equivalent reformulation, a coercion. State the equivalence in words; see below. A belief you cannot state is not `review`. |
| `disagrees` | Any `hypothesis-missing`, `hypothesis-added`, plain `conclusion-*`, `quantifier`, `strictness`, `domain`, `object-substituted`, `scope`, `vacuous`, or `unreadable`. |

Return `unknown` instead when the passage is missing or the two cannot be
aligned at all.

Where a report asks for rubric scores, `agrees` passes, `disagrees` rejects,
and `review` is left to a human, like a 3 in [faithfulness](faithfulness.md).

Anti-inflation guard: if your own detail lines say "meaningful",
"significant", "roughly", or "not formally established", the decision is
`disagrees`.

## Settling a `review`

`review` is the one decision you may not make alone, because you cannot see the
Lean and so cannot check what you are claiming. You do not know which
declarations the read-back covers either, and must not try to find out. State
the equivalence in words, against the item, and hand it on to someone who can
see the Lean. They settle it, for example by proving the equivalence in Lean,
or reject it.

Most `scope` findings need no such escalation and must not receive one. When a
read-back honestly covers less than the passage it cites, the remedy is at the
article — cite the part formalized, or formalize the rest.

## Output

One block per item, in this order, nothing else:

```text
item: <id>
passage card:
  objects: …
  hypotheses: 1. … 2. … (implicit: …)
  conclusion: …
read-back card:
  objects: …
  hypotheses: 1. … 2. …
  conclusion: …
discrepancies:
  - <category> — <one line>
equivalence to settle: <the equivalence, in words | none>
decision: <agrees | review | disagrees | unknown>
verdict: <one sentence, naming the binding discrepancy or "cards agree">
```

## Traps

- **Extra precision is not disagreement.** A read-back that explains what a
  definition means on the empty set, where the passage says nothing, is doing
  its job. Card the claim, not the word count.
- **Silence is not agreement.** If the passage claims two things and the
  read-back addresses one, that is `scope`, however well it treats the first.
- **Existence for uniqueness, local for global, weak for strict.** These are
  the quiet weakenings. Check each connective, not the shape of the sentence.
- **A read-back that reports a vacuous statement is telling you something.**
  Record `vacuous` and let the reviewer decide; do not rescue it.
- **You cannot see the Lean, so do not guess at it.** Judge the English in
  front of you. If the read-back is ambiguous, that ambiguity is the finding.
- **What does not show is not said.** A zero-width, control, or
  bidirectional-override character, or a TeX construct that hides what it
  wraps — `\phantom`, `\hphantom`, `\vphantom`, or a colour or style that makes
  text vanish — means the rendered read-back differs from the text you were
  given. Record `unreadable`, quote the construct, and do not card around it:
  a human reads the rendered version, not yours.
- **A wide locator is the article's fault, not the auditor's.** When the
  passage cites a whole section and the read-back renders one theorem from it,
  record `scope` against the article and say so; the auditor never saw the
  locator.
