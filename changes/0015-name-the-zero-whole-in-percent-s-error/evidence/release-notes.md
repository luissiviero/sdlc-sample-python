# Release notes — change 0015: Name the zero whole in percent's error

## What changed

`percent(1, 0)` raises `ZeroDivisionError` whose message names `whole`, for example `"whole must not be zero"`.

## Commits

- 0e4fed5 design(0015): Name the zero whole in percent's error
- b641069 design(0015): gate (b) evidence
- 5bd1b0b run(b): spend recorded; gate commands run after the session; gate (b) passed on the fast lane, the build follows (decision 30)
- f1f5fc5 fix(0015): reproducing test
- 82549de build(0015): catch zero whole and re-raise with the whole-naming message
- 1376511 build(0015): gate (c) evidence
- 85ab8e8 run(c): spend recorded; gate commands run after the session
- c3cd0ba test(0015): evidence
- 2b612b7 test(0015): gate (d) evidence
- 730857b run(d): spend recorded; gate commands run after the session
- e90c09c run(review): spend recorded
- 9d6110b run(review): spend recorded
- 86ea6d3 review(0015): fix round 1 - two findings parked (guardrail/locked paths)
- ed36458 review(0015): fix round 2 - same two findings still parked
- e1ee0db review(0015): fix round 3 (iteration cap) - same two findings still parked

## Evidence

test deferred to the runner, build deferred to the runner, lint deferred to the runner, verifier.md present, 1 screenshot(s)

## Review findings

3 Important, 1 nits

## Links

- [intent.md](../intent.md)
- [spec.md](../spec.md)
- [plan.md](../plan.md)
