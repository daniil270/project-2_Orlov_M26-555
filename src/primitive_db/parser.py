def parse_condition(condition_str, clause_type):
    """Парсит строку для where или set"""
    if not condition_str:
        return None

    if clause_type.lower() not in ("where", "set"):
        raise ValueError(
            f"Неизвестный тип условия: '{clause_type}'. Ожидалось where или set"
        )

    parts = condition_str.split("=")
    if len(parts) != 2:
        return None

    key = parts[0].strip()
    value_str = parts[1].strip()

    return {key: convert_value(value_str)}


def convert_value(value_str):
    """Преобразование в числовой или булевый тип, при возможности"""
    if (value_str.startswith('"') and value_str.endswith('"')) or \
            (value_str.startswith("'") and value_str.endswith("'")):
        return value_str[1:-1]

    try:
        return int(value_str)
    except ValueError:
        pass

    if value_str.lower() == "true":
        return True
    if value_str.lower() == "false":
        return False

    return value_str