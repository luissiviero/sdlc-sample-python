# Spec: name the part in percent's zero-whole error
Change id: 0017. Status: proposed. Produced by: sdlc plugin 1.0.14, /sdlc-design prompt v1 (article p.14). Skills: coding-standards, security-baseline, ux-conventions, data-conventions, definition-of-done (plugin 1.0.14); overrides: none

## Requirements
- `percent(5, 0)` raises `ZeroDivisionError` with the message exactly
  `"cannot express 5 as a percent of zero"` (intent Proposed outcome).
- The message names the `part` argument as the caller passed it, rendered with Python's own
  text for the value (`str`, the f-string default), so `percent(1.5, 0)` raises
  `"cannot express 1.5 as a percent of zero"` and `percent(1.0, 0)` raises
  `"cannot express 1.0 as a percent of zero"` (intent open question 1, answered below; the
  same rule change 0016 settled for `divide`).
- The message names `part`, never `part * 100`: `percent` keeps raising its own message in
  its `except ZeroDivisionError` clause with `from None`, as today, and does not let
  `divide`'s `"cannot divide 500 by zero"` through (intent open question 2, answered below).
- The exception type stays `ZeroDivisionError`; a caller that catches it is not affected
  (intent Proposed outcome).
- `percent`'s return value for a non-zero `whole` does not change (`percent(1, 4) == 25.0`,
  `percent(7, 100) == 7.0`, per `tests/test_calc.py::test_percent`).
- `divide`'s message stays exactly `"cannot divide 1 by zero"` for `divide(1, 0)`; `add` and
  `mean` do not change at all (intent Proposed outcome). `mean` divides by `len(values)` only
  after rejecting an empty collection, so it never reaches a zero divisor.
- `add`, `divide`, `percent` and `mean` keep their signatures and return values; the only
  behaviour change is the message text of `percent`'s zero-whole error (intent Constraints).
- `tests/test_messages.py` gains one test asserting the exact message of `percent(5, 0)`; its
  existing test `test_divide_by_zero_names_dividend` is not changed (intent Proposed outcome
  and Constraints; coding-standards rule 4: every behaviour change ships with a test that
  fails without it).
- `tests/test_flag.py` is not changed (intent Constraints; CLAUDE.md Layout).
- `tests/test_calc.py`: see the flagged concern. Its test
  `test_percent_zero_whole_error_names_whole` (lines 25–28) asserts the old message
  `"whole must not be zero"` and cannot pass once the first requirement is met. The design
  below updates that one assertion to the new message; the concern records that this departs
  from the intent's constraint that `tests/test_calc.py` is not changed.
- No new dependency; Python 3.10+, type hints on public functions, ruff line length 100
  (CLAUDE.md Conventions; coding-standards rules 5 and 8).
- The guardrail files (`.claude/**`, `CLAUDE.md`, `REVIEW.md`, `sdlc.yaml`, `bands.yaml`) are
  not edited (intent Constraints; definition-of-done "Always").
- No public function is added or removed, so the Layout section of `CLAUDE.md` stays correct
  as it is: its sentence on `percent` ("it raises the same on a zero `whole`") describes the
  exception type, which does not change, and it already names `tests/test_messages.py` as
  the module that "checks the error messages" (intent Affected users and systems; CLAUDE.md
  "Things Claude gets wrong" is about a new public function, which this change does not add).
- None of `sdlc.yaml`'s risk-list items (auth, data migrations, money movement, production
  config) apply: the change touches no authentication, no stored data, no money value and no
  deployment configuration. Security-baseline rule 8 and data-conventions rule 3 therefore
  do not apply.
- security-baseline does not otherwise apply: no endpoint, no new external input (the numeric
  parameters already exist), no secret, no new dependency, no shell or SQL construction, no
  outbound call. The `.env` fixture is not read or touched.
- ux-conventions does not apply: `sample_pkg` is a library with no user interface, and the
  skill exempts such projects. The exception message is the only text a person reads; the
  new wording follows the spirit of rule 4 (it says what happened in terms of the caller's
  own value and drops the internal parameter name `whole`), exactly as change 0016 did for
  `divide`.
- data-conventions does not apply: no schema, storage, migration, log statement or classified
  field is touched. The message echoes only the value of `part`, which the caller supplied to
  the same call, so it creates no new exposure of data the caller does not already hold.
- definition-of-done for phase (b): this spec, `plan.md`, the adversarial verdict and the
  gate (b) evidence are the deliverables; build, test and lint stay green in phase (c)
  (intent Proposed outcome; CLAUDE.md "Verifying your work").

## Design
- `sample_pkg/calc.py`, function `percent`: keep the `try: return divide(part * 100, whole)`
  shape and the `except ZeroDivisionError: raise ZeroDivisionError(...) from None` clause.
  Replace the fixed string `"whole must not be zero"` with an f-string built from `part`,
  `f"cannot express {part} as a percent of zero"`. The condition that raises (a zero `whole`
  detected inside `divide`), the exception type, the suppressed chaining (`from None`) and the
  return value on the non-zero path are unchanged. `part` is rendered as the caller passed it
  (an `int` prints as `5`, a `float` as `1.5` or `1.0`), matching `divide`'s rule.
