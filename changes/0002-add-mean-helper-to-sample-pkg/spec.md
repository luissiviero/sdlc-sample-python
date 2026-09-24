# Spec: add a mean helper to sample_pkg
Change id: 0002. Status: proposed. Produced by: sdlc plugin 0.2.14, /sdlc-design prompt v1 (article p.14). Skills: coding-standards, security-baseline, ux-conventions, data-conventions, definition-of-done (plugin 0.2.14); overrides: none

## Requirements
- `sample_pkg` gains `mean(values)`, returning the arithmetic mean of a sequence of numbers
  as a `float` (e.g. `mean([1, 2, 3, 4]) == 2.5`) (intent Proposed outcome).
- `mean` is implemented in `sample_pkg/calc.py`, next to `add`, `divide` and `percent`, and
  exported from `sample_pkg/__init__.py` and listed in `__all__` the same way the other
  three are (coding-standards rule 2: match the existing export pattern).
- `mean` takes a `Sequence[float]` and raises `ValueError('mean() requires at least one
  value')` on an empty sequence, raised explicitly by `mean` itself rather than inherited
  from `divide` — both decided by the deferred-review panel (see Flagged concerns and
  `evidence/decisions-b.json`, items 1 and 2).
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
- Signature: `mean(values: Sequence[float]) -> float`. Decided (by panel) over a generic
  `Iterable[float]`: a lazy iterable would need materialising (e.g. into a `list`) before
  both `sum()` and `len()` can run, since a generator is consumed once — extra code intent's
  "keep it minimal" constraint argues against, and no existing function in the package takes
  a lazy iterable. See `evidence/decisions-b.json` item 2.
- Empty input: `mean([])` raises `ValueError('mean() requires at least one value')` via a
  guard clause in `mean` itself. Decided (by panel) over letting `ZeroDivisionError`
  propagate from `divide`: an explicit `ValueError` names the problem as "no data" rather
  than an arithmetic mistake, matches `statistics.mean`'s convention, and is a behaviour
  `mean`'s own code and tests pin directly rather than a side effect of routing through
  `divide`. See `evidence/decisions-b.json` item 1.
- Non-empty input: `mean` computes the total with the built-in `sum()` and divides by
  `len(values)` through the existing `divide` helper (`divide(sum(values), len(values))`),
  reusing `divide`'s (unreachable, given the guard clause) zero-divisor handling rather than
  duplicating it — consistent with how `percent` is already built on `divide` (intent
  Constraints: "consistent with divide and percent").
- `sample_pkg/__init__.py`: `mean` is added to the `from .calc import ...` line and to
  `__all__`, alongside `add`, `divide`, `percent` — no other change to the module's shape.
- Nothing else in the package changes: `add`, `divide`, `percent` and their tests are
  untouched, and no new file or dependency is introduced.

## Open questions from intent
- "Empty sequence: raise `ZeroDivisionError` by going through `divide(sum, len)`
  (consistent with `percent(1, 0)`), raise `ValueError` (what `statistics.mean` does), or
  return `0.0`?" — answered by the deferred-review panel: raise `ValueError('mean() requires
  at least one value')`, raised explicitly by `mean` (not inherited from `divide`). Neither
  intent nor a loaded policy skill settled this outright — intent said "the owner has no
  preference: to be settled in design," and its own Problem section states this change
  exists partly to have the panel settle it inside the design phase — so it was carried to
  Flagged concerns and decided there. See `evidence/decisions-b.json` item 1.
- "Should `mean` accept any iterable (a generator is consumed once, so it must be
  materialised first) or only a `Sequence`?" — answered by the deferred-review panel:
  `Sequence[float]`. Same reasoning: no loaded policy skill settled the choice, so it was
  carried to Flagged concerns and decided there. See `evidence/decisions-b.json` item 2.

## Flagged concerns
- decided (by panel): `mean([])` raises `ValueError('mean() requires at least one value')`,
  raised explicitly by `mean` itself via a guard clause (not inherited from `divide`) —
  empty-sequence behaviour for `mean` was undecided going into the panel round
  (`ZeroDivisionError` via `divide`, `ValueError`, or `0.0`); no loaded policy skill settled
  it. See `evidence/decisions-b.json` item 1 and `evidence/panel/b-1-*`.
- decided (by panel): `Sequence[float]` — `mean`'s parameter type was undecided going into
  the panel round (a materialised `Sequence[float]` vs a general `Iterable[float]`); no
  loaded policy skill settled it. See `evidence/decisions-b.json` item 2 and
  `evidence/panel/b-2-*`.

## Acceptance
- `tests/test_calc.py` passes three new tests: a normal multi-value case (e.g.
  `mean([1, 2, 3, 4]) == 2.5`), a single-element case (e.g. `mean([5]) == 5.0`), and
  `test_mean_empty`, asserting `pytest.raises(ValueError)` around `mean([])`.
- `from sample_pkg import mean` succeeds and `"mean"` is in `sample_pkg.__all__`.
- `python -m compileall -q .` — no output, exit code 0.
- `python -m pytest` — all tests pass, including the 5 that pass today plus the 3 new ones
  (8 passed), and `tests/test_flag.py` is unchanged.
- `python -m ruff check .` — `All checks passed!`, exit code 0.
