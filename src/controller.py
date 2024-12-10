import config as cfg
from models.book import Book
from models.library import Library


class LibraryController:
    """ Контроллер библиотеки.

    Выполняет роль связующего звена между моделями и представлениями.

    Attributes:
        library: Объект библиотеки.
    """

    def __init__(self):
        """Инициализирует контроллер библиотеки.

        Создает объект библиотеки как атрибут контроллера.
        Передает конфигурацию библиотеки.
        """
        self.library = Library(cfg)

    def add_book(self, title: str, author: str, year: int):
        """Добавляет книгу в библиотеку.

        Передает название, автора и год издания книги.
        И вызывает соответствующий метод библиотеки.

        Args:
            title: Название книги.
            author: Автор книги.
            year: Год издания книги.
        """
        self.library.add_book(title, author, year)

    def delete_book(self, book_id: int) -> bool:
        """Удаляет книгу из библиотеки по ID.

        Принимает `ID` книги и вызывает соответствующий метод библиотеки.
        Чтобы удалить книгу, нужно передать ее `ID`.

        Args:
            book_id: `ID` книги, которую нужно удалить.

        Returns:
            `True`, если книга успешно удалена, иначе `False`.
        """
        return self.library.delete_book(book_id)

    def search_books(self, query: str, field: str) -> list[Book]:
        """Ищет книги в библиотеке по заданному полю.

        Вызывает соответствующий метод библиотеки.
        Поиск осуществляется по-умолчанию с `id`, `title`, `author` или `year`.
        Набор полей может быть изменен в файле `/config/config.ini`.

        Args:
            query: Запрос для поиска.
            field: Поле для поиска (например, `title` или `author`).

        Returns:
            Список книг, соответствующих запросу.
        """
        return self.library.search_books(query, field)

    def update_status(self, book_id: int, status: str) -> bool:
        """Обновляет статус книги.

        Принимает `ID` книги и новый статус (`в наличии` или `выдана`).
        Вызывает соответствующий метод библиотеки.
        Чтобы обновить статус книги, нужно передать ее `ID` и новый статус.

        Args:
            book_id: `ID` книги.
            status: Новый статус книги (`в наличии` или `выдана`).

        Returns:
            `True`, если статус обновлён, иначе `False`.
        """
        return self.library.update_status(book_id, status)

    def get_book(self, book_id: int) -> Book | None:
        """Возвращает книгу по её `ID`.

        Принимает `ID` книги и вызывает соответствующий метод библиотеки.
        Чтобы получить в ответ книгу, нужно передать корректный `ID`.

        Args:
            book_id: `ID` книги.

        Returns:
            Объект книги, если она найдена, иначе `None`.
        """
        return self.library.get_book_by_id(book_id)

    def get_books(self, books: list[Book] = None) -> str:
        """ Возвращает список книг в читаемом текстовом формате.

        Принимает список книг и вызывает соответствующий метод библиотеки.
        Чтобы получить подготовленную строку книг, нужно передать список книг.
        Если список книг не передан, берутся все книги из `self.library.books`.
        Если список книг пуст, возвращается сообщение о том, что книг нет.

        Args:
            books: Список книг. Если `None`, используются все
                книги из `self.library.books`.

        Returns:
            Отформатированный список книг или сообщение о том, что книг нет.
        """
        if books is None:
            books = self.library.books
        if not books:
            return "Книг не найдено."
        header = "Список книг:"
        lines = [
            f"ID: {book.id} | Название: {book.title} | Автор: {book.author} | "
            f"Год: {book.year} | Статус: {book.status}"
            for book in books
        ]
        return "\n".join([header] + lines)

