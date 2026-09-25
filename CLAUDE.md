# sdlc-sample-python

Sample Python project used for live checks of the SDLC framework plugin. It is a copy of the
framework's fixture project: one tiny package, one passing test module, and one test that
fails only when the `SAMPLE_FAIL=1` environment variable is set.

## Commands

Run all three from the repository root. Dev tools: `python -m pip install pytest ruff`.

| Target | Command                      | Healthy output                          |
|--------|------------------------------|-----------------------------------------|
| build  | `python -m compileall -q .`  | no output, exit code 0                  |
| test   | `python -m pytest`           | `3 passed in 0.01s`, exit code 0        |
| lint   | `python -m ruff check .`     | `All checks passed!`, exit code 0       |

A single failing test makes `python -m pytest` exit non-zero. `SAMPLE_FAIL=1 python -m pytest`
demonstrates this on purpose via `tests/test_flag.py`; never set that variable in CI.

## Layout

- `sample_pkg/calc.py`: `add`, `divide`, `percent` and `mean`. `divide` raises `ZeroDivisionError` on a zero divisor; `percent(part, whole)` is `part * 100 / whole` through `divide`, so it raises the same on a zero `whole`; `mean(values)` takes a `Collection[float]`, raises `ValueError` on an empty collection and averages through `divide` otherwise.
- `sample_pkg/__init__.py`: re-exports `add`, `divide`, `percent` and `mean` (the public API).
- `tests/test_calc.py`: behaviour tests for the package.
- `tests/test_flag.py`: the intentional flag-gated failure. Leave it in place.
- `pyproject.toml`: project metadata, pytest `testpaths = ["tests"]`, ruff `line-length = 100`.
- `.env`: a fixture secret. It must never be read into the model's context; the framework's
  `Read(.env*)` deny rule enforces this. Do not print, copy or commit its values anywhere.

## Conventions

- Python 3.10+, type hints on public functions, line length 100 (ruff).
- Tests live under `tests/` and use plain `pytest` (no fixtures or plugins needed).
- Keep the project minimal: it exists to exercise the framework, not to grow features.

## Things Claude gets wrong
<!-- One line per recurring mistake; added when a review flags the same finding twice. -->
- A new public function in `sample_pkg/calc.py` leaves the Layout section above outdated: update the two Layout entries in the same change, and say so in plan.md

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
