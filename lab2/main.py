from __future__ import annotations

from lab2.src.logic_engine import LogicEngine


def _print_menu() -> None:
    print("\n=== LAB2 MENU ===")
    print("1. Ввести логическую функцию")
    print("2. Построить таблицу истинности")
    print("3. Построить СДНФ и СКНФ")
    print("4. Вывести числовую форму СДНФ и СКНФ")
    print("5. Вывести индексную форму")
    print("6. Определить принадлежность к классам Поста")
    print("7. Построить полином Жегалкина")
    print("8. Найти фиктивные переменные")
    print("9. Булева дифференциация")
    print("10. Минимизация расчетным методом")
    print("11. Минимизация расчетно-табличным методом")
    print("12. Минимизация табличным методом (Карта Карно)")
    print("0. Выход")


def _require_engine(engine: LogicEngine | None) -> LogicEngine | None:
    if engine is None:
        print("Сначала выберите пункт 1 и введите функцию.")
        return None
    return engine


def _print_truth_table(engine: LogicEngine) -> None:
    rows = engine.truth_table()
    if not engine.variables:
        print(f"f = {rows[0]['f']}")
        return

    header = " | ".join(engine.variables + ["f"])
    print(header)
    print("-" * len(header))
    for row in rows:
        line = " | ".join(str(row[name]) for name in engine.variables + ["f"])
        print(line)


def _print_prime_table(table: dict[str, object]) -> None:
    columns = table["columns"]
    rows = table["rows"]
    if not columns or not rows:
        print("Таблица покрытий не требуется.")
        return

    header = "Импликанта | " + " ".join(str(c) for c in columns)
    print(header)
    print("-" * len(header))
    for row in rows:
        marks = " ".join("1" if mark else "0" for mark in row["marks"])
        print(f"{row['pattern']} ({row['term']}) | {marks}")


def _print_karnaugh(kmap: dict[str, object]) -> None:
    if kmap["type"] == "single":
        print(f"Строки: {', '.join(kmap['row_vars']) if kmap['row_vars'] else '-'}")
        print(f"Столбцы: {', '.join(kmap['col_vars']) if kmap['col_vars'] else '-'}")
        print("      " + " ".join(kmap["col_labels"]))
        for i, row in enumerate(kmap["rows"]):
            print(f"{kmap['row_labels'][i]:>4}  " + " ".join(str(v) for v in row))
        return

    print(f"Две карты по переменной {kmap['layer_var']}")
    print(f"Строки: {', '.join(kmap['row_vars'])}")
    print(f"Столбцы: {', '.join(kmap['col_vars'])}")
    for layer in [0, 1]:
        print(f"\n{ kmap['layer_var'] } = {layer}")
        print("      " + " ".join(kmap["col_labels"]))
        for i, row in enumerate(kmap["maps"][layer]):
            print(f"{kmap['row_labels'][i]:>4}  " + " ".join(str(v) for v in row))


def run_menu() -> None:
    engine: LogicEngine | None = None

    while True:
        _print_menu()
        choice = input("Пункт: ").strip()

        if choice == "0":
            print("Выход.")
            return

        try:
            if choice == "1":
                expression = input("Введите функцию: ").strip()
                engine = LogicEngine(expression)
                vars_line = ", ".join(engine.variables) if engine.variables else "нет"
                print(f"Функция сохранена. Переменные: {vars_line}")

            elif choice == "2":
                curr = _require_engine(engine)
                if curr is None:
                    continue
                _print_truth_table(curr)

            elif choice == "3":
                curr = _require_engine(engine)
                if curr is None:
                    continue
                forms = curr.canonical_forms()
                print(f"СДНФ: {forms['sdnf']}")
                print(f"СКНФ: {forms['sknf']}")

            elif choice == "4":
                curr = _require_engine(engine)
                if curr is None:
                    continue
                forms = curr.numeric_forms()
                print(f"СДНФ числа: {forms['sdnf_numbers']}")
                print(f"СКНФ числа: {forms['sknf_numbers']}")
                print(f"СДНФ: {forms['sdnf_numeric']}")
                print(f"СКНФ: {forms['sknf_numeric']}")

            elif choice == "5":
                curr = _require_engine(engine)
                if curr is None:
                    continue
                index = curr.index_form()
                print(f"Вектор: {index['vector']}")
                print(f"Индекс: {index['index']}")

            elif choice == "6":
                curr = _require_engine(engine)
                if curr is None:
                    continue
                classes = curr.post_classes()
                for name in ["T0", "T1", "S", "M", "L"]:
                    print(f"{name}: {classes[name]}")

            elif choice == "7":
                curr = _require_engine(engine)
                if curr is None:
                    continue
                poly = curr.zhegalkin_polynomial()
                print(f"Полином Жегалкина: {poly['polynomial']}")

            elif choice == "8":
                curr = _require_engine(engine)
                if curr is None:
                    continue
                fake = curr.fictive_variables()
                print(f"Фиктивные переменные: {fake if fake else 'нет'}")

            elif choice == "9":
                curr = _require_engine(engine)
                if curr is None:
                    continue
                raw = input("Введите переменные через пробел (1-4): ").strip().replace(",", " ")
                derivative_vars = [x.lower() for x in raw.split() if x]
                derivative = curr.boolean_derivative(derivative_vars)
                print(f"Производная по {derivative['variables']}")
                print(f"Вектор: {''.join(str(v) for v in derivative['truth_vector'])}")
                print(f"СДНФ: {derivative['sdnf']}")
                print(f"СКНФ: {derivative['sknf']}")

            elif choice == "10":
                curr = _require_engine(engine)
                if curr is None:
                    continue
                result = curr.minimize_calculation()
                print("ДНФ:")
                for idx, stage in enumerate(result["dnf"]["stages"], start=1):
                    print(f"Стадия {idx}: {stage}")
                print(f"Результат: {result['dnf']['result_expression']}")
                print("КНФ:")
                for idx, stage in enumerate(result["knf"]["stages"], start=1):
                    print(f"Стадия {idx}: {stage}")
                print(f"Результат: {result['knf']['result_expression']}")

            elif choice == "11":
                curr = _require_engine(engine)
                if curr is None:
                    continue
                result = curr.minimize_calculation_table()
                print("ДНФ:")
                for idx, stage in enumerate(result["dnf"]["stages"], start=1):
                    print(f"Стадия {idx}: {stage}")
                _print_prime_table(result["dnf"]["table"])
                print(f"Результат: {result['dnf']['result_expression']}")
                print("КНФ:")
                for idx, stage in enumerate(result["knf"]["stages"], start=1):
                    print(f"Стадия {idx}: {stage}")
                _print_prime_table(result["knf"]["table"])
                print(f"Результат: {result['knf']['result_expression']}")

            elif choice == "12":
                curr = _require_engine(engine)
                if curr is None:
                    continue
                result = curr.minimize_karnaugh()
                _print_karnaugh(result["map"])
                print(f"Минимальная ДНФ: {result['dnf']['result_expression']}")
                print(f"Минимальная КНФ: {result['knf']['result_expression']}")

            else:
                print("Пункт должен быть от 0 до 12.")

        except Exception as exc:
            print(f"Ошибка: {exc}")


if __name__ == "__main__":
    run_menu()
