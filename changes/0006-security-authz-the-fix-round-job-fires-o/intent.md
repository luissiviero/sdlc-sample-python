# Intent: security: authz: The fix-round job fires on any 'changes requested' pull_requ
Author: security review (phase f). Status: proposed. Change id: 0006. Entry route: incident scan:993a71ae434345d1.

## Problem
The weekly security review of the codebase at commit `2be0ff59f9f0` found an Important authz finding in `.github/workflows/sdlc-fix.yml:67`: The fix-round job fires on any 'changes requested' pull_request_review without checking the reviewer's repository association, so on this public repo any GitHub user with mere read access (not a collaborator) can submit a review whose free-text body is fed to a privileged, non-interactive Claude Code run (contents/pull-requests/issues/checks/actions: write, ANTHROPIC_API_KEY and CLAUDE_CODE_OAUTH_TOKEN in env) against an existing pull request - a prompt-injection channel that the label-gated routes in the same file don't share, since applying a label already requires GitHub triage/write permission.

Until it is fixed the weakness stays in the code the project ships. The review is read-only; nothing has been changed.

## Proposed outcome
The finding is bounded (one file, one patch): `.github/workflows/sdlc-fix.yml:67` no longer has the authz weakness, proven by a new test that reproduces it before the fix and passes after it. The review suggests this patch, stored as `evidence/suggested-patch.diff` for the build run to apply and check:

```diff
--- a/.github/workflows/sdlc-fix.yml
+++ b/.github/workflows/sdlc-fix.yml
@@ -63,9 +63,10 @@
     if: >-
       ${{ github.event_name == 'workflow_dispatch' ||
       (github.event_name == 'pull_request_review' &&
       github.event.review.state == 'changes_requested' &&
-      !endsWith(github.event.review.user.login, '[bot]')) ||
+      !endsWith(github.event.review.user.login, '[bot]') &&
+      contains(fromJSON('["OWNER","MEMBER","COLLABORATOR"]'), github.event.review.author_association)) ||
       (github.event_name == 'pull_request' &&
       (github.event.label.name == 'sdlc:accept-risk' ||
       github.event.label.name == 'sdlc:reset-iterations' ||
       github.event.label.name == 'sdlc:unlock-tests')) }}
```

## Affected users and systems
- `.github/workflows/sdlc-fix.yml` and whatever calls it
- Users of luissiviero/sdlc-sample-python

## Constraints
- The security-baseline skill applies to the fix; no new dependency without a Risks line in plan.md.
- A test that reproduces the vulnerability is written first; no pre-existing test is edited to make the fix pass.
- Never quote a credential in the change, its tests or its evidence.

## Open questions
none

## Evidence
- Where: `.github/workflows/sdlc-fix.yml:67` (https://github.com/luissiviero/sdlc-sample-python/blob/2be0ff59f9f08436d22e4cd4b27de7ad4629aaa2/.github/workflows/sdlc-fix.yml#L67)
- Class: authz; severity: Important; bounded: yes
- Commit reviewed: `2be0ff59f9f08436d22e4cd4b27de7ad4629aaa2`
- The review's words: "The fix-round job fires on any 'changes requested' pull_request_review without checking the reviewer's repository association, so on this public repo any GitHub user with mere read access (not a collaborator) can submit a review whose free-text body is fed to a privileged, non-interactive Claude Code run (contents/pull-requests/issues/checks/actions: write, ANTHROPIC_API_KEY and CLAUDE_CODE_OAUTH_TOKEN in env) against an existing pull request - a prompt-injection channel that the label-gated routes in the same file don't share, since applying a label already requires GitHub triage/write permission." (rule: Rule 1 Authentication)
- Finding signature: `993a71ae434345d1` (`evidence/scan-finding.json`); closing this pull request with a comment dismisses it, and it does not return (article p.47 step 4).
