import shlex

import prompt

from primitive_db import core, utils

PATH_TO_DB= "db_meta.json"


def print_help():
    """Функция вызова справки"""
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")


def run():
    """основной цикл программы"""
    metadata = utils.load_metadata(PATH_TO_DB)

    print("\n***База данных***\n")
    print_help()

    while True:
        try:
            user_input = prompt.string(">>>Введите команду: ").strip()
            if not user_input:
                continue

            parts = shlex.split(user_input)
            command = parts[0].lower()
            args = parts[1:]

            if command == "exit":
                print("Выход из программы...")
                break

            elif command == "help":
                print_help()

            elif command == "list_tables":
                print(core.list_tables(metadata))

            elif command == "create_table":
                if len(args) < 2:
                    print("Некорректное значение: Недостаточно аргументов.")
                    continue

                table_name = args[0]
                columns = args[1:]

                result = core.create_table(metadata, table_name, columns)
                print(result)

                if "Ошибка" not in result and "Некорректное" not in result:
                    utils.save_metadata(PATH_TO_DB, metadata)

            elif command == "drop_table":
                if len(args) != 1:
                    print("Некорректное значение: Неверное количество аргументов.")
                    continue

                table_name = args[0]
                result = core.drop_table(metadata, table_name)
                print(result)

                if "Ошибка" not in result:
                    utils.save_metadata(PATH_TO_DB, metadata)

            else:
                print(f"Функция '{command}' нет. Попробуйте снова.")

        except KeyboardInterrupt:
            print("\nВыход из программы...")
            break
        except Exception as e:
            print(f"Произошла ошибка: {e}")