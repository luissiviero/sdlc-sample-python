## Verdict
Object: decide `Collection[float]`, not the framed `Sequence[float]` vs `Iterable[float]` pair.

## The case against
1. The concern is a false dichotomy. The agreed body, `divide(sum(values), len(values))`, needs
   exactly `__iter__` + `__len__` — that is `collections.abc.Collection`. `Sequence` further
   demands `__getitem__`, `index`, `count` and ordering, none of which `mean` uses.
2. So "simpler / keep it minimal" does not favour `Sequence`: `Collection[float]` costs the same
   one import and zero materialising code, yet type-admits `set`, `frozenset`, `dict.keys()` and
   `dict.values()`, which already run correctly today. The minimality constraint defeats only
   `Iterable`; it says nothing for `Sequence` over `Collection`.
3. Picking `Sequence` therefore ships a signature that under-promises what the code does — a
   contract narrower than the implementation, which callers and any future type checker will
   read as a prohibition the author never meant.
4. Nothing in this project can catch the mistake either way: the definition-of-done targets are
   `compileall`, `pytest`, `ruff` — no type checker, no runtime `isinstance`. All three planned
   tests use list literals, so they pass identically under `Sequence`, `Collection` or a wrong
   `Iterable`. This is the "test that still passes with the bug": if the panel instead chose
   `Iterable[float]` and the implementer forgot `values = list(values)`, plan.md's Proof list
   would stay green while any generator caller got `TypeError: ... has no len()` — and argument
   evaluation order means `sum()` consumes the generator first, so even a caught-and-retried
   call sees it empty. Choosing `Iterable` must therefore also add a generator test to Acceptance.
5. Hidden coupling to concern 1: if empty input resolves to `0.0` written as
   `if not values: return 0.0`, truthiness is right for a `Collection` but silently wrong for an
   iterator (generators are always truthy). The docstring must say "a sized collection, not a
   one-shot iterator", or that trap is left for phase (c).
6. Counterweight I accept: nothing calls `mean` yet and widening a hint later is backward
   compatible, so the cost of `Sequence` is low. That argues the decision is cheap, not correct —
   the panel exists to settle it once.

I would accept plain `Sequence[float]` if the panel records a reason rather than a default:
that indexing/ordering is deliberately part of `mean`'s contract, or that the owner wants the
annotation vocabulary kept to `Sequence`/`Iterable` for consistency with a future function.
