from collections.abc import Collection


def add(a: float, b: float) -> float:
    return a + b


def divide(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("b must not be zero")
    return a / b


def percent(part: float, whole: float) -> float:
    return divide(part * 100, whole)


def mean(values: Collection[float]) -> float:
    """Return the arithmetic mean of values; raises ValueError if values is empty."""
    if not values:
        raise ValueError("mean() requires at least one value")
    return divide(sum(values), len(values))
