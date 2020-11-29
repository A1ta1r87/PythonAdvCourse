import json


class NewLibrary(dict):
    """Создает класс NewLibrary, наследуемый от класса dict.
    Объект класса обладает хар-ками из списка data_library,
    кот-ые заполняются при обращении к методам класса.
    Категории data_library:
        'Info' - список с краткой информацией о библиотеке
        'Books' - сведения о всех книгах библиотеки в виде словаря, где ключ - id книги, а значение - информация о ней;
        'Debtors' - словарь, содержащий данные о взявших книгу читателях,
                    в виде - id читательского билета: информация о владельце;
        'Given books' - информация о выданных книгах в виде аналогичном 'Books'
    """
    data_library = ['Info', 'Books', 'Debtors', 'Given books']

    def __init__(self, name, address):
        super().__init__()
        self.name = name
        self.address = address
        for i in NewLibrary.data_library:
            self.setdefault(i, {})
        self['Info'] = [self.name, self.address]

    def save_data(self):
        """Метод используемый для сохранения данных в json файл
        с кодировкой "utf-8" без экранирования не-ASCII символов
        """
        with open(f"{self['Info'][0]} db.json", 'w', encoding="utf-8") as json_file:
            json.dump(self, json_file, ensure_ascii=False)

    def load_data(self, json_file):
        """Метод загрузки данных из json файла с кодировкой 'utf-8'
        """
        with open(json_file, 'r', encoding='utf-8') as db_file:
            self.update(json.load(db_file))

    def add_book(self, book):
        """Функция, добавляющая книгу в библиотеку.
        Параметры:
        book - объект класса 'Book'.
        """
        self['Books'].setdefault(book.id, book.get_params_book())
        self['Books'][book.id].append('In stock')  # добавляем параметр "в наличии"

    def delete_book(self, book):
        """Функция, удаляющая книгу из библиотеки.
        Параметры:
        book - объект класса 'Book'.
        """
        self['Books'].pop(book.id, "")  # если объект в словаре не найден, возвращаем "".

    def give_out_book(self, book, reader):
        """Функция для выдачи книги из библиотеки.
        Параметры:
        book - объект класса 'Book'
        reader - объект класса 'Reader'.
        """
        self['Given books'].setdefault(book.id, book.get_params_book())
        self['Books'][book.id][3] = 'Out of stock'  # меняем значение параметра "в наличии"
        reader.taken_books.append(book.id)
        self['Debtors'].setdefault(reader.id, reader.get_params_reader())

    def return_book(self, book, reader):
        """Функция для возврата книги в библиотеку.
        Параметры:
        book - объект класса 'Book';
        reader - объект класса 'Reader'.
        """
        self['Given books'].pop(book.id, "")
        self['Books'][book.id][3] = 'In stock'  # меняем значение параметра "в наличии"
        reader.taken_books.remove(book.id)
        if not reader.taken_books:
            self['Debtors'].pop(reader.id, "")

    def show_all_books(self):
        """Функция, выводящая на экран все книги,
        кот-ые числятся за библиотекой.
        """
        print('Список книг библиотеки:\nID Info')
        for book_id, book in self['Books'].items():
            print(book_id, book)

    def show_given_books(self):
        """Функция, выводящая на экран книги,
        выданные читателям.
        """
        print('Книги, выданные читателям:\nID Info')
        for book_id, book in self['Given books'].items():
            print(book_id, book)

    def show_available_books(self):
        """Функция, выводящая на экран все доступные книги."""
        available_books = set(self['Books']) - set(self['Given books'])
        print('Доступны книги:\nID Info')
        for book_id in available_books:
            print(book_id, self['Books'][book_id])

    def sort_books(self, condition='title'):
        """Функция, выводящая на экран список книг,
        отсортированных по заданным параметрам.
        Параметры:
        'title' - сортировка по названию книги, является параметром по умолчанию
        'author' - сортировка по имени автора
        'year' - сортировка по году издания.
        """
        if condition in ('title', 'author', 'year'):
            # создаем список книг из словаря 'Books' и сортируем, назначая ключом сортировки
            # переданный в функцию параметр (0 - название книги, 1 - автор, 2 - год издания).
            index = 0 if condition == 'title' else (1 if condition == 'author' else 2)
            list_books = [book_info for book_info in self['Books'].values()]
            list_books.sort(key=lambda book_info: book_info[index])
            [print(book) for book in list_books]
        else:
            print("Incorrect parameter")


class Book:
    def __init__(self, book_id, title, author, year):
        self.id = book_id
        self.title = title
        self.author = author
        self.year = year

    def get_params_book(self):
        return [self.title, self.author, self.year]


class Reader:
    def __init__(self, reader_id, name, surname):
        self.id = reader_id
        self.name = name
        self.surname = surname
        self.taken_books = []

    def get_params_reader(self):
        return [self.name, self.surname, self.taken_books]


national_library = NewLibrary('National Library', 'Kyiv')
national_library2 = NewLibrary('Library', 'Odessa')
book1 = Book(1, 'ФМизери', 'Стивен Кинг', 1998)
book2 = Book(2, 'Руслан и людмила', 'А. С. Пушкин', 2013)
book3 = Book(3, 'БСобачье сердце', 'М. А. Булгаков', 2010)
book4 = Book(4, 'A', 'Джордж Оруэлл', 2015)
book5 = Book(5, 'На игле', 'Ирвин Уэлш', 1993)

reader3 = Reader('192', 'Alex', 'Petrov')
reader2 = Reader('92', 'Pavel', 'Kinchev')
reader1 = Reader('99', 'Oleg', 'Miheev')

national_library.add_book(book1)
national_library.add_book(book2)
national_library.add_book(book3)
national_library.add_book(book4)
national_library.add_book(book5)
# national_library.delete_book(book3)
national_library.give_out_book(book4, reader1)
national_library.give_out_book(book3, reader1)
national_library.give_out_book(book1, reader1)
# print(national_library['Given books'])

# print(national_library['Debtors'])
# print(national_library.debtors)
# national_library.sort_books('year')
# national_library.return_book(book3, reader1)
# national_library.return_book(book1, reader1)
# national_library.return_book(book4, reader1)
# print(national_library.debtors)
# national_library.show_available_books()
# national_library.show_all_books()
# national_library.show_checked_out_books()
# print(national_library['Debtors'])
national_library.save_data()
national_library2.load_data('National Library db.json')
print(national_library2)
