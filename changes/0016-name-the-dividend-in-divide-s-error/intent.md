# Intent: name the dividend in divide's error
Author: Luis Siviero (owner). Status: proposed. Change id: 0016. Entry route: idea.

## Problem
`divide(1, 0)` raises `ZeroDivisionError("b must not be zero")`. The message names a
parameter, not the call: whoever reads the traceback learns that some divisor was zero but
not what was being divided, and has to go back to the calling code to find out.

This is also the sample's next change on plugin 1.0.12. Its runs are the live checks the
framework still owes (framework NOTES §49, "Still not verified"): the fast lane on an
intent PR the owner opens, not as a draft; the review request reaching the owner's phone at
gate (e); and, if the runs meet them, the 1.0.10 paths. The code change is kept small on
purpose.

## Proposed outcome
- `divide(1, 0)` raises `ZeroDivisionError` with the message `"cannot divide 1 by zero"`:
  the message names the dividend that was being divided.
- The exception type stays `ZeroDivisionError`, so callers that catch it are not affected.
- `percent`'s message on a zero `whole` stays `"whole must not be zero"`, and `mean`'s
  behaviour does not change (its divisor is never zero).
- A new test file, `tests/test_messages.py`, checks the message of `divide(1, 0)`.
- Build, test and lint stay green: `python -m compileall -q .`, `python -m pytest`,
  `python -m ruff check .`.

## Affected users and systems
- The owner and anyone importing `sample_pkg` who reads the error of a zero divisor.
- Files: `sample_pkg/calc.py` (the message in `divide`) and the new
  `tests/test_messages.py`.
- No public function is added or removed, and the Layout section of `CLAUDE.md` already
  covers `tests/test_messages.py` (the owner's PR #76), so it stays correct.
- No services, data stores or external parties.

## Constraints
- No new dependencies; plain Python 3.10+ with type hints, line length 100 (ruff).
- `add`, `divide`, `percent` and `mean` keep their signatures and return values; only the
  message of `divide`'s zero-divisor error changes.
- `tests/test_calc.py` and `tests/test_flag.py` are not touched.
- The guardrail files (`.claude/**`, `CLAUDE.md`, `REVIEW.md`, `sdlc.yaml`, `bands.yaml`)
  are not edited.

## Open questions
- How is a non-integer dividend written in the message, for example `divide(1.5, 0)` or
  `divide(1.0, 0)`? The default is Python's own text for the value (`"cannot divide 1.5 by
  zero"`, `"cannot divide 1.0 by zero"`); to be settled in design.
