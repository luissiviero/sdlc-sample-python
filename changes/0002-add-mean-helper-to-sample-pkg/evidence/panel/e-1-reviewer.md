## Verdict
Uphold the finding as Important and correctly resolved — mark it settled, no further edit needed.

## Why
- REVIEW.md Framework rules require: "Flag when the change has made CLAUDE.md outdated" and "the second occurrence of the same finding across reviews produces a one-line entry in CLAUDE.md ... proposed in the review for the owner." Both apply: CLAUDE.md:22-23 still lists only `add`, `divide`, `percent`, and `changes/.review-seen.json` shows this exact CLAUDE.md-outdated pattern occurring in change 0001 (signatures `182179ac0f8bd565`, `f608c482d17f4e00`) and twice already within 0002 (`3c842277b239326e`, `cc24ed45af8ee34d`, count 2) — well past the second occurrence.
- The rule's remedy is "proposed in the review for the owner," not a direct CLAUDE.md edit. `evidence/claude-md-proposals.md` already exists and contains exactly this: a one-line "Things Claude gets wrong" entry proposed for the owner, worded from this same finding.
- Editing CLAUDE.md directly would violate intent.md's Constraints ("guardrail files ... are not edited in the run; the CLAUDE.md line is proposed for the owner") and REVIEW.md's own guardrail rule ("diff must not touch ... CLAUDE.md ... unless the change is the framework itself").
- `status.yaml` confirms `review_override: deferred` and this is item 1 of phase (e)'s panel; the finding is real and Important by rule, but the artifact the rule demands (the proposed line) is already produced, so the correct disposition is to record it as settled/resolved-as-designed rather than escalate for more work.
- Nothing in spec.md, plan.md, or the diff evidence contradicts this: plan.md step 5 explicitly defers the CLAUDE.md line to "the build PR description ... for the owner to add directly."
