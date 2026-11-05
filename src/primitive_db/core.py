from prettytable import PrettyTable


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


def insert(metadata, table_name, values):
    """проверяет и подготавливает новую запись для таблицы"""
    if table_name not in metadata:
        return None, f"Ошибка: Таблица '{table_name}' не существует."

    schema = metadata[table_name]
    columns_without_id = [col for col in schema if not col.startswith("ID:")]

    if len(values) != len(columns_without_id):
        return None, f" Неверное количество. Ожидалось {len(columns_without_id)}."

    new_record = {}
    for i, col in enumerate(columns_without_id):
        col_name, col_type = col.split(":")
        val = values[i]

        if col_type == "int":
            try:
                val = int(val)
            except ValueError:
                return None, f"Ошибка: Значение '{val}' не является целым числом."
        elif col_type == "bool":
            if str(val).lower() in ("true", "1"):
                val = True
            elif str(val).lower() in ("false", "0"):
                val = False
            else:
                return None, f"Ошибка: Значение '{val}' не является boolean."
        elif col_type == "str":
            val = str(val)

        new_record[col_name] = val

    return new_record, None


def select(table_data, where_clause=None):
    """фильтрует данные и возвращает их в виде таблицы"""
    filtered_data = table_data

    if where_clause:
        col_name, col_value = list(where_clause.items())[0]
        filtered_data = [
            row for row in table_data
            if str(row.get(col_name)) == str(col_value)
        ]

    if not filtered_data:
        return filtered_data, "Нет данных, удовлетворяющих условию."

    table = PrettyTable()
    table.field_names = filtered_data[0].keys()

    for row in filtered_data:
        table.add_row(row.values())

    return filtered_data, table.get_string()


def update(table_data, set_clause, where_clause):
    """обновляет записи по условию"""
    updated_count = 0
    col_to_set, new_value = list(set_clause.items())[0]
    where_col, where_val = list(where_clause.items())[0]

    for row in table_data:
        if str(row.get(where_col)) == str(where_val):
            if isinstance(row.get(col_to_set), int) and str(new_value).isdigit():
                new_value = int(new_value)
            elif isinstance(row.get(col_to_set), bool):
                new_value = str(new_value).lower() in ("true", "1")

            row[col_to_set] = new_value
            updated_count += 1

    if updated_count == 0:
        return table_data, "Записи не найдены."
    return table_data, f"Записей обновлено: {updated_count}."


def delete(table_data, where_clause):
    """удаляет записи по условию"""
    where_col, where_val = list(where_clause.items())[0]
    initial_length = len(table_data)

    new_data = [row for row in table_data if str(row.get(where_col)) != str(where_val)]

    deleted_count = initial_length - len(new_data)
    if deleted_count == 0:
        return table_data, "Записи не найдены."
    return new_data, f"Записей удалено: {deleted_count}."