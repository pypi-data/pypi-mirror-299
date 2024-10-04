from ArmTreeNode import ArmTreeMap
def main():
    # Создание экземпляра ArmTreeMap
    tree_map = ArmTreeMap()

    # Тестирование метода put
    tree_map.insert("key1", "value1")
    tree_map.insert("key2", "value2")
    tree_map.insert("key3", "value3")
    print("После добавления элементов:", tree_map.search("key1"), tree_map.search("key2"), tree_map.search("key3"))  # Ожидается: value1 value2 value3

    # Тестирование метода search
    print("Значение для 'key1':", tree_map.search("key1"))  # Ожидается: "value1"
    print("Значение для 'key2':", tree_map.search("key2"))  # Ожидается: "value2"
    print("Значение для 'key4':", tree_map.search("key4"))  # Ожидается: None

    # Тестирование метода delete
    tree_map.delete("key2")
    print("После удаления 'key2':", tree_map.search("key2"))  # Ожидается: None
    print("Значение для 'key1':", tree_map.search("key1"))  # Ожидается: "value1"
    print("Значение для 'key3':", tree_map.search("key3"))  # Ожидается: "value3"

if __name__ == "__main__":
    main()