def create_table(metadata, table_name, columns):
    """создает новую таблицу в базе данных"""
    if table_name in metadata:
        return f"Ошибка: Таблица '{table_name}' уже существует."

    valid_types = {"int", "str", "bool"}

    for col in columns:
        if ":" not in col:
            return f"Некорректное значение: '{col}'. Попробуйте снова."
        col_type = col.split(":")[1]
        if col_type not in valid_types:
            return f"Некорректное значение: '{col_type}'. Попробуйте снова."

    if not any(c.startswith("ID:") for c in columns):
        columns = ["ID:int"] + columns

    metadata[table_name] = columns
    return f"Таблица '{table_name}' успешно создана со столбцами: {', '.join(columns)}"


def drop_table(metadata, table_name):
    """удаляет таблицу из базы данных"""
    if table_name not in metadata:
        return f"Ошибка: Таблица '{table_name}' не существует."

    del metadata[table_name]
    return f"Таблица '{table_name}' успешно удалена."


def list_tables(metadata):
    """озвращает список таблиц"""
    if not metadata:
        return "В базе данных пока нет таблиц."

    return "\n".join([f"- {table}" for table in metadata.keys()])