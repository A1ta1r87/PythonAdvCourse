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
        # Base.metadata.create_all(self.e)

        # create session
        self.session = Session(bind=self.e)

        self.load_data_from_db()

    def load_data_from_db(self):
        for reader in self.session.query(Reader).order_by(Reader.id):
            self['Readers'].setdefault(reader.id, reader)
            # self.reader_list.append(reader)
        for book in self.session.query(Book).order_by(Book.id):
            self['Books'].setdefault(book.id, book)

    def add_book(self, book: Book):
        """Функция, добавляющая книгу в библиотеку.
        Параметры:
        book - объект класса 'Book'.
        """
        self.session.add(book)
        self.session.commit()
        book = self.session.query(Book).order_by(Book.id.desc()).limit(1).one()
        self['Books'].setdefault(book.id, book)
        return f'The book was successfully added.'

    def add_reader(self, reader: Reader):
        self.session.add(reader)
        self.session.commit()
        reader = self.session.query(Reader).order_by(Reader.id.desc()).limit(1).one()
        self['Readers'].setdefault(reader.id, reader)
        return f'The reader was successfully added.'

    def delete_book(self, book_id: int):
        """Функция, удаляющая книгу из библиотеки.
        Параметры:
        book - объект класса 'Book'.
        """
        if book_id in self['Books'].keys():
            title = self['Books'][book_id].title
            book = self['Books'][book_id]
            self['Books'].pop(book_id)
            # self.session.query(Book).filter(Book.id==book_id).delete()
            self.session.delete(book)
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
            if not book.in_stock:
                given_books.setdefault(id, book)
        return given_books

    def get_available_books(self):
        """Функция, возвращающая доступные читателю книги."""
        available_books = {}
        for id, book in self['Books'].items():
            if book.in_stock:
                available_books.setdefault(id, book)
        return available_books

    def give_book(self, reader_id: int, book_id: int):
        if reader_id not in self['Readers'].keys():
            return "There is no reader with such id."
        reader = self['Readers'][reader_id]
        if book_id not in self['Books'].keys():
            return f'There is no book in our library with id {book_id}.'
        book = self['Books'][book_id]
        if not book.in_stock:
            return f'This book was given to another reader.'
        book.in_stock = False
        book.reader_id = reader.id
        if not reader.is_debtor:
            reader.is_debtor = True
        reader.taken_books.append(book.id)
        self.session.add_all([book, reader])
        print(reader)
        self.session.commit()
        print(reader)
        return 'The book was successfully given!'

    def return_book(self, reader_id: int, book_id: int):
        if reader_id not in self['Readers'].keys():
            return "There is no reader with such id."
        reader = self['Readers'][reader_id]
        if not reader.is_debtor:
            return 'You don`t need to return anything.'
        if book_id not in self['Books'].keys():
            return f'There is no book in our library with id {book_id}.'
        book = self['Books'][book_id]
        if book.in_stock:
            return f'This book is already in library.'
        if book.reader_id != reader.id:
            return 'You don`t take this book'
        book.in_stock = True
        book.reader_id = None
        # taken_books = reader.taken_books.pop(book.id)
        # if len(taken_books) == 0:
        #     reader.is_debtor = False
        self.session.add_all([book, reader])
        self.session.commit()
        return 'The book was successfully returned!'

    def sort_books(self, condition='title'):
        """Функция, возвращающая книги, отсортированные по указанному параметру в формате json.
        'title' - сортировка по названию книги, является параметром по умолчанию
        'author' - сортировка по имени автора
        'year' - сортировка по году издания.
        Если параметр указан неверно - возвращает False
        """
        if condition in ('title', 'author', 'year'):
            return dict(sorted(self['Books'].items(), key=lambda item: item[1].title if condition == 'title' else(item[1].author if condition == 'author' else item[1].year)))
        else:
            return False


