from controller import LibraryController, cfg


class LibraryView:
    """Класс представления библиотеки.

    Используется для взаимодействия с пользователем.

    Attributes:
        controller: Контроллер библиотеки.
        actions: Словарь действий для меню.
    """

    def __init__(self):
        """Инициализирует экземпляр класса.

        Создает экземпляр контроллера библиотеки.
        Определяет действия для меню.
        """
        self.controller = LibraryController()
        self.actions = {
            "1": ("Добавить книгу", self._add_book),
            "2": ("Удалить книгу", self._delete_book),
            "3": ("Найти книгу", self._search_books),
            "4": ("Показать все книги", self._display_books),
            "5": ("Изменить статус книги", self._update_status),
            "6": ("Выйти", self._exit_program),
        }

    def main_menu(self):
        """Главное меню.

        Представляет интерфейс меню в консоли.
        Обрабатывает ввод пользователя по его пунктам.
        """
        while True:
            self._print_menu()
            choice = input("Выберите действие: ").strip()
            action = self.actions.get(choice)
            if action:
                action[1]()
            else:
                print("Неверный выбор. Попробуйте снова.")

    def _print_menu(self):
        """Печатает меню.

        Печатает текст интерфейса меню в консоль.
        """
        print("\nМеню:")
        for key, (desc, _) in self.actions.items():
            print(f"{key}. {desc}")

    def _add_book(self):
        """Добавление новой книги.

        Запрашивает у пользователя данные новой книги.
        Проверяет их на корректность и добавляет книгу в библиотеку.
        В случае ошибки выводит сообщение об ошибке.
        """
        data = self._collect_input({
            "title": ("Название книги", str),
            "author": ("Автор книги", str),
            "year": ("Год издания", int),
        })
        if data:
            try:
                self.controller.add_book(
                    data["title"],
                    data["author"],
                    data["year"]
                )
                print("Книга успешно добавлена.")
            except Exception as e:
                self._handle_error(e)

    def _delete_book(self):
        """Удаление книги по `ID`.

        Удаляет книгу из библиотеки по `ID`.
        Запрашивает у пользователя `ID` книги.
        Проверяет их на корректность и удаляет книгу из библиотеки.
        В случае ошибки выводит сообщение об ошибке.
        """
        data = self._collect_input({"id": ("ID книги", int)})
        if data:
            try:
                book_id = data["id"]
                book = self.controller.get_book(book_id)
                if not book:
                    print("Книга с таким ID не найдена.")
                    return
                print(f"Книга: {book.title}\nТекущий статус: {book.status}")
                clarification = self._collect_input({"answer": ("Удалить эту книгу? (y/n)", ["y", "n"])})
                if clarification["answer"].lower() != "y":
                    print("Действие отменено. Возврат в меню.")
                    return
                if self.controller.delete_book(book_id):
                    print("Книга удалена.")
                else:
                    print(f"Не удалось удалить книгу с ID {book_id}.")
            except Exception as e:
                self._handle_error(e)

    def _search_books(self):
        """Поиск книги по полю.

        Запрашивает у пользователя поле для (фильтрации) поиска.
        Поля берутся из конфигурации.
        Далее запрашивает значение для поиска.
        Проверяет их на корректность и выполняет поиск книги.
        В случае ошибки выводит сообщение об ошибке.
        """
        data = self._collect_input({
            "field": (
                f"Поле поиска {', '.join(cfg.SEARCH_FIELDS)}",
                cfg.SEARCH_FIELDS
            ),
            "query": ("Значение для поиска", str)
        })
        if not data:
            return
        try:
            books = self.controller.search_books(
                data["query"],
                data["field"]
            )
            self._display_books(books)
        except Exception as e:
            self._handle_error(e)

    def _display_books(self, books: list = None):
        """ Отображение списка книг.

        Отображает список книг в консоли.
        Если список книг пуст, выводит сообщение о том, что книг нет.
        Если список книг не задан, выведет все книги из библиотеки.

        Args:
            books: Список книг для отображения или (опционально). По-умолчанию `None`.
        """
        formatted_books = self.controller.get_books(books)
        print(formatted_books)

    def _update_status(self):
        """Обновление статуса книги.

        Запрашивает у пользователя `ID` книги.
        Проверяет наличие книги в библиотеке по `ID`.
        Если книга найдена, выводит ее название и текущий статус.
        Запрашивает у пользователя новый статус книги.
        Проверяет их на корректность и обновляет статус книги.
        Если книга не найдена, выводит сообщение об ошибке.
        """
        book_id = self._collect_input({"id": ("ID книги", int)})["id"]
        book = self.controller.get_book(book_id)
        if not book:
            print("Книга с таким ID не найдена.")
            return
        print(f"Книга: {book.title}\nТекущий статус: {book.status}")
        data = self._collect_input({
            "status": (
                "Новый статус (в наличии/выдана)",
                ["в наличии", "выдана"]
            )
        })
        data["id"] = book_id
        if not data:
            return
        try:
            updated = self.controller.update_status(
                    data["id"],
                    data["status"].lower()
            )
            print(
                "Статус успешно обновлён."
                if updated else "Книга с таким ID не найдена."
            )
        except Exception as e:
            self._handle_error(e)

    def _exit_program(self):
        """Завершение программы.

        Просто выходит из программы, попрощавшись.
        """
        print("До свидания!")
        exit(0)

    def _collect_input(self, fields: dict) -> dict | None:
        """Прием пользовательского ввода.

        Собирает пользовательский ввод для заданных полей с проверкой типов
        и возможностью отмены. Если ввод был отменён, возвращает `None`.

        Args:
            fields: Словарь `{ключ: (описание, тип/валидатор)}`

        Returns:
            Словарь {`ключ: значение}` с валидированным вводом.
            Если ввод был отменён, возвращает `None`.
        """
        data = {}
        print("\nДля отмены действия введите '!stop' в любом поле.")
        try:
            for key, (prompt, expected_type) in fields.items():
                while True:
                    value = input(f"\n{prompt}: ").strip()
                    if value.lower() == "!stop":
                        print("Действие отменено. Возврат в главное меню.")
                        return None
                    try:
                        if isinstance(expected_type, list):
                            if value.lower() not in expected_type:
                                raise ValueError(
                                    "Недопустимое значение. Ожидается одно из:"
                                    f" {', '.join(expected_type)}")
                        elif expected_type == int:
                            value = self._validate_num(value)
                        elif expected_type == float:
                            value = self._validate_num(value, True)
                        elif expected_type == str:
                            if not value:
                                raise ValueError("Строка не может быть пустой")
                        else:
                            raise ValueError(
                                f"Неподдерживаемый тип: {expected_type}"
                            )
                        data[key] = value
                        break
                    except ValueError as e:
                        print(f"Ошибка ввода: {e}.")
        except Exception as e:
            self._handle_error(e)
            return None
        return data

    def _validate_num(self, value: str, is_float: bool = False) -> int | float:
        """Валидация числового ввода.

        Проверяет, что значение является числом (целым или дробным).
        Если значение не является числом, выбрасывает исключение.

        Args:
            value: Введённое пользователем значение.
            is_float: Если `True`, ожидается дробное число.
             Если `False`, ожидается целое число.

        Returns:
            Целое/Дробное число, введённое пользователем.

        Raises:
            ValueError: Если значение не преобразовано в указанный тип.
        """
        try:
            return int(value) if not is_float else float(value)
        except ValueError:
            raise ValueError(
                f"Недопустимое значение. Ожидается "
                f"{'дробное' if is_float else 'целое'} число."
        )

    def _handle_error(self, error: Exception):
        """Обрабатывает ошибки.

        Выводит сообщения об ошибках в консоль.
        """
        print(f"Ошибка: {error}")
