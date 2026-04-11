from lab2 import main
from lab2.src.logic_engine import LogicEngine


def test_minimization_constant_paths_and_helpers():
    zero = LogicEngine("0")
    one = LogicEngine("1")

    dnf_zero = zero._minimize_dnf([], include_table=False)
    assert dnf_zero["result_expression"] == "0"

    dnf_one = one._minimize_dnf([0], include_table=True)
    assert dnf_one["result_expression"] == "1"
    assert dnf_one["table"]["columns"] == [0]

    knf_one = one._minimize_knf([], include_table=False)
    assert knf_one["result_expression"] == "1"

    knf_zero = zero._minimize_knf([0], include_table=True)
    assert knf_zero["result_expression"] == "0"
    assert knf_zero["table"]["columns"] == [0]

    assert zero._term_to_dnf(("-",)) == "1"
    assert zero._term_to_knf_clause_from_zero_cube(("-",)) == "0"
    assert zero._literal_count(("-", "1", "0")) == 2
    assert zero._select_cover([], []) == []


def test_select_cover_combination_search_path():
    engine = LogicEngine("a|b")
    terms = [("0", "-"), ("-", "0"), ("-", "1"), ("1", "-")]
    selected = engine._select_cover(terms, [0, 1, 2, 3])
    assert len(selected) == 2


def test_minimization_bits_and_karnaugh_5_vars():
    engine = LogicEngine("a&b&c&d&e")
    assert engine._bits_of(5, 3) == [1, 0, 1]
    assert engine._bits_of(0, 0) == []

    kmap = engine._karnaugh_table()
    assert kmap["type"] == "double"
    assert kmap["layer_var"] == "a"
    assert 0 in kmap["maps"] and 1 in kmap["maps"]
