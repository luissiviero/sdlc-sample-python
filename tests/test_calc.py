import pytest

from sample_pkg import add, divide, mean, percent


def test_add():
    assert add(2, 3) == 5


def test_divide_by_zero_raises():
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)


def test_percent():
    assert percent(1, 4) == 25.0
    assert percent(7, 100) == 7.0


def test_percent_zero_whole_raises():
    with pytest.raises(ZeroDivisionError):
        percent(1, 0)


def test_mean():
    assert mean([1, 2, 3, 4]) == 2.5


def test_mean_single_element():
    assert mean([5]) == 5.0


def test_mean_empty():
    with pytest.raises(ValueError):
        mean([])


def test_mean_accepts_non_sequence_collection():
    assert mean({1.0, 2.0, 3.0}) == 2.0
