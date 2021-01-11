from base_class_sql import Base
from book import Book
from reader import Reader
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


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

        # create tables
        # Base.metadata.create_all(self.e)

        # create session
        self.session = Session(bind=self.e)

        self.load_data_from_db()

    def load_data_from_db(self):
        """
        Загружает данные библиотеки из бд, заполняя словари 'Readers' и 'Books'
        """
        for reader in self.session.query(Reader).order_by(Reader.id):
            self['Readers'].setdefault(reader.id, reader)
        for book in self.session.query(Book).order_by(Book.id):
            self['Books'].setdefault(book.id, book)

    def add_book(self, book: Book):
        """
        Добавить книгу в библиотеку.
        :param book: объект класса Book;
        :return: сообщение об успешном добавлении книги
        """
        self.session.add(book)
        self.session.commit()
        book = self.session.query(Book).order_by(Book.id.desc()).limit(1).one()
        self['Books'].setdefault(book.id, book)
        return f'Книга "{book.title}" успешно добавлена в библиотеку.'

    def add_reader(self, reader: Reader):
        """
        Добавить читателя.
        :param reader: объект класса Reader;
        :return: сообщение об успешном добавлении читателя
        """
        self.session.add(reader)
        self.session.commit()
        reader = self.session.query(Reader).order_by(Reader.id.desc()).limit(1).one()
        self['Readers'].setdefault(reader.id, reader)
        return f'Читатель "{reader.get_fullname()}" успешно добавлен в библиотеку.'

    def delete_book(self, book_id: int):
        """Удалить книгу из библиотеки.
        :param book_id: номер книги в библиотеке
        :return: сообщение об успешном удалении книги
                или сообщение об ошибке (если книги с таким номером не найдено)
        """
        if book_id in self['Books'].keys():
            book = self['Books'][book_id]
            # self.session.query(Book).filter(Book.id==book_id).delete()
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
        """ Получить книги, отданные читателям."""
        given_books = {}
        for id, book in self['Books'].items():
            if not book.in_stock:
                given_books.setdefault(id, book)
        return given_books

    def get_available_books(self):
        """Получить доступные книги."""
        available_books = {}
        for id, book in self['Books'].items():
            if book.in_stock:
                available_books.setdefault(id, book)
        return available_books

    def give_book(self, reader_id: int, book_id: int):
        """
        Выдать книгу  читателю.
        :param reader_id: номер читателя
        :param book_id: номер книги
        :return: сообщение об успешной выдаче книги или сообщение об ошибке
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
        self.session.add_all([book, reader])
        self.session.commit()
        return f'Книга "{book.title}" успешно выдана.'

    def return_book(self, reader_id: int, book_id: int):
        """
        Вернуть книгу в библиотеку.
        :param reader_id: номер читателя
        :param book_id: номер книги
        :return: сообщение об успешном возврате книги или сообщение об ошибке
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

    def sort_books(self, condition='id', needed_books='all'):
        """
        Отсортировать книги по заданному условию.
        :param condition:   'id' - по номеру (параметр по умолчанию)
                            'title' - по названию
                            'author' - по имени автора
                            'year' - по году издания
        :param needed_books: книги, кот-ые необходимо отсортировать: 'all' - все книги библиотеки;
                                                                     'given' - выданные книги;
                                                                     'available' - доступные книги
        :return: отсортированный словарь книг, либо False в случае неверно указанных параметров
        """
        if condition in ('id', 'title', 'author', 'year'):
            if needed_books == 'given':
                books = self.get_given_books().items()
            elif needed_books == 'available':
                books = self.get_available_books().items()
            else:
                books = self['Books'].items()
            return dict(sorted(books, key=lambda item: item[1].id if condition == 'id' else
             (item[1].title if condition == 'title' else
              (item[1].author if condition == 'author' else
               item[1].year))))
        else:
            return False
