# Release notes — change 0017: Name the part in percent's zero-whole error

## What changed

`percent(5, 0)` raises `ZeroDivisionError` with the message `"cannot express 5 as a percent of zero"`: the message names the part.

## Commits

- 25c5e03 build(0017): percent's zero-whole error names the part
- 7695ee7 build(0017): gate (c) evidence
- b3a8ddd run(c): spend recorded; gate commands run after the session
- 1553ae5 test(0017): evidence
- 2fe20cd test(0017): gate (d) evidence
- 8e68e28 run(d): spend recorded; gate commands run after the session
- 767ce1f run(review): spend recorded

## Evidence

test green, build green, lint green, verifier.md present, 1 screenshot(s)

## Review findings

0 Important, 2 nits

## Links

- [intent.md](../intent.md)
- [spec.md](../spec.md)
- [plan.md](../plan.md)
