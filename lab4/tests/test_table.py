import pytest

from lab4.src.hash_row import HashRow
from lab4.src.hash_table import HashTable


def test_table_create():
    size = 23
    table = HashTable(size)
    assert len(table.rows) == size
    
def test_hash_func():
    table = HashTable(23)
    word = "бВ"
    word_hash1 = 33 * 1 + 2
    word_hast2 = table._calc_hash(word)
    assert word_hash1 == word_hast2
    
def test_search_and_insert():
    table = HashTable(23)
    table.insert("Авиация", "Самолеты")
    table.insert("Танки", "пушки")
    table.insert("Танки", "пушки")
    table.insert("Танк", "пуш")

    assert table.search("Танк") is not None
    
def test_delete():
    table = HashTable(23)
    table.insert("Авиация", "Самолеты")
    table.insert("Танки", "пушки")
    table.insert("Танки", "пушки")
    table.insert("Танк", "пуш")
    
    _, _, value = table.delete("Танк")
    assert value == "пуш"
    assert table.search("Танк") is None
    assert table.delete("Танк") is None