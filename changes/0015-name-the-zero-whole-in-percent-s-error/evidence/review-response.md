# Review response — change 0015 (phase e)

Review mode: `parked` (`sdlc.yaml: review`). Two Important findings stand after the fix
round below; neither can be fixed from this session without touching a protected or
locked path, so both are left for the owner's decision at the gate.

## Parked findings

### 1. `CLAUDE.md:14` — Commands table's healthy test output is outdated
`CLAUDE.md` is a guardrail file (`.claude/**`, `CLAUDE.md`, `REVIEW.md`, `sdlc.yaml` are
always protected; the hook denies edits to it from this session). The fix this change
makes raises the passing-test count from 9 to 10, so the Commands table's healthy output
for `test` ("9 passed in 0.01s") is now stale. `review/cli.py validate` already proposes
the corrected line under "Things Claude gets wrong is not the section to use" — see the
PR's "Proposed CLAUDE.md lines" block; the owner applies it in the PR review.

### 2. `tests/test_calc.py` — pre-existing test file modified in a fix-type change
This is a fix-type change (`status.yaml: change_type: fix`), and `tests_locked: true` has
been set since the build phase locked it at commit `82549de8` (the reproducing test for
this fix, `test_percent_zero_whole_error_names_whole`, was appended to the pre-existing
`tests/test_calc.py` rather than a new file, before the lock took effect). The
`test_file_lock` hook now denies any edit to `tests/**` for the rest of this change, so the
file cannot be moved into a new test module or otherwise altered from this session. No
existing test's code was changed — the diff only appends one new test function — and
`gate-d.json`'s `test_lock` check already confirms no test file changed since the lock
commit. The framework's deterministic check still flags any diff touching a pre-existing
test file in a fix-type change, append-only or not, so this is recorded here for the
owner: either waive it in a review comment, or treat it as the lesson that a fix-type
change's reproducing test belongs in a new file from the first commit.

Both findings recur unchanged across fix rounds because neither is fixable from this
session; they are expected to still be open when gate (e) parks.

## Fix-round log
- Round 1 (commit `86ea6d39`): both findings confirmed still present and unfixable from
  this session; no code change made.
- Round 2: re-reviewed at the new HEAD; same two root causes stand (the second review pass
  additionally reported a line-level duplicate of finding 2, `tests/test_calc.py:25`, which
  is the same underlying issue — the test file was touched at all in a fix-type change —
  not a third distinct problem). No code change made; nothing further to fix.
- Round 3 (iteration cap for this routine-classified change): re-reviewed again; the same
  two root causes stand, independently re-verified by the reviewer against the current
  HEAD each time, not copied forward. No further fix is possible without editing a
  guardrail file (`CLAUDE.md`) or a locked test path (`tests/test_calc.py`, locked since
  commit `82549de8`). This is the last fix round the iteration cap (3, routine
  classification) allows; gate (e) is expected to park on these two findings.
