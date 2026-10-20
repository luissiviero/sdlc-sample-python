import pytest

from sample_pkg import divide, percent


def test_divide_by_zero_names_dividend():
    with pytest.raises(ZeroDivisionError) as excinfo:
        divide(1, 0)
    assert str(excinfo.value) == "cannot divide 1 by zero"


def test_percent_zero_whole_names_part():
    with pytest.raises(ZeroDivisionError) as excinfo:
        percent(5, 0)
    assert str(excinfo.value) == "cannot express 5 as a percent of zero"
