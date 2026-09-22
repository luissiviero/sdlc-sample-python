# Fix response — change 0001, phase (b), round 2 (iteration 2 of cap 2)

Requests collected on 2026-09-22 for PR #5 (`sdlc/0001/b`, head c41c26d before this round):
no review threads, no reviews, no PR comments, no check runs. The change requests are the two
items of the park recorded in `status.yaml: parked_reason` and `evidence/gate-b.json`
"What I need from you" at 87d0476.

| # | Request | What changed | Commit |
|---|---------|--------------|--------|
| 1 | `adversarial_review` (round 1): the pinned formula `divide(part, whole) * 100` returns `7.000000000000001` for `percent(7, 100)` (also 29/100, 57/100) and the planned tests cannot catch it. | Applied the reviewer's reading (a), the one that changes the least while keeping every recorded decision: spec.md Design, Open questions and Requirements and plan.md Files that change / step 1 now pin `return divide(part * 100, whole)`; spec.md Acceptance, plan.md step 3 and Proof add the assertion `percent(7, 100) == 7.0` inside `test_percent` (still two new test functions, still `5 passed`). plan.md Risks explains the operand order; Options not taken records the old formula. Delegation to `divide`, one zero-check, the same `ZeroDivisionError` and message, raw float and no rounding are unchanged. Verified against the real `divide`: 1/4, 7/100, 29/100, 57/100, 3/8, 50/200, 0/5, 150/100 all come back exact under the new order. Reading (b), recording that float noise on exact inputs is accepted, was not taken: accepting a wrong value is the owner's call, not a fix round's. If the owner prefers (b), a review comment saying so is the next round. | 23f9e5d |
| 2 | `risk_list`: hit on spec.md text — the Security-baseline bullet spelled out the four `sdlc.yaml` items. | Reworded to "Rule 8 was checked against `sdlc.yaml` `risk_list`: none of its items is touched" (the smallest change; the items are not named anywhere else in spec.md). plan.md's matching Risks line was shortened the same way for consistency. No `accept-risk` (owner action) was needed or run. | 23f9e5d |

## Gate after this round

`gate/cli.py check --phase b` at 23f9e5d: **wait** (human gate, label `sdlc:b-ready`), all nine
checks green — limits (iterations 2 of cap 2, non-routine), artifacts, design_scope,
open_concerns, commands (build/test/lint exit 0), guardrails, risk_list ("no risk-list item
touched"), owner_actions, adversarial_review ("continue"). The park is cleared; the next step
is the owner's merge of PR #5.

The fresh adversarial reviewer (verdict `continue`, non-routine) recorded three nits, none
Important and none applied: (1) scaling `part` first overflows for |part| above about 1.8e306
(`percent(1e307, 1e307)` is `inf` where the old order gave `100.0`; both orders give `inf` for
1e308/1) — unrealistic magnitudes for a percent helper, recorded so the owner sees the
trade-off; (2) the branch is one commit behind `main` (the owner's plugin pin bump to 0.2.5),
no conflict; (3) `.env` is tracked on `main` as the declared fixture, pre-existing, not read.

Iterations used: 2 of the cap 2. A further round parks on the limit unless the owner resets
the count with `gate/cli.py set-iterations`.

Nothing was posted on the PR, nothing resolved on the owner's behalf, no guardrail file
edited, intent.md untouched. The spec header still records plugin 0.2.4 (the branch's
`sdlc.yaml` pin); `main` has moved to 0.2.5 since, which is a merge-time detail, not a request.
