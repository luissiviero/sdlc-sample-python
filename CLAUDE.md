# sdlc-sample-python

Sample Python project for live checks of the SDLC framework plugin (`sdlc@sdlc-framework`).
It mirrors the framework's fixture project: one tiny package, one passing test module, one
test that fails only when `SAMPLE_FAIL=1` is set, and a `.env` the plugin's deny rule must
keep out of the model's context.

## Commands
- Build: `python -m compileall -q .` — healthy: no output and exit code 0
- Test: `python -m pytest` — healthy: `3 passed in 0.01s` and exit code 0
- Lint: `python -m ruff check .` — healthy: `All checks passed!`
- `SAMPLE_FAIL=1 python -m pytest` must exit non-zero (one failing test); that is the point
  of `tests/test_flag.py`, not a bug to fix.

## Conventions
- Python ≥ 3.10, standard library only; pytest and ruff are the only dev tools.
- Config lives in `pyproject.toml` (pytest `testpaths = ["tests"]`, ruff `line-length = 100`).
- Never read or print `.env`; it exists to prove the guardrail, not to configure anything.
- Keep the project deliberately tiny: it is a fixture, not an application.

## Architecture
- `sample_pkg/calc.py`: `add` and `divide` (raises `ZeroDivisionError` on zero divisor).
- `sample_pkg/__init__.py`: re-exports `add` and `divide`.
- `tests/test_calc.py`: behaviour of the two functions.
- `tests/test_flag.py`: the flag-controlled intentional failure.

## Things Claude gets wrong
<!-- One line per recurring mistake; added when a review flags the same finding twice. -->
- (none yet)

## SDLC framework
- Every change lives in `changes/<id>-<slug>/` (intent.md → spec.md + plan.md → evidence/);
  phase branches are `sdlc/<id>/<phase>`; see `changes/README.md`.
- Never edit `.claude/**`, `CLAUDE.md`, `REVIEW.md` or `sdlc.yaml` in a run: they are
  guardrails the owner changes in a reviewed PR. Never use bypass-permissions mode.
- When a run cannot finish, park: write "what I need from you", never notify.

## Verifying your work
<!-- Verbatim structure of the article's verification block (p.28). -->
- Build: `python -m compileall -q .` (must finish with no output and exit code 0)
- Test: `python -m pytest` (all green; never skip or delete a failing test)
- Lint: `python -m ruff check .` (zero warnings)
Run all three before reporting any task complete, and paste the output.
If a test fails, fix the code, not the test.
