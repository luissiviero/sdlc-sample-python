**Commands run** (CI session, `SDLC_GATE_COMMANDS=runner` is set — the three gate targets were not run in this session; read, not run):

- Read `evidence/gate-b.json` — the runner's run on commit `0e4fed526e8d7ec6e145d86446c8e9671a8bebdb` ("design(0015): Name the zero whole in percent's error") of `2026-10-19T14:19:30Z`. This is the record of the phase before (c), i.e. phase (b); phase (c) has no `gate-c.json` of its own yet in this evidence directory (this session is producing (c)'s result). This is the tree phase (c) started from, not the final tree: the final tree's result is the runner's own run after this session, shown in check run `sdlc/d` and in `gate-c.json`'s own record; nothing reported here stands in for that.
  - `commands` check: `ok: true`, `details.ran_by: "runner"`, no `details.deferred`.
    - build — `python -m compileall -q .` — exit 0 — output: `` (empty)
    - test — `python -m pytest` — exit 0 — output tail: `tests/test_calc.py ........                                              [ 88%]\ntests/test_flag.py .                                                     [100%]\n\n============================== 9 passed in 0.02s ===============================`
    - lint — `python -m ruff check .` — exit 0 — output: `All checks passed!`
- `evidence/build.log`, `evidence/test.log`, `evidence/lint.log` — not present yet (expected only at phases (d) and (e) per the brief; none exist in this change's evidence directory at end of (c)).
- `evidence/failing-test.log` (read, not a gate record) — first line: `============================= test session starts ==============================`. This is the step-1 reproducing-test-fails artifact from phase (b)/(c) setup (`test_percent_zero_whole_error_names_whole` failing against the pre-fix code with `AssertionError: assert 'b must not be zero' == 'whole must not be zero'`), consistent with plan.md step 1.

**Behavior exercised**

Direct calls via a small script (`sys.path` pointing at the repo, no `.env*` read, run with `python3`), not through pytest or any test-runner invocation:
- `percent(1, 0)` → raised `ZeroDivisionError('whole must not be zero')`, with `__cause__ is None` and `__suppress_context__ is True` — confirms both the new message text and the `from None` suppression the Design section specifies.
- `divide(5, 0)` (nearest neighboring flow 1) → raised `ZeroDivisionError('b must not be zero')`, unchanged, as spec.md requires ("`divide(a, 0)` is unchanged").
- `percent(25, 50)` (nearest neighboring flow 2, non-zero whole) → returned `50.0`, a correct ordinary percentage, unaffected by the fix.

Also read `sample_pkg/calc.py` and the diff for commit `82549de` directly: `percent` now wraps `divide(part * 100, whole)` in `try/except ZeroDivisionError: raise ZeroDivisionError("whole must not be zero") from None`, exactly matching plan.md step 2 and spec.md's Design section; `divide`, `add`, `mean` are byte-for-byte untouched in this diff. Read `tests/test_calc.py`: the new test `test_percent_zero_whole_error_names_whole` asserts `str(excinfo.value) == "whole must not be zero"` for `percent(1, 0)`, and the two existing tests `test_percent_zero_whole_raises` and `test_divide_by_zero_raises` are present and unmodified, matching plan.md's Proof list.

**Not exercised**

- The pytest run itself on the current (post-fix) tree — not run in this CI session per the no-test-runner rule; `gate-b.json` above is the prior phase's record, not a run of today's code.
- `mean()` and `add()` behavior — unchanged by this diff and not called in this session (plan.md and spec.md both state they're untouched; not independently verified here beyond reading the diff).
- Windows / non-Linux platform — this session ran only on Linux (the sandbox host); no Windows run was done either way.
- Inputs just outside the Acceptance section's examples beyond `percent(25, 50)` and `divide(5, 0)` (e.g. negative `whole`, float `whole` very close to but not exactly zero) — not tried.
- The build/lint/test targets on the final tree (this phase's own commit) — that is the runner's job after this session, reported in check run `sdlc/d`.

**Mismatches with plan.md / spec.md**

None.

**Verdict**

matches the plan
