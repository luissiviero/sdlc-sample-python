# Intent: security: ssrf: sandbox.failIfUnavailable is false, so on any runner where
Author: security review (phase f). Status: proposed. Change id: 0011. Entry route: incident scan:eda9f21137cf4079.

## Problem
The weekly security review of the codebase at commit `94c013506f5d` found an Important ssrf finding in `.claude/settings.json:41`: sandbox.failIfUnavailable is false, so on any runner where the OS-level sandbox cannot be initialized the session silently runs unsandboxed instead of stopping, dropping the sandbox's network allow-list (github.com, pypi.org, files.pythonhosted.org) that is supposed to bound every outbound call a session's allowed Bash commands (e.g. `git push`, `pip install`) can make.

Until it is fixed the weakness stays in the code the project ships. The review is read-only; nothing has been changed.

## Proposed outcome
The finding is bounded (one file, one patch): `.claude/settings.json:41` no longer has the ssrf weakness, proven by a new test that reproduces it before the fix and passes after it. The review suggests this patch, stored as `evidence/suggested-patch.diff` for the build run to apply and check:

```diff
--- a/.claude/settings.json
+++ b/.claude/settings.json
@@ -39,7 +39,7 @@
   "sandbox": {
     "enabled": true,
-    "failIfUnavailable": false,
+    "failIfUnavailable": true,
     "allowUnsandboxedCommands": false,
     "network": {
       "allowedDomains": [
```

## Affected users and systems
- `.claude/settings.json` and whatever calls it
- Users of luissiviero/sdlc-sample-python

## Constraints
- The security-baseline skill applies to the fix; no new dependency without a Risks line in plan.md.
- A test that reproduces the vulnerability is written first; no pre-existing test is edited to make the fix pass.
- Never quote a credential in the change, its tests or its evidence.

## Open questions
none

## Evidence
- Where: `.claude/settings.json:41` (https://github.com/luissiviero/sdlc-sample-python/blob/94c013506f5d782870868bfb0d65ff43ba74ca95/.claude/settings.json#L41)
- Class: ssrf; severity: Important; bounded: yes
- Commit reviewed: `94c013506f5d782870868bfb0d65ff43ba74ca95`
- The review's words: "sandbox.failIfUnavailable is false, so on any runner where the OS-level sandbox cannot be initialized the session silently runs unsandboxed instead of stopping, dropping the sandbox's network allow-list (github.com, pypi.org, files.pythonhosted.org) that is supposed to bound every outbound call a session's allowed Bash commands (e.g. `git push`, `pip install`) can make." (rule: Rule 7 Network)
- Finding signature: `eda9f21137cf4079` (`evidence/scan-finding.json`); closing this pull request with a comment dismisses it, and it does not return (article p.47 step 4).
