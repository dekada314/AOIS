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
