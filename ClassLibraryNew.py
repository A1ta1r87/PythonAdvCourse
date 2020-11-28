class NewLibrary(dict):
    """Создает класс NewLibrary, наследуемый от класса dict.
    Полями атрибутов класса являются словари:
    books - содержащий сведения о книгах в виде - id книги: информация о ней;
    debtors - о читателях, взявших книгу в виде - id читательского билета: информации о читателе;
    all_checked_out_books - о выданных книгах в виде аналогичном books.
    """
    def __init__(self):
        self.books = {}
        self.debtors = {}
        self.all_checked_out_books = {}

    def add_book(self, book):
        """Функция, добавляющая книгу в библиотеку.
        Параметры:
        book - объект класса 'Book'.
        """
        book.is_in_stock = True
        self.books.update({book.id: [book.title, book.author, book.year, book.is_in_stock]})

    def delete_book(self, book):
        """Функция, удаляющая книгу из библиотеки.
        Параметры:
        book - объект класса 'Book'.
        """
        self.books.pop(book.id, "")  # если объект в словаре не найден, возвращаем "".
        book.is_in_stock = False

    def check_out_book(self, book, reader):
        """Функция для выдачи книги из библиотеки.
        Параметры:
        book - объект класса 'Book'
        reader - объект класса 'Reader'.
        """
        reader.debtor = True
        reader.borrowed_books.append(book.title)
        book.is_in_stock = False
        self.all_checked_out_books.update({book.id: [book.title, book.author, book.year]})
        self.debtors.update({reader.id: [reader.name, reader.surname, reader.borrowed_books]})

    def return_book(self, book, reader):
        """Функция для возврата книги в библиотеку.
        Параметры:
        book - объект класса 'Book'
        reader - объект класса 'Reader'.
        """
        self.all_checked_out_books.pop(book.id, "")  # если объект в словаре не найден, возвращаем "".
        book.is_in_stock = True
        reader.borrowed_books.remove(book.title)
        if not reader.borrowed_books:
            reader.debtor = False
            self.debtors.pop(reader.id, "")

    def show_all_books(self):
        """Функция, выводящая на экран все книги,
        кот-ый числятся за библиотекой.
        """
        print('Список книг библиотеки:')
        for book_id, book in self.books.items():
            print(f'{book_id}: {book[:3]}')  # выводим данные о книге до параметра "в наличии."

    def show_checked_out_books(self):
        """Функция, выводящая на экран книги,
        выданные читателям.
        """
        print('Книги, выданные читателям')
        for book_id, book in self.all_checked_out_books.items():
            print(f'{book_id}: {book}')

    def show_available_books(self):
        """Функция, выводящая на экран все доступные книги."""
        available_books = set(self.books) - set(self.all_checked_out_books)
        print('Доступны книги: ')
        for book_id in available_books:
            print(f'{book_id}: {self.books[book_id][:3]}')

    def sort_books(self, field='title'):
        """Функция, выводящая на экран список книг,
        отсортированных по заданным параметрам.
        Параметры:
        'title' - сортировка по названию книги, является параметром по умолчанию
        'author' - сортировка по имени автора
        'year' - сортировка по году издания.
        """
        index = 0 if field == 'title' else (1 if field == 'author' else (2 if field == 'year' else None))
        if index:
            # создаем список из значений книг в словаре books класса NewLibrary и сортируем,
            # назначая ключом переданный в функцию параметр (0 - название книги, 1 - автор, 2 - год издания).
            list_books = [book_info for book_info in self.books.values()]
            list_books.sort(key=lambda book_info: book_info[index])
            print(list_books)
        else:
            print("Incorrect parameter")


def my_init_book(self, book_id, title, author, year):
    """Функция, определяющая отрибуты экземпляров класса 'Book'."""
    self.id = book_id
    self.title = title
    self.author = author
    self.year = year
    self.is_in_stock = None


def my_init_reader(self, reader_id, name, surname):
    """Функция, определяющая отрибуты экземпляров класса 'Reader'."""
    self.id = reader_id
    self.name = name
    self.surname = surname
    self.debtor = None
    self.borrowed_books = []


Reader = type("Reader", (NewLibrary,), {'__init__': my_init_reader})
Book = type("Book", (NewLibrary,), {'__init__': my_init_book})

national_library = NewLibrary()

book1 = Book(1, 'ФМизери', 'Стивен Кинг', 1998)
book2 = Book(2, 'Руслан и людмила', 'А. С. Пушкин', 2013)
book3 = Book(3, 'БСобачье сердце', 'М. А. Булгаков', 2010)
book4 = Book(4, 'A', 'Джордж Оруэлл', 2015)
book5 = Book(5, 'На игле', 'Ирвин Уэлш', 1993)

reader3 = Reader('192', 'Alex', 'Petrov')
reader2 = Reader('92', 'Pavel', 'Kinchev')
reader1 = Reader('99', 'Oleg', 'Miheev' )

national_library.add_book(book1)
national_library.add_book(book2)
national_library.add_book(book3)
national_library.add_book(book4)
national_library.add_book(book5)

national_library.check_out_book(book4, reader1)
national_library.check_out_book(book3, reader2)
national_library.check_out_book(book1, reader2)

# print(national_library.debtors)
# national_library.sort_books('year')
# national_library.return_book(book3, reader2)
# national_library.return_book(book1, reader2)
# print(national_library.debtors)
# national_library.show_available_books()
# national_library.show_all_books()
# national_library.show_checked_out_books()


