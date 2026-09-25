# Fix round response

Review: PR #35, `luissiviero`, CHANGES_REQUESTED, 2026-09-25T20:18:06Z.

- Request: "this rehearsal is meant to exercise the Go path. Rewrite `evidence/proposal.json`
  to propose the project runbook `runbook:rollback-deploy` (no arguments) with a rationale
  that says it is a rehearsal of the Go authorization, and update the intent's Proposed
  outcome to match. Everything else stays as it is."
  Applied: rewrote `evidence/proposal.json` (route `runbook:rollback-deploy`, `args: {}`,
  rationale naming this as a rehearsal of the Go authorization) and updated `intent.md`'s
  "Proposed outcome" section to match, commit `9abaac3`. Re-ran
  `detect/cli.py dispatch --commit` on the new proposal: since this finding is itself
  `forced: true` / `rule: forced`, a forced finding never pre-approves a runbook regardless
  of the route's normal authorization, so the resolved authorization is `go` and the outcome
  is `go-requested` (not the `preapproved` a non-forced rehearsed rollback would get under
  decision 26) — this is the Go path the request asked to exercise. Gate (f) re-run and
  parked again, this time on `route: runbook rollback-deploy touches a running system
  (authorization: go): Go requested`, asking for `sdlc:go` on the PR. Nothing else in the
  change folder was touched.
