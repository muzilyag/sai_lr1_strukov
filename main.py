from expert_system import ExpertSystem
from utils import *


def main() -> None:
    es = ExpertSystem()
    while True:
        print_menu()
        choice: str = input("Выберите действие: ")
        match choice:
            case "1":
                es.show_kb()
            case "2":
                if_dict, then_obj, then_val = input_rule()
                es.add_rule(if_dict, then_obj, then_val)
            case "3":
                id_if: int = int(input("Введите id правила: "))
                es.show_rule(id_if)
                if_dict, then_obj, then_val = input_rule()
                es.edit_rule(id_if, if_dict, then_obj, then_val)
            case "4":
                id_if: int = int(input("Введите id правила: "))
                es.delete_rule(id_if)
            case "5":
                es.show_working_mem()
            case "6":
                es.init_start_situation()
                es.run()
            case _:
                print("Пока!")
                break


if __name__ == "__main__":
    main()