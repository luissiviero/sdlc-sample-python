# Spec: add a mean helper to sample_pkg
Change id: 0002. Status: proposed. Produced by: sdlc plugin 0.2.14, /sdlc-design prompt v1 (article p.14). Skills: coding-standards, security-baseline, ux-conventions, data-conventions, definition-of-done (plugin 0.2.14); overrides: none

## Requirements
- `sample_pkg` gains `mean(values)`, returning the arithmetic mean of a sequence of numbers
  as a `float` (e.g. `mean([1, 2, 3, 4]) == 2.5`) (intent Proposed outcome).
- `mean` is implemented in `sample_pkg/calc.py`, next to `add`, `divide` and `percent`, and
  exported from `sample_pkg/__init__.py` and listed in `__all__` the same way the other
  three are (coding-standards rule 2: match the existing export pattern).
- The exact behaviour on an empty sequence, and whether `mean` accepts any iterable or only
  a `Sequence`, are not decided by this spec pass — see Open questions from intent and
  Flagged concerns. Acceptance below is written so either resolution satisfies it.
- `tests/test_calc.py` gains tests for the normal case, the single-element case and the
  empty case; no behaviour change ships without a test that fails without it
  (coding-standards rule 4).
- `add`, `divide` and `percent` keep their current signatures and behaviour; they and
  `tests/test_flag.py` are not touched by this change (intent Constraints).
- No new dependency: `mean` is written by hand, not as a wrapper around
  `statistics.mean` (intent Constraints; coding-standards rule 5).
- `mean`'s public signature carries type hints, and the file stays inside the project's
  100-column line length (coding-standards rule 8; `pyproject.toml: [tool.ruff]
  line-length = 100`).
- `python -m compileall -q .`, `python -m pytest` and `python -m ruff check .` (the
  `sdlc.yaml: commands` targets) all stay green (definition-of-done).
- security-baseline does not apply: `mean` is a pure in-process function with no endpoint,
  no external input beyond an ordinary Python argument, no secret, and no network call
  (rules 1, 2, 3, 7 n/a).
- ux-conventions does not apply: the project has no user interface and this change adds
  none.
- data-conventions does not apply: `mean` stores nothing, defines no schema, and handles no
  personal or sensitive data; its input is transient in-memory numbers.
- None of `sdlc.yaml: risk_list` (auth, data migrations, money movement, production
  config) is touched by this change.
- The guardrail files (`.claude/**`, `CLAUDE.md`, `REVIEW.md`, `sdlc.yaml`) are not edited
  by this run; the one-line `CLAUDE.md` Layout update intent.md asks for is proposed for
  the owner in the build PR (phase c), not made here (intent Constraints).

## Design
- `sample_pkg/calc.py` gains one function, `mean`, written in the same plain-function,
  type-hinted style as `add`, `divide` and `percent` — no class, no module-level state.
- For a non-empty input, `mean` computes the total with the built-in `sum()` and divides by
  `len(values)` through the existing `divide` helper (`divide(sum(values), len(values))`),
  so `mean` reuses `divide`'s zero-divisor handling instead of duplicating it — consistent
  with how `percent` is already built on `divide` (intent Constraints: "consistent with
  divide and percent").
- Parameter type: accepting a generic `Iterable[float]` requires materialising it (e.g. into
  a `list`) before both `sum()` and `len()` can run, since a generator is consumed once —
  extra code the intent's "keep it minimal" constraint argues against. Accepting only a
  `Sequence[float]` needs no such step but narrows what a caller can pass. This is not
  settled here (Flagged concerns); the signature in Acceptance is written generically as
  "a sequence of numbers" pending the decision.
- Empty input: intent lists three candidate behaviours (raise `ZeroDivisionError` via
  `divide`, raise `ValueError`, or return `0.0`) and says the owner has no preference. This
  is not settled here either (Flagged concerns). Whichever is chosen becomes the one line of
  docstring on `mean` that states it, and the empty-case assertion in
  `tests/test_calc.py::test_mean_empty`.
- `sample_pkg/__init__.py`: `mean` is added to the `from .calc import ...` line and to
  `__all__`, alongside `add`, `divide`, `percent` — no other change to the module's shape.
- Nothing else in the package changes: `add`, `divide`, `percent` and their tests are
  untouched, and no new file or dependency is introduced.

## Open questions from intent
- "Empty sequence: raise `ZeroDivisionError` by going through `divide(sum, len)`
  (consistent with `percent(1, 0)`), raise `ValueError` (what `statistics.mean` does), or
  return `0.0`?" — carried forward. Intent says "the owner has no preference: to be settled
  in design," and none of the five loaded policy skills (coding-standards,
  security-baseline, ux-conventions, data-conventions, definition-of-done) states an
  error-handling rule that picks between them. The codebase shows a precedent
  (`percent(1, 0)` already raises `ZeroDivisionError`) but nothing that mandates following
  it for a new function. Intent's own Problem section states this change exists partly to
  have the deferred-review panel settle this inside the design phase — carried to Flagged
  concerns for that panel.
- "Should `mean` accept any iterable (a generator is consumed once, so it must be
  materialised first) or only a `Sequence`?" — carried forward, same reasoning: no loaded
  policy skill settles the iterable-vs-`Sequence` choice, and intent leaves it to design's
  judgment. Carried to Flagged concerns for the panel.

## Flagged concerns
- decided (by panel): mean([]) raises ValueError('mean() requires at least one value'), raised explicitly by mean itself via a guard clause (not inherited from divide) — Empty-sequence behaviour for `mean` is undecided: `ZeroDivisionError` (via `divide`),
  `ValueError`, or `0.0`. No loaded policy skill settles it (see Open questions from
  intent). Needs the panel's (or owner's) decision before `plan.md`'s test list and the
  docstring wording can be final.
- decided (by panel): decided (by panel): `Sequence[float]` — mean's parameter type is undecided: a materialised `Sequence[float]` (simpler, matches intent's "keep it minimal") or a general `Iterable[float]` (more permissive, needs materialising code the minimal constraint argues against). — `mean`'s parameter type is undecided: a materialised `Sequence[float]` (simpler, matches
  intent's "keep it minimal") or a general `Iterable[float]` (more permissive, needs
  materialising code the minimal constraint argues against). No loaded policy skill settles
  it (see Open questions from intent). Needs the panel's (or owner's) decision before
  `plan.md`'s design can name the exact signature.

## Acceptance
- `tests/test_calc.py` passes three new tests: a normal multi-value case (e.g.
  `mean([1, 2, 3, 4]) == 2.5`), a single-element case (e.g. `mean([5]) == 5.0`), and an
  empty-input case whose assertion matches whichever behaviour Flagged concern 1 resolves
  to (an exception assertion or an equality check against `0.0`).
- `from sample_pkg import mean` succeeds and `"mean"` is in `sample_pkg.__all__`.
- `python -m compileall -q .` — no output, exit code 0.
- `python -m pytest` — all tests pass, including the 5 that pass today plus the 3 new ones
  (8 passed), and `tests/test_flag.py` is unchanged.
- `python -m ruff check .` — `All checks passed!`, exit code 0.
