# Plan: add a mean helper to sample_pkg (from intent.md 2026-09-24, spec.md 2026-09-24)

## Files that change
- `sample_pkg/calc.py` — add `mean(values)`, a new function next to `add`, `divide` and
  `percent`, implemented via `divide(sum(values), len(values))` for the non-empty case.
- `sample_pkg/__init__.py` — add `mean` to the `from .calc import ...` line and to
  `__all__`.
- `tests/test_calc.py` — add `test_mean`, `test_mean_single_element` and `test_mean_empty`.

## Order of work
1. Add `mean` to `sample_pkg/calc.py` with a type-hinted signature and a one-line docstring
   stating the empty-input behaviour. The exact parameter type (`Sequence[float]` vs
   `Iterable[float]`) and the exact empty-input behaviour (`ZeroDivisionError` via `divide`,
   `ValueError`, or `0.0`) are spec.md Flagged concerns 1 and 2, still open when this plan is
   written; this step, and step 3's `test_mean_empty`, implement whichever the panel (or the
   owner) decides. This plan.md is updated in the same commit as that decision if either
   choice changes what is written here (phase (b) process, `/sdlc-design` step 6).
2. Add `mean` to `sample_pkg/__init__.py`'s import line and `__all__`, in the same position
   relative to `add`, `divide`, `percent` as they already appear.
3. Add three tests to `tests/test_calc.py`: `test_mean` (a normal multi-value case, e.g.
   `mean([1, 2, 3, 4]) == 2.5`), `test_mean_single_element` (e.g. `mean([5]) == 5.0`), and
   `test_mean_empty` (an assertion matching whichever empty-input behaviour step 1 resolved
   to — `pytest.raises(...)` or an equality check against `0.0`).
4. Run `python -m compileall -q .`, `python -m pytest` and `python -m ruff check .`; all
   three must be green before this change is considered built.
5. Note, in the build PR description, a proposed one-line addition to `CLAUDE.md`'s Layout
   section describing `mean` (e.g. next to the existing `sample_pkg/calc.py` line) for the
   owner to add directly — `CLAUDE.md` is a guardrail file this run does not edit (intent
   Constraints).

## Risks
- Flagged concerns 1 and 2 in spec.md (empty-input behaviour, parameter type) are open at
  the time this plan is written. Nothing today calls `mean`, so no existing caller is at
  risk either way; the risk is committing step 1's implementation and step 3's
  `test_mean_empty` to an assumption the panel or owner later overturns, which would need
  step 1 and step 3 reworked and this plan updated in the same commit.
- Most risky step: step 1. It is the only step whose exact content depends on an undecided
  question — how `mean` behaves on empty input is the one behaviour a future caller could
  come to rely on, so picking the wrong one before the panel decides is the step most likely
  to need rework.
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
- This plan is implementable by an engineer who never saw this conversation for everything
  except the exact signature and the exact empty-input assertion, which spec.md carries
  forward as open flagged concerns for the panel (or the owner) to decide; which three files
  change, what each edit does, the non-empty test cases, and which three commands must stay
  green are all concrete already. Once the panel records its decision, this plan is updated
  in the same commit with the concrete signature and assertion, and is then fully
  self-contained.

## Options not taken
- Wrapping `statistics.mean` — rejected; intent Constraints say explicitly it "is not to be
  wrapped."
- A variadic signature (`mean(*values)`) instead of `mean(values)` taking one sequence
  argument — rejected; it does not match `add`/`divide`/`percent`'s style and intent
  explicitly asks for `mean(values)` over "a sequence of numbers."
- Returning `Optional[float]` (`None` on empty input) instead of one of intent's three
  listed empty-input options — rejected; it is not one of the choices intent offers, and it
  would push a `None`-check onto every caller instead of resolving the question once.
- A weighted mean, or any other option/parameter — rejected; intent Constraints say "no
  weights, no options."

## Proof
- `tests/test_calc.py::test_mean` — new test, written in step 3.
- `tests/test_calc.py::test_mean_single_element` — new test, written in step 3.
- `tests/test_calc.py::test_mean_empty` — new test, written in step 3; its assertion is
  pending the empty-input decision (spec.md Flagged concern 1).
- `python -m pytest` exits 0 with 8 passed (the 5 that pass today plus the 3 new ones).
- `python -m ruff check .` exits 0, printing `All checks passed!`.
- `python -m compileall -q .` exits 0 with no output.
