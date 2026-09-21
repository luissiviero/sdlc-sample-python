# Intent: add a percent helper to sample_pkg
Author: Luis Siviero (owner). Status: draft. Change id: 0001. Entry route: idea.

## Problem
`sample_pkg` exposes `add` and `divide` only. Anyone who wants a percentage today has to
combine `divide` with a multiplication by hand and decide for themselves how to treat a zero
total. That is a small nuisance, but the project's job is to exercise the SDLC framework on a
realistic feature change, and there is no second feature to walk through the phases yet.

## Proposed outcome
- `sample_pkg` exports a `percent(part, whole)` function that returns `part` as a percentage
  of `whole` (for example `percent(1, 4)` returns `25.0`).
- A zero `whole` raises `ZeroDivisionError`, the same behaviour as `divide`.
- The function is listed in `sample_pkg/__init__.py` and `__all__`, and `tests/test_calc.py`
  covers a normal case and the zero case.
- Build, test and lint stay green: `python -m compileall -q .`, `python -m pytest`,
  `python -m ruff check .`.

## Affected users and systems
- The owner and anyone importing `sample_pkg`.
- Files: `sample_pkg/calc.py`, `sample_pkg/__init__.py`, `tests/test_calc.py`, and the
  Layout section of `CLAUDE.md` (a one-line update, proposed in the PR for the owner).
- No services, data stores or external parties.

## Constraints
- No new dependencies; plain Python 3.10+ with type hints, line length 100 (ruff).
- `add` and `divide` keep their signatures and behaviour.
- `tests/test_flag.py` stays untouched.
- Keep it minimal: one function, no rounding options or formatting features.
- The guardrail files (`.claude/**`, `CLAUDE.md`, `REVIEW.md`, `sdlc.yaml`) are not edited in
  the run; the CLAUDE.md line is proposed for the owner in the build PR.

## Open questions
- Should `percent` reuse `divide` internally so the zero-total error has one source, or
  check for zero itself? To be settled in design.
- Should the result be rounded (for example to two decimals) or left as the raw float? The
  default proposed here is the raw float.
