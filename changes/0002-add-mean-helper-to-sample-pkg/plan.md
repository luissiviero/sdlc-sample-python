# Plan: add a mean helper to sample_pkg (from intent.md 2026-09-24, spec.md 2026-09-24)

## Files that change
- `sample_pkg/calc.py` — add `mean(values: Collection[float]) -> float`, a new function next
  to `add`, `divide` and `percent`, raising `ValueError` on an empty `values` and otherwise
  returning `divide(sum(values), len(values))`.
- `sample_pkg/__init__.py` — add `mean` to the `from .calc import ...` line and to
  `__all__`.
- `tests/test_calc.py` — add `test_mean`, `test_mean_single_element`, `test_mean_empty` and
  `test_mean_accepts_non_sequence_collection` (spec.md Flagged concern 2, overturned to
  `Collection[float]`: a test using a `set`, which is a `Collection` but not a `Sequence`,
  is the one thing that actually exercises the widened contract — the other three all pass
  a `list`, which was already both).

## Order of work
1. Add `mean` to `sample_pkg/calc.py`:
   ```python
   def mean(values: Collection[float]) -> float:
       """Return the arithmetic mean of values; raises ValueError if values is empty."""
       if not values:
           raise ValueError("mean() requires at least one value")
       return divide(sum(values), len(values))
   ```
   Empty-input behaviour is decided (by panel): an explicit `ValueError('mean() requires at
   least one value')` raised by `mean` itself via a guard clause, not inherited from
   `divide` (spec.md Flagged concern 1). Parameter type is decided (owner, overturning the
   panel): `Collection[float]`, not `Sequence[float]` (spec.md Flagged concern 2) — `sum`
   and `len` are all the body needs, so `Collection[float]` is the honest contract at no
   extra code, while still rejecting a generator (no `__len__`), which keeps "no
   materialising". Import `Collection` from `typing` (project targets Python 3.10+;
   `collections.abc.Collection` is also valid at runtime for the hint but `typing.Collection`
   matches how a reader expects a typing-only import here — either is acceptable, `typing`
   is used for consistency with common Python 3.10 style).
2. Add `mean` to `sample_pkg/__init__.py`'s import line and `__all__`, in the same position
   relative to `add`, `divide`, `percent` as they already appear.
3. Add four tests to `tests/test_calc.py`:
   - `test_mean`: e.g. `mean([1, 2, 3, 4]) == 2.5`.
   - `test_mean_single_element`: e.g. `mean([5]) == 5.0`.
   - `test_mean_empty`: `with pytest.raises(ValueError): mean([])`.
   - `test_mean_accepts_non_sequence_collection`: e.g. `mean({1.0, 2.0, 3.0}) == 2.0`, a
     `set` — a `Collection[float]` that is not a `Sequence[float]` (no order, no indexing) —
     to pin the widened contract the overturned Flagged concern 2 asks for.
4. Run `python -m compileall -q .`, `python -m pytest` and `python -m ruff check .`; all
   three must be green before this change is considered built.
5. Note, in the build PR description, a proposed one-line addition to `CLAUDE.md`'s Layout
   section describing `mean` (e.g. next to the existing `sample_pkg/calc.py` line) for the
   owner to add directly — `CLAUDE.md` is a guardrail file this run does not edit (intent
   Constraints).

## Risks
- Both of spec.md's flagged concerns are now closed: empty-input behaviour by the
  deferred-review panel (`evidence/decisions-b.json` item 1, `evidence/panel/b-1-*`), and
  parameter type by the panel's initial pick overturned by the owner's review comment in
  favour of `Collection[float]` (`evidence/decisions-b.json` item 2, now marked
  `overturned`, and `evidence/fix-response.md`); nothing today calls `mean`, so no existing
  caller is affected by either choice.
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
  This still holds under `Collection[float]`: a generator has no `__len__`, so it is rejected
  there too.
- `Sequence[float]` as the parameter type — the panel's initial pick for Flagged concern 2
  (the devil's advocate's `Collection[float]` alternative was judged out of the item's framed
  Sequence-vs-Iterable scope at the time). Overturned by the owner's review comment on
  `evidence/decisions-b.md`: `sum` and `len` are all the body needs, so `Collection[float]`
  is the honest contract at no extra code — the advocate's original point. See
  `evidence/decisions-b.json` item 2 (`overturned`) and `evidence/fix-response.md`.
- A weighted mean, or any other option/parameter — rejected; intent Constraints say "no
  weights, no options."

## Proof
- `tests/test_calc.py::test_mean` — new test, written in step 3.
- `tests/test_calc.py::test_mean_single_element` — new test, written in step 3.
- `tests/test_calc.py::test_mean_empty` — new test, written in step 3;
  `pytest.raises(ValueError)` around `mean([])`.
- `tests/test_calc.py::test_mean_accepts_non_sequence_collection` — new test, written in
  step 3; passes a `set` to `mean`, pinning the `Collection[float]` contract the overturned
  Flagged concern 2 decided.
- `python -m pytest` exits 0 with 9 passed (the 5 that pass today plus the 4 new ones).
- `python -m ruff check .` exits 0, printing `All checks passed!`.
- `python -m compileall -q .` exits 0 with no output.
