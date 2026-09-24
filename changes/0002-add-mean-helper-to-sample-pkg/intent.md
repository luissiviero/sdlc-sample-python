# Intent: add a mean helper to sample_pkg
Author: Luis Siviero (owner). Status: proposed. Change id: 0002. Entry route: idea.

## Problem
`sample_pkg` exposes `add`, `divide` and `percent`. Averaging a list of numbers today means
`divide(sum(values), len(values))` by hand, and each caller decides on their own what an
empty list means. The project's job is to exercise the SDLC framework on realistic feature
changes, and this one is the first to run under **deferred review** (`status.yaml:
review_override: deferred`, decision 21, plugin 0.2.14): its purpose is as much to see the
review panel settle the open questions below inside the design phase as to add the function.

## Proposed outcome
- `sample_pkg` exports a `mean(values)` function that returns the arithmetic mean of a
  sequence of numbers as a float (for example `mean([1, 2, 3, 4])` returns `2.5`).
- The behaviour on an empty sequence is decided in design (open question below) and stated
  in the docstring and covered by a test.
- The function is listed in `sample_pkg/__init__.py` and `__all__`, and `tests/test_calc.py`
  covers a normal case, a single-element case and the empty case.
- Build, test and lint stay green: `python -m compileall -q .`, `python -m pytest`,
  `python -m ruff check .`.
- The design phase's spec closes its flagged concerns as `decided (by panel): …`, the
  design PR opens with "Decisions taken for you (N)", and `changes/0002-…/evidence/`
  carries `decisions-b.md` and the `panel/` files.

## Affected users and systems
- The owner and anyone importing `sample_pkg`.
- Files: `sample_pkg/calc.py`, `sample_pkg/__init__.py`, `tests/test_calc.py`, and the
  Layout section of `CLAUDE.md` (a one-line update, proposed in the PR for the owner).
- No services, data stores or external parties.

## Constraints
- No new dependencies; plain Python 3.10+ with type hints, line length 100 (ruff). The
  standard library's `statistics.mean` is not to be wrapped: the point is one small function
  of our own, consistent with `divide` and `percent`.
- `add`, `divide` and `percent` keep their signatures and behaviour.
- `tests/test_flag.py` stays untouched.
- Keep it minimal: one function, no weights, no options.
- The guardrail files (`.claude/**`, `CLAUDE.md`, `REVIEW.md`, `sdlc.yaml`) are not edited in
  the run; the CLAUDE.md line is proposed for the owner in the build PR.

## Open questions
- Empty sequence: raise `ZeroDivisionError` by going through `divide(sum, len)` (consistent
  with `percent(1, 0)`), raise `ValueError` (what `statistics.mean` does), or return `0.0`?
  The owner has no preference: to be settled in design.
- Should `mean` accept any iterable (a generator is consumed once, so it must be
  materialised first) or only a `Sequence`? To be settled in design.
