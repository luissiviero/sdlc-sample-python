# Plan: security: supply-chain: sdlc-fix.yml, sdlc-abandon.yml, sdlc-runbook.yml and (from intent.md 2026-09-28, spec.md 2026-09-28)

## Files that change
- `tests/test_workflow_pin_trust.py` — new. The reproducing test: for each of the six
  workflow files below, extracts the `id: pin` step's `run:` block by plain text search and
  executes it inside a throwaway git fixture whose `origin/<default>` and working-tree
  copies of `.github/scripts/sdlc_pin.py` print different sentinel values; asserts the
  `origin/<default>` sentinel is the one that ran. Written first, and seen to fail against
  the unfixed workflow files (build guide step 25 pattern; the change is `change_type:
  feature` in `status.yaml` but the intent's own Constraints require this regardless).
- `.github/workflows/sdlc-fix.yml` — the `pin` step (currently `sdlc-fix.yml:93-97`) gains a
  preliminary `git fetch origin "$SDLC_DEFAULT_BRANCH"` and executes
  `git show "origin/$SDLC_DEFAULT_BRANCH:.github/scripts/sdlc_pin.py"` piped to `python`
  instead of `python .github/scripts/sdlc_pin.py` from the working tree; `id: pin` and its
  `ref`/`claude_code` outputs are unchanged.
- `.github/workflows/sdlc-abandon.yml` — same change to its `pin` step
  (currently `sdlc-abandon.yml:61-65`).
- `.github/workflows/sdlc-runbook.yml` — same change to its `pin` step
  (currently `sdlc-runbook.yml:57-61`).
- `.github/workflows/sdlc-evals.yml` — same change to its `pin` step
  (currently `sdlc-evals.yml:56-60`).
- `.github/workflows/sdlc-test.yml` — same change to its `pin` step (the narrower instance
  this design pass found; spec.md Open questions #1).
- `.github/workflows/sdlc-deploy.yml` — same change to its `pin` step (same reason).
- `evals/cases/0008-security-supply-chain-sdlc-fix-yml-sdlc/prompt.md` — new. States the
  vulnerability class per `evals/README.md`'s layout: a workflow step executes a repository
  script straight out of an untrusted, unreviewed checkout before any review gate.
- `evals/cases/0008-security-supply-chain-sdlc-fix-yml-sdlc/checks.yaml` — new. Requires the
  diff to stay inside the six workflow files, `tests/` and `evals/`, and requires
  `python -m pytest tests/test_workflow_pin_trust.py` to exit 0.

## Order of work
1. Write `tests/test_workflow_pin_trust.py` and run it; confirm it fails against the current
   (unfixed) content of all six workflow files — the reproducing test, written before any
   fix (intent Constraints).
2. Fix `.github/workflows/sdlc-fix.yml`'s `pin` step; re-run the test and confirm that
   file's case now passes while the other five still fail.
3. Fix `.github/workflows/sdlc-abandon.yml`'s `pin` step the same way.
4. Fix `.github/workflows/sdlc-runbook.yml`'s `pin` step the same way.
5. Fix `.github/workflows/sdlc-evals.yml`'s `pin` step the same way.
6. Fix `.github/workflows/sdlc-test.yml`'s `pin` step the same way.
7. Fix `.github/workflows/sdlc-deploy.yml`'s `pin` step the same way; run the full test file
   and confirm all six cases pass.
8. Add the eval case (`evals/cases/0008-security-supply-chain-sdlc-fix-yml-sdlc/prompt.md`
   and `checks.yaml`).
9. Run the project's verification block in full: `python -m compileall -q .`,
   `python -m pytest`, `python -m ruff check .`; paste the literal output (CLAUDE.md
   Verifying your work; definition-of-done).

## Risks
1. **What this could break**: every one of the twelve SDLC workflows reads
   `steps.pin.outputs.ref`/`steps.pin.outputs.claude_code` from the `pin` step — the
   `actions/checkout` of `luissiviero/sdlc-framework` and the `npm install -g
   @anthropic-ai/claude-code@...` step, in all twelve files, not just the six touched here.
   A malformed `pin` step in any of the six breaks every later phase run through that
   workflow (nobody would be notified — a run that can't finish parks). Callers: none
   outside the workflow files themselves; no Python code imports or calls `sdlc_pin.py`
   directly.
2. **Riskiest step**: step 1 through 7 (rewriting the `pin` step's `run:` content in each of
   the six files) — a one-character mistake in the `git show`/pipe syntax silently breaks
   the pin step for that workflow's every future run, and nothing in `ci.yml` (Python
   build/test/lint only) would catch a broken workflow step; only the new reproducing test
   and, ultimately, the workflow actually firing in CI would. Mitigation: apply the exact
   same snippet at all six sites (reduces one-off mistakes), and make the reproducing test
   execute the real extracted shell snippet (not just grep for a string) so a syntactically
   broken pin step fails the test too.
3. **Fetch-ordering risk** (spec.md Flagged concerns): `git show
   "origin/$SDLC_DEFAULT_BRANCH:..."` needs that ref present locally. `sdlc-fix.yml`'s first
   checkout uses `fetch-depth: 0` but only for the checked-out ref, not necessarily every
   remote branch, so `origin/$SDLC_DEFAULT_BRANCH` may not exist locally yet at the `pin`
   step; the added `git fetch origin "$SDLC_DEFAULT_BRANCH"` must run before the `git show`,
   in all six files. Not yet confirmed for `sdlc-abandon.yml`/`sdlc-runbook.yml`/
   `sdlc-evals.yml`/`sdlc-test.yml`/`sdlc-deploy.yml`'s own checkout options individually —
   phase (c) confirms each one and adds the fetch regardless, since it is cheap and
   idempotent.
4. **`sdlc_pin.py` run via a pipe, not a file path**: piping the script's bytes to
   `python -` means `sys.argv[0]`/`__file__` are not a real path. Phase (c) must confirm
   `sdlc_pin.py` does not rely on `__file__` (its own relative imports, if any) before
   relying on this invocation shape; if it does, the fetch step instead writes the trusted
   bytes to a temp file and invokes `python <tempfile>` (`$TMPDIR`, not `/tmp` per the
   project's sandbox convention).
5. **Risk-list hit** (`production config`): flagged in spec.md, open; the change parks at
   gate (b) until the owner accepts it (`state/cli.py accept-risk`) — expected, not a defect
   to fix here.

## Options not taken
- **Re-architecting the primary checkout** (default branch first, PR content pulled in only
  for the specific paths each workflow legitimately needs) instead of fixing only the
  `sdlc_pin.py` invocation: rejected. `sdlc-fix.yml`/`sdlc-abandon.yml`/`sdlc-runbook.yml`
  intentionally check out the PR's own head to commit back onto it (the files' own header
  comments say so); replacing that primary checkout would be a much larger, riskier change
  than the vulnerability requires, and the finding's actual mechanism is specifically that
  the *script* runs untrusted, not that the PR content is checked out at all.
- **A shared composite action or script file** instead of the same snippet repeated six
  times: rejected (spec.md, Open questions #2) — a shared file living in this repository's
  tree would face the identical trust problem if it were itself read from the PR-head
  checkout; the six sites would still each need the same `git fetch`/`git show` guard ahead
  of using it, so a shared file adds indirection without removing the duplication.
- **A YAML-parsing test** (`import yaml`, walk the parsed steps) instead of text extraction
  plus an executable fixture: rejected (spec.md Flagged concerns, closed) — introduces a
  runtime dependency this project does not otherwise have, against coding-standards rule 5
  and CLAUDE.md's "Keep the project minimal" convention, for a check that a plain-text
  extraction of one named step (`id: pin`) does not need.
- **Narrowing the fix to only the four files the finding names**, leaving `sdlc-test.yml`
  and `sdlc-deploy.yml` for a follow-up change: considered, not taken by this plan (spec.md
  Flagged concerns leaves it open for the owner to override) — the intent's own Proposed
  outcome asks for "every other place with the same pattern," and the design pass found two
  more with the identical structural flaw, so this plan fixes all six; the owner can still
  ask for the narrower scope with a review comment (`/sdlc-fix`).

## Proof
- `tests/test_workflow_pin_trust.py` (new; written in step 1) — fails on the current six
  files, passes once all six are fixed. This is the test named by the intent's "a test that
  reproduces the vulnerability is written first" constraint.
- `python -m pytest` — all tests pass (the existing `tests/test_calc.py`,
  `tests/test_flag.py`, plus the new file); paste the literal `N passed in ...` line.
- `python -m compileall -q .` — no output, exit code 0.
- `python -m ruff check .` — `All checks passed!`.
- `evals/cases/0008-security-supply-chain-sdlc-fix-yml-sdlc/checks.yaml` — the case's own
  check that `python -m pytest tests/test_workflow_pin_trust.py` exits 0 (evidence that the
  eval case actually exercises the fix, not just documents it).

## Interrogation
1. **What could this change break?** Every one of the twelve SDLC workflows depends on the
   `pin` step's `ref`/`claude_code` outputs (see Risks #1); only six are edited, but a
   mistake in any of them stops that workflow's every future phase run. No Python caller
   depends on `sdlc_pin.py`'s CLI directly — it is invoked only from workflow YAML.
2. **Which step is riskiest, and why?** Rewriting the `pin` step's shell content in each of
   the six files (Order of work steps 2–7): it sits on the critical path of every phase this
   project runs through CI, and nothing in the existing Python test/lint/build targets can
   catch a broken GitHub Actions step directly — only the new reproducing test, which
   executes the real extracted snippet, stands in for that check (Risks #2).
3. **What other options were considered, and why not?** See Options not taken: a checkout
   re-architecture (too large for the actual flaw), a shared composite-action file (doesn't
   remove the duplication, adds indirection), a YAML-parsing test (new dependency against
   project convention), and narrowing scope to the four named files (left open for the owner
   rather than decided here, since the intent asks for full coverage of the pattern).
4. **Could an engineer who never saw this conversation implement this from the plan alone?**
   Yes, with two things worth restating here since they are easy to miss from Files that
   change alone: (a) the fix is to *which copy* of `sdlc_pin.py` executes, not to the
   primary PR-head/merge-ref checkout, which stays as it is in all six files; (b) the
   `git fetch origin "$SDLC_DEFAULT_BRANCH"` addition must land *before* the `git show`
   that extracts the trusted script, in every file, or the extraction fails closed (Risks
   #3).
5. **Does every item in Proof exist as a runnable test, or is it still to be written?**
   `tests/test_workflow_pin_trust.py` and the eval case's `checks.yaml` are both still to be
   written (Order of work steps 1 and 8); `tests/test_calc.py` and `tests/test_flag.py`
   already exist and are unmodified by this change.
