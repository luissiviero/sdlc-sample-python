# Plan: name the dividend in divide's error (from intent.md 2026-10-19, spec.md 2026-10-19)

## Files that change
- `sample_pkg/calc.py` — in `divide`, change the raised message from the fixed string
  `"b must not be zero"` to `f"cannot divide {a} by zero"`; no other line in the file moves.
- `tests/test_messages.py` (new) — asserts `divide(1, 0)` raises `ZeroDivisionError` whose
  `str(...)` is exactly `"cannot divide 1 by zero"`.

## Order of work
1. In `sample_pkg/calc.py`, change `divide`'s raise from
   `raise ZeroDivisionError("b must not be zero")` to
   `raise ZeroDivisionError(f"cannot divide {a} by zero")`. One line, one commit.
2. Add `tests/test_messages.py`, importing `divide` from `sample_pkg` (matching the import
   style of `tests/test_calc.py`), with a test that calls `divide(1, 0)` inside
   `pytest.raises(ZeroDivisionError)` and asserts `str(excinfo.value) == "cannot divide 1 by
   zero"`.
3. Run `python -m compileall -q .`, `python -m pytest`, `python -m ruff check .`; all three
   must exit 0 with the healthy output `CLAUDE.md` describes.

## Risks
- Lowest-risk change in the project: a single string literal inside one `raise`, in a
  function whose signature, condition and return value are untouched. The riskiest step is
  step 1, only because it is the one line that changes behaviour at all — a typo in the
  f-string (e.g. formatting `b` instead of `a`) would silently name the wrong operand and
  only show up by reading the new test's assertion carefully.
- Callers that match on the exact exception message, not just the type, would break. Checked:
  `tests/test_calc.py`'s `test_divide_by_zero_raises` only checks the type
  (`pytest.raises(ZeroDivisionError)`, no message assertion), and
  `test_percent_zero_whole_error_names_whole` asserts `percent`'s own literal message
  (`"whole must not be zero"`), which `percent` raises itself and never derives from
  `divide`'s text (`sample_pkg/calc.py:17-18`). No other file in the repository matches the
  string `"b must not be zero"` or otherwise depends on `divide`'s message text. No external
  caller exists inside this repository to check.
- `mean` calls `divide` but only after its own empty-collection check, so it can never
  trigger `divide`'s zero-divisor branch at all; this plan does not touch `mean`.
- No new dependency, no schema, no migration, no risk-list item (auth, data migrations,
  money movement, production config) is touched — nothing to mitigate there.

## Options not taken
- Formatting the dividend with `repr(a)` instead of an f-string's default `str(a)`: rejected
  because the intent's own examples (`"cannot divide 1.5 by zero"`, `"cannot divide 1.0 by
  zero"`) match `str()`'s output, not `repr()`'s (identical for `float` and `int` here, but
  `str()` is the conventional choice for a user-facing message and what the spec's Design
  section specifies).
- Also updating `percent` to build its message from `whole`: rejected — out of scope. The
  intent's Proposed outcome explicitly keeps `percent`'s message fixed at `"whole must not
  be zero"`, and `percent` already raises that message independently of `divide`'s text, so
  no change to `percent` is needed to satisfy the intent.
- Writing the new test inside `tests/test_calc.py` instead of a new `tests/test_messages.py`:
  rejected — the intent names `tests/test_messages.py` specifically, and `CLAUDE.md`'s
  Layout section already documents that file as the one that "checks the error messages"
  (added in PR #76), so creating it keeps the codebase matching its own documentation.
- Adding a test for `divide(1.5, 0)` / `divide(1.0, 0)` message formatting: not added as a
  new test — the intent's acceptance target is `divide(1, 0)` specifically, and
  `tests/test_calc.py`'s existing `test_divide_by_zero_raises` already exercises the
  zero-divisor path with an integer dividend. The non-integer cases are the answered open
  question's justification for the f-string's default formatting, not a stated requirement
  to test; adding them would be scope beyond what intent.md and spec.md's Acceptance ask
  for.

## Proof
- `tests/test_messages.py::test_divide_by_zero_names_dividend` (name indicative; the test to
  be written in step 2) — asserts `str(excinfo.value) == "cannot divide 1 by zero"` for
  `divide(1, 0)`. Still to be written; this plan is what requires it.
- `tests/test_calc.py::test_divide_by_zero_raises` — existing test, must keep passing
  unchanged (type-only check, unaffected by the message change).
- `tests/test_calc.py::test_percent_zero_whole_error_names_whole` — existing test, must keep
  passing unchanged (asserts `percent`'s own message, `"whole must not be zero"`).
- `tests/test_calc.py::test_mean*` and `test_percent`, `test_add` — existing tests, must keep
  passing unchanged; untouched by this plan.
- `tests/test_flag.py` — existing test, untouched, must keep passing (`SAMPLE_FAIL=1` is
  never set in this run).
- `python -m compileall -q .`, `python -m pytest`, `python -m ruff check .` — all three must
  exit 0 with the healthy output `CLAUDE.md`'s Commands table describes.
