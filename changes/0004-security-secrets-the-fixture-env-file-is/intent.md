# Intent: security: secrets: The fixture `.env` file is committed and tracked in git (pre
Author: security review (phase f). Status: proposed. Change id: 0004. Entry route: incident scan:78079f5d37f8daa3.

## Problem
The weekly security review of the codebase at commit `26e6ad73a12a` found an Important secrets finding in `.env:1`: The fixture `.env` file is committed and tracked in git (present since the seed commit, not listed in .gitignore), so the credential it holds is permanently retrievable from repository history for anyone with repo/clone access, even though the Read(.env*) deny rule stops the model from viewing it in a session.

Until it is fixed the weakness stays in the code the project ships. The review is read-only; nothing has been changed.

## Proposed outcome
No instance of this secrets weakness remains in the codebase: the case at `.env:1` and every other place with the same pattern are fixed, each proven by a test, and an eval case for the class keeps it from returning (article p.48 step 7).

## Affected users and systems
- `.env` and whatever calls it; the design pass finds the other places
- Users of luissiviero/sdlc-sample-python

## Constraints
- The security-baseline skill applies to the fix; no new dependency without a Risks line in plan.md.
- A test that reproduces the vulnerability is written first; no pre-existing test is edited to make the fix pass.
- Never quote a credential in the change, its tests or its evidence.

## Open questions
- Where else does the secrets pattern occur, and does one fix cover every place?
- Is a shared guard (a helper, a middleware, a schema) better than local fixes?
- Which eval case captures the class so it does not return?

## Evidence
- Where: `.env:1` (https://github.com/luissiviero/sdlc-sample-python/blob/26e6ad73a12a64b206eae2deac2da425ab6912b6/.env#L1)
- Class: secrets; severity: Important; bounded: no
- Commit reviewed: `26e6ad73a12a64b206eae2deac2da425ab6912b6`
- The review's words: "The fixture `.env` file is committed and tracked in git (present since the seed commit, not listed in .gitignore), so the credential it holds is permanently retrievable from repository history for anyone with repo/clone access, even though the Read(.env*) deny rule stops the model from viewing it in a session." (rule: Rule 3 Secrets)
- Finding signature: `78079f5d37f8daa3` (`evidence/scan-finding.json`); closing this pull request with a comment dismisses it, and it does not return (article p.47 step 4).
