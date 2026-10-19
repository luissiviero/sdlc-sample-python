import pytest

from sample_pkg import divide


def test_divide_by_zero_names_dividend():
    with pytest.raises(ZeroDivisionError) as excinfo:
        divide(1, 0)
    assert str(excinfo.value) == "cannot divide 1 by zero"
