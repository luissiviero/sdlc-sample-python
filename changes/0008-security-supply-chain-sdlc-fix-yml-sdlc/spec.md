# Spec: security: supply-chain: sdlc-fix.yml, sdlc-abandon.yml, sdlc-runbook.yml and
Change id: 0008. Status: proposed. Produced by: sdlc plugin 0.2.26, /sdlc-design prompt v1 (article p.14). Skills: coding-standards, security-baseline, ux-conventions, data-conventions, definition-of-done (plugin 0.2.26); overrides: none

## Requirements
- Every workflow step that runs `.github/scripts/sdlc_pin.py` after checking out an
  unmerged/unreviewed PR ref (head or merge ref) executes the default branch's copy of the
  script, never the just-checked-out working-tree copy — in `.github/workflows/sdlc-fix.yml`,
  `sdlc-abandon.yml`, `sdlc-runbook.yml`, `sdlc-evals.yml` (named in the finding) and
  `sdlc-test.yml`, `sdlc-deploy.yml` (the same pattern, found by this design pass; see
  Open questions #1). Security-baseline rule 6 ("no `eval`/`exec` ... on external data").
- The `ref=`/`claude_code=` outputs every workflow's later steps consume
  (`actions/checkout` of `luissiviero/sdlc-framework`, `npm install -g
  @anthropic-ai/claude-code@"$CLAUDE_CODE_VERSION"`) are therefore always produced by the
  trusted copy of the script, in all six files.
- `sdlc_pin.py`'s existing behaviour (reading `sdlc.yaml`'s `plugin.version` /
  `plugin.claude_code` from the default branch via its own `--ref` argument) is unchanged;
  only which copy of the `.py` file's bytes execute changes.
- The six files that already avoid the pattern are not touched: `sdlc-build.yml` and
  `sdlc-design.yml` (job gated on `pull_request.merged == true` before anything but the
  "find the change" step runs), `sdlc-release.yml` (checkout pinned to
  `merge_commit_sha`, read-only permissions, no model secret), `sdlc-detect.yml`,
  `sdlc-digest.yml`, `sdlc-scan.yml` (no `pull_request` trigger at all). Coding-standards
  rule 3 ("one change, one concern").
- A reproducing test exists (intent Constraints) that fails against the current six files
  and passes once each is fixed, without executing real GitHub Actions and without a new
  runtime dependency (coding-standards rule 5; CLAUDE.md "Keep the project minimal").
- No credential appears in the change, its test or its evidence (security-baseline rule 3;
  intent Constraints).
- An eval case is added under `evals/cases/` capturing this vulnerability class (intent
  Proposed outcome; article p.48 step 7).
- No pre-existing test is edited to make the fix pass (intent Constraints; coding-standards
  rule 4).
- `CLAUDE.md`'s Layout section does not need an update: its "Things Claude gets wrong" rule
  is scoped to a new public function in `sample_pkg/calc.py`, which this change does not
  add. `CLAUDE.md` is guardrail-protected regardless (never edited by a run) — no edit is
  proposed either way.
- `data-conventions` and `ux-conventions`: not applicable — the change touches no schema,
  migration, stored field, event contract or user-facing surface.

## Design
`sdlc_pin.py` already draws a trust boundary around the *data* it reads: called with
`--ref "origin/$SDLC_DEFAULT_BRANCH"`, it reads `sdlc.yaml`'s pin block from the default
branch (via `git show <ref>:<file>`) rather than from whatever `sdlc.yaml` happens to sit in
the working tree. It does not draw the same boundary around its own *code*: every affected
workflow's `pin` step runs `python .github/scripts/sdlc_pin.py ...` straight from the
working tree, which for `sdlc-fix.yml`, `sdlc-abandon.yml`, `sdlc-runbook.yml` and
`sdlc-evals.yml` is the just-checked-out PR head or merge ref — content an attacker
controls. `sdlc-test.yml` and `sdlc-deploy.yml` check out the PR's merge ref (no explicit
`ref:`, so `actions/checkout`'s default) and run the same `pin` step before
`run_phase.py`'s own actor-identity check executes later in the job, reachable once an
`sdlc:c-approved`/`sdlc:d-approved` label is applied (needs triage/write access, unlike the
other four).

