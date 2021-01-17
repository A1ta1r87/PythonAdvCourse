from base_class_sql import Base
from book import Book
from reader import Reader
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import re


class Library(dict):
    """
    Класс Library, унаследованный от класса dict.
    Содержит поля:
        'Books' - словарь объектов класса Book;
        'Readers' - словарь объектов класса Reader.
    Доступные методы:
        load_data_from_db   - загрузка данных из базы данных;
        add_book            - добавляет книгу в библиотеку;
        add_reader          - добавляет читателя;
        delete_book         - удаляет книгу из библиотеки;
        get_all_books       - предоставляет список всех книг библиотеки;
        get_given_books     - предоставляет список выданных на руки книг;
        get_available_books - предоставляет список доступных книг;
        give_book           - взять книгу;
        return_book         - вернуть книгу;
        sort_books          - вернуть отсортированные по заданному условию книги.
    """

    def __init__(self):
        """
        Конструктор класса Library. Инициализирует поля Books и Readers, подключение к базе данных.
        Создает таблицы/загружает данные из бд, стартует сессию.
        """
        super().__init__()
        self['Books'] = {}
        self['Readers'] = {}

        self.e = create_engine('postgresql://postgres:postgrespass@localhost:5432/postgres_orm')

        # создаем сессию
        self.session = Session(bind=self.e)

        # проверяем, существуют ли таблицы 'reader' и 'book', если нет - создаем их
        table_reader = self.session.execute("select * from information_schema.tables where table_name='reader'")
        table_book = self.session.execute("select * from information_schema.tables where table_name='book'")
        if not (table_reader.rowcount and table_book.rowcount):
            Base.metadata.create_all(self.e)  # создаем таблицы

        self.load_data_from_db()

    def load_data_from_db(self) -> None:
        """
        Загружает данные библиотеки из бд, заполняя словари 'Readers' и 'Books'.
        Returns:
             None
        """
        for reader in self.session.query(Reader).order_by(Reader.id):
            self['Readers'].setdefault(reader.id, reader)
        for book in self.session.query(Book).order_by(Book.id):
            self['Books'].setdefault(book.id, book)

    def add_book(self, book: Book):
        """
        Добавить книгу в библиотеку.
        Args:
            book: книга, объект класса Book
        Returns:
            сообщение об успешном добавлении книги
        """
        self.session.add(book)
        self.session.commit()
        self['Books'].setdefault(book.id, book)
        return f'Книга "{book.title}" успешно добавлена в библиотеку.'

    def add_reader(self, reader: Reader):
        """
        Добавить читателя.
        Args:
            reader: читатель, объект класса Reader
        Returns:
            сообщение об успешном добавлении читателя
        """
        self.session.add(reader)
        self.session.commit()
        self['Readers'].setdefault(reader.id, reader)
        return f'Читатель "{reader.get_fullname()}" успешно добавлен в библиотеку.'

    def check_email_exists(self, email: str):
        """
        Проверить, зарегистрирован ли в базе такой 'email'
        Args:
            email: строка с адресом электронной почты
        Returns:
            читателя, объект класса 'Reader', с соответствующим 'email'; и 'None', если такой 'email' не зарегистрирован
        """
        return self.session.query(Reader).filter(Reader.email == email).first()

    def delete_book(self, book_id: int):
        """
        Удалить книгу из библиотеки.
        Args:
            book_id: номер книги в библиотеке
        Returns:
            сообщение об успешном удалении книги или сообщение об ошибке (если книги с таким номером не найдено)
        """
        if book_id in self['Books'].keys():
            book = self['Books'][book_id]
            self.session.delete(book)
            self.session.commit()
            self['Books'].pop(book_id)
            return f'Книга "{book.title}" успешно удалена из библиотеки.'
        else:
            return f'В библиотеке нет книги с номером "{book_id}".'

    def get_all_books(self):
        """Получить все книги,
        кот-ые числятся за библиотекой.
        """
        return self['Books']

    def get_given_books(self):
        """ Получить все книги, отданные читателям."""
        given_books = {}
        for id, book in self['Books'].items():
            if not book.in_stock:
                given_books.setdefault(id, book)
        return given_books

    def get_given_books_to_reader(self, reader_id):
        """
        Получить книги, отданные конкретному читателю.
        Args:
            reader_id: номер читателя в базе данных
        Returns:
            словарь книг, в виде {номер книги: объект книга}
        """
        given_books = {}
        for id, book in self['Books'].items():
            if book.reader_id == reader_id:
                given_books.setdefault(id, book)
        return given_books

    def get_available_books(self):
        """
        Получить доступные книги.
        Returns:
            словарь книг, в виде {номер книги: объект книга}
        """
        available_books = {}
        for id, book in self['Books'].items():
            if book.in_stock:
                available_books.setdefault(id, book)
        return available_books

    def give_book(self, reader_id: int, book_id: int):
        """
        Выдать книгу  читателю.
        Args:
            reader_id: номер читателя
            book_id: номер книги
        Returns:
            сообщение об успешной выдаче книги или сообщение об ошибке
        """
        if reader_id not in self['Readers'].keys():
            return f'Читателя с номером "{reader_id}" нет в библиотеке .'
        reader = self['Readers'][reader_id]
        if book_id not in self['Books'].keys():
            return f'Книги с номером "{book_id}" нет в библиотеке.'
        book = self['Books'][book_id]
        if not book.in_stock:
            return 'К сожалению, этой книги нет в наличии.'
        book.in_stock = False
        book.reader_id = reader.id
        if not reader.is_debtor:
            reader.is_debtor = True
        self.session.commit()
        return f'Книга "{book.title}" успешно выдана.'

    def return_book(self, reader_id: int, book_id: int):
        """
        Вернуть книгу в библиотеку.
        Args:
            reader_id: номер читателя
            book_id: номер книги
        Returns:
            сообщение об успешном возврате книги или сообщение об ошибке
        """
        if reader_id not in self['Readers'].keys():
            return f'Читателя с номером "{reader_id}" нет в библиотеке .'
        reader = self['Readers'][reader_id]
        if not reader.is_debtor:
            return 'Вам не нужно ничего возвращать.'
        if book_id not in self['Books'].keys():
            return f'Книги с номером "{book_id}" нет в библиотеке.'
        book = self['Books'][book_id]
        if book.in_stock:
            return f'Книга с номером "{book_id}" уже в библиотеке.'
        if book.reader_id != reader.id:
            return 'Вы не брали эту книгу'
        book.in_stock = True
        book.reader_id = None
        taken_books = self.session.query(Book.reader_id).filter(Book.reader_id == reader.id).all()
        if len(taken_books) == 0:
            reader.is_debtor = False
        self.session.add_all([book, reader])
        self.session.commit()
        return f'Книга "{book.title}" успешно возвращена!'

    def search_in_library(self, search_exp: str):
        """
        Найти книгу в библиотеке по заданному шаблону. Поиск ведется по полям Id, Название, Автор, Год.
        Args:
            search_exp: строка - шаблон, по кот-ому ведется поиск совпадений,
                слово, часть слова, год, номер книги.
        Returns:
            Книги, в кот-ых найдены совпадения с шаблоном в виде словаря, либо пустой словарь
        """
        matched_books = {}
        for id, book in self['Books'].items():
            data_search = [str(book.id), book.title, book.author, str(book.year)]
            if re.search(search_exp.lower(), ''.join(data_search).lower()):
                matched_books[id] = book
        return matched_books
