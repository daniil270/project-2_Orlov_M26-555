import json
import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"


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
    """загружает данные таблицы из data"""
    # Теперь путь абсолютный и всегда ведет в корень проекта
    filepath = DATA_DIR / f"{table_name}.json"

    if not os.path.exists(filepath):
        return []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def save_table_data(table_name, data):
    """сохраняет данные таблицы в data"""
    # Если папки data нет в корне проекта, создаем её
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    filepath = DATA_DIR / f"{table_name}.json"

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)