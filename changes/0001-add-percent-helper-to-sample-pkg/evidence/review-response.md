# Review response — change 0001, phase (e)

## Important finding: CLAUDE.md's Layout line for `sample_pkg/calc.py` is stale (`CLAUDE.md:22`)

The finding is correct, and I could not close it within this run's fix-iteration cap
(2 rounds for a non-routine change; both are now spent).

What was tried: `spec.md`'s Design section says the one-line addition is "proposed as a
suggestion in the build-phase PR body for the owner to apply," since `CLAUDE.md` is a
protected path I cannot edit directly. The framework has exactly one mechanism that puts
proposed `CLAUDE.md` text into the PR body: `evidence/claude-md-proposals.md`, rendered
under "## Proposed CLAUDE.md lines" by `pr/description.py`. I wrote that file with the
proposed replacement line (`sample_pkg/calc.py`: `add`, `divide` and `percent`, plus the
`percent`/`ZeroDivisionError` note) and committed it.

That file is also owned by `review/cli.py validate` (`review/findings.py: PROPOSALS_FILE`),
which regenerates it from `claude_md_lines(repeated)` every time validate runs, and deletes
it when `repeated` is empty. `repeated` only holds findings whose signature was first seen
on an *earlier* change (`update_seen` in `review/findings.py`); this is change 0001's own
first review of its own diff, so both signatures have `first_change == last_change ==
"0001"` in `changes/.review-seen.json`, `repeated` is empty, and the very next `validate`
run (this one) unlinked the file I had just committed. The mechanism spec.md's Design
pointed at only fires for a finding that has already recurred across a *different* change —
it has no path for proposing a brand-new, first-occurrence line, which is exactly this
case (`percent` shipping for the first time).

I'm leaving the finding open rather than silently reworking it further: the fix would need
either a change to how `pr/description.py`/`review/cli.py` source proposed lines (plugin
code, out of scope for a project-level change and not something this run should alter), or
the owner applying the one-line `CLAUDE.md` edit by hand. The proposed text, for reference:

> `sample_pkg/calc.py`: `add`, `divide` and `percent`. `divide` raises `ZeroDivisionError`
> on a zero divisor; `percent` reuses `divide`, so a zero `whole` raises the same error.

## Nit: `sample_pkg/calc.py:12` float overflow at extreme magnitudes

Not fixed (nits are not fixed in this loop). Already surfaced and accepted as not-Important
in prior rounds; restated by this round's reviewer for completeness.
