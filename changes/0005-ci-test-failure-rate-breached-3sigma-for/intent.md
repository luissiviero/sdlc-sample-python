# Intent: ci_test_failure_rate breached 3sigma (forced) on 2026-09-25
Author: Claude (sdlc-maintain, phase f diagnosis). Status: proposed. Change id: 0005. Entry route: incident dcfe764c7235cd9c.

## Problem
The detection loop for the `ci_test_failure_rate` metric fired at tier 3 on 2026-09-25, but
the finding record (`evidence/detection.json`) shows `"forced": true` and
`"rule": "forced"`: this run was triggered by `workflow_dispatch` as a rehearsal of the
detect → diagnose → route → PR pipeline, not by an observed breach. Every data field the
rule would normally use is empty or null: `observations: []`, `n_baseline: 0`, `n_tail: 0`,
`mean: null`, `sigma: null`, `sigmas: null`, `latest: null`, `failed_run_urls: []`,
`commits: []`, `breach_start: null`. The record's own `reason` states it plainly: "no
complete-day observation in the window: the source returned none."

## Proposed outcome
No code or test change: there is no anomaly to fix. The outcome of this incident is the
rehearsal itself succeeding — confirming that a forced tier-3 finding is correctly turned
into an incident change, diagnosed read-only, and routed to a `pull_request` for the owner's
triage, with the empty evidence explicitly called out rather than a route invented to fit
the tier. The owner's expected action is to dismiss this PR (close with a comment) once the
rehearsal is confirmed to have exercised the pipeline correctly.

## Affected users and systems
- This repository's SDLC maintain/detect pipeline (`framework/plugin/detect`,
  `framework/plugin/gate`, `framework/plugin/state`).
- No production code, package (`sample_pkg/`) or test (`tests/`) is affected.
- The owner, who triages the resulting PR.

## Constraints
- Read-only investigation: no source file may change as part of this diagnosis.
- No new PII or data involved.
- Never propose a route the `detect/cli.py routes` output did not list.

## Open questions
- None for this incident. Whether the underlying `ci_test_failure_rate` source should be
  configured so a genuine (non-forced) run has real baseline data (`n_baseline` was 0 even
  before forcing) is worth the owner's attention separately, but is not an open question this
  intent needs design to answer, since no fix is proposed here.

## Evidence
- Metric: `ci_test_failure_rate`, tier 3, rule `forced`, signature `dcfe764c7235cd9c`,
  detected at 2026-09-25T17:27:44Z (`evidence/detection.json`).
- `forced: true` — this is a rehearsal of the loop dispatched manually, not an organic
  breach; the article and build guide note a forced finding "never pre-approves a runbook"
  at dispatch time regardless of the route proposed here.
- All quantitative fields in the record (`mean`, `sigma`, `sigmas`, `latest`, `observations`,
  `n_baseline`, `n_tail`, `breach_start`) are `null` or empty/zero, and `failed_run_urls` and
  `commits` are both empty arrays — there is no failed CI run to inspect with
  `gh run view --log-failed` and no commit in a breach window to examine with `git log`.
  Both were checked against the record before writing this intent; there was nothing to
  fetch.
- Ruled out: a flaky test (no failing run or test is named anywhere in the record, so
  `runbook:quarantine-flaky-test` has no test node id to target); a bad commit introducing
  failures (no commits are listed in the breach window, so `runbook:revert-pr` has no sha to
  target).
- Lessons: `lessons/README.md` was read; no incident files exist yet under `lessons/` (this
  would be the repository's first), so no prior lesson applied here.
