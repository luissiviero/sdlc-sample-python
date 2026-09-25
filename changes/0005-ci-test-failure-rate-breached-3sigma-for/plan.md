# Plan: ci_test_failure_rate breached 3sigma (forced) on 2026-09-25 (from intent.md 2026-09-25, spec.md 2026-09-25)

## Files that change
- None under `sample_pkg/` or `tests/`: this is a no-op change (spec.md Design).
- `changes/0005-ci-test-failure-rate-breached-3sigma-for/`: `spec.md` and `plan.md` are
  written now; `evidence/` gains the phase (c) and (d) run artifacts (build/test/lint logs,
  verifier report, adversarial verdicts, gate evidence) as later phases execute. Those are
  evidence, not source, so they need no further plan.md update as they are added.

## Order of work
1. Phase (c) build: run the project's existing commands unchanged —
   `python -m compileall -q .`, `python -m pytest`, `python -m ruff check .` — and save their
   literal output as evidence that nothing in `sample_pkg/` or `tests/` needs to change. No
   reproducing test is written (spec.md Flagged concerns): there is no failing behavior to
   reproduce one for.
2. Phase (d) test: repeat the same three commands in a fresh context; save `evidence/test.log`,
   `build.log`, `lint.log`.
3. Phase (e): publish the PR summary (no code change; all three commands green; incident
   confirmed to be an empty rehearsal) for the owner's merge, which closes the incident
   (`sdlc.yaml: deploy.action` is `none`, so nothing runs after merge).

## Risks
- Procedural risk only: a later phase's automation could assume every `fix`-type change
  commits a reproducing test before locking test paths, and misfire on this change for
  having none. Mitigation: spec.md's Flagged concerns names this departure from the generic
  fix-type default explicitly, citing intent.md's read-only constraint, so the owner
  confirms it at gate (b) before phase (c) runs.
- No caller, consumer or data shape is touched (no source file changes), so there is nothing
  downstream this change can break.
- The riskiest step is step 1 (phase (c) build) only in the sense that it is the first phase
  that could, in principle, find a reason to touch source; since spec.md's Design commits to
  no implementation, the risk is a process one (see above), not a code one.

## Options not taken
1. Writing a reproducing test to follow the generic fix-type convention literally: not done,
   because there is no failing behavior to reproduce it for — `evidence/detection.json` and
   intent.md both confirm the finding is an empty rehearsal, and intent.md's Constraints
   forbid any source file change.
2. Treating this as a plain no-op change outside the incident pipeline (skipping phases
   (c)-(e)): not done, because `status.yaml: entry_route: incident` and decision 25 route a
   merged incident intent through the full phase sequence regardless of whether a code fix
   results, for traceability.
3. Proposing a fix to the `ci_test_failure_rate` source's baseline data (`n_baseline` was 0
   even before forcing): not done, because intent.md explicitly excludes it from this design
   ("not an open question this intent needs design to answer, since no fix is proposed
   here").

## Proof
- `python -m compileall -q .` — no output, exit code 0.
- `python -m pytest` — `9 passed in 0.01s`, exit code 0 (all 9 existing tests; none added,
  removed or skipped).
- `python -m ruff check .` — `All checks passed!`, exit code 0.
- All three are existing, already-runnable project commands (`sdlc.yaml: commands`), not
  tests still to be written: this change adds none.