- `divide`, `add`, `mean` and `sample_pkg/__init__.py`: unchanged. `divide` keeps
  `f"cannot divide {a} by zero"`; `percent` still never surfaces that text.
- `tests/test_messages.py`: gains a second test, beside `test_divide_by_zero_names_dividend`,
  that calls `percent(5, 0)` under `pytest.raises(ZeroDivisionError)` and asserts
  `str(excinfo.value) == "cannot express 5 as a percent of zero"`. The import line widens to
  bring in `percent` from `sample_pkg`, matching the module's existing import style.
- `tests/test_calc.py`, test `test_percent_zero_whole_error_names_whole`: the one assertion
  on the message text changes from `"whole must not be zero"` to
  `"cannot express 1 as a percent of zero"` (that test calls `percent(1, 0)`). Nothing else in
  the module moves. This is the departure recorded under Flagged concerns; if the owner or
  the panel decides otherwise, the alternative is recorded there.
- Error behaviour summary after the change: `percent(x, 0)` raises
  `ZeroDivisionError("cannot express <x> as a percent of zero")` with no chained cause;
  `divide(x, 0)` raises `ZeroDivisionError("cannot divide <x> by zero")`; `mean([])` raises
  `ValueError("mean() requires at least one value")`.

## Open questions from intent
- "How is a non-integer part written in the message, for example `percent(1.5, 0)`? The
  default is Python's own text for the value (`"cannot express 1.5 as a percent of zero"`),
  as change 0016 settled for `divide`; to be confirmed in design." — Answered: confirmed.
  The message is an f-string, `f"cannot express {part} as a percent of zero"`, which renders
  `part` the way `str()` does: `1.5` for `percent(1.5, 0)`, `1.0` for `percent(1.0, 0)`,
  `5` for `percent(5, 0)`. This is the rule `divide` already follows
  (`sample_pkg/calc.py:10`, decided in `changes/0016-.../spec.md` Open questions), so the two
  messages follow one rule, which is the intent's stated problem.
- "Does `percent` keep raising its own message (today it re-raises with `from None`), or let
  `divide`'s message through? The default is its own message, so the reader sees the part,
  not `part * 100`." — Answered: its own message, as the intent prefers. The codebase shows
  why: `percent` calls `divide(part * 100, whole)` (`sample_pkg/calc.py:16`), so letting
  `divide`'s text through would print `"cannot divide 500 by zero"` for `percent(5, 0)`, a
  value the caller never passed. The `except ... raise ... from None` shape stays, so the
  traceback shows one exception with the part the caller passed.

## Flagged concerns
- The intent's Proposed outcome and its Constraints contradict each other on
  `tests/test_calc.py`. The Constraints say `tests/test_calc.py` is not changed, but its
  existing test `test_percent_zero_whole_error_names_whole` (`tests/test_calc.py:25-28`)
  asserts `str(excinfo.value) == "whole must not be zero"` for `percent(1, 0)`, which fails
  as soon as the message becomes `"cannot express 1 as a percent of zero"`. Both cannot hold.
  The design chooses the Proposed outcome (the message changes) and updates that one
  assertion in `tests/test_calc.py` to the new text, because the intent's Problem statement
  is the message, the test is the old behaviour written down, and the change is a `feature`
  (`status.yaml: change_type`), so the test lock of fix-type changes does not apply. This is
  not closed by a policy: coding-standards rule 4 and CLAUDE.md ("fix the code, not the
  test") address a test that regresses, not a test that pins a behaviour the owner asked to
  change, and neither says which of the intent's two statements wins. The alternative, if the
  owner wants `tests/test_calc.py` untouched, is to keep the old message, which abandons the
  intent's Proposed outcome. The owner (or the panel under deferred review) decides which
  statement of the intent gives way.

## Acceptance
- `percent(5, 0)` raises `ZeroDivisionError` and
  `str(exception) == "cannot express 5 as a percent of zero"`, asserted by the new test in
  `tests/test_messages.py`.
- `percent(1, 0)` raises with `str(exception) == "cannot express 1 as a percent of zero"`,
  asserted by the updated `tests/test_calc.py::test_percent_zero_whole_error_names_whole`.
- `percent(1.5, 0)` raises with `str(exception) == "cannot express 1.5 as a percent of zero"`
  (message formatting; consistent with the requirement, not required by a test).
- Existing tests keep passing unchanged: `tests/test_messages.py::test_divide_by_zero_names_dividend`
  (`"cannot divide 1 by zero"`), and in `tests/test_calc.py`: `test_add`,
  `test_divide_by_zero_raises`, `test_percent`, `test_percent_zero_whole_raises`,
  `test_mean`, `test_mean_single_element`, `test_mean_empty`,
  `test_mean_accepts_non_sequence_collection`.
- `tests/test_flag.py` is untouched and `SAMPLE_FAIL` is never set.
- `python -m compileall -q .` exits 0 with no output.
- `python -m pytest` exits 0 with every test passing (11 tests once the new one is added).
- `python -m ruff check .` exits 0 with `All checks passed!`.
