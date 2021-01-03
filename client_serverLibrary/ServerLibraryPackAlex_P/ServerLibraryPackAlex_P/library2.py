import json


class NewLibrary(dict):
    """Создает класс NewLibrary, наследуемый от класса dict.
    Объект класса обладает хар-ками из списка data_library,
    кот-ые заполняются при обращении к методам класса.
    Категории data_library:
        'Info' - список с краткой информацией о библиотеке
        'Books' - сведения о всех книгах библиотеки в виде словаря, где ключ - id книги, а значение - информация о ней;
        'Readers', 'Debtors' - словари, содержащие данные о читателях,
                    в виде - id читательского билета: информация о владельце;
        'Given books' - информация о выданных книгах в виде аналогичном 'Books'
    """
    data_library = ['Info', 'Books', 'Readers', 'Debtors', 'Given books']

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

    def add_reader(self, reader):
        """Функция, добавляющая данные о читателе в библиотеку."""
        self['Readers'].setdefault(reader.id, reader.get_params_reader())

    def delete_book(self, book):
        """Функция, удаляющая книгу из библиотеки.
        Параметры:
        book - объект класса 'Book'.
        """
        self['Books'].pop(book.id, "")  # если объект в словаре не найден, возвращаем "".

    def give_out_book(self, reader_id, book_id):
        """Функция для выдачи книги из библиотеки.
        Параметры:
        book_id - индекс кгиги в списке книг библиотеки 'Books'
        reader_id - id читателя в списке читателей библиотеки 'Readers'.
        """
        self['Given books'].setdefault(book_id, self['Books'][book_id])
        self['Books'][book_id][3] = 'Out of stock'  # меняем значение параметра "в наличии"
        self['Readers'][reader_id][2].append(book_id)
        self['Debtors'].update({reader_id: self['Readers'][reader_id]})
        print(self['Readers'])
        print(self['Given books'])
        print(self['Debtors'])

    def return_book(self, reader_id, book_id):
        """Функция для возврата книги в библиотеку.
        Параметры:
        book_id - индекс кгиги в списке книг библиотеки 'Books'
        reader_id - id читателя в списке читателей библиотеки 'Readers'.
        """
        self['Given books'].pop(book_id, "")
        self['Books'][book_id][3] = 'In stock'  # меняем значение параметра "в наличии"
        self['Readers'][reader_id][2].remove(book_id) # удаляем книгу из списка книг читателя
        if not self['Readers'][reader_id][2]:
            self['Debtors'].pop(reader_id, "")

    def show_all_books(self):
        """Функция, возвращающая все книги,
        кот-ые числятся за библиотекой в формате json.
        """
        all_books = {'Список всех книг в библиотеке': ''}
        for book_id, book in self['Books'].items():
            all_books.update({book_id: book[:3]})
        return json.dumps(all_books)

    def show_given_books(self):
        """Функция, возвращающая книги,
        выданные читателям в формате json.
        """
        given_books = {'Книги, выданные читателям': ''}
        for book_id, book in self['Given books'].items():
            given_books.update({book_id: book[:3]})
        return json.dumps(given_books)

    def show_available_books(self):
        """Функция, возвращающая доступные книги в формате json."""
        available_books = set(self['Books']) - set(self['Given books'])
        available_books_dict = {'Доступные книги': ''}
        for book_id in available_books:
            available_books_dict.update({book_id: self['Books'][book_id][:3]})
        return json.dumps(available_books_dict)

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
            sorted_books = {id: info[:3] for id, info in sorted(self['Books'].items(), key=lambda item: item[1][index])}
            return json.dumps(sorted_books)
        else:
            return False


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

reader3 = Reader(192, 'Alex', 'Petrov')
reader2 = Reader(92, 'Pavel', 'Kinchev')
reader1 = Reader(99, 'Oleg', 'Miheev')

national_library.add_book(book1)
national_library.add_book(book2)
national_library.add_book(book3)
national_library.add_book(book4)
national_library.add_book(book5)
national_library.add_reader(reader2)
national_library.add_reader(reader1)
national_library.add_reader(reader3)
# # national_library.delete_book(book3)
# national_library.give_out_book(99, 4)
# national_library.give_out_book(99, 3)
# national_library.give_out_book(92, 5)
# national_library.give_out_book(book1, reader1)
# # print(national_library['Given books'])
#
# # print(national_library['Debtors'])
# # print(national_library.debtors)
# # national_library.sort_books('year')
# # national_library.return_book(book3, reader1)
# # national_library.return_book(book1, reader1)
# # national_library.return_book(book4, reader1)
# # print(national_library.debtors)
# national_library.sort_books('year')
# print(national_library['Readers'])
# print(national_library['Given books'])
# print(national_library['Debtors'])
# national_library.save_data()
# national_library2.load_data('National Library db.json')
# print(national_library2)
