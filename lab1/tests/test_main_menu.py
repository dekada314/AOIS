from lab1 import main


def test_int_input_retries(monkeypatch, capsys):
    responses = iter(["abc", "42"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))
    value = main._int_input("Введите число: ")
    captured = capsys.readouterr()
    assert value == 42
    assert "Введите целое число." in captured.out



def test_run_menu_all_options_happy_path(monkeypatch, capsys):
    responses = iter(
        [
            "1",
            "-5",
            "2",
            "1",
            "2",
            "3",
            "5",
            "3",
            "4",
            "2",
            "3",
            "5",
            "7",
            "2",
            "6",
            "1.5",
            "0.5",
            "+",
            "7",
            "12",
            "3",
            "0",
        ]
    )
    monkeypatch.setattr("builtins.input", lambda _: next(responses))
    main.run_menu()
    captured = capsys.readouterr()
    out = captured.out

    assert "Прямой (2):" in out
    assert "SUM (10): 3" in out
    assert "RES (10): 2" in out
    assert "MUL (10): 6" in out
    assert "RES (10): 3.50000" in out
    assert "SUM GrayBCD (2):" in out
    assert "Выход." in out
