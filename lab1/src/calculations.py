from .conversions import IntConverter


class LabCalculator:
    def __init__(self, converter: IntConverter | None = None, division_precision: int = 5):
        self.converter = converter or IntConverter()
        self.division_precision = division_precision

    def convert_number(self, number: int) -> dict[str, int | list[int]]:
        direct_bits = self.converter.to_direct(number)
        reverse_bits = self.converter.to_reverse(number)
        additional_bits = self.converter.to_additional(number)
        return {
            "direct_bits": direct_bits,
            "reverse_bits": reverse_bits,
            "additional_bits": additional_bits,
            "direct_decimal": self.converter.from_direct(direct_bits),
            "reverse_decimal": self.converter.from_reverse(reverse_bits),
            "additional_decimal": self.converter.from_additional(additional_bits),
        }

    def add_additional(self, a: int, b: int) -> dict[str, int | list[int]]:
        a_bits = self.converter.to_additional(a)
        b_bits = self.converter.to_additional(b)
        result_bits = self.converter.add_bits(a_bits, b_bits)
        return {
            "a_bits": a_bits,
            "b_bits": b_bits,
            "result_bits": result_bits,
            "result_decimal": self.converter.from_additional(result_bits),
        }

    def subtract_additional(self, a: int, b: int) -> dict[str, int | list[int]]:
        a_bits = self.converter.to_additional(a)
        b_bits = self.converter.to_additional(b)
        neg_b_bits = self.converter.negate_twos(b_bits)
        result_bits = self.converter.add_bits(a_bits, neg_b_bits)
        return {
            "a_bits": a_bits,
            "b_bits": b_bits,
            "neg_b_bits": neg_b_bits,
            "result_bits": result_bits,
            "result_decimal": self.converter.from_additional(result_bits),
        }

    @staticmethod
    def _shift_left(bits: list[int], shift: int) -> list[int]:
        if shift <= 0:
            return bits[:]
        if shift >= len(bits):
            return [0] * len(bits)
        return bits[shift:] + ([0] * shift)

    def multiply_direct(self, a: int, b: int) -> dict[str, int | list[int]]:
        a_bits = self.converter.to_direct(a)
        b_bits = self.converter.to_direct(b)
        mag_a = a_bits[1:]
        mag_b = b_bits[1:]
        result_mag = [0] * len(mag_a)

        index = len(mag_b) - 1
        while index >= 0:
            if mag_b[index] == 1:
                shift = (len(mag_b) - 1) - index
                partial = self._shift_left(mag_a, shift)
                result_mag = self.converter.add_bits(result_mag, partial)
            index -= 1

        sign_bit = a_bits[0] ^ b_bits[0]
        if all(bit == 0 for bit in result_mag):
            sign_bit = 0
        result_bits = [sign_bit] + result_mag
        return {
            "a_bits": a_bits,
            "b_bits": b_bits,
            "result_bits": result_bits,
            "result_decimal": self.converter.from_direct(result_bits),
        }

    def divide_direct(self, a: int, b: int) -> dict[str, int | str | list[int]]:
        if b == 0:
            raise ZeroDivisionError("Division by zero")

        sign_negative = (a < 0) ^ (b < 0)
        abs_a = abs(a)
        abs_b = abs(b)

        integer_part = abs_a // abs_b
        remainder = abs_a % abs_b

        decimal_digits: list[int] = []
        for _ in range(self.division_precision):
            remainder *= 10
            digit = remainder // abs_b
            remainder %= abs_b
            decimal_digits.append(digit)

        fraction_bits: list[int] = []
        remainder_bin = abs_a % abs_b
        for _ in range(self.converter.register_size):
            remainder_bin *= 2
            if remainder_bin >= abs_b:
                fraction_bits.append(1)
                remainder_bin -= abs_b
            else:
                fraction_bits.append(0)

        signed_int = -integer_part if sign_negative else integer_part
        integer_bits = self.converter.to_direct(signed_int)
        if integer_part == 0 and sign_negative:
            integer_bits[0] = 1

        decimal_result = f"{'-' if sign_negative else ''}{integer_part}.{''.join(str(d) for d in decimal_digits)}"
        return {
            "integer_bits": integer_bits,
            "fraction_bits": fraction_bits,
            "decimal_result": decimal_result,
            "integer_decimal_part": signed_int,
        }

    def float_operation(self, a: float, b: float, operation: str) -> dict[str, float | list[int]]:
        if operation not in {"+", "-", "*", "/"}:
            raise ValueError("Operation must be one of: + - * /")

        a_bits = self.converter.to_float32(a)
        b_bits = self.converter.to_float32(b)
        a_value = self.converter.from_float32(a_bits)
        b_value = self.converter.from_float32(b_bits)

        if operation == "+":
            result_value = a_value + b_value
        elif operation == "-":
            result_value = a_value - b_value
        elif operation == "*":
            result_value = a_value * b_value
        else:
            if b_value == 0.0:
                sign = a_bits[0] ^ b_bits[0]
                inf_bits = [sign] + ([1] * 8) + ([0] * 23)
                return {
                    "a_bits": a_bits,
                    "b_bits": b_bits,
                    "result_bits": inf_bits,
                    "a_decimal": a_value,
                    "b_decimal": b_value,
                    "result_decimal": self.converter.from_float32(inf_bits),
                }
            result_value = a_value / b_value

        result_bits = self.converter.to_float32(result_value)
        return {
            "a_bits": a_bits,
            "b_bits": b_bits,
            "result_bits": result_bits,
            "a_decimal": a_value,
            "b_decimal": b_value,
            "result_decimal": self.converter.from_float32(result_bits),
        }

    @staticmethod
    def _number_to_digits(number: int) -> list[int]:
        if number == 0:
            return [0]
        digits_reversed: list[int] = []
        value = number
        while value > 0:
            digits_reversed.append(value % 10)
            value //= 10
        return digits_reversed[::-1]

    def _gray_digit(self, digit: int) -> list[int]:
        bcd = self.converter.unsigned_to_binary(digit, 4)
        return [bcd[0], bcd[0] ^ bcd[1], bcd[1] ^ bcd[2], bcd[2] ^ bcd[3]]

    def gray_bcd_encode(self, number: int) -> list[int]:
        if number < 0:
            raise ValueError("Gray BCD supports only non-negative numbers")
        digits = self._number_to_digits(number)
        if len(digits) > self.converter.register_size // 4:
            raise OverflowError("Number does not fit in 32 bits of Gray BCD")

        bits = [0] * self.converter.register_size
        index = self.converter.register_size - (len(digits) * 4)
        for digit in digits:
            encoded = self._gray_digit(digit)
            for bit in encoded:
                bits[index] = bit
                index += 1
        return bits

    def gray_bcd_add(self, a: int, b: int) -> dict[str, int | list[int]]:
        if a < 0 or b < 0:
            raise ValueError("Gray BCD supports only non-negative numbers")

        digits_a = self._number_to_digits(a)
        digits_b = self._number_to_digits(b)
        i = len(digits_a) - 1
        j = len(digits_b) - 1
        carry = 0
        result_rev: list[int] = []

        while i >= 0 or j >= 0 or carry:
            da = digits_a[i] if i >= 0 else 0
            db = digits_b[j] if j >= 0 else 0
            curr = da + db + carry
            carry = 1 if curr >= 10 else 0
            if curr >= 10:
                curr -= 10
            result_rev.append(curr)
            i -= 1
            j -= 1

        result_digits = result_rev[::-1]
        result_decimal = 0
        for digit in result_digits:
            result_decimal = (result_decimal * 10) + digit

        return {
            "a_bits": self.gray_bcd_encode(a),
            "b_bits": self.gray_bcd_encode(b),
            "result_bits": self.gray_bcd_encode(result_decimal),
            "result_decimal": result_decimal,
        }
