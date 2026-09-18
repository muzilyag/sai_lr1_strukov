class WorkingMemory:
    def __init__(self):
        self._facts: dict[str, str] = {}

    def add_fact(self, obj: str, val: str) -> None:
        if obj in self._facts and self._facts[obj] != val:
            raise ValueError(f"Конфликт фактов: '{obj}' уже имеет значение '{self._facts[obj]}', "
                             f"попытка записи '{val}'")
        self._facts[obj] = val

    def get_fact(self, obj: str) -> str | None:
        return self._facts.get(obj)

    def is_match(self, conditions: dict[str, str]) -> bool:
        for obj, val in conditions.items():
            if self.get_fact(obj) != val:
                return False
        return True

    def clear(self) -> None:
        self._facts.clear()

    def __str__(self) -> str:
        if not self._facts:
            return "{Empty}"
        result: str = "\n"
        for obj, val in self._facts.items():
            result += f"\t> {obj}: {val}\n"
        return result 
    