The fix extends `sdlc_pin.py`'s existing trust boundary from the data it reads to the code
that runs: each of the six `pin` steps gains a preliminary
`git fetch origin "$SDLC_DEFAULT_BRANCH"` (the ref is not necessarily present locally at
this point in the job today — `sdlc_pin.py` currently fetches it lazily, from inside the
untrusted copy, only when it reads `sdlc.yaml`), then extracts and runs the default
branch's copy of the script instead of the working-tree path, e.g.
`git show "origin/$SDLC_DEFAULT_BRANCH:.github/scripts/sdlc_pin.py" | python - --ref
"origin/$SDLC_DEFAULT_BRANCH"` (exact invocation is a phase (c) implementation detail; the
`id: pin` step and its `ref`/`claude_code` `GITHUB_OUTPUT` contract are unchanged so every
downstream step in all twelve workflows keeps working). The primary checkout of the PR
head/merge ref is untouched in all six files: later steps (pushing commits back to the PR
branch in `sdlc-fix.yml`/`sdlc-abandon.yml`/`sdlc-runbook.yml`, reading the PR's own
`changes/<id>-<slug>/` folder) legitimately need it; only the `sdlc_pin.py` invocation
changes. There is no separate shared file or composite action: the same snippet is applied
identically at all six call sites, because a shared action file living in this repository's
own tree would face the identical trust problem if it were itself read from the PR-head
checkout (see Open questions #2).

The reproducing test (`tests/`, exact filename in plan.md) avoids adding a YAML-parsing
dependency (see Flagged concerns): it locates the `pin` step's `run:` block in each of the
six workflow files by plain text search (the step is identified by `id: pin`, no full YAML
parse needed for one step), then executes the extracted shell snippet inside a throwaway
git fixture whose `origin/<default>` and working-tree copies of `sdlc_pin.py` are rigged to
print different sentinel values; the test asserts the sentinel that actually ran is the
`origin/<default>` one. Run against the current files this fails (the working-tree sentinel
runs); it passes once all six are fixed.

The eval case (`evals/cases/0008-security-supply-chain-sdlc-fix-yml-sdlc/`, `evals/`
is currently empty — this is the suite's first case) follows `evals/README.md`'s documented
layout: `prompt.md` restates the vulnerability class (a workflow step executes a repository
script straight out of an untrusted, unreviewed checkout before any review gate), and
`checks.yaml` requires the diff to stay inside the six workflow files, `tests/` and
`evals/`, and requires the reproducing test's command to exit 0.

## Open questions from intent
- "Where else does the supply-chain pattern occur, and does one fix cover every place?"
  Answered from the codebase: beyond the four files the finding names, `sdlc-test.yml` and
  `sdlc-deploy.yml` show a narrower instance of the same class — a checkout of the PR's
  merge ref, then the `pin` step's `sdlc_pin.py` execution, before `run_phase.py`'s own
  actor-identity check runs later in the job — reachable only once a triage/write-permission
  label is applied. `sdlc-build.yml`/`sdlc-design.yml` are already safe (gated on
  `pull_request.merged == true` before anything but the "find the change" step runs).
  `sdlc-release.yml` already implements the correct pattern (checkout pinned to
  `merge_commit_sha`, read-only permissions, no model secret) and is a template for the fix.
  `sdlc-detect.yml`/`sdlc-digest.yml`/`sdlc-scan.yml` have no `pull_request` trigger. One
  fix — execute the default branch's copy of `sdlc_pin.py`, never the checkout's
  working-tree copy — covers every place with the pattern, applied identically at the six
  sites named in Requirements.
- "Is a shared guard (a helper, a middleware, a schema) better than local fixes?" Answered:
  the guard is the same snippet repeated at all six call sites, not a shared file or
  composite action — see Design, last paragraph of the first section.
- "Which eval case captures the class so it does not return?" Answered: shape given in
  Design's last paragraph, following `evals/README.md`'s documented layout; the exact
  `checks.yaml` content is written in phase (c) (plan.md lists it under Files that change).

## Flagged concerns
- Risk-list item `production config` (sdlc.yaml) is touched: the six workflows hold a
  write-scoped `GITHUB_TOKEN` and, in four of the six, both model secrets, and they directly
  control the CI/CD pipeline that gates production actions (`sdlc.yaml: deploy.production:
  true`), including `sdlc-deploy.yml` itself (phase e). Security-baseline rule 8. Open —
  needs the owner's `state/cli.py accept-risk`.
- Scope beyond the four files the finding names: including `sdlc-test.yml` and
  `sdlc-deploy.yml` is this design's judgment call (Open questions #1); their exploitation
  bar is higher than the other four (a triage/write-permission label must be applied first).
  The owner may prefer to narrow the fix to the four named files and track the other two
  separately. Open.
- Step-ordering prerequisite: extracting the trusted copy via `git show
  "origin/$SDLC_DEFAULT_BRANCH:.github/scripts/sdlc_pin.py"` needs that ref fetched locally
  first; none of the six workflows fetch it before the `pin` step today (`sdlc_pin.py`
  currently fetches it lazily, from inside the untrusted copy, only when it reads
  `sdlc.yaml`). The fix adds an explicit `git fetch` ahead of an existing step every SDLC
  workflow phase depends on. A guess made because the intent does not specify the mechanism.
  Open.
- Test approach is new territory for this project: nothing in `tests/` today exercises
  `.github/workflows/*.yml`; the shape (extract a step's shell block by text search, execute
  it against a rigged git fixture) is this design's proposal, not an established project
  pattern. Open — the owner should confirm it before build.
- [x] No new runtime dependency for the reproducing test: decided per coding-standards
  rule 5 (no new dependency without a `plan.md` Risks line and the owner's merge) and
  CLAUDE.md's "Keep the project minimal" convention — the test uses text extraction of the
  `pin` step's `run:` block plus an executable shell-fixture check, not a YAML-parsing
  library, even though `PyYAML` happens to be importable in this environment.

## Acceptance
- All six touched workflow files keep a step `id: pin` producing `ref=`/`claude_code=`
  `GITHUB_OUTPUT` values in the same shape as today, now sourced only from the default
  branch's copy of `.github/scripts/sdlc_pin.py`.
- The new reproducing test fails against the pre-fix content of the six files and passes
  once all six are fixed, run via `python -m pytest`.
- `python -m compileall -q .` exits 0 with no output; `python -m pytest` reports all tests
  passed (the existing 9 plus the new one(s)); `python -m ruff check .` reports
  `All checks passed!`.
- `evals/cases/0008-security-supply-chain-sdlc-fix-yml-sdlc/{prompt.md,checks.yaml}` exists,
  matching `evals/README.md`'s documented layout.
- The diff touches only the six named workflow files, `tests/`, `evals/cases/` and this
  change's own `changes/0008-security-supply-chain-sdlc-fix-yml-sdlc/` folder — no `.env`,
  no other `changes/<id>-<slug>/`, no `.claude/**`, `CLAUDE.md`, `REVIEW.md` or `sdlc.yaml`.
