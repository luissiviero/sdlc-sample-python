# Verifier report: change 0017 (phase c build, branch `sdlc/0017/c`, HEAD `25c5e03`)

The changed behaviour matches plan.md and spec.md: every message, the empty cause and all three neighbouring flows came back as the plan describes. One limit: this is a CI session, so I did not run build, test or lint. The runner's result on the final tree is what counts, and it appears in the check run `sdlc/d`.

## Commands run

`SDLC_GATE_COMMANDS=runner` is set, so I ran none of the three targets. Everything below was **read, not run**.

**Which tree:** I read `evidence/gate-b.json`, the runner's run on commit `66f5edfe233e1dee8702970ff6445037fc3ad1c5` of `2026-10-20T10:33:20Z`. That is the tree this phase started from, not the final one. The final tree's result comes from the runner, which runs the three targets once after this session. It shows that result in the check run `sdlc/d` and in this phase's own gate record. A red target there starts the next fix round by itself, and nothing in this report stands in for it. As instructed, I did not open `gate-c.json`.

The record's `commands` check reads `"ok": true`, `"reason": "build, test and lint exit 0"`, `"ran_by": "runner"`, and it has no `deferred` flag:
- **build:** `python -m compileall -q .`, exit code 0, output `""`.
- **test:** `python -m pytest`, exit code 0. Output tail:
  ```
  collected 11 items
  tests/test_calc.py .........                                             [ 81%]
  tests/test_flag.py .                                                     [ 90%]
  tests/test_messages.py .                                                 [100%]
  ============================== 11 passed in 0.02s ==============================
  ```
- **lint:** `python -m ruff check .`, exit code 0, output `All checks passed!`.

Other gate (b) checks: `limits`, `artifacts`, `design_scope`, `open_concerns`, `panel`, `commands`, `guardrails`, `risk_list`, `owner_actions`, `adversarial_review` and `reviewer_model` all read `ok: true` with no `deferred` flag. There is no separate `evidence` check in that record. The gate result itself is `wait` (label `sdlc:b-ready`).

Logs: `evidence/test.log`, `build.log` and `lint.log` do not exist yet (`ls: cannot access ...`). That is expected in phase (c), since the runner writes them at (d) and (e).

## Behavior exercised

I called the package directly with `python -I -c` and `sys.path` pointed at the repo root. Import resolved to `.../sample_pkg/__init__.py`.

Changed behaviour, from the spec's Acceptance plus inputs just outside it:
```
percent (5, 0) ZeroDivisionError 'cannot express 5 as a percent of zero' cause= None suppress_context= True
percent (1, 0) ZeroDivisionError 'cannot express 1 as a percent of zero' cause= None suppress_context= True
percent (1.5, 0) ZeroDivisionError 'cannot express 1.5 as a percent of zero' cause= None suppress_context= True
percent (1.0, 0) ZeroDivisionError 'cannot express 1.0 as a percent of zero' cause= None suppress_context= True
percent (5, 0.0) ZeroDivisionError 'cannot express 5 as a percent of zero' cause= None suppress_context= True
percent (-2, 0) ZeroDivisionError 'cannot express -2 as a percent of zero' cause= None suppress_context= True
percent (0, 0) ZeroDivisionError 'cannot express 0 as a percent of zero' cause= None suppress_context= True
```
- There is no chained cause, and the `from None` suppression is kept.
- The message names `part`, never `part * 100` (no `500`).

Neighbouring flow 1, `percent` with a non-zero `whole`:
```
percent(1,4) = 25.0 percent(7,100) = 7.0 percent(5,1e-9) = 499999999999.99994
```

Neighbouring flow 2, `divide`, `add` and `mean`:
```
divide (1, 0) 'cannot divide 1 by zero' cause= None
divide (1.5, 0) 'cannot divide 1.5 by zero' cause= None
divide(6,3) = 2.0 add(2,3) = 5
mean([1,2,3]) = 2.0 mean({4.0}) = 4.0
mean([]) ValueError 'mean() requires at least one value'
```

Static checks against the plan:
- `git show HEAD` touches only line 18 of `sample_pkg/calc.py` (the plan's step 1).
- In `tests/test_messages.py` the import widened to `divide, percent` and `test_percent_zero_whole_names_part` was added (step 2).
- In `tests/test_calc.py` only line 28's assertion changed, and the test name was kept (step 3).
- `git diff --stat 543b434 HEAD -- tests/test_flag.py sample_pkg/__init__.py CLAUDE.md sdlc.yaml .claude REVIEW.md` printed nothing.
- `grep "^def test_"` lists 12 test functions (9 in calc, 2 in messages, 1 in flag), which matches the expected `12 passed`.

## Not exercised

- **Targets on the final tree:** build, test and lint were not run on HEAD `25c5e03`. That result belongs to the runner (check run `sdlc/d`). The gate (b) record covers `66f5edf`, which comes before the source edit.
- **Test runner:** I did not start pytest, not even with `-k`, so the two new or updated test assertions were not executed here.
- **Platforms:** Linux with Python 3 only. Windows, macOS and other Python versions were not run.
- **Inputs not tried:** `bool`, `Decimal`, `Fraction`, NaN/inf, numpy scalars and non-numeric `part`, and negative zero as `whole`.
- **Blocked command:** a variant that appended `echo "exit=$?"` was denied by the permission system (no approval surface in this session). I re-ran it without the echo, so exit codes of my direct calls were not captured separately. The output above is complete and has no traceback.
- **`.env` in `git status`:** it shows as ` M .env` in the working tree. I did not read it or inspect its diff. This is most likely the sandbox masking the denied file, not a change by this phase, but I did not confirm that.

## Mismatches with plan.md / spec.md

None.

## Verdict

`matches the plan`

Relevant files:
- `/home/runner/work/sdlc-sample-python/sdlc-sample-python/sample_pkg/calc.py`
- `/home/runner/work/sdlc-sample-python/sdlc-sample-python/tests/test_messages.py`
- `/home/runner/work/sdlc-sample-python/sdlc-sample-python/tests/test_calc.py`
- `/home/runner/work/sdlc-sample-python/sdlc-sample-python/changes/0017-name-the-part-in-percent-s-zero-whole-er/plan.md`
- `/home/runner/work/sdlc-sample-python/sdlc-sample-python/changes/0017-name-the-part-in-percent-s-zero-whole-er/spec.md`
- `/home/runner/work/sdlc-sample-python/sdlc-sample-python/changes/0017-name-the-part-in-percent-s-zero-whole-er/evidence/gate-b.json`
