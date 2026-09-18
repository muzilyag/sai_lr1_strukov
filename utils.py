import questionary


def input_rule() -> tuple[dict[str, str], str, str] | None:
    if_dict: dict[str, str] = {}
    print("Ввод правила (оставьте объект пустым для перехода к THEN-части, введите '0' для отмены)")
    
    while True:
        obj: str | None = questionary.text("Введите объект условия:").ask()
        if obj is None or obj.strip() == "0":
            print("Ввод правила отменён!")
            return None
            
        obj = obj.strip()
        if not obj:
            break
            
        val: str | None = questionary.text(f"Введите значение условия {obj}:").ask()
        if val is None:
            return None
        if_dict[obj] = val.strip()

    if not if_dict:
        print("Правило должно иметь как минимум одно условие! Отмена.")
        return None

    then_obj: str | None = questionary.text("Введите THEN объект:").ask()
    if not then_obj:
        return None
        
    then_val: str | None = questionary.text("Введите THEN значение:").ask()
    if not then_val:
        return None

    return if_dict, then_obj.strip(), then_val.strip()