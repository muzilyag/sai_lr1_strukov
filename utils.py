def print_menu() -> None:
    print("МЕНЮ")
    print("1. Показать существующуие правила")
    print("2. Добавить правило")
    print("3. Редактировать правило по id")
    print("4. Удалить правило по id")
    print("5. Показать рабочую память")
    print("6. Запуск машины")
    print("Любая другая клавиша: выход")


def input_rule() -> tuple[dict, str, str] | None:
    while True:
        if_dict: dict = {}
        print("Ввод правила (нажмите Enter при пустом объекте, " \
        "чтобы закончить, или введите '0' для отмены)")
        while True:
            obj = input("Введите объект условия: ")
            if obj == "0":
                print("Ввод правила отменён!")
                return None
            if not obj:
                break
            val: str = input(f"Введите значение условия {obj}: ").strip()
            if_dict[obj] = val

        if not if_dict:
            print("Правило должно иметь условие! Если хотите отменить ввод правил, введите '0'")
            continue

        then_obj: str = input("Введите THEN объект: ")
        then_val: str = input("Введите THEN значение: ")
        if then_obj and then_val:
            return if_dict, then_obj, then_val
        print("Неверная THEN часть! Отмена")
        return None