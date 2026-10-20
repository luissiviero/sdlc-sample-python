# Intent: name the part in percent's zero-whole error
Author: Luis Siviero (owner). Status: proposed. Change id: 0017. Entry route: idea.

## Problem
`percent(5, 0)` raises `ZeroDivisionError("whole must not be zero")`. Since change 0016,
`divide(1, 0)` says which number was being divided (`"cannot divide 1 by zero"`), but
`percent` still names only its parameter: whoever reads the traceback learns that some whole
was zero, not which part was being expressed as a percent of it, and has to go back to the
calling code to find out. The two messages now follow different rules.

This is also the sample's first change on plugin 1.0.14. Its runs are the first live reading
of R7 (framework NOTES §51): whether CI reaches `claude-opus-5-5` and `claude-fable-5-1` as
the sample's `sdlc.yaml` model rows ask, whether CLI 2.1.278 honours the Fable pin, and
where the in-run reviewer and the panel advocate run. It is also the sample change that
framework R56 waits for. The code change is kept small on purpose.

## Proposed outcome
- `percent(5, 0)` raises `ZeroDivisionError` with the message
  `"cannot express 5 as a percent of zero"`: the message names the part.
- The exception type stays `ZeroDivisionError`, so callers that catch it are not affected.
- `percent`'s result for a non-zero `whole` does not change, and neither do `divide`'s
  message (`"cannot divide 1 by zero"`), `mean`'s or `add`'s behaviour.
- `tests/test_messages.py` gains a test that checks the message of `percent(5, 0)`.
- Build, test and lint stay green: `python -m compileall -q .`, `python -m pytest`,
  `python -m ruff check .`.

## Affected users and systems
- The owner and anyone importing `sample_pkg` who reads the error of a zero `whole`.
- Files: `sample_pkg/calc.py` (the message in `percent`) and `tests/test_messages.py`
  (one added test).
- No public function is added or removed, so the Layout section of `CLAUDE.md` stays
  correct; its sentence on `percent` ("it raises the same on a zero `whole`") describes the
  exception type, which does not change.
- No services, data stores or external parties.

## Constraints
- No new dependencies; plain Python 3.10+ with type hints, line length 100 (ruff).
- `add`, `divide`, `percent` and `mean` keep their signatures and return values; only the
  message of `percent`'s zero-whole error changes.
- The existing test in `tests/test_messages.py`, `tests/test_calc.py` and
  `tests/test_flag.py` are not changed.
- The guardrail files (`.claude/**`, `CLAUDE.md`, `REVIEW.md`, `sdlc.yaml`, `bands.yaml`)
  are not edited.

## Open questions
- How is a non-integer part written in the message, for example `percent(1.5, 0)`? The
  default is Python's own text for the value (`"cannot express 1.5 as a percent of zero"`),
  as change 0016 settled for `divide`; to be confirmed in design.
- Does `percent` keep raising its own message (today it re-raises with `from None`), or let
  `divide`'s message through? The default is its own message, so the reader sees the part,
  not `part * 100`.
