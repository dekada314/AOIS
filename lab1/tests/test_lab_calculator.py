from lab1.src.calculations import LabCalculator
from lab1.src.conversions import IntConverter


def _make_calc() -> tuple[IntConverter, LabCalculator]:
    conv = IntConverter()
    calc = LabCalculator(conv)
    return conv, calc


def test_add_sub_additional():
    _, calc = _make_calc()
    add_result = calc.add_additional(25, -9)
    sub_result = calc.subtract_additional(25, -9)
    assert add_result["result_decimal"] == 16
    assert sub_result["result_decimal"] == 34

def test_divide_direct():
    _, calc = _make_calc()
    result = calc.divide_direct(37, -5)
    assert result["decimal_result"] == "-7.40000"
    assert len(result["fraction_bits"]) == 32

def test_gray_bcd_add():
    _, calc = _make_calc()
    result = calc.gray_bcd_add(1234, 567)
    assert result["result_decimal"] == 1801
    assert len(result["result_bits"]) == 32
