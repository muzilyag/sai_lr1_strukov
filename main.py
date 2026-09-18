import questionary

from expert_system import ExpertSystem
from utils import input_rule


def main() -> None:
    es = ExpertSystem()
    while True:
        choice: str | None = questionary.select(
            "МЕНЮ",
            choices=[
                questionary.Choice("1. Показать существующие правила", "1"),
                questionary.Choice("2. Добавить правило", "2"),
                questionary.Choice("3. Редактировать правило по номеру", "3"),
                questionary.Choice("4. Удалить правило по номеру", "4"),
                questionary.Choice("5. Показать рабочую память", "5"),
                questionary.Choice("6. Запуск машины", "6"),
                questionary.Choice("0. Выход", "0"),
            ]
        ).ask()

        if choice is None or choice == "0":
            break

        match choice:
            case "1":
                es.show_kb()
            case "2":
                temp_data: tuple[dict[str, str], str, str] | None = input_rule()
                if not temp_data:
                    continue
                if_dict, then_obj, then_val = temp_data
                es.add_rule(if_dict, then_obj, then_val)
            case "3":
                id_str: str | None = questionary.text("Введите номер правила (для отмены введите 0):").ask()
                if not id_str or not id_str.isdigit():
                    print("Отмена. Ожидалось число.")
                    continue
                if id_str == "0":
                    print("Отмена.")
                    continue
                id_if: int = int(id_str)
                es.show_rule(id_if)
                temp_data: tuple[dict[str, str], str, str] | None = input_rule()
                if not temp_data:
                    continue
                if_dict, then_obj, then_val = temp_data
                es.edit_rule(id_if, if_dict, then_obj, then_val)
            case "4":
                id_str: str | None = questionary.text("Введите номер правила:").ask()
                if not id_str or not id_str.isdigit():
                    print("Отмена. Ожидалось число.")
                    continue
                es.delete_rule(int(id_str))
            case "5":
                es.show_working_mem()
            case "6":
                es.init_start_situation()
                es.run()


if __name__ == "__main__":
    main()