# Spec: name the zero whole in percent's error
Change id: 0015. Status: proposed. Produced by: sdlc plugin 1.0.10, /sdlc-design prompt v1 (article p.14). Skills: coding-standards, security-baseline, ux-conventions, data-conventions, definition-of-done (plugin 1.0.10); overrides: none

## Requirements
- `percent(part, 0)` raises `ZeroDivisionError` whose message is exactly `"whole must not be zero"`, naming the parameter the caller passed.
- `divide(a, 0)` is unchanged: it still raises `ZeroDivisionError("b must not be zero")`.
- The exception type raised by `percent` on a zero `whole` stays `ZeroDivisionError` (coding-standards rule 2: match the existing error-handling idiom; callers catching `ZeroDivisionError` today keep working).
- Signatures and return values of `add`, `divide`, `percent` and `mean` are unchanged.
- A new test in `tests/test_calc.py` asserts the exact message of `percent(1, 0)`'s `ZeroDivisionError`; written before the fix and failing against the current code (change type `fix`; coding-standards rule 4, "every behavior change ships with a test that fails without it").
- No new dependency (coding-standards rule 5; security-baseline rule 6).
- `python -m compileall -q .`, `python -m pytest` and `python -m ruff check .` stay green (CLAUDE.md "Verifying your work").
- `tests/test_flag.py` and every guardrail file (`.claude/**`, `CLAUDE.md`, `REVIEW.md`, `sdlc.yaml`) stay untouched.
- `ux-conventions` does not apply: this change raises a library exception, not a user interface, screen or CLI surface.
- `data-conventions` does not apply: no stored field, schema, migration, pipeline or personal data is touched.
- `security-baseline` applies only through "no new dependency" (above): there is no endpoint, authentication, secret or external input in this change.
- No `sdlc.yaml: risk_list` item (auth, data migrations, money movement, production config) is touched.

## Design
- In `sample_pkg/calc.py`, `percent(part, whole)` catches the `ZeroDivisionError` that `divide(part * 100, whole)` raises when `whole == 0`, and re-raises `ZeroDivisionError("whole must not be zero") from None`. The `from None` suppresses chaining onto `divide`'s exception, so a caller's traceback shows only `percent`'s own error, not `divide`'s internal one.
- `divide()` itself is not changed: it keeps raising `ZeroDivisionError("b must not be zero")` on `b == 0`, so `tests/test_divide_by_zero_raises` and `mean`'s behavior (which also goes through `divide`) are unaffected.
- No change to `add`, `mean`, `sample_pkg/__init__.py`'s re-exports, or any call site: `percent` has no other callers in this package.
- No public function is added or removed, so the two `CLAUDE.md` Layout entries for `sample_pkg/calc.py` and `tests/test_calc.py` stay accurate as written (the intent already notes this).

## Open questions from intent
- "Should `percent` check `whole` itself before calling `divide`, or catch the `ZeroDivisionError` from `divide` and raise a new one with the right message?" — Answered: catch the `ZeroDivisionError` from `divide` and re-raise with the new message (see Design). A pre-check (`if whole == 0: raise ...` inside `percent`, before calling `divide`) would duplicate the zero-check condition `divide` already owns in a second place; catching keeps that condition in one place and only changes the message `percent` presents (coding-standards rule 2, match the existing idiom rather than introduce a parallel one). The intent notes the proposed outcome holds either way, so this is a design choice, not an open requirement.

## Flagged concerns
- none

## Acceptance
- `tests/test_calc.py` has a test (e.g. `test_percent_zero_whole_error_names_whole`) asserting the exact string `"whole must not be zero"` from `percent(1, 0)`'s `ZeroDivisionError`; it fails against the current code and passes after the fix.
- The existing `test_percent_zero_whole_raises` and `test_divide_by_zero_raises` keep passing unchanged.
- `python -m pytest` reports all tests passed (10: the 9 current plus the new one), exit code 0.
- `python -m compileall -q .` finishes with no output, exit code 0.
- `python -m ruff check .` reports `All checks passed!`, exit code 0.
