# Intent: ci_test_failure_rate breached 2sigma (forced) on 2026-09-28
Author: sdlc-maintain (automated diagnosis). Status: proposed. Change id: 0009. Entry route: incident dcfe764c7235cd9c.

## Problem
Restated for the record: this finding was forced (a manual `workflow_dispatch` rehearsal of
the detection loop, not an organic breach) and no code change follows from it.

The detection loop's `ci_test_failure_rate` metric fired a tier 2 finding on 2026-09-28, but
the finding record (`evidence/detection.json`) shows `"forced": true` and
`"reason": "tier 2 forced by workflow_dispatch (a rehearsal of the loop)"` — this run was
triggered manually to rehearse the incident pipeline, not by a real statistical breach.
`mean` and `sigma` are both `null` (no baseline was computed) and the latest observation
(2026-09-28) is `value: 0.0` with `failed: 0` out of 8 runs. There is no live signal that CI
is actually failing more often than usual.

## Proposed outcome
No code fix is needed. The owner triages this PR by closing it with a comment noting it was
a rehearsal (the abandon workflow records the dismissal), unless the owner independently
knows of a real regression this rehearsal happened to coincide with.

## Affected users and systems
None. No source file, test, or CI workflow is implicated by the record; the only recent
commits in the breach window are SDLC framework/workflow maintenance (`sdlc.yaml` updates,
the plugin 0.2.28 workflow upgrade) and PR merges, none of which touch `sample_pkg/` or
`tests/`.

## Constraints
None beyond the framework's own: this diagnosis run must not edit anything outside
`changes/0009-ci-test-failure-rate-breached-2sigma-for/`, must not touch source, and must not
fix or run the test suite (the fix, if any were needed, is a separate change starting at
gate (a)).

## Open questions
None for this rehearsal. If the owner has a real regression in mind that this forced run was
meant to stand in for, that context is not present anywhere in this repo's evidence and would
need to be supplied separately.

## Evidence
- Metric: `ci_test_failure_rate`, tier 2, rule `forced` (not a real threshold rule — see
  `rules_hit: ["forced"]` in `evidence/detection.json`).
- `mean: null`, `sigma: null`, `n_baseline: 0` — no real baseline/threshold was breached;
  this is a rehearsal artifact of `workflow_dispatch`, not an organic 2σ event.
- Latest observation (2026-09-28): `value: 0.0`, `failed: 0` of 8 runs, `failed_run_urls: []`
  — the day the "breach" is dated to has zero failures.
- The only failed run in the 4-day tail window is from 2026-09-26
  (https://github.com/luissiviero/sdlc-sample-python/actions/runs/36257154359, PR #43
  "luissiviero-patch-9"): `gh run view` shows it failed at the **Install the toolchain**
  step, before Lint or Test ran — a toolchain/setup problem, not a test regression, and two
  days before the declared breach date.
- Commits in the breach window (from the detection record) are all SDLC framework
  maintenance (`sdlc.yaml` updates, the plugin 0.2.28 workflow-copy upgrade, PR merges
  #48–#50); none touch `sample_pkg/` or `tests/`.
- Ruled out: an organic test-failure-rate regression (no baseline exists to regress from,
  and the latest day has zero failures); a code change causing the one tail-window failure
  (that failure was an infra step failure, not a test failure, and predates the commits
  listed).
- `lessons/` contains only `README.md` — no prior incident of this class to compare against.
