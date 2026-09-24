# Plan: add a mean helper to sample_pkg (from intent.md 2026-09-24, spec.md 2026-09-24)

## Files that change
- `sample_pkg/calc.py` — add `mean(values: Sequence[float]) -> float`, a new function next
  to `add`, `divide` and `percent`, raising `ValueError` on an empty `values` and otherwise
  returning `divide(sum(values), len(values))`.
- `sample_pkg/__init__.py` — add `mean` to the `from .calc import ...` line and to
  `__all__`.
- `tests/test_calc.py` — add `test_mean`, `test_mean_single_element` and `test_mean_empty`.

## Order of work
1. Add `mean` to `sample_pkg/calc.py`:
   ```python
   def mean(values: Sequence[float]) -> float:
       """Return the arithmetic mean of values; raises ValueError if values is empty."""
       if not values:
           raise ValueError("mean() requires at least one value")
       return divide(sum(values), len(values))
   ```
   Parameter type and empty-input behaviour are decided (by panel): `Sequence[float]`
   (spec.md Flagged concern 2) and an explicit `ValueError('mean() requires at least one
   value')` raised by `mean` itself via a guard clause, not inherited from `divide` (spec.md
   Flagged concern 1). Import `Sequence` from `typing` (project targets Python 3.10+;
   `collections.abc.Sequence` is also valid at runtime for the hint but `typing.Sequence`
   matches how a reader expects a typing-only import here — either is acceptable, `typing`
   is used for consistency with common Python 3.10 style).
2. Add `mean` to `sample_pkg/__init__.py`'s import line and `__all__`, in the same position
   relative to `add`, `divide`, `percent` as they already appear.
3. Add three tests to `tests/test_calc.py`:
   - `test_mean`: e.g. `mean([1, 2, 3, 4]) == 2.5`.
   - `test_mean_single_element`: e.g. `mean([5]) == 5.0`.
   - `test_mean_empty`: `with pytest.raises(ValueError): mean([])`.
4. Run `python -m compileall -q .`, `python -m pytest` and `python -m ruff check .`; all
   three must be green before this change is considered built.
5. Note, in the build PR description, a proposed one-line addition to `CLAUDE.md`'s Layout
   section describing `mean` (e.g. next to the existing `sample_pkg/calc.py` line) for the
   owner to add directly — `CLAUDE.md` is a guardrail file this run does not edit (intent
   Constraints).

## Risks
- Both of spec.md's flagged concerns (empty-input behaviour, parameter type) are now closed
  by the deferred-review panel (`evidence/decisions-b.json`, `evidence/panel/b-1-*`,
  `evidence/panel/b-2-*`); nothing today calls `mean`, so no existing caller is affected by
  either choice.
- Most risky step: step 1. It is the only step with logic (a guard clause plus a call into
  `divide`); getting the guard condition or the exception type wrong is the one way this
  change could ship the wrong behaviour, since `mean` has no existing caller to catch it in
  review.
- No caller, consumer or data shape besides the ones named in Files that change is touched:
  `mean` is new (nothing calls it yet), `add`, `divide` and `percent` keep their current
  signatures and behaviour, `sample_pkg.__all__` only gains a name (additive, so `from
  sample_pkg import *` breaks nothing existing), and this change stores nothing and defines
  no schema.
- `mean` is the first function in `sample_pkg/calc.py` to carry a docstring; `add`, `divide`
  and `percent` stay undocumented. This is a small, deliberate style inconsistency inside
  the file, required by intent.md's "stated in the docstring" requirement for the resolved
  empty-input behaviour.
- No production or runtime risk: `sdlc.yaml: deploy.action` is `none`, so merging this
  change publishes or deploys nothing.
- This plan is implementable by an engineer who never saw this conversation: every file,
  the exact signature, the exact empty-input behaviour, the three test assertions and the
  three commands that must stay green are all stated concretely above.

## Options not taken
- Wrapping `statistics.mean` — rejected; intent Constraints say explicitly it "is not to be
  wrapped."
- A variadic signature (`mean(*values)`) instead of `mean(values)` taking one sequence
  argument — rejected; it does not match `add`/`divide`/`percent`'s style and intent
  explicitly asks for `mean(values)` over "a sequence of numbers."
- Returning `Optional[float]` (`None` on empty input) instead of one of intent's three
  listed empty-input options — rejected; it is not one of the choices intent offers, and it
  would push a `None`-check onto every caller instead of resolving the question once.
- Letting `ZeroDivisionError` propagate from `divide(sum(values), len(values))` unchanged on
  empty input — this was the reviewer's pick in the panel round on spec.md Flagged concern 1
  (matches the `percent(1, 0)` precedent, no extra code) but the devil's advocate and the
  conciliator preferred an explicit `ValueError` raised by `mean` itself: it names the
  problem as "no data" rather than an arithmetic mistake, matches `statistics.mean`'s
  convention, and is a behaviour `mean`'s own code and tests pin rather than a side effect of
  routing through `divide`. Decided (by panel); see `evidence/decisions-b.json` item 1.
- `Iterable[float]` as the parameter type — rejected in the panel round on Flagged concern 2:
  it needs materialising code (a generator is consumed once) that intent's "keep it minimal"
  constraint argues against, and no existing function in the package takes a lazy iterable.
  The devil's advocate additionally proposed `Collection[float]` as a third option; the
  conciliator judged deciding a type outside the `Sequence`-vs-`Iterable` choice framed by
  this item was outside the item's scope, and decided `Sequence[float]`. Decided (by panel);
  see `evidence/decisions-b.json` item 2.
- A weighted mean, or any other option/parameter — rejected; intent Constraints say "no
  weights, no options."

## Proof
- `tests/test_calc.py::test_mean` — new test, written in step 3.
- `tests/test_calc.py::test_mean_single_element` — new test, written in step 3.
- `tests/test_calc.py::test_mean_empty` — new test, written in step 3;
  `pytest.raises(ValueError)` around `mean([])`.
- `python -m pytest` exits 0 with 8 passed (the 5 that pass today plus the 3 new ones).
- `python -m ruff check .` exits 0, printing `All checks passed!`.
- `python -m compileall -q .` exits 0 with no output.
