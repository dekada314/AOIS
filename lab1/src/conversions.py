import math


class IntConverter:
    def __init__(self, register_size: int = 32):
        if register_size != 32:
            raise ValueError("This lab implementation supports only 32 bits")
        self.register_size = register_size
        self.magnitude_size = register_size - 1
        self.float_exp_bits = 8
        self.float_mantissa_bits = 23
        self.float_bias = 127

    def validate_bits(self, bits: list[int], expected_size: int | None = None) -> None:
        size = self.register_size if expected_size is None else expected_size
        if len(bits) != size:
            raise ValueError(f"Expected {size} bits, got {len(bits)}")
        for bit in bits:
            if bit not in (0, 1):
                raise ValueError("Bit array may contain only 0 and 1")

    @staticmethod
    def bits_to_string(bits: list[int]) -> str:
        return "".join(str(bit) for bit in bits)

    def unsigned_to_binary(self, number: int, width: int | None = None) -> list[int]:
        if number < 0:
            raise ValueError("Number must be non-negative")
        size = self.register_size if width is None else width
        bits = [0] * size
        value = number
        index = size - 1
        while value > 0 and index >= 0:
            bits[index] = value % 2
            value //= 2
            index -= 1
        if value != 0:
            raise OverflowError(f"{number} does not fit in {size} bits")
        return bits

    def unsigned_from_binary(self, bits: list[int]) -> int:
        self.validate_bits(bits, len(bits))
        value = 0
        for bit in bits:
            value = (value * 2) + bit
        return value

    def invert(self, bits: list[int]) -> list[int]:
        return [0 if bit == 1 else 1 for bit in bits]

    def plus_one(self, bits: list[int]) -> list[int]:
        out = bits[:]
        index = len(out) - 1
        while index >= 0:
            if out[index] == 0:
                out[index] = 1
                return out
            out[index] = 0
            index -= 1
        return out

    def add_bits(self, bits_a: list[int], bits_b: list[int]) -> list[int]:
        if len(bits_a) != len(bits_b):
            raise ValueError("Bit arrays must have the same width")
        out = [0] * len(bits_a)
        carry = 0
        index = len(bits_a) - 1
        while index >= 0:
            curr = bits_a[index] + bits_b[index] + carry
            out[index] = curr % 2
            carry = curr // 2
            index -= 1
        return out

    def negate_twos(self, bits: list[int]) -> list[int]:
        return self.plus_one(self.invert(bits))

    def to_direct(self, number: int) -> list[int]:
        max_value = (1 << self.magnitude_size) - 1
        if abs(number) > max_value:
            raise OverflowError(f"{number} is out of range for direct code")
        sign_bit = 1 if number < 0 else 0
        return [sign_bit] + self.unsigned_to_binary(abs(number), self.magnitude_size)

    def from_direct(self, bits: list[int]) -> int:
        self.validate_bits(bits, self.register_size)
        value = self.unsigned_from_binary(bits[1:])
        return -value if bits[0] == 1 else value

    def to_reverse(self, number: int) -> list[int]:
        if number >= 0:
            return self.to_direct(number)
        return self.invert(self.to_direct(abs(number)))

    def from_reverse(self, bits: list[int]) -> int:
        self.validate_bits(bits, self.register_size)
        if bits[0] == 0:
            return self.from_direct(bits)
        return -self.from_direct(self.invert(bits))

    def to_additional(self, number: int) -> list[int]:
        min_value = -(1 << self.magnitude_size)
        max_value = (1 << self.magnitude_size) - 1
        if number < min_value or number > max_value:
            raise OverflowError(f"{number} is out of range for additional code")
        if number >= 0:
            return self.unsigned_to_binary(number, self.register_size)
        return self.negate_twos(self.unsigned_to_binary(abs(number), self.register_size))

    def from_additional(self, bits: list[int]) -> int:
        self.validate_bits(bits, self.register_size)
        if bits[0] == 0:
            return self.unsigned_from_binary(bits)
        return -self.unsigned_from_binary(self.negate_twos(bits))

    def _pow2(self, power: int) -> float:
        value = 1.0
        if power >= 0:
            for _ in range(power):
                value *= 2.0
            return value
        for _ in range(-power):
            value /= 2.0
        return value

    def to_float32(self, number: float) -> list[int]:
        if math.isnan(number):
            return [0] + ([1] * self.float_exp_bits) + ([0] * (self.float_mantissa_bits - 1)) + [1]

        sign_bit = 1 if math.copysign(1.0, number) < 0 else 0
        value = -number if sign_bit == 1 else number
        if value == 0.0:
            return [sign_bit] + ([0] * 31)
        if math.isinf(value):
            return [sign_bit] + ([1] * self.float_exp_bits) + ([0] * self.float_mantissa_bits)

        int_part = int(value)
        frac_part = value - int_part

        if int_part > 0:
            int_bits = self.unsigned_to_binary(int_part, max(1, int_part.bit_length()))
            exponent = len(int_bits) - 1
            mantissa_source = int_bits[1:]
        else:
            frac_bits: list[int] = []
            for _ in range(64):
                frac_part *= 2.0
                if frac_part >= 1.0:
                    frac_bits.append(1)
                    frac_part -= 1.0
                else:
                    frac_bits.append(0)
            shift = 0
            while shift < len(frac_bits) and frac_bits[shift] == 0:
                shift += 1
            if shift == len(frac_bits):
                return [sign_bit] + ([0] * 31)
            exponent = -(shift + 1)
            mantissa_source = frac_bits[shift + 1 :]

        while len(mantissa_source) < self.float_mantissa_bits:
            frac_part *= 2.0
            if frac_part >= 1.0:
                mantissa_source.append(1)
                frac_part -= 1.0
            else:
                mantissa_source.append(0)

        biased = exponent + self.float_bias
        if biased <= 0:
            return [sign_bit] + ([0] * 31)
        if biased >= 255:
            return [sign_bit] + ([1] * self.float_exp_bits) + ([0] * self.float_mantissa_bits)

        exponent_bits = self.unsigned_to_binary(biased, self.float_exp_bits)
        mantissa_bits = mantissa_source[: self.float_mantissa_bits]
        return [sign_bit] + exponent_bits + mantissa_bits

    def from_float32(self, bits: list[int]) -> float:
        self.validate_bits(bits, self.register_size)
        sign = -1.0 if bits[0] == 1 else 1.0
        exponent_bits = bits[1 : 1 + self.float_exp_bits]
        mantissa_bits = bits[1 + self.float_exp_bits :]

        exponent_raw = self.unsigned_from_binary(exponent_bits)
        if exponent_raw == 0 and not any(mantissa_bits):
            return -0.0 if sign < 0 else 0.0
        if exponent_raw == 255:
            if any(mantissa_bits):
                return float("nan")
            return sign * float("inf")
        if exponent_raw == 0:
            return 0.0

        exponent = exponent_raw - self.float_bias
        mantissa = 1.0
        weight = 0.5
        for bit in mantissa_bits:
            if bit == 1:
                mantissa += weight
            weight /= 2.0
        return sign * mantissa * self._pow2(exponent)
