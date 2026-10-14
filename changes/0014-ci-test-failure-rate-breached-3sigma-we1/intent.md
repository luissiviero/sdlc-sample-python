# Intent: ci_test_failure_rate breached 3sigma (we1) on 2026-10-13
Author: sdlc-maintain (automated diagnosis). Status: proposed. Change id: 0014. Entry route: incident 68b6897ece2328d6.

## Problem
The `ci_test_failure_rate` metric breached its 3-sigma control band (rule `we1`): on
2026-10-13 the daily failure rate was 0.4 (2 of 5 CI runs failed) against a 30-day baseline
mean of 0.0065 and sigma of 0.0215 — 18.27 sigma from the mean. Both failed runs
(https://github.com/luissiviero/sdlc-sample-python/actions/runs/38361643987 and
https://github.com/luissiviero/sdlc-sample-python/actions/runs/38361544355) trace to the
same commit: `c61007b` ("Add initial provocation tests with assertions", PR #58), merged to
`main` as `edc4f4b` at 2026-10-13T07:16:33Z. That commit added `tests/test_provocation.py`
with `assert 1 == 2` and `assert "a" == "b"`.

## Proposed outcome
No code fix is needed: the responsible commit was already reverted on `main` ten minutes
after it landed, via PR #59 (`7a7f739` / `78abbb0`, merged 2026-10-13T07:26:39Z) — well
before this diagnosis ran (2026-10-14). Every CI run on `main` since the revert has been
green (most recently 2026-10-14T12:59:48Z). The outcome of this change is to record the
incident as resolved and let the owner dismiss it, optionally capturing a lesson so a
similarly short-lived, already-reverted breach is recognized faster next time.

## Affected users and systems
- `.github/workflows/ci.yml` (the `CI` workflow the detection metric counts): the `test` job
  runs `Lint` before `Test`, so the failure surfaced as a lint error, not a test failure, and
  the `Test` step never ran on either failed run.
- `tests/test_provocation.py`: added and removed within the same 10 minutes; not present on
  `main` today.
- The SDLC detection pipeline (decision 15, `ci_test_failure_rate`): its commit-window
  listing in `evidence/detection.json` does not include the actual responsible commits
  (`edc4f4b`/`c61007b`, both 2026-10-13) — the listed commits are all from 2026-10-14 and are
  unrelated (CLAUDE.md guideline update, plugin version bump). This is a detection-side
  observation, not something this run changed.

## Constraints
None beyond the framework's own: this run touched nothing outside `changes/0014-ci-test-failure-rate-breached-3sigma-we1/`; no source, test or workflow file was edited.

## Open questions
- Should the owner simply dismiss this incident given `main` has been green since
  2026-10-13T07:26:39Z, or is a lesson entry worth writing even for a self-corrected breach?
- Was PR #58/#59 an intentional rehearsal of the detection pipeline (this project exists to
  exercise the SDLC framework) rather than an accidental regression? Nothing in the record
  marks it `forced: true`, so detection treated it as a real breach either way.
- Should `ci.yml`'s `Test` step run even when `Lint` fails (e.g. `if: always()`), so a lint
  break doesn't mask whether the tests themselves would have passed? Out of scope for this
  diagnosis (would be a source change).

## Evidence
- Metric: `ci_test_failure_rate`, tier 3, rule `we1`. Latest value 0.4 vs. baseline mean
  0.006494, sigma 0.021536 (18.27 sigma), breach since 2026-10-13.
  Source: `changes/0014-ci-test-failure-rate-breached-3sigma-we1/evidence/detection.json`.
- Both failed runs' `headSha` resolve to the same commit: run 38361643987 (push to `main`)
  → `edc4f4b` (merge of PR #58); run 38361544355 (pull_request) → `c61007b` (PR #58's own
  commit). Checked via `gh run view <id> --json headSha,headBranch,event,createdAt,displayTitle`.
- Both runs' job `test` failed at the `Lint` step (`python -m ruff check .`); the `Test`
  step shows skipped in both (`gh run view <id>`), consistent with `ci.yml` running `Lint`
  before `Test` with no `if: always()`.
- Reproduced the lint failure in isolation (not on the working tree): wrote `c61007b`'s
  `tests/test_provocation.py` content to a scratch temp file and ran
  `python -m ruff check` against it — it fails with `PLR0133 Two constants compared in a
  comparison` on both `1 == 2` and `"a" == "b"`.
- `git log --format='%H %ai %s' edc4f4b~1..78abbb0` confirms the revert (`7a7f739`, merged as
  `78abbb0`) landed 2026-10-13T07:26:39Z, ~10 minutes after the breaking commit.
- `gh run list --branch main --limit 10` shows every `CI` run on `main` after the revert
  completed `success`, most recently 2026-10-14T12:59:48Z.
- Ruled out: a flaky/intermittent test (the failure is a deterministic lint error on a
  specific commit's content, not a test that fails only sometimes with no code change behind
  it) — `runbook:quarantine-flaky-test` does not fit. Ruled out `runbook:revert-pr` — the
  responsible commit is already reverted on `main`; there is nothing left to revert.
  Ruled out `runbook:rollback-deploy` — this is not a deployment/production incident.
- Lessons: `lessons/index.md` is stale/missing (`lessons/index.py check` exits 1; it prints
  only "No lessons yet." while the real index would differ). Per the stale-index fallback,
  read every file under `lessons/` directly — there are none yet (`lessons/README.md` is the
  only file, describing the format; no lesson has been written). No existing lesson applied.
- Could not fetch the failed-step logs directly (`gh run view <id> --log-failed`) because
  `gh` needs to create a cache directory at `/home/runner/.cache/gh`, which is read-only in
  this sandbox, and no writable-cache workaround was available within this run's tool
  constraints; the Lint-step diagnosis above was reached via `gh run view` (no `--log-failed`),
  `--json` metadata, and an isolated reproduction instead.
