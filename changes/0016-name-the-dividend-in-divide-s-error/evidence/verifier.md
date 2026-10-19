# Verifier report — change 0016, phase (d) test

CI session (`SDLC_GATE_COMMANDS=runner` is set): this session did not run
`python -m compileall -q .`, `python -m pytest`, or `python -m ruff check .` itself. Phase
(d)'s own `build.log`, `test.log` and `lint.log` in this evidence folder each still open
with the line `— deferred to the runner —` (timestamp `2026-10-19T19:36:02Z`): that marker
means this session wrote them minutes ago and the runner — outside the sandbox, after this
session ends — will replace them with real output and write phase (d)'s own gate record.
Per the phase runbook, the evidence of record for this check is the record of the phase
before this one, i.e. gate (c), read below — not phase (d)'s own (deferred) record.

## Commands run

Read, not run (CI session) — read `evidence/gate-c.json`, the runner's run on commit
`1dccdb324c81e0bf92985602a31f99bd2b58ba79` at `2026-10-19T19:34:07Z`. This is the tree phase
(d) started from, not the final tree: the final tree's result is the runner's own run of the
three targets after this session, reported in gate (d)'s own record and the check run
`sdlc/d`; nothing below stands in for that.

- `commands` check in `evidence/gate-c.json`: `ok: true`, `ran_by: "runner"`, no
  `details.deferred` flag present (not deferred).
  - build: `python -m compileall -q .` — exit code `0`, output `""`.
  - test: `python -m pytest` — exit code `0`, output tail:
    `tests/test_calc.py .........                                             [ 81%]`
    `tests/test_flag.py .                                                     [ 90%]`
    `tests/test_messages.py .                                                 [100%]`
    `============================== 11 passed in 0.02s ==============================`
  - lint: `python -m ruff check .` — exit code `0`, output `"All checks passed!\n"`.
- `evidence/build.log` (phase d, this session's own file) first line: `# python -m compileall -q . — deferred to the runner — 2026-10-19T19:36:02Z` — deferred, not a failure; this session wrote it and the runner will replace it.
- `evidence/test.log` (phase d, this session's own file) first line: `# python -m pytest — deferred to the runner — 2026-10-19T19:36:02Z` — deferred, not a failure.
- `evidence/lint.log` (phase d, this session's own file) first line: `# python -m ruff check . — deferred to the runner — 2026-10-19T19:36:02Z` — deferred, not a failure.
- No stale phase-(c) logs with real output remain in this folder (all three were overwritten
  with phase (d)'s deferred markers); gate (c)'s `commands` entry above is the only record of
  phase (c)'s real build/test/lint output, and it is green.

Current `HEAD` (`cd0d0200ef40f3cc64e91989d0791681574a41f6`) is ahead of gate (c)'s recorded
`head` by two evidence/bookkeeping commits only (`79ba739` gate (c) evidence, `cd0d020` run(c)
spend record); no change to `sample_pkg/calc.py` or `tests/` happened after the commit gate
(c) verified, so gate (c)'s green commands entry still covers the code on this tree.

## Behavior exercised

Direct script call (no test runner, no `.env*` read), run in this session:

```
from sample_pkg import divide, percent
divide(1, 0)    -> ZeroDivisionError: cannot divide 1 by zero
divide(1.5, 0)  -> ZeroDivisionError: cannot divide 1.5 by zero
divide(1.0, 0)  -> ZeroDivisionError: cannot divide 1.0 by zero
percent(5, 0)   -> ZeroDivisionError: whole must not be zero
divide(10, 2)   -> 5.0
```

Output observed, verbatim:
```
1 -> cannot divide 1 by zero
1.5 -> cannot divide 1.5 by zero
1.0 -> cannot divide 1.0 by zero
percent -> whole must not be zero
divide(10,2) -> 5.0
```

This exercises: the changed path (`divide` on a zero divisor, the spec's Acceptance
examples `divide(1,0)`, `divide(1.5,0)`, `divide(1.0,0)`), one neighboring flow
(`percent` on a zero `whole`, confirming its message is unchanged and independent of
`divide`'s text), and one input just outside the changed path (`divide(10, 2)`, the
non-zero-divisor case, confirming the return value is untouched).

Also read the diff directly:
- `sample_pkg/calc.py`: `divide` raises `ZeroDivisionError(f"cannot divide {a} by zero")` —
  matches plan.md step 1 and spec.md Design exactly (f-string on `a`, not `b`).
- `tests/test_messages.py`: new file, `test_divide_by_zero_names_dividend` asserts
  `divide(1, 0)` raises `ZeroDivisionError` with `str(excinfo.value) ==
  "cannot divide 1 by zero"` — matches plan.md step 2 and spec.md's new-test-module
  requirement exactly (name is indicative in plan.md; the chosen name matches its intent).
- `percent` and `mean` in `sample_pkg/calc.py` are byte-for-byte unchanged from what
  plan.md says stays untouched.
- `CLAUDE.md` Layout section: no new public function was added (only a string literal
  changed inside existing `divide`), so the "Things Claude gets wrong" rule about updating
  Layout on a new public function does not apply here, consistent with spec.md's own note.

## Not exercised

- Phase (d)'s own build/test/lint targets on the final tree — not run in this CI session;
  the runner runs them once after this session and reports the result in gate (d)'s own
  record and the check run `sdlc/d`.
- Windows (this session ran on Linux only); the reverse platform gap does not apply the
  other way since no platform-specific code is touched.
- `tests/test_calc.py` and `tests/test_flag.py` were not re-run in this session (only read
  and confirmed unchanged); their last known-good run is gate (c)'s `commands` entry above
  (11 passed, including the new `test_messages.py`).
- Non-numeric or exotic inputs to `divide` (e.g. complex numbers, `Decimal`) were not tried;
  the spec's Acceptance section names only `1`, `1.5`, `1.0` as dividends and this report
  does not speak to behavior outside that set.
- `mean`'s call path into `divide` was not separately exercised in this session (the spec
  and plan both state, and the code confirms by reading, that `mean` never reaches a zero
  divisor), so this report does not independently demonstrate that invariant by execution.

## Mismatches with plan.md / spec.md

None found. `sample_pkg/calc.py`'s `divide` and `tests/test_messages.py` match plan.md's
"Files that change" / "Order of work" and spec.md's Design / Acceptance sections exactly,
confirmed both by reading the diff and by direct execution of the four cases above.

## Verdict

matches the plan
