# Intent: ci_test_failure_rate breached 3sigma (forced) on 2026-09-25
Author: sdlc-maintain (automated diagnosis). Status: proposed. Change id: 0007. Entry route: incident dcfe764c7235cd9c.

## Problem
The detection loop's `ci_test_failure_rate` metric fired a tier 3 finding on 2026-09-25 at
20:14:15Z. The finding record (`evidence/detection.json`) shows `rule: "forced"` and
`forced: true`: this was triggered by a manual `workflow_dispatch` rehearsal of the
detection loop, not by an organic breach. The record's `reason` field states it directly:
"tier 3 forced by workflow_dispatch (a rehearsal of the loop); no complete-day observation
in the window: the source returned none." Every data field that would normally carry the
anomaly — `mean`, `sigma`, `sigmas`, `latest`, `observations`, `n_baseline`, `n_tail`,
`breach_start`, `commits`, `failed_run_urls` — is null, zero or empty. There is no test
failure signal to diagnose.

## Proposed outcome
No code fix is proposed: there is no anomaly in the running system to fix. Per the owner's
fix-round review comment, this rehearsal is meant to exercise the Go path: the route
proposal (`evidence/proposal.json`) names `runbook:rollback-deploy` (no arguments), listed
as a rehearsed rollback on a declared production for 2026-09-25 (decision 26). The rehearsal
exercises the tier 3 diagnosis-and-routing path end to end (this intent, the route proposal,
gate (f), and the Go authorization mechanics) so the owner can confirm the loop behaves
correctly on a forced trigger through to a runbook route. The outcome is a reviewed record of
that rehearsal; the owner closes this PR with a comment once satisfied the mechanics worked,
per the framework's dismissal path.

## Affected users and systems
None. No production system, test suite or CI pipeline was actually degraded. The only
"system" exercised is the SDLC framework's own detect → maintain → gate (f) pipeline for
this sample project.

## Constraints
- No source file may be edited by this diagnosis (read-only investigation).
- `.claude/**`, `CLAUDE.md`, `REVIEW.md`, `sdlc.yaml`, `bands.yaml` and
  `evidence/detection.json` must not be touched.
- The route proposed must be one `detect/cli.py routes` actually lists for this tier; a
  forced finding never pre-approves a runbook regardless of the route named here.

## Open questions
- None for the diagnosis itself. For the owner: confirm this was an intentional rehearsal
  (e.g. via a manually triggered `workflow_dispatch` run) rather than a misconfigured
  detector that produced a forced/empty record unexpectedly.

## Evidence
- Metric: `ci_test_failure_rate`. Tier: 3. Rule: `forced` (`rules_hit: ["forced"]`).
  Direction: `above`. Signature: `dcfe764c7235cd9c`. Source: `github-actions`.
  Window: 30 days.
- All quantitative fields (`mean`, `sigma`, `sigmas`, `latest`, `observations`,
  `n_baseline`, `n_tail`) are null/zero/empty, and `breach_start`, `commits` and
  `failed_run_urls` are empty — consistent with a forced rehearsal rather than an
  organically detected breach.
- Investigation per step 2 (`gh run view` on failed runs, `git log` over the breach window)
  found nothing to inspect: `failed_run_urls` and `commits` are both empty, so there are no
  runs or commits in scope.
- `lessons/` contains only `README.md` (the template); no prior incident has been recorded,
  so no earlier lesson applies here.
- Ruled out: an organic test-failure-rate breach (no observation data exists to support
  one), a specific flaky test (none named), and a specific bad commit (none in the window).
