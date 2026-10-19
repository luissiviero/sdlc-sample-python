# Plan: name the zero whole in percent's error (from intent.md 2026-10-19, spec.md 2026-10-19)

## Files that change
- `tests/test_calc.py`: add a test asserting the exact message of `percent(1, 0)`'s `ZeroDivisionError`.
- `sample_pkg/calc.py`: `percent` catches the `ZeroDivisionError` from `divide(part * 100, whole)` and re-raises `ZeroDivisionError("whole must not be zero") from None`.

## Order of work
1. Write the reproducing test in `tests/test_calc.py` (e.g. `test_percent_zero_whole_error_names_whole`, asserting `str(excinfo.value) == "whole must not be zero"` for `percent(1, 0)`); run `python -m pytest` and see it fail against the current code (change type `fix`, build guide step 25).
2. Implement the fix in `sample_pkg/calc.py`: wrap the `divide(part * 100, whole)` call in `percent` with `try/except ZeroDivisionError: raise ZeroDivisionError("whole must not be zero") from None`. Leave `divide`, `add` and `mean` untouched.
3. Run `python -m compileall -q .`, `python -m pytest` and `python -m ruff check .`; confirm all green, including the new test and the two existing tests that touch this path (`test_percent_zero_whole_raises`, `test_divide_by_zero_raises`).

## Risks
- **What this could break** (interrogation Q1): `percent`'s only caller in this repo is `tests/test_calc.py`; `sample_pkg/__init__.py` re-exports it but nothing in the package calls it internally. `divide` and `mean` are untouched, so `test_divide_by_zero_raises`, `test_mean_empty` and the other `mean` tests are unaffected — `mean`'s own zero case is guarded by its own `ValueError` check before it ever reaches `divide` with a zero divisor. A caller outside this repo that pattern-matches `percent`'s old message text (`"b must not be zero"`, inherited from `divide`) would see a different string after this change; the intent accepts this (it is the point of the fix) and keeps the exception type `ZeroDivisionError` so a `try/except ZeroDivisionError` caller keeps working.
- **Riskiest step** (interrogation Q2): step 2. The only way to depart from the design is to omit `from None` (which still passes every test here, since none inspect `__cause__`/`__context__`, but departs from spec.md's Design) or to duplicate a `whole == 0` pre-check instead of catching `divide`'s exception (spec.md's Open questions already settles against this). Mitigation: implement exactly the catch-and-reraise `from None` form spec.md describes.
- No public function is added or removed, so the two `CLAUDE.md` Layout entries (for `sample_pkg/calc.py` and `tests/test_calc.py`) stay accurate as written; this plan does not touch them (per "Things Claude gets wrong" in `CLAUDE.md`, flagged here to say explicitly that no Layout update is needed).

## Options not taken
- **Pre-check `whole == 0` inside `percent` before calling `divide`** — not chosen: it would duplicate the zero-check condition `divide` already owns in a second place, instead of catching the exception `divide` already raises (spec.md Design/Open questions; coding-standards rule 2, match the existing idiom).
- **Changing `divide`'s own message** — not chosen: the intent requires `divide(1, 0)` to keep raising `ZeroDivisionError("b must not be zero")` unchanged.
- **A custom exception subclass of `ZeroDivisionError`** (e.g. carrying the parameter name as a field) — not chosen: the intent requires the exception type to stay exactly `ZeroDivisionError`, and `CLAUDE.md` says to keep the project minimal; a subclass is unneeded machinery for a one-line message change.

## Proof
- `tests/test_calc.py::test_percent_zero_whole_error_names_whole` (new, written in step 1) — asserts the exact message text.
- `tests/test_calc.py::test_percent_zero_whole_raises` (existing) — still passes: exception type unchanged.
- `tests/test_calc.py::test_divide_by_zero_raises` (existing) — still passes: `divide` unchanged.
- `python -m pytest` — all tests pass (10: the 9 current plus the new one), exit code 0.
- `python -m compileall -q .` — no output, exit code 0.
- `python -m ruff check .` — `All checks passed!`, exit code 0.
- (interrogation Q5: every item above is a named, runnable test; only the first is still to be written, in step 1, and it is named as the file that proves this change — build guide step 25.)

Interrogation Q4 (could an engineer who never saw this conversation implement the change from this plan alone?): yes — the exact message text, the exception type, the file and function, the catch-and-reraise shape with `from None`, and the test's exact assertion are all stated above; no further context is needed.
