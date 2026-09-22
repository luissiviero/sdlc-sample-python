# Plan: add a percent helper to sample_pkg (from intent.md 2026-09-20, spec.md 2026-09-22)

## Files that change
- `sample_pkg/calc.py` — add `percent(part: float, whole: float) -> float`, defined after
  `divide`, implemented as `return divide(part, whole) * 100`.
- `sample_pkg/__init__.py` — import `percent` from `.calc` alongside `add` and `divide`; add
  `"percent"` to `__all__` after `"divide"`.
- `tests/test_calc.py` — add `test_percent` (a normal case, e.g. `percent(1, 4) == 25.0`) and
  `test_percent_zero_whole_raises` (`pytest.raises(ZeroDivisionError): percent(1, 0)`),
  following the existing `test_add` / `test_divide_by_zero_raises` style (plain `assert` /
  `pytest.raises`, no fixtures).

No other file changes. `CLAUDE.md`'s Layout line for `percent` is not committed here (it is a
guardrail file); it is text proposed in the phase-(e) build PR body for the owner to apply
themselves.

## Order of work
1. In `sample_pkg/calc.py`, add:
   ```python
   def percent(part: float, whole: float) -> float:
       return divide(part, whole) * 100
   ```
   directly after the existing `divide` function.
2. In `sample_pkg/__init__.py`, change `from .calc import add, divide` to
   `from .calc import add, divide, percent` and `__all__ = ["add", "divide"]` to
   `__all__ = ["add", "divide", "percent"]`.
3. In `tests/test_calc.py`, add `test_percent` and `test_percent_zero_whole_raises` after the
   existing two tests, importing `percent` alongside `add` and `divide` in the existing
   `from sample_pkg import ...` line.
4. Run the three project commands from `sdlc.yaml` and confirm the healthy output in
   `CLAUDE.md`: `python -m compileall -q .` (no output), `python -m pytest` (`5 passed`),
   `python -m ruff check .` (`All checks passed!`).

Each step is one commit-sized change; step 1 and step 2 land together in one commit since
`__init__.py` would otherwise import a name that does not exist yet.

## Risks
- What this could break (interrogation Q1): `percent` is new and additive; nothing currently
  imports it, so no existing caller is affected. The only two things it touches that already
  exist are `divide` (called, not modified) and `sample_pkg/__init__.py`'s `__all__` list
  (appended to, not reordered) — both changes are additive, so `add`, `divide` and their
  current callers/tests keep working unchanged.
- Riskiest step (interrogation Q2): step 1, because `percent` delegates to `divide` rather than
  checking for a zero `whole` itself. If `divide`'s zero-check or exception type ever changes,
  `percent`'s behaviour changes silently with it. Mitigation: `test_percent_zero_whole_raises`
  pins `percent`'s contract (raises `ZeroDivisionError` on a zero `whole`) independently of
  `divide`'s implementation, so a future change to `divide` that breaks this contract fails
  `percent`'s own test, not just `divide`'s.
- No new dependency, no data migration, no auth, money-movement or production-config surface —
  none of `sdlc.yaml`'s `risk_list` items apply, so this change does not park on that check.
- The message text of the `ZeroDivisionError` ("b must not be zero") is `divide`'s, not
  `percent`'s. spec.md's Flagged concerns records the owner's decision (2026-09-22): keep the
  delegation to `divide` and accept the inherited message. Step 1 therefore stays as written;
  `percent` does not raise its own error, and no test asserts the message text.

## Options not taken
- A local zero-check inside `percent` instead of delegating to `divide` (interrogation Q3):
  considered, not chosen, because it would duplicate the zero-check logic that already exists
  in `divide`, and spec.md's Design section decided to keep the zero-check in one place
  (coding-standards rule 2: match the surrounding code). The owner confirmed this choice by
  closing the Flagged concern in spec.md (2026-09-22): the inherited message is accepted.
- Rounding the result (e.g. `round(value, 2)`): considered, not chosen, because intent.md's
  Constraints rule it out ("no rounding options or formatting features").
- A docstring on `percent`: considered, not chosen, because neither `add` nor `divide` has one
  and coding-standards rule 2 says to match the surrounding code.

## Proof
- `tests/test_calc.py::test_percent` — new test, written in step 3 — asserts a normal case
  equivalent to `percent(1, 4) == 25.0`.
- `tests/test_calc.py::test_percent_zero_whole_raises` — new test, written in step 3 — asserts
  `percent(1, 0)` raises `ZeroDivisionError`, using `pytest.raises`.
- `python -m pytest` — existing target, run in step 4 — must report `5 passed` (the 2 existing
  `test_calc.py` cases, the 2 new `percent` cases, and `test_flag.py`'s one case), exit code 0.
- `python -m compileall -q .` — existing target, run in step 4 — must finish with no output,
  exit code 0.
- `python -m ruff check .` — existing target, run in step 4 — must report `All checks passed!`,
  exit code 0.
- An engineer who has not seen this conversation can implement the change from Order of work
  alone (interrogation Q4): the exact function body, the exact import/`__all__` edit, and the
  two test names and their assertions are given above; nothing here depends on context outside
  this file, spec.md and the existing source.
