# Intent: ci_test_failure_rate breached 3sigma (we1) on 2026-10-13
Author: sdlc-maintain (phase f diagnosis). Status: proposed. Change id: 0013. Entry route: incident 68b6897ece2328d6.

## Problem
On 2026-10-13 the `ci_test_failure_rate` detector fired a tier-3 (we1) alert: the day's
value jumped to 0.4 (2 of 5 CI runs failed) against a 30-day baseline mean of 0.0065 and
sigma of 0.0215 — an 18.27 sigma excursion. Both failed runs
(https://github.com/luissiviero/sdlc-sample-python/actions/runs/38361643987,
https://github.com/luissiviero/sdlc-sample-python/actions/runs/38361544355) failed at the
workflow's `Lint` step (`python -m ruff check .`); the `Test` step never ran. The metric
name is slightly misleading here — the job that failed is CI as a whole, and in this case
the failure was a lint error, not a failing pytest test.

## Proposed outcome
No design-phase code change is required: the commit that caused the breach was already
reverted on `main` 3 minutes after it merged, before this diagnosis ran (see Evidence).
`main` is green. The outcome of this change is a record of the incident (this intent, for
the owner's triage) and, if the owner agrees, a `lessons/` entry written when this intent is
closed, so a future placeholder/scratch test file with always-false assertions is recognized
faster (ruff's `PLR0133` already catches it, as it did here).

## Affected users and systems
- `tests/` directory and the repository's CI workflow (`.github/workflows/ci.yml`, job
  `test`, steps `Lint` then `Test`).
- No production system, no deploy, no user-facing behavior: this is a sample/fixture
  project exercising the SDLC framework.

## Constraints
- No source code changes are proposed by this diagnosis (phase (f) is read-only on source).
- Keep the project minimal per `CLAUDE.md`: no new tooling or process proposed beyond an
  optional `lessons/` entry.

## Open questions
- Should the owner want a `lessons/2026-10-ci-test-failure-rate-breached-3sigma-we1.md`
  entry written even though the fix (the revert) already shipped outside this change's
  lifecycle? (The `lessons/` convention expects the entry to ride the fix PR; here the fix
  predates this incident's filing.)
- None regarding root cause: it is fully explained by the evidence below.

## Evidence
- Metric: `ci_test_failure_rate`, tier 3, rule `we1` (single point far outside the control
  band). Baseline mean 0.006493506493506493, sigma 0.021536524612697398, 11 baseline points
  over the 30-day window; latest observation on 2026-10-13: value 0.4 (2 of 5 runs failed),
  18.27 sigma from the mean. Source: `changes/0013-ci-test-failure-rate-breached-3sigma-we1/evidence/detection.json`
  (not edited).
- Breach window commits (from the detection record, newest first): `78abbb0` (merge PR #59,
  the revert), `7a7f739` (`Revert "Add initial provocation tests with assertions"`),
  `edc4f4b` (merge PR #58), `c61007b` (`Add initial provocation tests with assertions`,
  added `tests/test_provocation.py` with `assert 1 == 2` and `assert "a" == "b"`).
- `gh run view 38361544355 --json headSha,event` → pull_request run on branch
  `luissiviero-patch-16`, headSha `c61007b`; `gh run view 38361643987 --json headSha,event`
  → push run on `main`, headSha `edc4f4b` (the merge of PR #58). Both runs' job logs show
  `Lint` failed (exit code 1) and `Test` was skipped (`-`); `--log-failed` could not be
  fetched in this session (network egress to
  `results-receiver.actions.githubusercontent.com` is denied in this sandbox), so the
  specific lint rule was confirmed independently: `git show c61007b:tests/test_provocation.py`
  piped through `python -m ruff check --isolated --stdin-filename tests/test_provocation.py -`
  reproduces the failure — `PLR0133 Two constants compared in a comparison` on both new
  assertions. `python -m ruff check .` on the current, already-reverted working tree passes
  (`All checks passed!`).
- Timing: commit timestamps (local, -03:00) show the merge of PR #58 (`edc4f4b`) at
  04:16:33 and the revert (`7a7f739`) at 04:19:43 — 3 minutes and 10 seconds later, matching
  the push-run's `createdAt` of 2026-10-13T07:16:37Z (UTC). The bad commit was on `main` for
  only a few minutes before a human reverted it, well before this detection/diagnosis ran.
- Ruled out: not a flaky/intermittent test (the `Test` step never executed in either failed
  run, and the failure is 100% reproducible against the offending file, not probabilistic);
  not a dependency or infra issue (`Install the toolchain` succeeded in both runs); not a
  rollback-worthy deploy issue (this project has no deploy in the breach window relevant
  here, and `main` is already clean).
- Lessons checked: `lessons/README.md` only (no incident lesson files exist yet); this is
  the first recorded incident of this class, so there was no prior lesson to apply.
