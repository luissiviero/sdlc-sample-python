# Spec: add a percent helper to sample_pkg
Change id: 0001. Status: proposed. Produced by: sdlc plugin 0.2.4, /sdlc-design prompt v1 (article p.14). Skills: coding-standards, security-baseline, ux-conventions, data-conventions, definition-of-done (plugin 0.2.4); overrides: none

## Requirements
- `sample_pkg/calc.py` adds `percent(part: float, whole: float) -> float` returning `part` as a
  percentage of `whole`; `percent(1, 4)` returns `25.0` (intent Proposed outcome). An exactly
  representable percentage comes back exact: `percent(7, 100)` returns `7.0`, not
  `7.000000000000001` (intent Problem: "`part` as a percentage of `whole`"; adversarial review
  of round 1).
- A zero `whole` raises `ZeroDivisionError`, the same exception type `divide` raises for a zero
  divisor (intent Proposed outcome).
- `percent` is exported from `sample_pkg/__init__.py` and added to `__all__`, alongside `add`
  and `divide` (intent Proposed outcome).
- `tests/test_calc.py` gets a normal case and a zero-`whole` case for `percent` (intent Proposed
  outcome; coding-standards rule 4: every behaviour change ships with a test that fails
  without it).
- `add` and `divide` keep their current signatures and behaviour; `tests/test_flag.py` stays
  untouched (intent Constraints).
- No new dependency; plain Python 3.10+ with a type hint on the public function, line length
  100 (CLAUDE.md Conventions; coding-standards rule 5 — no dependency is added, so the rule is
  satisfied trivially).
- `python -m compileall -q .`, `python -m pytest` and `python -m ruff check .` all stay green
  (CLAUDE.md Commands; definition-of-done "(b) design" and "(c) build" targets).
- Coding-standards: applied — rule 2 (match `calc.py`'s existing style: `add` and `divide` have
  no docstrings, so `percent` has none either), rule 4 (test coverage above), rule 7 (small,
  explicit function, no dead code).
- Security-baseline: does not fully apply — `percent` is pure arithmetic on its two arguments;
  there is no endpoint, external input parsing, secret, shell/SQL/file access or new
  dependency for rules 1–3 and 6–7 to constrain. Rule 8 was checked against `sdlc.yaml`
  `risk_list`: none of its items is touched.
- Data-conventions: does not apply — no stored field, schema, migration, event contract or
  personal data is introduced.
- UX-conventions: does not apply — `sample_pkg` is a library with no user-facing screen, CLI
  output or displayed error message; the raised `ZeroDivisionError` is a Python API contract,
  not UI copy.

## Design
- `sample_pkg/calc.py`: add `percent(part: float, whole: float) -> float` after `divide`,
  implemented as `return divide(part * 100, whole)`. `part` is scaled before the division, so
  an exact percentage is not perturbed by float rounding of the quotient (`percent(7, 100)` is
  `7.0`; `divide(part, whole) * 100` would give `7.000000000000001`). Reusing `divide` gives
  the zero-check one implementation (see Open questions below) and keeps the file's existing
  two-function, no-docstring style.
- `sample_pkg/__init__.py`: import and re-export `percent` next to `add` and `divide`; add it
  to `__all__` in the same order the functions are defined in `calc.py`.
- Error behaviour: the `ZeroDivisionError` raised for a zero `whole` is the same exception
  `divide` raises ("b must not be zero"), inherited by calling `divide` rather than
  re-implemented (see Flagged concerns).
- Nothing else in the package changes: `add`, `divide` and their signatures, `tests/test_flag.py`,
  and the `deploy`/`maintain` configuration in `sdlc.yaml` stay as they are.
- `CLAUDE.md`'s Layout section is not edited in this run (it is a guardrail file); the
  one-line addition describing `percent` is proposed as a suggestion in the build-phase PR
  body for the owner to apply, per intent's Affected users and systems.

## Open questions from intent
- "Should `percent` reuse `divide` internally so the zero-total error has one source, or check
  for zero itself?" — Answered: reuse `divide` (`percent = divide(part * 100, whole)`). This
  matches `calc.py`'s existing pattern where `divide` is the only place that checks for a zero
  divisor (coding-standards rule 2: match the surrounding code), so the zero-check keeps one
  implementation instead of two.
- "Should the result be rounded (for example to two decimals) or left as the raw float?" —
  Answered from intent.md's own Constraints, which already settle it: "Keep it minimal: one
  function, no rounding options or formatting features." `percent` returns the raw float from
  `divide(part * 100, whole)`, no rounding.

## Flagged concerns
- [x] Reusing `divide` means the zero-`whole` `ZeroDivisionError` carries `divide`'s own
  message, "b must not be zero", which names `divide`'s parameter (`b`) rather than
  `percent`'s (`whole`). This was a guess made because the intent is silent on message
  wording. Decided by the owner (2026-09-22): keep the reuse of `divide` and accept the
  inherited message. The intent requires the same exception type only, not specific message
  text, and `divide` stays the single zero-check in the package; `percent` does not raise its
  own error.

## Acceptance
- `tests/test_calc.py` passes two new cases: a normal case asserting `percent(1, 4) == 25.0`
  and the exact-percentage input `percent(7, 100) == 7.0`, and `pytest.raises(ZeroDivisionError)`
  for a zero `whole`.
- `python -m pytest` reports all 5 tests passing (the existing `test_add`,
  `test_divide_by_zero_raises` and `test_intentional_failure_behind_flag`, plus the 2 new
  `percent` cases), exit code 0.
- `python -m compileall -q .` finishes with no output, exit code 0.
- `python -m ruff check .` reports `All checks passed!`, exit code 0.
- `sample_pkg/__init__.py` exports `percent` and lists it in `__all__`.
