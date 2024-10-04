from ArmHashMap import ArmHashMap
def main():
    # Создание экземпляра ArmHashMap
    hashmap = ArmHashMap(initial_capacity=4)

    # Тестирование метода put
    hashmap.put("key1", "value1")
    hashmap.put("key2", "value2")
    hashmap.put("key3", "value3")
    print("После добавления элементов:", len(hashmap))  # Ожидается: 3

    # Тестирование метода get
    print("Значение для 'key1':", hashmap.get("key1"))  # Ожидается: "value1"
    print("Значение для 'key2':", hashmap.get("key2"))  # Ожидается: "value2"
    print("Значение для 'key4':", hashmap.get("key4"))  # Ожидается: None

    # Тестирование метода remove
    print("Удаление 'key2':", hashmap.remove("key2"))  # Ожидается: True
    print("Удаление 'key4':", hashmap.remove("key4"))  # Ожидается: False
    print("После удаления элементов:", len(hashmap))  # Ожидается: 2

    # Тестирование метода __len__
    print("Размер хэш-таблицы:", len(hashmap))  # Ожидается: 2

if __name__ == "__main__":
    main()