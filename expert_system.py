import json

import questionary

from working_memory import WorkingMemory


class ExpertSystem:
    def __init__(self, kb: str = "./kb.json") -> None:
        self._kb_file: str = kb
        self._kb: list[dict] = []
        self._working_mem: WorkingMemory = WorkingMemory()
        self._load_kb()

    def _load_kb(self) -> None:
        with open(self._kb_file, "r", encoding="utf-8") as f:
            self._kb = json.load(f)
    
    def _save_kb(self) -> None:
        with open(self._kb_file, "w", encoding="utf-8") as f:
            json.dump(self._kb, f, ensure_ascii=False, indent=4)

    def show_kb(self) -> None:
        if not self._kb:
            print("База знаний пуста! Добавьте правила")
            return
        for i in range(len(self._kb)):
            self.show_rule(i + 1)   

    def show_rule(self, id_if: int) -> None:
        if not (0 < id_if <= len(self._kb)):   
            print(f"Неверный номер = {id_if}: ничего не найдено")
            return
        knowledge: dict = self._kb[id_if - 1]
        print(f"Правило #{id_if}:")
        print("\tЕСЛИ:")
        for obj, val in knowledge["if"].items():
            print(f"\t-> {obj}: {val}")
        print("\tТО:")
        print(f"\t-> {knowledge['then']['object']}: {knowledge['then']['value']}\n")

    def add_rule(self, if_dict: dict[str, str], then_obj: str, then_val: str) -> bool:
        new_knowledge: dict = {
            "if": if_dict,
            "then": {
                "object": then_obj,
                "value": then_val
            }
        }
        self._kb.append(new_knowledge)
        self._save_kb()
        print("Правило успешно добавлено")
        return True
    
    def edit_rule(self, id_if: int, new_if: dict[str, str], new_then_obj: str, new_then_val: str) -> bool:
        if not (0 < id_if <= len(self._kb)):   
            print(f"Неверный номер = {id_if}: ничего не найдено")
            return False
        self._kb[id_if - 1] = {
            "if": new_if,
            "then": {
                "object": new_then_obj, 
                "value": new_then_val
            }
        }
        self._save_kb()
        print("Правило успешно изменено")
        return True
        
    def delete_rule(self, id_if: int) -> bool:
        if not (0 < id_if <= len(self._kb)):   
            print(f"Неверный номер = {id_if}: ничего не найдено")
            return False
        self._kb.pop(id_if - 1)
        self._save_kb()
        print("Правило успешно удалено")
        return True

    def show_working_mem(self) -> None:
        print(f"[РАБОЧАЯ ПАМЯТЬ]: {self._working_mem}")

    def init_start_situation(self) -> None:
        self._working_mem.clear()
        self._working_mem.add_fact("показы", "много")
        self._working_mem.add_fact("клики", "мало")

    def run(self) -> None:
        used_rules: set[int] = set()
        derived_objects: set[str] = {rule["then"]["object"] for rule in self._kb}
        
        while True:
            self.show_working_mem()
            triggered: bool = False
            for i, knowledge in enumerate(self._kb):
                if i in used_rules:
                    continue
                
                if self._working_mem.is_match(knowledge["if"]):
                    then_obj: str = knowledge["then"]["object"]
                    then_val: str = knowledge["then"]["value"]
                    try:
                        self._working_mem.add_fact(then_obj, then_val)
                        print(f"-> Правило #{i + 1} совпало! Добавлено в память: {then_obj}: {then_val}")
                    except ValueError as e:
                        print(f"[ВНИМАНИЕ] {e}.")
                    used_rules.add(i)
                    triggered = True
                    break
                    
            if triggered:
                continue
                
            candidates_map: dict[str, list[str]] = {}
            for i, knowledge in enumerate(self._kb):
                if i in used_rules:
                    continue
                
                rule_is_dead: bool = False
                match_count: int = 0
                
                for obj, val in knowledge["if"].items():
                    fact = self._working_mem.get_fact(obj)
                    if fact is None:
                        continue
                    if fact != val:
                        rule_is_dead = True
                        break
                    else:
                        match_count += 1
                            
                if rule_is_dead or match_count == 0:
                    continue
                
                for obj, val in knowledge["if"].items():
                    if (self._working_mem.get_fact(obj) is not None) or (obj in derived_objects):
                        continue
                        
                    if obj not in candidates_map:
                        candidates_map[obj] = []
                    if val not in candidates_map[obj]:
                        candidates_map[obj].append(val)
            
            if not candidates_map:
                print("\n>>> Нет релевантных данных для продолжения (тупик) <<<")
                break

            choices = [questionary.Choice(obj, obj) for obj in candidates_map]
            choices.append(questionary.Choice(">>> Закончить размышление", "0"))

            choice_str: str | None = questionary.select(
                "Доступные неизвестные факты для проверки:",
                choices=choices
            ).ask()

            if not choice_str or choice_str == "0":
                break
                
            expected_vals = candidates_map[choice_str]
            
            if len(expected_vals) == 1:
                expected_val = expected_vals[0]
                is_true = questionary.confirm(f"{choice_str} {expected_val}?").ask()
                self._working_mem.add_fact(choice_str, expected_val if is_true else f"не_{expected_val}")
            else:
                val_choices = [questionary.Choice(v, v) for v in expected_vals]
                val_choices.append(questionary.Choice(">>> Ни одно из списка", "none"))
                val_choice = questionary.select(
                    f"Выберите значение для '{choice_str}':",
                    choices=val_choices
                ).ask()
                self._working_mem.add_fact(choice_str, "неизвестно" if val_choice == "none" else val_choice)      
            print("Факт обработан!")

        print(">>> ИТОГОВЫЙ РЕЗУЛЬТАТ РАССУЖДЕНИЙ <<<")
        self.show_working_mem()
        
        found_conclusions: bool = False
        for obj in derived_objects:
            val = self._working_mem.get_fact(obj)
            if val is not None:
                print(f"> {obj}: {val} <")
                found_conclusions = True
                
        if not found_conclusions:
            print("...Заключений не получено...")