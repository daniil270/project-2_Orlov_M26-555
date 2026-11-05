import prompt


def welcome():
    print("\nПервая попытка запустить проект!\n")
    print("***")
    print("<command> exit - выйти из программы")
    print("<command> help - справочная информация")

    while True:
        command = prompt.string("Введите команду: ").strip()

        if command == "exit":
            print("Выход из программы...")
            break

        elif command == "help":
            print("\n<command> exit - выйти из программы")
            print("<command> help - справочная информация")

        else:
            if command:
                print(f"Неизвестная команда: '{command}'. Введите 'help' для справки.")