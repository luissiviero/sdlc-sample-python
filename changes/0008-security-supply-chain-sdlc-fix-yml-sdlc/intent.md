# Intent: security: supply-chain: sdlc-fix.yml, sdlc-abandon.yml, sdlc-runbook.yml and
Author: security review (phase f). Status: proposed. Change id: 0008. Entry route: incident scan:25040a03deaeb46c.

## Problem
The weekly security review of the codebase at commit `52cacff59117` found an Important supply-chain finding in `.github/workflows/sdlc-fix.yml:87`: sdlc-fix.yml, sdlc-abandon.yml, sdlc-runbook.yml and sdlc-evals.yml all check out an unmerged, unreviewed pull-request head (or its merge ref) and then execute `.github/scripts/sdlc_pin.py` straight out of that checkout before any review gate runs, so anyone who can push the head branch of an open PR (a same-repo contributor, or the PR author for evals.yml's plain `pull_request` trigger) can replace that script to point the next `actions/checkout` of `luissiviero/sdlc-framework` at a ref they control, or to emit an arbitrary npm version string, and get their own code executed in a job that holds ANTHROPIC_API_KEY, CLAUDE_CODE_OAUTH_TOKEN and a GITHUB_TOKEN scoped contents/pull-requests/issues/checks/actions write - entirely bypassing the branch-protection/PR-review gate the rest of the pipeline relies on, since the PR never has to be merged or approved for the run to fire.

Until it is fixed the weakness stays in the code the project ships. The review is read-only; nothing has been changed.

## Proposed outcome
No instance of this supply-chain weakness remains in the codebase: the case at `.github/workflows/sdlc-fix.yml:87` and every other place with the same pattern are fixed, each proven by a test, and an eval case for the class keeps it from returning (article p.48 step 7).

## Affected users and systems
- `.github/workflows/sdlc-fix.yml` and whatever calls it; the design pass finds the other places
- Users of luissiviero/sdlc-sample-python

## Constraints
- The security-baseline skill applies to the fix; no new dependency without a Risks line in plan.md.
- A test that reproduces the vulnerability is written first; no pre-existing test is edited to make the fix pass.
- Never quote a credential in the change, its tests or its evidence.

## Open questions
- Where else does the supply-chain pattern occur, and does one fix cover every place?
- Is a shared guard (a helper, a middleware, a schema) better than local fixes?
- Which eval case captures the class so it does not return?

## Evidence
- Where: `.github/workflows/sdlc-fix.yml:87` (https://github.com/luissiviero/sdlc-sample-python/blob/52cacff591170f1fa98be1ff3dbfc06e5048d6ee/.github/workflows/sdlc-fix.yml#L87)
- Class: supply-chain; severity: Important; bounded: no
- Commit reviewed: `52cacff591170f1fa98be1ff3dbfc06e5048d6ee`
- The review's words: "sdlc-fix.yml, sdlc-abandon.yml, sdlc-runbook.yml and sdlc-evals.yml all check out an unmerged, unreviewed pull-request head (or its merge ref) and then execute `.github/scripts/sdlc_pin.py` straight out of that checkout before any review gate runs, so anyone who can push the head branch of an open PR (a same-repo contributor, or the PR author for evals.yml's plain `pull_request` trigger) can replace that script to point the next `actions/checkout` of `luissiviero/sdlc-framework` at a ref they control, or to emit an arbitrary npm version string, and get their own code executed in a job that holds ANTHROPIC_API_KEY, CLAUDE_CODE_OAUTH_TOKEN and a GITHUB_TOKEN scoped contents/pull-requests/issues/checks/actions write - entirely bypassing the branch-protection/PR-review gate the rest of the pipeline relies on, since the PR never has to be merged or approved for the run to fire." (rule: Rule 2 Input)
- Finding signature: `25040a03deaeb46c` (`evidence/scan-finding.json`); closing this pull request with a comment dismisses it, and it does not return (article p.47 step 4).
