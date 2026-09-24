## Verdict
Reject this escalation item — the missing logs are not required at gate (c) and the point restates a deterministic check; continue.

## The case against
1. The premise is factually inverted. `plugin/gate/artifacts.py` sets
   `REQUIRED_EVIDENCE = {"c": (verifier.md,), "d": (test.log, build.log, lint.log, verifier.md),
   "e": (...)}`. `test.log`/`build.log`/`lint.log` are **phase (d)** artifacts, not build-phase
   ones; `definition-of-done/SKILL.md` says the same ("(d) test: fresh-context full run;
   `evidence/test.log`, `build.log`, `lint.log` ... verifier.md"), while its (c) list ends at
   "verifier report in `evidence/verifier.md`; adversarial verdict; gate (c)".
2. The "established convention" cited from change 0001 is a phase-(d) convention: 0001's
   `gate-d.json` carries the check `"evidence present: test.log, build.log, lint.log,
   verifier.md"`, and 0001's `test.log` shows `5 passed`, the post-build state collected in the
   test phase. Change 0002 has no logs for phase (b) either — and gate (b) passed.
3. Those logs are written by `plugin/evidence/collect.py`, a deterministic collector, not by the
   build agent; escalating because the agent did not hand-write them asks for an artifact the
   framework produces elsewhere, and parks a change on a step that has not come due.
4. The audit path the item says a person lacks exists and is machine-made: the gate's own
   `commands` check re-runs build, test and lint at HEAD in a fresh checkout and stores the
   literal stdout plus exit codes in `gate-c.json` (see `gate-b.json`, `"commands": ... "9/5
   passed"`, exit 0). That check runs *after* this verdict, so its absence now proves nothing —
   and quoting it as a reason is precisely the forbidden move (fifth live run, 2026-09-21).
5. `REVIEW.md` "Do not report" names "anything under `changes/*/evidence/`". This item is
   entirely about the contents of that directory.
6. The substantive proof is in the diff, not in `verifier.md`: four tests pin each acceptance
   line (`2.5`, `5.0`, `pytest.raises(ValueError)`, `mean({1.0,2.0,3.0}) == 2.0` for the
   `Collection` contract). `verifier.md` adds what a log cannot — generator rejection, `percent`
   and `divide` unchanged, `__all__` ordering — and discloses its permission denials honestly.

I would decide: overturn item 1, no escalation on this ground. I would accept the escalation if
`REQUIRED_EVIDENCE["c"]` listed the three logs, if the gate's `commands` check were disabled for
phase (c), or if an acceptance criterion rested on `verifier.md`'s word alone with no test in the
diff pinning it — none of which holds here.
