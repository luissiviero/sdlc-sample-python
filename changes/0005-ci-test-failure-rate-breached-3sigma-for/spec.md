# Spec: ci_test_failure_rate breached 3sigma (forced) on 2026-09-25
Change id: 0005. Status: proposed. Produced by: sdlc plugin 0.2.19, /sdlc-design prompt v1 (article p.14). Skills: coding-standards, security-baseline, ux-conventions, data-conventions, definition-of-done (plugin 0.2.19); overrides: none

## Requirements
- The change makes no change to `sample_pkg/` or `tests/`: `evidence/detection.json` shows a
  forced rehearsal (`forced: true`, `rule: forced`) with every quantitative field null or
  empty, so there is no CI test-failure anomaly to fix (intent Problem, Proposed outcome).
- The change carries the confirmation, for the owner, that the detect → diagnose → route →
  PR pipeline exercised correctly end to end for a forced tier-3 finding (intent Proposed
  outcome).
- coding-standards rule 4 ("every behavior change ships with a test that fails without it")
  does not apply: there is no behavior change.
- coding-standards rule 5 (new dependency needs a Risks line) does not apply: no dependency
  is added.
- security-baseline rules 1-7 (authentication, input, secrets, data, audit, dependencies,
  network) do not apply: no endpoint, secret, external input or dependency is touched. Rule 8
  (a risk-list hit) was checked against `sdlc.yaml: risk_list` (auth, data migrations, money
  movement, production config): none is touched.
- ux-conventions does not apply: this project has no user interface and this change adds
  none.
- data-conventions does not apply: no schema, migration, stored field or personal data is
  added, touched or logged.
- definition-of-done: the phase (b) artifact set (spec.md and plan.md, adversarial verdict,
  gate (b)) still applies even though the change itself is a no-op, because a merged incident
  intent is routed through the full phase sequence for traceability (decision 25; `status.yaml:
  entry_route: incident`, `gate.phase: a`, `result: passed`).
- Build, test and lint stay exactly as green as they are today (`python -m compileall -q .`,
  `python -m pytest`, `python -m ruff check .`); the change proves this rather than changing
  it.

## Design
- No module, file, interface or data shape in this repository changes. The design of this
  change is procedural: the change folder
  (`changes/0005-ci-test-failure-rate-breached-3sigma-for/`) carries the rehearsal record
  (`intent.md`, this `spec.md`, `plan.md`, `evidence/`) through phases (b)-(e) so the
  incident closes with full traceability, per decision 25's treatment of a merged incident
  intent whose diagnosis found nothing to fix.
- Phase (c) build has no implementation step; it runs the project's existing build/test/lint
  targets unchanged and records their output as evidence that the rehearsal touched nothing
  in `sample_pkg/` or `tests/`.
- Phase (d) test repeats the same fresh-context run for the same reason.
- Phase (e) is the owner's merge (or dismissal) of the resulting PR, closing the incident;
  `sdlc.yaml: deploy.action` is `none`, so nothing runs after merge.

## Open questions from intent
- Intent's "Open questions" section states: "None for this incident." It also notes, as an
  aside and not as a question for this design: whether the `ci_test_failure_rate` source
  should be configured so a genuine (non-forced) run has real baseline data
  (`n_baseline` was 0 even before forcing). Intent is explicit that this "is not an open
  question this intent needs design to answer, since no fix is proposed here" — carried
  forward to the owner as a separate future concern, not answered or acted on by this design.

## Flagged concerns
- Fix-type reproducing-test rule vs. intent's read-only constraint: the `plan-template`
  skill's rule for a `fix`-type change (`status.yaml: change_type: fix`) is that the first
  item of Order of work is "write the reproducing test and see it fail," locking the test
  paths from then on. intent.md's Constraints section states plainly "Read-only
  investigation: no source file may change as part of this diagnosis," and its Proposed
  outcome states "No code or test change: there is no anomaly to fix" — there is no failing
  behavior to write a reproducing test for. `plan.md` below follows intent.md (no reproducing
  test, no test-file lock) rather than the generic fix-type default. This is left open for
  the owner: intent.md is the gate-(a)-approved source and states the constraint explicitly,
  but it is not one of the five policy skills, so this design does not close the concern
  itself — the owner's sign-off at gate (b) (a human gate in every profile) is the
  confirmation that skipping the reproducing test is correct for this rehearsal-classed
  incident.

## Acceptance
- `python -m compileall -q .` — no output, exit code 0 (unchanged).
- `python -m pytest` — `9 passed in 0.01s`, exit code 0 (unchanged: no test added, removed or
  skipped).
- `python -m ruff check .` — `All checks passed!`, exit code 0 (unchanged).
- No diff under `sample_pkg/` or `tests/` at any phase of this change; the only diff across
  phases (b)-(e) stays inside
  `changes/0005-ci-test-failure-rate-breached-3sigma-for/`.
- The owner's merge (or dismissal) of the resulting PR is the measure of "done" for this
  incident.
