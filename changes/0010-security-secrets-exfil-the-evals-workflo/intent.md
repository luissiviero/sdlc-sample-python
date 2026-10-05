# Intent: security: secrets-exfil: The evals workflow runs on a plain `pull_request` trigger
Author: security review (phase f). Status: proposed. Change id: 0010. Entry route: incident scan:992cb085c9e477eb.

## Problem
The weekly security review of the codebase at commit `94c013506f5d` found an Important secrets-exfil finding in `.github/workflows/sdlc-evals.yml:28`: The evals workflow runs on a plain `pull_request` trigger (not `pull_request_target`) scoped only by a `paths` filter on CLAUDE.md/.claude/**/evals/**, so a pull request from any fork that touches one of those paths executes that fork's own copy of this workflow file and of sdlc.yaml's commands.setup, with ANTHROPIC_API_KEY and CLAUDE_CODE_OAUTH_TOKEN available in the job's environment - letting an attacker who opens such a PR add a step (or a setup command) that exfiltrates both secrets over the open internet, since GitHub Actions runners are not subject to the project's own Claude-sandbox network allowlist.

Until it is fixed the weakness stays in the code the project ships. The review is read-only; nothing has been changed.

## Proposed outcome
The finding is bounded (one file, one patch): `.github/workflows/sdlc-evals.yml:28` no longer has the secrets-exfil weakness, proven by a new test that reproduces it before the fix and passes after it. The review suggests this patch, stored as `evidence/suggested-patch.diff` for the build run to apply and check:

```diff
--- a/.github/workflows/sdlc-evals.yml
+++ b/.github/workflows/sdlc-evals.yml
@@ -46,6 +46,11 @@
 jobs:
   evals:
     runs-on: ubuntu-latest
     timeout-minutes: 120
+    # A pull_request run executes the workflow file (and sdlc.yaml commands.setup) from the
+    # PR's own branch, not the default branch's copy; for a fork PR that would hand this
+    # job's secrets, and arbitrary code execution, to content this repository does not
+    # control. Only run with secrets for same-repository branches, schedule or dispatch.
+    if: ${{ github.event_name != 'pull_request' || github.event.pull_request.head.repo.full_name == github.repository }}
     steps:
       - name: Check out the project
         uses: actions/checkout@v5
```

## Affected users and systems
- `.github/workflows/sdlc-evals.yml` and whatever calls it
- Users of luissiviero/sdlc-sample-python

## Constraints
- The security-baseline skill applies to the fix; no new dependency without a Risks line in plan.md.
- A test that reproduces the vulnerability is written first; no pre-existing test is edited to make the fix pass.
- Never quote a credential in the change, its tests or its evidence.

## Open questions
none

## Evidence
- Where: `.github/workflows/sdlc-evals.yml:28` (https://github.com/luissiviero/sdlc-sample-python/blob/94c013506f5d782870868bfb0d65ff43ba74ca95/.github/workflows/sdlc-evals.yml#L28)
- Class: secrets-exfil; severity: Important; bounded: yes
- Commit reviewed: `94c013506f5d782870868bfb0d65ff43ba74ca95`
- The review's words: "The evals workflow runs on a plain `pull_request` trigger (not `pull_request_target`) scoped only by a `paths` filter on CLAUDE.md/.claude/**/evals/**, so a pull request from any fork that touches one of those paths executes that fork's own copy of this workflow file and of sdlc.yaml's commands.setup, with ANTHROPIC_API_KEY and CLAUDE_CODE_OAUTH_TOKEN available in the job's environment - letting an attacker who opens such a PR add a step (or a setup command) that exfiltrates both secrets over the open internet, since GitHub Actions runners are not subject to the project's own Claude-sandbox network allowlist." (rule: Rule 3 Secrets / Rule 7 Network)
- Finding signature: `992cb085c9e477eb` (`evidence/scan-finding.json`); closing this pull request with a comment dismisses it, and it does not return (article p.47 step 4).
