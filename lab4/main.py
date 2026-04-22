from src.hash_row import HashRow
from src.hash_table import HashTable

TABLE_SIZE = 23

data = {
    "Армия": "Сухопутные войска",
    "Флот": "Военно-морские силы",
    "Авиация": "Истребительная авиация",
    "Оружие": "Стрелковое вооружение",
    "Танки": "Бронетанковая техника",
    "Артиллерия": "Самоходные гаубицы",
    "Ракеты": "Баллистические ракеты",
    "Боеприпасы": "Фугасные снаряды",
    "Броня": "Композитная броня",
    "Разведка": "Спутниковая разведка",
    "Связь": "Тактическая радиосвязь",
    "Медицина": "Полевой госпиталь",
    "Пехота": "Мотострелковые подразделения",
    "Тыл": "Материально-техническое обеспечение",
    "Камуфляж": "Маскировочная окраска"
}

def main():
    table = HashTable(TABLE_SIZE)
    for key, value in data.items():
        table.insert(key, value)

    while True:
        print("\nМеню\n\n"
              "1. Показать таблицу\n"
              "2. Добавить пару\n"
              "3. Найти по значению\n"
              "4. Удалить по значению\n"
              "0. Выход\n")
        
        try:
            choise = int(input("Выбор:"))
        except:
            raise ValueError("Неверный формат ввода")
        
        match choise:
            case 0:
                break
            case 1:
                print(f"{'№':<3} | {'V':<5} | {'h(v)':<5} | {'ID':<15} | C U T L D | P0 | P1")
                print('-' * 60)
                for index, row in enumerate(table.rows):
                    v = table._calc_hash(row.id) if row.id else 0
                    h = table._define_index(v) if row.id else 0
                    flags = f"{row.c} {row.u} {row.t} {row.l} {row.d}"
                    print(f"{index:<3} | {v:<5} | {h:<5} | {row.id[:14]:<15} | {flags} | {row.p0:<2} | {row.pi[:20]}")
                
                print(f"\nКоэффицент заполнения: {table.get_fill_factor():.2f}")
            case 2:
                key = input("Введите ключ:")
                value = input("Введите значение:")
                index, key, value = table.insert(key, value)
                if value:
                    print(f"Пара {key}: {value} добавлена")
                else:
                    print("Пара уже есть в таблице")
            case 3:
                key = input("Введите ключ:")
                index, key, value = table.search(key)
                if value:
                    print(f"Найденное значение: {value}")
                else:
                    print("Такого значения не найдено")
            case 4:
                key = input("Введите ключ:")
                index, key, value = table.delete(key)
                if value:
                    print(f"Удалена пара значений {key}: {value}")
            case _:
                print("Выбрана невозможная операция")
                break

if __name__ == "__main__":
    main()