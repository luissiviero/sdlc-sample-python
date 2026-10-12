# Intent: security: authz: The permissions.deny list only blocks the Edit tool from
Author: security review (phase f). Status: proposed. Change id: 0012. Entry route: incident scan:d6f98f0dff40c7c4.

## Problem
The weekly security review of the codebase at commit `94c013506f5d` found an Important authz finding in `.claude/settings.json:14`: The permissions.deny list only blocks the Edit tool from touching guardrail files (.claude/**, CLAUDE.md, REVIEW.md, sdlc.yaml), but permissions.allow grants unrestricted `Bash(git *)`, so any Claude session (build, test, fix, review) can overwrite those same files via git (e.g. `git checkout <ref> -- CLAUDE.md`, `git show <ref>:sdlc.yaml > sdlc.yaml`, or a direct commit+push) without ever invoking the denied Edit tool, defeating the 'owner changes guardrails only in a reviewed PR' policy stated in CLAUDE.md.

Until it is fixed the weakness stays in the code the project ships. The review is read-only; nothing has been changed.

## Proposed outcome
No instance of this authz weakness remains in the codebase: the case at `.claude/settings.json:14` and every other place with the same pattern are fixed, each proven by a test, and an eval case for the class keeps it from returning (article p.48 step 7).

## Affected users and systems
- `.claude/settings.json` and whatever calls it; the design pass finds the other places
- Users of luissiviero/sdlc-sample-python

## Constraints
- The security-baseline skill applies to the fix; no new dependency without a Risks line in plan.md.
- A test that reproduces the vulnerability is written first; no pre-existing test is edited to make the fix pass.
- Never quote a credential in the change, its tests or its evidence.

## Open questions
- Where else does the authz pattern occur, and does one fix cover every place?
- Is a shared guard (a helper, a middleware, a schema) better than local fixes?
- Which eval case captures the class so it does not return?

## Evidence
- Where: `.claude/settings.json:14` (https://github.com/luissiviero/sdlc-sample-python/blob/94c013506f5d782870868bfb0d65ff43ba74ca95/.claude/settings.json#L14)
- Class: authz; severity: Important; bounded: no
- Commit reviewed: `94c013506f5d782870868bfb0d65ff43ba74ca95`
- The review's words: "The permissions.deny list only blocks the Edit tool from touching guardrail files (.claude/**, CLAUDE.md, REVIEW.md, sdlc.yaml), but permissions.allow grants unrestricted `Bash(git *)`, so any Claude session (build, test, fix, review) can overwrite those same files via git (e.g. `git checkout <ref> -- CLAUDE.md`, `git show <ref>:sdlc.yaml > sdlc.yaml`, or a direct commit+push) without ever invoking the denied Edit tool, defeating the 'owner changes guardrails only in a reviewed PR' policy stated in CLAUDE.md." (rule: Rule 1 Authorization / project guardrail policy (CLAUDE.md: never edit .claude/**, CLAUDE.md, REVIEW.md, sdlc.yaml))
- Finding signature: `d6f98f0dff40c7c4` (`evidence/scan-finding.json`); closing this pull request with a comment dismisses it, and it does not return (article p.47 step 4).
