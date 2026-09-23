<!-- Proposed CLAUDE.md line (spec.md Design: "the one-line addition describing percent is
     proposed as a suggestion in the build-phase PR body for the owner to apply"). Replaces
     the current Layout line for sample_pkg/calc.py. Only the owner edits CLAUDE.md. -->
- `sample_pkg/calc.py`: `add`, `divide` and `percent`. `divide` raises `ZeroDivisionError` on a zero divisor; `percent` reuses `divide`, so a zero `whole` raises the same error.
