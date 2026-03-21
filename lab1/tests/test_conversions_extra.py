import math

import pytest

from lab1.src.conversions import IntConverter


def test_converter_init_validation():
    with pytest.raises(ValueError):
        IntConverter(16)


def test_unsigned_conversion_errors_and_ok():
    conv = IntConverter()
    with pytest.raises(ValueError):
        conv.unsigned_to_binary(-1)
    with pytest.raises(OverflowError):
        conv.unsigned_to_binary(8, width=3)

    bits = conv.unsigned_to_binary(13, width=6)
    assert bits == [0, 0, 1, 1, 0, 1]
    assert conv.unsigned_from_binary(bits) == 13


def test_add_bits_and_helpers():
    conv = IntConverter()
    with pytest.raises(ValueError):
        conv.add_bits([1, 0], [1])

    assert conv.bits_to_string([1, 0, 1]) == "101"
    assert conv.invert([1, 0, 1]) == [0, 1, 0]
    assert conv.plus_one([0, 1, 1]) == [1, 0, 0]
    assert conv.negate_twos([0, 0, 0, 1]) == [1, 1, 1, 1]


def test_direct_reverse_additional_overflow_and_boundaries():
    conv = IntConverter()
    with pytest.raises(OverflowError):
        conv.to_direct(2**31)
    with pytest.raises(OverflowError):
        conv.to_additional(2**31)
    with pytest.raises(OverflowError):
        conv.to_additional(-(2**31) - 1)

    min_value_bits = conv.to_additional(-(2**31))
    assert conv.from_additional(min_value_bits) == -(2**31)

    reverse_bits = conv.to_reverse(-17)
    assert conv.from_reverse(reverse_bits) == -17


def test_float32_special_values():
    conv = IntConverter()

    nan_bits = conv.to_float32(float("nan"))
    assert nan_bits[1:9] == [1] * 8
    assert any(nan_bits[9:])

    inf_bits = conv.to_float32(float("inf"))
    ninf_bits = conv.to_float32(float("-inf"))
    assert inf_bits[0] == 0 and inf_bits[1:9] == [1] * 8 and not any(inf_bits[9:])
    assert ninf_bits[0] == 1 and ninf_bits[1:9] == [1] * 8 and not any(ninf_bits[9:])

    zero_bits = conv.to_float32(0.0)
    neg_zero_bits = conv.to_float32(-0.0)
    assert zero_bits == [0] + [0] * 31
    assert neg_zero_bits[0] == 1 and neg_zero_bits[1:] == [0] * 31
    assert math.copysign(1.0, conv.from_float32(neg_zero_bits)) < 0



