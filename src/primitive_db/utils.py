import json
import os


def load_metadata(filepath):
    """Загружает данные из JSON файла. Возвращает пустой словарь, если его нет."""
    if not os.path.exists(filepath):
        return {}

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}


def save_metadata(filepath, data):
    """Сохраняет данные в JSON."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def load_table_data(table_name):
    """загружает данные конкретной таблицы из data"""
    filepath = os.path.join("data", f"{table_name}.json")

    if not os.path.exists(filepath):
        return []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def save_table_data(table_name, data):
    """сохраняет данные конкретной таблицы в data"""
    if not os.path.exists("data"):
        os.makedirs("data")

    filepath = os.path.join("data", f"{table_name}.json")

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)