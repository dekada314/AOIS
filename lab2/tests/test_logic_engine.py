from lab2.src.logic_engine import LogicEngine


def test_truth_table_and_forms_for_or():
    engine = LogicEngine("a|b")

    assert engine.variables == ["a", "b"]
    assert engine.truth_vector == [0, 1, 1, 1]

    forms = engine.canonical_forms()
    assert forms["sdnf"] == "(!a&b)|(a&!b)|(a&b)"
    assert forms["sknf"] == "(a|b)"

    numeric = engine.numeric_forms()
    assert numeric["sdnf_numbers"] == [1, 2, 3]
    assert numeric["sknf_numbers"] == [0]
    assert numeric["sdnf_numeric"] == "Σ(1,2,3)"
    assert numeric["sknf_numeric"] == "Π(0)"

    index = engine.index_form()
    assert index["vector"] == "0111"
    assert index["index"] == 7


def test_post_and_zhegalkin_for_or():
    engine = LogicEngine("a|b")

    classes = engine.post_classes()
    assert classes == {"T0": True, "T1": True, "S": False, "M": True, "L": False}

    poly = engine.zhegalkin_polynomial()
    assert poly["polynomial"] == "a ^ b ^ a&b"


def test_fictive_variable_detected():
    engine = LogicEngine("a|b|(c&!c)")
    assert engine.fictive_variables() == ["c"]

def test_karnaugh_output():
    engine = LogicEngine("a|b")
    result = engine.minimize_karnaugh()

    kmap = result["map"]
    assert kmap["type"] == "single"
    assert kmap["rows"] == [[0, 1], [1, 1]]

    assert result["dnf"]["result_expression"] in {"a|b", "b|a"}
    assert result["knf"]["result_expression"] == "(a|b)"


def test_boolean_derivative_returns_minimal_sdnf_without_derivative_variable():
    engine = LogicEngine("a&b")

    derivative = engine.boolean_derivative(["a"])

    assert derivative["truth_vector"] == [0, 1, 0, 1]
    assert derivative["result_variables"] == ["b"]
    assert derivative["result_truth_vector"] == [0, 1]
    assert derivative["sdnf"] == "b"
