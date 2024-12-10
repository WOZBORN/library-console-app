import json
import os

from .book import Book



class Library:
    """Модель библиотеки.

    Представляет библиотеку, содержащую список книг.
    Содержит методы для добавления, удаления и поиска книг.

    Attributes:
        books: Список книг в библиотеке.
        config: Объект конфигурации.
    """
    def __init__(self, config: object):
        """Инициализирует библиотеку.

        Вызывается при создании нового экземпляра библиотеки.
        Загружает список книг из файла, указанного в конфигурации.

        Args:
            config: Объект конфигурации.
        """
        self.config = config
        self.books = self.load_books()

    def load_books(self) -> list[Book]:
        """Загружает список книг из файла.

        Загружает список книг из файла, указанного в конфигурации.
        Если файл не существует, возвращает пустой список.

        Returns:
            list: Список книг в библиотеке.
        """
        if not os.path.exists(self.config.DATA_FILE):
            return []
        with open(self.config.DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return [Book.from_dict(book) for book in data]

    def save_books(self):
        """Сохраняет список книг в файл.

        Сохраняет список книг в файл, указанный в конфигурации.
        """
        with open(self.config.DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(
                [book.to_dict() for book in self.books],
                file,
                indent=4,
                ensure_ascii=False
            )

    def add_book(self, title: str, author: str, year: int):
        """Добавляет книгу в библиотеку.

        Добавляет новую книгу в список книг в библиотеке.

        Args:
            title: Название книги.
            author: Автор книги.
            year: Год издания книги.
        """
        book_id = len(self.books) + 1
        new_book = Book(book_id, title, author, year)
        self.books.append(new_book)
        self.save_books()

    def delete_book(self, book_id: int) -> bool:
        """Удаляет книгу из библиотеки.

        Удаляет книгу из списка книг в библиотеке по `ID`.
        Чтобы удалить книгу, необходимо указать ее `ID`.
        Если книга с указанным `ID` не находится в библиотеке, возвращает `False`.

        Args:
            book_id: `ID` книги.

        Returns:
            bool: `True`, если книга удалена, иначе `False`.
        """
        book = self.get_book_by_id(book_id)
        if book:
            self.books.remove(book)
            self.save_books()
            return True
        return False

    def get_book_by_id(self, book_id: int) -> Book | None:
        """Получает книгу из библиотеки по `ID`.

        Поиск книги в библиотеке осуществляется по `ID`.
        Если книга с указанным `ID` не находится в библиотеке, возвращает `None`.

        Args:
            book_id: `ID` книги.

        Returns:
            Book: Книга, соответствующая указанному `ID`, иначе `None`.
        """
        for book in self.books:
            if book.id == book_id:
                return book
        return None

    def search_books(self, query: str, field: str) -> list[Book]:
        """Ищет книги в библиотеке по заданному полю.

        Ищет книги в библиотеке по заданному (фильтру) полю `field`.
        Поиск осуществляется по-умолчанию с `id`, `title`, `author` или `year`.
        Набор полей может быть изменен в файле `/config/config.ini`.

        Args:
            query: Запрос для поиска.
            field: Поле для поиска (например, `title` или `author`).

        Returns:
            Список книг, соответствующих запросу.
        """
        result = []
        test_book = Book(None, None, None, None)
        available_keys = vars(test_book).keys()
        if field.lower() not in available_keys:
            raise ValueError(f"""
            Неверное поле \"{field}\" для поиска в конфигурации.
            Доступные поля: {', '.join(available_keys)}
            Проверьте файл конфигурации /config/config.ini
            """)
        for book in self.books:
            attribute_value = str(getattr(book, field.lower(), ""))
            if query.lower() in attribute_value.lower():
                result.append(book)
        return result

    def update_status(self, book_id: int, status: str) -> bool:
        """Обновляет статус книги в библиотеке.

        Обновляет статус книги в библиотеке по `ID` и новому статусу.
        Чтобы обновить статус книги, необходимо указать ее `ID` и новый статус.
        Если книга с указанным `ID` не находится в библиотеке, возвращает `False`.

        Args:
            book_id: `ID` книги.
            status: Новый статус книги.

        Returns:
            bool: `True`, если статус обновлен, иначе `False`.
        """
        book = self.get_book_by_id(book_id)
        if book:
            book.status = status
            self.save_books()
            return True
        return False