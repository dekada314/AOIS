from lab1.src.calculations import LabCalculator
from lab1.src.conversions import IntConverter


def _int_input(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("Введите целое число.")


def _float_input(prompt: str) -> float:
    while True:
        raw = input(prompt).strip().replace(",", ".")
        try:
            return float(raw)
        except ValueError:
            print("Введите число с плавающей точкой.")


def _print_menu() -> None:
    print("\n=== MENU ===")
    print("1. Перевод 10->2: прямой/обратный/дополнительный")
    print("2. Сложение в дополнительном коде")
    print("3. Вычитание через отрицание и сложение")
    print("4. Умножение в прямом коде")
    print("5. Деление в прямом коде (точность 5 знаков)")
    print("6. IEEE-754 (32 бита): + - * /")
    print("7. Gray BCD: сложение")
    print("0. Выход")


def run_menu() -> None:
    conv = IntConverter()
    calc = LabCalculator(conv)

    while True:
        _print_menu()
        choice = input("Пункт: ").strip()

        if choice == "0":
            print("Выход.")
            return

        try:
            if choice == "1":
                number = _int_input("Число (10): ")
                result = calc.convert_number(number)
                print(f"Прямой (2): {conv.bits_to_string(result['direct_bits'])} | (10): {result['direct_decimal']}")
                print(f"Обратный (2): {conv.bits_to_string(result['reverse_bits'])} | (10): {result['reverse_decimal']}")
                print(
                    f"Дополнительный (2): {conv.bits_to_string(result['additional_bits'])} | (10): {result['additional_decimal']}"
                )

            elif choice == "2":
                a = _int_input("Введите число 1: ")
                b = _int_input("Введите число 2: ")
                result = calc.add_additional(a, b)
                print(f"A (2): {conv.bits_to_string(result['a_bits'])}")
                print(f"B (2): {conv.bits_to_string(result['b_bits'])}")
                print(f"SUM (2): {conv.bits_to_string(result['result_bits'])}")
                print(f"SUM (10): {result['result_decimal']}")

            elif choice == "3":
                a = _int_input("Введите число 1: ")
                b = _int_input("Введите число 2: ")
                result = calc.subtract_additional(a, b)
                print(f"A (2): {conv.bits_to_string(result['a_bits'])}")
                print(f"B (2): {conv.bits_to_string(result['b_bits'])}")
                print(f"-B (2): {conv.bits_to_string(result['neg_b_bits'])}")
                print(f"RES (2): {conv.bits_to_string(result['result_bits'])}")
                print(f"RES (10): {result['result_decimal']}")

            elif choice == "4":
                a = _int_input("Введите число 1: ")
                b = _int_input("Введите число 2: ")
                result = calc.multiply_direct(a, b)
                print(f"A (2): {conv.bits_to_string(result['a_bits'])}")
                print(f"B (2): {conv.bits_to_string(result['b_bits'])}")
                print(f"MUL (2): {conv.bits_to_string(result['result_bits'])}")
                print(f"MUL (10): {result['result_decimal']}")

            elif choice == "5":
                a = _int_input("Введите число 1: ")
                b = _int_input("Введите число 2: ")
                result = calc.divide_direct(a, b)
                print(f"Целая часть (2): {conv.bits_to_string(result['integer_bits'])}")
                print(f"Дробная часть (2): {conv.bits_to_string(result['fraction_bits'])}")
                print(f"RES (10): {result['decimal_result']}")

            elif choice == "6":
                a = _float_input("Введите число 1: ")
                b = _float_input("Введите число 2: ")
                op = input("Операция (+, -, *, /): ").strip()
                result = calc.float_operation(a, b, op)
                print(f"A (2): {conv.bits_to_string(result['a_bits'])}")
                print(f"B (2): {conv.bits_to_string(result['b_bits'])}")
                print(f"RES (2): {conv.bits_to_string(result['result_bits'])}")
                print(f"A (10): {result['a_decimal']}")
                print(f"B (10): {result['b_decimal']}")
                print(f"RES (10): {result['result_decimal']}")

            elif choice == "7":
                a = _int_input("Введите число 1 (>=0): ")
                b = _int_input("Введите число 2 (>=0): ")
                result = calc.gray_bcd_add(a, b)
                print(f"A GrayBCD (2): {conv.bits_to_string(result['a_bits'])}")
                print(f"B GrayBCD (2): {conv.bits_to_string(result['b_bits'])}")
                print(f"SUM GrayBCD (2): {conv.bits_to_string(result['result_bits'])}")
                print(f"SUM (10): {result['result_decimal']}")

            else:
                print("Пункт должен быть от 0 до 7.")

        except Exception as exc:
            print(f"Ошибка: {exc}")


if __name__ == "__main__":
    run_menu()
