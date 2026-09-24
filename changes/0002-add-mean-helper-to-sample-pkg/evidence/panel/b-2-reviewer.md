## Verdict
Decide `Sequence[float]`.

## Why
- Intent's Constraints are explicit and binding: "Keep it minimal: one function, no weights,
  no options." spec.md's own Design section already applies this reasoning to this exact
  choice: `Iterable[float]` "requires materialising it (e.g. into a `list`) before both
  `sum()` and `len()` can run" — extra code the minimal constraint argues against — while
  `Sequence[float]` "needs no such step." No loaded policy skill overrides this; the intent
  constraint is the rule that settles it.
- coding-standards rule 2 ("match the surrounding code... a new style is a decision for the
  owner, not a side effect of a change") cuts the same way: `add`, `divide`, `percent` in
  `sample_pkg/calc.py` take plain scalar arguments with no existing precedent for accepting
  a lazy iterable; widening the accepted type is a scope decision, not something to default
  into.
- No caller exists yet (plan.md Risks: "nothing today calls `mean`, so no existing caller is
  at risk either way"), so there is no present need `Iterable` would serve — permissiveness
  has no consumer to justify it against the minimal constraint.
- This is a design judgment call, not a bug/security/compliance breach under REVIEW.md's
  "What Important means here," so it does not block on its own; but where a rule (intent's
  minimal constraint) does speak to it, the review follows the rule over either option's
  taste appeal. `mean(values: Sequence[float]) -> float` is what plan.md should name.
