from lab2 import main


def test_menu_flow(monkeypatch, capsys):
    answers = iter(
        [
            "1",
            "a|b",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "a",
            "10",
            "11",
            "12",
            "0",
        ]
    )

    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    main.run_menu()
    out = capsys.readouterr().out

    assert "Функция сохранена." in out
    assert "СДНФ:" in out
    assert "СКНФ:" in out
    assert "Индекс:" in out
    assert "T0:" in out
    assert "Полином Жегалкина:" in out
    assert "Фиктивные переменные:" in out
    assert "Производная по" in out
    assert "Минимальная ДНФ:" in out
    assert "Выход." in out


def test_menu_requires_expression(monkeypatch, capsys):
    answers = iter(["2", "0"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    main.run_menu()
    out = capsys.readouterr().out
    assert "Сначала выберите пункт 1" in out


def test_menu_full_report_option(monkeypatch, capsys):
    answers = iter(["1", "a|b", "13", "a", "0"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    main.run_menu()
    out = capsys.readouterr().out

    assert "13. Вывести все пункты" in out
    assert "=== Полный отчет ===" in out
    assert "[2] Таблица истинности" in out
    assert "[3] СДНФ и СКНФ" in out
    assert "[4] Числовая форма СДНФ и СКНФ" in out
    assert "[5] Индексная форма" in out
    assert "[6] Классы Поста" in out
    assert "[7] Полином Жегалкина" in out
    assert "[8] Фиктивные переменные" in out
    assert "[9] Булева дифференциация" in out
    assert "[10] Минимизация расчетным методом" in out
    assert "[11] Минимизация расчетно-табличным методом" in out
    assert "[12] Минимизация табличным методом (Карта Карно)" in out
    assert "Минимальная ДНФ:" in out
    assert "Минимальная КНФ:" in out
