from base_class_sql import Base
from book import Book
from reader import Reader
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


class Library(dict):
    def __init__(self, name, address):
        super().__init__()
        self.name = name
        self.address = address
        self['Info'] = [self.name, self.address]
        self['Books'] = {}
        self['Readers'] = {}

        self.e = create_engine('postgresql://postgres:postgrespass@localhost:5432/postgres_orm')

        # create tables
        Base.metadata.create_all(self.e)

        # create session
        self.session = Session(bind=self.e)

        self.load_data_from_db()

    def load_data_from_db(self):
        for reader in self.session.query(Reader).order_by(Reader.id):
            self['Readers'].setdefault(reader.id, reader.get_params_reader())
            # self.reader_list.append(reader)
        for book in self.session.query(Book).order_by(Book.id):
            self['Books'].setdefault(book.id, book.get_params_book())

    def add_book(self, book: Book):
        """Функция, добавляющая книгу в библиотеку.
        Параметры:
        book - объект класса 'Book'.
        """
        self['Books'].setdefault(book.id, book.get_params_book())
        self.session.add(book)
        self.session.commit()

    def add_reader(self, reader: Reader):
        self['Readers'].setdefault(reader.id, reader.get_params_reader())
        self.session.add(reader)
        self.session.commit()

    def delete_book(self, book_id: int):
        """Функция, удаляющая книгу из библиотеки.
        Параметры:
        book - объект класса 'Book'.
        """
        if book_id in self['Books'].keys():
            title = self['Books'][book_id][0]
            self['Books'].pop(book_id)
            self.session.query(Book).filter(Book.id==book_id).delete()
            self.session.commit()
            return f'The book "{title}" was successfully deleted'
        else:
            return f'There is no book in our library with id {book_id}.'


    def get_all_books(self):
        """Функция, возвращающая все книги,
        кот-ые числятся за библиотекой.
        """
        return self['Books']

    def get_given_books(self):
        given_books = {}
        for id, book in self['Books'].items():
            if not book[3]:
                given_books.setdefault(id, book)
        return given_books

    def get_available_books(self):
        """Функция, возвращающая доступные читателю книги."""
        available_books = {}
        for id, book in self['Books'].items():
            if book[3]:
                available_books.setdefault(id, book)
        return available_books

    def give_book(self, reader_id: int, book_id: int):
        reader = self['Readers'].get(reader_id)
        if reader:
            pass
        else:
            return "There is no reader with such id."

    def sort_books(self, condition='title'):
        """Функция, возвращающая книги, отсортированные по указанному параметру в формате json.
        'title' - сортировка по названию книги, является параметром по умолчанию
        'author' - сортировка по имени автора
        'year' - сортировка по году издания.
        Если параметр указан неверно - возвращает False
        """
        if condition in ('title', 'author', 'year'):
            # создаем список книг из словаря 'Books' и сортируем, назначая ключом сортировки
            # переданный в функцию параметр (0 - название книги, 1 - автор, 2 - год издания).
            index = 0 if condition == 'title' else (1 if condition == 'author' else 2)
            return dict(sorted(self['Books'].items(), key=lambda item: item[1][index]))
        else:
            return False
