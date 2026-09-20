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
