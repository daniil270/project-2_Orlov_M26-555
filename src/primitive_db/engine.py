import shlex

import prompt

from primitive_db import core, parser, utils

PATH_TO_DB = "db_meta.json"


def print_help():
    """Функция вызова справки"""
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    print("\n***Операции с данными***")
    print("<command> insert into <имя_таблицы> values (<значение1>, <значение2>, ...) - создать запись")
    print("<command> select from <имя_таблицы> - прочитать все записи")
    print("<command> select from <имя_таблицы> where <столбец> = <значение> - прочитать записи по условию")
    print("<command> update <имя_таблицы> set <столбец> = <значение> \
    where <столбец> = <значение> - обновить запись")
    print("<command> delete from <имя_таблицы> where <столбец> = <значение> - удалить запись")
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


            elif command == "insert":
                if len(args) < 3 or args[0].lower() != "into" or args[2].lower() != "values":
                    print("Неизвестная функция.")
                    continue

                table_name = args[1]
                raw_values = " ".join(args[3:])
                clean_values = raw_values.replace(",", " ").replace("(", " ").replace(")", " ")
                values = shlex.split(clean_values)

                table_data = utils.load_table_data(table_name)
                new_id = max([r.get("ID", 0) for r in table_data], default=0) + 1

                new_record, error = core.insert(metadata, table_name, values)
                if error:
                    print(error)
                else:
                    new_record["ID"] = new_id
                    table_data.append(new_record)
                    utils.save_table_data(table_name, table_data)
                    print(f"Запись с ID={new_id}  добавлена в таблицу '{table_name}'.")

            elif command == "select":
                if len(args) < 2 or args[0].lower() != "from":
                    print("Неизвестная функция")
                    continue

                table_name = args[1]

                if table_name not in metadata:
                    print(f"Ошибка: Таблица '{table_name}' не существует.")
                    continue

                table_data = utils.load_table_data(table_name)
                where_clause = None

                # Проверяем, есть ли условие WHERE
                if "where" in args:
                    where_index = args.index("where")
                    where_str = " ".join(args[where_index + 1:])
                    where_clause = parser.parse_condition(where_str, "where")

                _, display = core.select(table_data, where_clause)
                print(display)

            elif command == "update":
                if len(args) < 4 or args[1].lower() != "set":
                    print("Неизвестная функция.")
                    continue

                table_name = args[0]

                if "where" not in args:
                    print("Неизвестная функция.")
                    continue

                where_index = args.index("where")
                set_str = " ".join(args[2:where_index])
                where_str = " ".join(args[where_index + 1:])

                set_clause = parser.parse_condition(set_str, "set")
                where_clause = parser.parse_condition(where_str, "where")

                if not set_clause or not where_clause:
                    print("Неизвестная функция")
                    continue

                table_data = utils.load_table_data(table_name)
                new_data, msg = core.update(table_data, set_clause, where_clause)
                print(msg)
                utils.save_table_data(table_name, new_data)

            elif command == "delete":
                if len(args) < 4 or args[0].lower() != "from":
                    print("Неизвестная функция")
                    continue

                table_name = args[1]

                if "where" not in args:
                    print("Неизвестная функция")
                    continue

                where_index = args.index("where")
                where_str = " ".join(args[where_index + 1:])
                where_clause = parser.parse_condition(where_str, "where")

                if not where_clause:
                    print("Неизвестная функция")
                    continue

                table_data = utils.load_table_data(table_name)
                new_data, msg = core.delete(table_data, where_clause)
                print(msg)
                utils.save_table_data(table_name, new_data)

            else:
                print(f"Функции '{command}' нет. Попробуйте снова.")

        except KeyboardInterrupt:
            print("\nВыход из программы...")
            break
        except Exception as e:
            print(f"Произошла ошибка: {e}")