# Verifier report: change 0017, phase (d)

## Commands run

All three entries below were **read, not run**. This is a CI session (`SDLC_GATE_COMMANDS=runner`).

I read `evidence/gate-c.json`, the runner's run on commit `64818838d7f6c3d7245b063507311912872df6e3` at `2026-10-20T13:52:11Z` (`ran_by: runner`). That is the tree this phase started from, not the final one. The final tree's result belongs to the runner: it runs the three targets once after this session and shows the result in the check run `sdlc/d`, so nothing reported here stands in for it.

`git diff --stat 6481883 HEAD` lists only files under `changes/0017-.../`. The commits after the gate (c) head (`7695ee7`, `b3a8ddd`) touch no file in `sample_pkg/` or `tests/`, and `git status --short -- sample_pkg tests` printed nothing.

The `commands` check reads `"ok": true`, `"reason": "build, test and lint exit 0"`:
- **build**: `python -m compileall -q .`, exit_code 0, output `""`
- **test**: `python -m pytest`, exit_code 0, tail:
  ```
  collected 12 items

  tests/test_calc.py .........                                             [ 75%]
  tests/test_flag.py .                                                     [ 83%]
  tests/test_messages.py ..                                                [100%]

  ============================== 12 passed in 0.01s ==============================
  ```
- **lint**: `python -m ruff check .`, exit_code 0, output `All checks passed!`
- The `evidence` check reads `"ok": true` (`evidence present: verifier.md`). Neither the `commands` check nor the `evidence` check has `details.deferred`.

First line of each log:
- `test.log`: `# python -m pytest — deferred to the runner — 2026-10-20T13:53:47Z`
- `build.log`: `# python -m compileall -q . — deferred to the runner — 2026-10-20T13:53:47Z`
- `lint.log`: `# python -m ruff check . — deferred to the runner — 2026-10-20T13:53:47Z`

These are not failures. This phase's session wrote these placeholders, and the runner will replace them with the real output.

I did not read `gate-d.json`.

One action was blocked. My first attempt to read the gate record used a shell command with a variable in it. That command needed approval, and this session has no way to grant it, so it was denied automatically. I read the same files with the Read tool instead, which gave the same information.

## Behavior exercised

**Source diff.** `git diff 543b434 HEAD -- sample_pkg tests` shows three files changed and nothing else:
- `sample_pkg/calc.py:18`: `raise ZeroDivisionError("whole must not be zero") from None` became `raise ZeroDivisionError(f"cannot express {part} as a percent of zero") from None`. The `try`, the `except` and the `from None` are unchanged.
- `tests/test_messages.py`: the import is now `from sample_pkg import divide, percent`. A new test, `test_percent_zero_whole_names_part`, asserts `"cannot express 5 as a percent of zero"` for `percent(5, 0)`. `test_divide_by_zero_names_dividend` is unchanged.
- `tests/test_calc.py:28`: the assertion is now `"cannot express 1 as a percent of zero"`. The test name and the rest of the file are unchanged.

`tests/test_flag.py` is not in the diff, so it is untouched. `sample_pkg/__init__.py` and the guardrail files are not in it either.

**Direct calls.** I ran `python3 -I -c ...` from the repository root, importing from `sample_pkg`. No test runner and no `.env*` file was involved. Literal output:
```
(5, 0) ZeroDivisionError 'cannot express 5 as a percent of zero' cause: None suppress: True
(1, 0) ZeroDivisionError 'cannot express 1 as a percent of zero' cause: None suppress: True
(1.5, 0) ZeroDivisionError 'cannot express 1.5 as a percent of zero' cause: None suppress: True
(1.0, 0) ZeroDivisionError 'cannot express 1.0 as a percent of zero' cause: None suppress: True
(-2, 0) ZeroDivisionError 'cannot express -2 as a percent of zero' cause: None suppress: True
(5, 0.0) ZeroDivisionError 'cannot express 5 as a percent of zero' cause: None suppress: True
percent(1,4) 25.0 percent(7,100) 7.0 percent(5,1e-300) 5e+302
divide(1,0) 'cannot divide 1 by zero'
mean([]) 'mean() requires at least one value'
mean 2.5 2.0 add 5
```

How this lines up with the spec's Acceptance section:
- `percent(5, 0)`, `percent(1, 0)` and `percent(1.5, 0)` give exactly the required messages. `percent(1.0, 0)` gives `1.0`, as the Requirements say.
- `from None` still holds: the cause is `None` and the context is suppressed.
- The non-zero results are unchanged: `percent(1, 4)` is 25.0 and `percent(7, 100)` is 7.0.
- The two nearest neighbors are unchanged: `divide(1, 0)` keeps its message, and `mean` and `add` behave as before.
- Inputs just outside the named ones (a negative part, a float zero `whole`, a tiny non-zero `whole`) behave consistently with the f-string rule.

## Not exercised

- The full test suite on the final tree: I read the gate (c) record instead of running it. The runner's result in `sdlc/d` is the one that counts.
- Build and lint on the final tree, for the same reason.
- Windows and macOS: I ran on Linux with Python 3.12.3 only.
- `part` values that are not plain numbers (`Decimal`, `Fraction`, numpy scalars, `nan`, `inf`): not tried.
- `SAMPLE_FAIL=1`: not set, by design.

## Mismatches with plan.md / spec.md

None.

## Verdict

**matches the plan**
