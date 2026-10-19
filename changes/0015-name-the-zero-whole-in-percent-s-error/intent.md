# Intent: name the zero whole in percent's error
Author: Luis Siviero (owner). Status: proposed. Change id: 0015. Entry route: idea.

## Problem
`percent(part, whole)` goes through `divide(part * 100, whole)`, so `percent(1, 0)` raises
`ZeroDivisionError("b must not be zero")`. The caller passed `whole`, not `b`: the message
names a parameter of another function, and whoever reads the traceback has to open
`calc.py` to learn which argument was wrong.

This is also the sample's first change after its upgrade to plugin 1.0.10 and the project's
GitHub App. Its runs are the live proof the framework still owes (framework NOTES §47, "Not
verified yet"): the App's pushes starting CI with no approval click, the review request
reaching the owner, the build caps of the new workflows. The fix is kept small on purpose;
the runs matter more than the code.

## Proposed outcome
- `percent(1, 0)` raises `ZeroDivisionError` whose message names `whole`, for example
  `"whole must not be zero"`.
- The exception type stays `ZeroDivisionError`, so existing callers that catch it are not
  affected.
- `divide(1, 0)` keeps its current message, `"b must not be zero"`.
- A test in `tests/test_calc.py` checks the message of `percent(1, 0)`; it is written first
  and fails before the fix (change type: fix).
- Build, test and lint stay green: `python -m compileall -q .`, `python -m pytest`,
  `python -m ruff check .`.

## Affected users and systems
- The owner and anyone importing `sample_pkg` who reads the error of a zero `whole`.
- Files: `sample_pkg/calc.py` and `tests/test_calc.py`.
- No public function is added or removed, so the Layout section of `CLAUDE.md` stays
  correct ("raises the same on a zero `whole`" still means the same exception type).
- No services, data stores or external parties.

## Constraints
- No new dependencies; plain Python 3.10+ with type hints, line length 100 (ruff).
- `add`, `divide`, `percent` and `mean` keep their signatures and return values; only the
  message of `percent`'s zero-`whole` error changes.
- `tests/test_flag.py` stays untouched.
- The guardrail files (`.claude/**`, `CLAUDE.md`, `REVIEW.md`, `sdlc.yaml`, `bands.yaml`)
  are not edited.

## Open questions
- Should `percent` check `whole` itself before calling `divide`, or catch the
  `ZeroDivisionError` from `divide` and raise a new one with the right message? To be
  settled in design; the outcome above holds either way.
