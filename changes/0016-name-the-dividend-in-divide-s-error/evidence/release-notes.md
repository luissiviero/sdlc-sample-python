# Release notes — change 0016: Name the dividend in divide's error

## What changed

`divide(1, 0)` raises `ZeroDivisionError` with the message `"cannot divide 1 by zero"`: the message names the dividend that was being divided.

## Commits

- 614594e intent(0016): Name the dividend in divide's error
- b064d37 run(b): fast lane from intent PR #77 at 614594e11b (decision 30)
- 9433cc6 design(0016): Name the dividend in divide's error
- b02d846 design(0016): gate (b) evidence
- 28b25c0 run(b): spend recorded; gate commands run after the session; gate (b) passed on the fast lane, the build follows (decision 30)
- ce39d18 build(0016): name the dividend in divide's error message
- cb2c87f build(0016): add test_messages.py for divide's zero-divisor message
- 79ba739 build(0016): gate (c) evidence
- cd0d020 run(c): spend recorded; gate commands run after the session
- 83af39b test(0016): evidence
- 30ccc40 test(0016): gate (d) evidence
- bf53fa2 run(d): spend recorded; gate commands run after the session
- feb06c7 review(0016): gate (e) review pass

## Evidence

test green, build green, lint green, verifier.md present, 1 screenshot(s)

## Review findings

0 Important, 0 nits

## Links

- [intent.md](../intent.md)
- [spec.md](../spec.md)
- [plan.md](../plan.md)
