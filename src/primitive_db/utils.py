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