import json


class ExpertSystem:
    def __init__(self, kb="./kb.json"):
        self._kb_file: str = kb
        self._kb: list = []
        self._working_mem: dict = {}
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

        for i, knowledge in enumerate(self._kb):
            if_string: str = [f"{obj}={val}" for obj, val in knowledge["if"].items()]
            if_part: str = " И ".join(if_string)
            then_part: str = f"{knowledge['then']['object']}={knowledge['then']['value']}"
            print(f"{i + 1}. ЕСЛИ {if_part} ТО {then_part}")


    def show_rule(self, id_if: int) -> None:
        if not (0 < id_if <= len(self._kb)):   
            print(f"Неверный id = {id_if}: ничего не найдено")
            return
        knowledge = self._kb[id_if - 1]
        if_string: str = [f"{obj}={val}" for obj, val in knowledge["if"].items()]
        if_part: str = " И ".join(if_string)
        then_part: str = f"{knowledge['then']['object']}={knowledge['then']['value']}"
        print(f"{id_if}. ЕСЛИ {if_part} ТО {then_part}")


    def add_rule(self, if_dict: dict, then_obj: str, then_val: str) -> bool:
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
    

    def edit_rule(self, id_if: int, new_if: dict, new_then_obj: str, new_then_val) -> bool:
        if not (0 < id_if <= len(self._kb)):   
            print(f"Неверный id = {id_if}: ничего не найдено")
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
            print(f"Неверный id = {id_if}: ничего не найдено")
            return False
        self._kb.pop(id_if - 1)
        self._save_kb()
        print("Правило успешно удалено")
        return True


    def show_working_mem(self) -> None:
        print(f"[РАБОЧАЯ ПАМЯТЬ]: {self._working_mem if self._working_mem else '{Empty}'}")


    def init_start_situation(self) -> None:
        self._working_mem = {
            "температура": "высокая",
            "кашель": "да"
        }


    def run(self) -> None:
        used_rules: set = set()
        res_obj: str = ""
        res_val: str = ""
        while True:
            self.show_working_mem()
            triggered: bool = False
            for i, knowledge in enumerate(self._kb):
                if i in used_rules:
                    continue
                rules_match: bool = True
                for obj, val in knowledge["if"].items():
                    if self._working_mem.get(obj) != val:
                        rules_match = False
                        break
                if rules_match:
                    then_obj: str = knowledge["then"]["object"]
                    then_val: str = knowledge["then"]["value"]
                    if self._working_mem.get(then_obj) != then_val:
                        self._working_mem[then_obj] = then_val
                        print(f"-> Правило #{i + 1} совпало! Добавить в память: {then_obj} = {then_val}")
                        res_obj = then_obj
                        res_val = then_val
                    used_rules.add(i)
                    triggered = True
                    break
            if triggered:
                continue
            if not triggered:
                new_obj: str = input(">>> Введите объект факта (или нажмите Enter для окончания " \
                "размышления): ").strip()
                if not new_obj:
                    print(">>> ИТОГ! <<<")
                    self.show_working_mem()
                    if res_obj and res_val:
                        print(f"-> Результат: {res_obj} = {res_val}")
                    else:
                        print("Нет подходящих правил")
                    return
                new_val: str = input("Введите значение факта: ").strip()
                self._working_mem[new_obj] = new_val
                print("Факт добавлен!")