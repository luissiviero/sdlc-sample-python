# Plan: name the part in percent's zero-whole error (from intent.md 2026-10-20, spec.md 2026-10-20)

## Files that change
- `sample_pkg/calc.py` — in `percent`, change the re-raised message from the fixed string
  `"whole must not be zero"` to `f"cannot express {part} as a percent of zero"`; the `try`,
  the `except ZeroDivisionError`, the `from None` and every other line in the file stay as
  they are.
- `tests/test_messages.py` — import `percent` beside `divide` from `sample_pkg`; add one test
  asserting `percent(5, 0)` raises `ZeroDivisionError` whose `str(...)` is exactly
  `"cannot express 5 as a percent of zero"`. The existing test is not touched.
- `tests/test_calc.py` — in `test_percent_zero_whole_error_names_whole`, change the asserted
  message from `"whole must not be zero"` to `"cannot express 1 as a percent of zero"`
  (the test calls `percent(1, 0)`). Nothing else in the module moves. This edit is the open
  flagged concern in `spec.md`; if the owner or the panel decides the other way (keep the
  old message and leave `tests/test_calc.py` alone), drop this file and step 3 and the
  change reduces to no source edit at all, which abandons the intent's Proposed outcome.

## Order of work
1. In `sample_pkg/calc.py`, line 18, change
   `raise ZeroDivisionError("whole must not be zero") from None` to
   `raise ZeroDivisionError(f"cannot express {part} as a percent of zero") from None`.
   One line.
2. In `tests/test_messages.py`, change the import to `from sample_pkg import divide, percent`
   and append a test `test_percent_zero_whole_names_part` that calls `percent(5, 0)` inside
   `with pytest.raises(ZeroDivisionError) as excinfo:` and asserts
   `str(excinfo.value) == "cannot express 5 as a percent of zero"`, in the same shape as the
   existing `test_divide_by_zero_names_dividend`.
3. In `tests/test_calc.py`, line 28, change the assertion to
   `assert str(excinfo.value) == "cannot express 1 as a percent of zero"`. Keep the test's
   name and the rest of the module unchanged.
4. Run `python -m compileall -q .`, `python -m pytest` and `python -m ruff check .` from the
   repository root; all three must exit 0 with the healthy output `CLAUDE.md`'s Commands
   table describes (no output; `11 passed`; `All checks passed!`). Paste the output.
Steps 1 to 3 can land in one commit: the plan-sync hook requires the commit that touches
source to carry `plan.md` only when it departs from this list, and it does not.

## Risks
- A single string literal inside one `raise` changes; the function's signature, condition,
  exception type and return value are untouched. The riskiest step is step 1, only because it
  is the one line that changes behaviour: formatting `part * 100` or `whole` instead of
  `part` would name the wrong value and would show up only in the new test's assertion
  (`5`, not `500` or `0`). Dropping `from None` by accident would re-attach `divide`'s
  exception as the cause and show `"cannot divide 500 by zero"` in the traceback, which no
  test catches; the implementer must keep the clause as it is.
- Callers matching the exact old message break by design. Checked with Grep: the string
  `"whole must not be zero"` occurs in source only in `sample_pkg/calc.py:18` and in
  `tests/test_calc.py:28` (step 3 updates it); every other occurrence is inside the change
  folders of changes 0015, 0016 and 0017 (historical records and this plan, not edited by
  the build). No other caller exists inside this repository.
- Step 3 edits a test file the intent's Constraints say is not changed; this is the open
  flagged concern in `spec.md`. The change is `feature`-typed, so `sdlc.yaml: test_paths`
  does not lock the file (the lock is for `fix`-type changes). If the decision at the gate
  goes the other way, the build must not run steps 1 to 3 as written; see the note in Files
  that change.
- `test_percent_zero_whole_error_names_whole` keeps a name that says "names whole" while
  asserting a message that names the part. Renaming it was considered (Options not taken)
  and rejected to keep the edit to the one assertion line the concern covers.
- `divide` and `mean` are not touched; `mean` never reaches a zero divisor because it rejects
  an empty collection first. `tests/test_flag.py` is not touched and `SAMPLE_FAIL` is never
  set.
- No new dependency, no schema, no migration, no risk-list item (auth, data migrations,
  money movement, production config) and no guardrail file is touched. `CLAUDE.md`'s Layout
  section stays correct: no public function is added or removed, and its sentence on
  `percent` describes the exception type, not the message text.

## Options not taken
- Keeping the old message to leave `tests/test_calc.py` untouched: rejected as the default,
  because the intent's Problem and Proposed outcome are the new message and the test is the
  old behaviour written down. Recorded as the alternative under the flagged concern, for the
  owner or the panel.
- Letting `divide`'s message through (dropping the `except` clause in `percent`): rejected,
  because `percent` calls `divide(part * 100, whole)` and the message would read
  `"cannot divide 500 by zero"` for `percent(5, 0)`, a value the caller never passed. The
  intent's open question 2 prefers the own message for this reason.
- Checking `whole == 0` in `percent` before calling `divide`, instead of catching
  `ZeroDivisionError`: rejected; it would change the function's shape for no gain and the
  intent asks for a message change only.
- Formatting `part` with `repr()` or a fixed number format: rejected; the intent's example
  `"cannot express 1.5 as a percent of zero"` is `str()`'s output, and `divide` already uses
  the f-string default (change 0016).
- Renaming `test_percent_zero_whole_error_names_whole` to say "names part": rejected to keep
  the edit to the one assertion line; a rename is a second departure from the intent's
  constraint for a cosmetic gain. The new test in `tests/test_messages.py` carries the
  descriptive name.
- Deleting `test_percent_zero_whole_error_names_whole` instead of updating it (the new test
  in `tests/test_messages.py` covers the message): rejected; coding-standards rule 4 forbids
  deleting a failing test, and updating the assertion keeps the coverage of `percent(1, 0)`.
- Adding tests for `percent(1.5, 0)` and `percent(1.0, 0)`: not added; the intent's
  acceptance target is `percent(5, 0)` and the formatting rule is the same f-string default
  `divide` uses, which change 0016 settled without a dedicated test.

## Proof
- `tests/test_messages.py::test_percent_zero_whole_names_part` — still to be written in step
  2; asserts `str(excinfo.value) == "cannot express 5 as a percent of zero"` for
  `percent(5, 0)`. It fails on the current code and passes after step 1.
- `tests/test_calc.py::test_percent_zero_whole_error_names_whole` — existing test, updated in
  step 3 to assert `"cannot express 1 as a percent of zero"` for `percent(1, 0)`.
- `tests/test_messages.py::test_divide_by_zero_names_dividend` — existing test, unchanged,
  must keep passing (`"cannot divide 1 by zero"`).
- `tests/test_calc.py::test_add`, `test_divide_by_zero_raises`, `test_percent`,
  `test_percent_zero_whole_raises`, `test_mean`, `test_mean_single_element`,
  `test_mean_empty`, `test_mean_accepts_non_sequence_collection` — existing tests, unchanged,
  must keep passing.
- `tests/test_flag.py::test_intentional_failure_behind_flag` — existing test, untouched,
  passes because `SAMPLE_FAIL` is never set.
- `python -m compileall -q .` (no output, exit 0), `python -m pytest` (`11 passed`, exit 0),
  `python -m ruff check .` (`All checks passed!`, exit 0), as `CLAUDE.md`'s Commands table
  describes.
