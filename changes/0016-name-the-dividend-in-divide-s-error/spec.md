# Spec: name the dividend in divide's error
Change id: 0016. Status: proposed. Produced by: sdlc plugin 1.0.12, /sdlc-design prompt v1 (article p.14). Skills: coding-standards, security-baseline, ux-conventions, data-conventions, definition-of-done (plugin 1.0.12); overrides: none

## Requirements
- `divide(1, 0)` raises `ZeroDivisionError` with the message `"cannot divide 1 by zero"` (intent Proposed outcome).
- The message names the dividend `a` using Python's own text for the value (`str`/f-string
  conversion), so `divide(1.5, 0)` raises `"cannot divide 1.5 by zero"` and `divide(1.0, 0)`
  raises `"cannot divide 1.0 by zero"` (intent open question, answered below).
- The exception type stays `ZeroDivisionError`; no caller that catches it is affected
  (intent Proposed outcome).
- `percent`'s message on a zero `whole` stays exactly `"whole must not be zero"`, unchanged
  (intent Proposed outcome). `percent` already raises its own literal message in its
  `except ZeroDivisionError` clause (`sample_pkg/calc.py:17-18`), independent of the text
  `divide` raises, so this requirement needs no code change in `percent` — only in `divide`.
- `mean`'s behaviour does not change: its divisor is `len(values)`, which is never zero once
  the empty-collection check (`if not values: raise ValueError(...)`) has passed, so it never
  observes `divide`'s `ZeroDivisionError` at all (intent Proposed outcome).
- `add`, `divide`, `percent` and `mean` keep their signatures and return values; only the
  message text of `divide`'s zero-divisor error changes (intent Constraints).
- A new test module verifies the exact message of `divide(1, 0)`; `tests/test_calc.py` and
  `tests/test_flag.py` are not touched (intent Constraints; coding-standards rule 4: every
  behaviour change ships with a test that fails without it).
- No new dependency; Python 3.10+, type hints on public functions, ruff line length 100
  (CLAUDE.md Conventions; coding-standards rules 5 and 8).
- Guardrail files (`.claude/**`, `CLAUDE.md`, `REVIEW.md`, `sdlc.yaml`, `bands.yaml`) are not
  edited (intent Constraints; definition-of-done "Always").
- No public function is added or removed, so the Layout section of `CLAUDE.md` stays
  correct as-is: it already names `tests/test_messages.py` as the file that "checks the
  error messages" (CLAUDE.md Layout, added in PR #76) and its one-line description of
  `divide` does not quote the exact message text (intent Affected users and systems).
- None of `sdlc.yaml`'s risk-list items (auth, data migrations, money movement, production
  config) apply to this change: it touches no authentication, no stored data, no money
  value and no deployment configuration — security-baseline rule 8 and data-conventions
  rule 3 therefore do not apply.
- security-baseline otherwise does not apply beyond the risk-list check above: no endpoint,
  no external input parsing beyond the existing numeric parameters, no secret, no new
  dependency, no shell/SQL construction, no outbound network call is touched.
- ux-conventions does not apply: `sample_pkg` is a library with no user interface (the skill
  itself exempts "projects without a user interface"); the only user-facing surface is the
  exception message text read by a caller or developer. The change is consistent with rule
  4's intent even though the rule targets UI copy: it drops the internal parameter name `b`
  in favour of the caller's own value, so the message still "says what happened" without
  exposing an internal name any more than the current message's `b` already does.
- data-conventions does not apply: no schema, storage, migration, log statement or classified
  field is touched. The message echoes only the value of `a`, which the caller already
  supplied as an argument to the same call — the message creates no new exposure of data
  the caller does not already hold.

## Design
- `sample_pkg/calc.py`, function `divide`: change the raised message from the fixed string
  `"b must not be zero"` to one built from the dividend, `a`, using an f-string, so the
  message is `f"cannot divide {a} by zero"`. The condition that raises (`if b == 0`), the
  exception type (`ZeroDivisionError`), and the return value on the non-zero path are
  unchanged.
- `sample_pkg/__init__.py`: unchanged — it re-exports `add`, `divide`, `percent`, `mean`,
  none of whose signatures move.
- `percent`: unchanged. It already catches `divide`'s `ZeroDivisionError` and re-raises its
  own `"whole must not be zero"` via `raise ... from None`, so it never surfaces `divide`'s
  message text to its own callers.
- `mean`: unchanged. It calls `divide(sum(values), len(values))` only after `values` is
  known non-empty, so `b` (`len(values)`) is never zero and `divide`'s new message is never
  constructed on that path.
- New test module under `tests/`: asserts `divide(1, 0)` raises `ZeroDivisionError` whose
  `str(...)` is exactly `"cannot divide 1 by zero"`. (File name, placement among other test
  modules, and whether it also re-asserts `percent`'s unchanged message are implementation
  order-of-work, for `plan.md`.)

## Open questions from intent
- "How is a non-integer dividend written in the message, for example `divide(1.5, 0)` or
  `divide(1.0, 0)`? The default is Python's own text for the value (`"cannot divide 1.5 by
  zero"`, `"cannot divide 1.0 by zero"`); to be settled in design." — Answered: adopt the
  intent's own stated default. The message is built with an f-string, `f"cannot divide {a}
  by zero"`, which renders a value the same way `str()` does — exactly the two examples the
  intent gives. No codebase convention conflicts with this (no other message in
  `sample_pkg/calc.py` formats a value today), so there is nothing to choose between.

## Flagged concerns
none

## Acceptance
- `divide(1, 0)` raises `ZeroDivisionError` and `str(exception) == "cannot divide 1 by zero"`.
- `divide(1.5, 0)` raises with `str(exception) == "cannot divide 1.5 by zero"` and
  `divide(1.0, 0)` raises with `str(exception) == "cannot divide 1.0 by zero"` (message
  formatting, not required by an existing test but consistent with the requirement above).
- Existing behaviour tests keep passing unchanged: `test_divide_by_zero_raises`,
  `test_percent`, `test_percent_zero_whole_raises`,
  `test_percent_zero_whole_error_names_whole` (asserts `"whole must not be zero"`),
  `test_mean`, `test_mean_single_element`, `test_mean_empty`,
  `test_mean_accepts_non_sequence_collection`, `test_add` — all in `tests/test_calc.py`,
  untouched.
- `tests/test_flag.py` is untouched and its `SAMPLE_FAIL=1`-gated behaviour is unaffected.
- `python -m compileall -q .` exits 0 with no output.
- `python -m pytest` exits 0, every test passing, including the new message test.
- `python -m ruff check .` exits 0 with `All checks passed!`.
