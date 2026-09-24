## Verdict
Decided: empty sequence raises `ZeroDivisionError` via `divide(sum(values), len(values))` — no special-casing.

## Why
- coding-standards rule 2 (`framework/plugin/skills/coding-standards/SKILL.md`): "Match the
  surrounding code: naming, layout, error handling, the language's idioms. A new style is a
  decision for the owner, not a side effect of a change." `sample_pkg/calc.py` already has a
  precedent: `divide` raises `ZeroDivisionError` on a zero divisor, and `percent` inherits
  that behaviour unchanged (`percent(part, whole)` -> `divide(part * 100, whole)`). Picking
  `ValueError` or `0.0` for `mean` would be a new error-handling style the owner hasn't
  asked for — rule 2 says that's not this design pass's call to make on its own.
- spec.md's own Design section already commits to the mechanism that produces this outcome:
  "`mean` reuses `divide`'s zero-divisor handling instead of duplicating it — consistent with
  how `percent` is already built on `divide`" (intent Constraints: "consistent with divide
  and percent"). `ZeroDivisionError` is what that wiring yields with zero extra code.
- intent.md Constraints: "Keep it minimal: one function, no weights, no options." Raising
  `ValueError` needs a try/except translation; returning `0.0` needs an early-return guard.
  Letting `ZeroDivisionError` propagate needs neither — the only zero-extra-code choice.
- Not a taste call: it is the one option two independent rules (match-surrounding-code,
  keep-it-minimal) both land on; the other two candidates require code the constraints argue
  against and a style precedent that doesn't exist in this file.
