## Verdict
No objection to letting the Proposed outcome win and updating the one assertion in `tests/test_calc.py`, on the condition that the decision record says it supersedes change 0015's outcome "the message names `whole`".

## The case against
1. The easy answer treats the Constraint as a slip. Part of it is not. `test_percent_zero_whole_error_names_whole` is the proof test of change 0015 (a fix whose test was written first). That change's owner-stated outcome was "`percent(1, 0)` raises `ZeroDivisionError` whose message names `whole`". The new text, "cannot express 1 as a percent of zero", drops the word `whole`. The spec counts that as a gain (ux "drops the internal parameter name"). In effect, the edit reverses a settled owner outcome by editing that outcome's own proof test.
2. After the edit, the test's name still says "names_whole" while its assertion names the part. The plan rejects a rename "to keep the edit to one line". The result is a test whose name misstates what it checks, inside the very file the owner asked to leave alone.
3. The point of a "tests are not changed" constraint is to stop a run from changing an assertion until the suite goes green. This resolution does exactly that kind of edit. The only thing that sets it apart is that the panel, not the owner, approves it.
Why this is still not a park reason:
- The 0017 intent was written later by the same owner. It gives the exact new message, which carries no `whole`. So the owner knowingly let go of 0015's wording.
- The intent's "Affected users and systems" list leaves out `tests/test_calc.py`. That shows the owner did not know the file pinned the message, so the Constraint conflicts by accident.
- The updated assertion is just as strict (exact equality), so nothing gets weaker. The other choice, keeping the old message, cancels the whole change.
- No message can satisfy both statements, because the existing test asserts exact equality.
What I would decide: the Proposed outcome wins and the assertion is updated. The decision text should say "supersedes 0015's 'names `whole`' outcome". The test's stale name should be either renamed or listed as a known nit.
What would make me accept the plan exactly as written: the owner confirming that a misleading test name is acceptable in the sample.
