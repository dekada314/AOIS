import math

import pytest

from lab1.src.calculations import LabCalculator
from lab1.src.conversions import IntConverter


def _make_calc() -> LabCalculator:
    return LabCalculator(IntConverter())


def test_shift_left_and_digits_helpers():
    assert LabCalculator._shift_left([1, 0, 1], 0) == [1, 0, 1]
    assert LabCalculator._shift_left([1, 0, 1], 5) == [0, 0, 0]
    assert LabCalculator._number_to_digits(0) == [0]
    assert LabCalculator._number_to_digits(905) == [9, 0, 5]


def test_divide_direct_zero_and_negative_small_result():
    calc = _make_calc()
    with pytest.raises(ZeroDivisionError):
        calc.divide_direct(10, 0)

    result = calc.divide_direct(1, -2)
    assert result["decimal_result"] == "-0.50000"
    assert result["integer_bits"][0] == 1


def test_multiply_zero_sign_is_zero():
    calc = _make_calc()
    result = calc.multiply_direct(0, -123)
    assert result["result_decimal"] == 0
    assert result["result_bits"][0] == 0


def test_float_operation_invalid_and_division_by_zero_branch():
    calc = _make_calc()
    with pytest.raises(ValueError):
        calc.float_operation(1.0, 2.0, "%")

    result = calc.float_operation(5.0, 0.0, "/")
    assert math.isinf(result["result_decimal"])
    assert result["result_bits"][1:9] == [1] * 8


def test_float_operation_sub_mul_div_nonzero():
    calc = _make_calc()
    sub_result = calc.float_operation(7.5, 2.0, "-")
    mul_result = calc.float_operation(1.5, 2.0, "*")
    div_result = calc.float_operation(7.0, 2.0, "/")

    assert sub_result["result_decimal"] == 5.5
    assert mul_result["result_decimal"] == 3.0
    assert div_result["result_decimal"] == 3.5


    result = calc.gray_bcd_add(999, 1)
    assert result["result_decimal"] == 1000
    assert len(result["result_bits"]) == 32
