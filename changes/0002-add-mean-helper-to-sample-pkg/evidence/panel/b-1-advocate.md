## Verdict
Reject the obvious resolution: `mean([])` should raise an explicit `ValueError` from `mean` itself, not inherit `ZeroDivisionError` from `divide` (and `0.0` must be rejected outright).

## The case against
The easy answer — keep `divide(sum(values), len(values))` bare and let `divide` raise — is not a
decision, it is the absence of one: the behaviour intent.md asked design to *choose* would be an
accident of the implementation, emerging from a helper's internals rather than from `mean`'s own
code. Intent requires the behaviour "stated in the docstring"; a docstring line describing a raise
that no statement in the function performs documents a side effect, and the next person who writes
`sum(values) / len(values)` inline is free to change it without touching the docstring.
The consistency-with-`percent` argument is a false analogy. `percent(1, 0)`'s divisor is the
caller's own argument, so `ZeroDivisionError("b must not be zero")` is actionable. `mean([])`'s
divisor is derived (`len`), the caller supplied no `b`, and the message they get names a parameter
of a function they never called — an internal name leaking into the diagnostic (ux-conventions
rule 4's spirit, even though spec.md reasonably marks that skill n/a here).
It also breaks the caller this function is for. `ZeroDivisionError` is an `ArithmeticError`;
callers already wrap arithmetic in `except ZeroDivisionError` to substitute or retry, and would
silently fold "I have no data" into "I divided by zero" — two different remedies. Anyone arriving
from `statistics.mean` writes `except ValueError` (`StatisticsError` subclasses it) and is silently
broken. Intent's Problem says each caller today invents its own empty-list answer, so there is no
incumbent contract to preserve — only an accident to ratify.
And the test would pass with the bug still in. `pytest.raises(ZeroDivisionError): mean([])` is
satisfied by `divide(len(values), sum(values))`, by `divide(0, 0)`, by any body that reaches
`divide` with a zero second argument; it pins `divide`'s behaviour, not `mean`'s. An explicit
`if not values: raise ValueError("mean() requires at least one value")` with
`pytest.raises(ValueError, match=...)` pins code this change owns.
Separately, `0.0` is the worst of the three and needs no panel: it fabricates a datum, reporting
"no data" as a real average that then propagates through downstream arithmetic undetected.

What I would decide: explicit guard, `ValueError`, docstring line, message-matching test.
What would make me accept `ZeroDivisionError`: an owner-stated convention in CLAUDE.md that
`sample_pkg`'s arithmetic helpers surface arithmetic errors uniformly, *plus* a message raised by
`mean` naming the empty input (not `divide`'s "b") and a test asserting that message — i.e. the
behaviour still owned and proved by `mean`.
