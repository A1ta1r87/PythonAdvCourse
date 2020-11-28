class Library:

    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.books = []
        self.debtors = []
        self.all_checked_out_books = []

    def add_book(self, book, amount=1):
        if book not in self.books:
            self.books.append(book)
        book.amount += amount
        book.is_in_stock = True

    def delete_book(self, book, amount=1):
        if book.amount <= amount:
            self.books.remove(book)
            book.is_in_stock = False
            book.amount = 0
        else:
            book.amount -= amount

    def check_out_book(self, book, reader):
        available_books = book.amount - book.check_outed
        if available_books >= 1:
            self.all_checked_out_books.append(book)
            self.debtors.append(reader)
            book.check_outed += 1
            reader.debtor = True
            reader.borrowed_books.append(book.title)
            if available_books == 1:
                book.is_in_stock = False
        else:
            print("This book is not available now")

    def return_book(self, book, reader):
        self.all_checked_out_books.remove(book)
        book.check_outed -= 1
        book.is_in_stock = True
        reader.borrowed_books.remove(book.title)
        self.debtors.remove(reader)
        if reader not in self.debtors:
            reader.debtor = False

    def show_all_books(self):
        for books in self.books:
            print(books.title)

    def show_checked_out_books(self):
        for books in self.all_checked_out_books:
            print(books.title)

    def show_available_books(self):
        books_in_library = list(set(self.books) - set(self.all_checked_out_books))
        for books in books_in_library:
            print(books.title)

    def sort_books(self, field='title'):
        flag = False
        if field == 'title':
            list_books = [book.title for book in self.books]
            flag = True
        elif field == 'author':
            list_books = [book.author for book in self.books]
            flag = True
        elif field == 'year':
            list_books = [book.year for book in self.books]
            flag = True
        else:
            print("Incorrect parameter")
        if flag:
            print(sorted(list_books))


class Book(Library):
    def __init__(self, book_id, title, author, year):
        self.id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.is_in_stock = None
        self.amount = 0
        self.check_outed = 0

    def get_params(self):
        return [self.id, self.title, self.author, self.year, self.is_in_stock]


class Reader(Library):
    def __init__(self, name, surname, reader_id):
        self.name = name
        self.surname = surname
        self.reader_id = reader_id
        self.debtor = None
        self.borrowed_books = []

    def get_params(self):
        return [self.name, self.surname, self.reader_id, self.borrowed_books]


national_library = Library('National Library', 'Kiev')
book1 = Book(1, 'Misery', 'Stephen King', 1998)
book2 = Book(2, 'Руслан и людмила', 'А. С. Пушкин', 2013)
book3 = Book(3, 'КСобачье сердце', 'М. А. Булгаков', 2010)
book4 = Book(4, 'A1984', 'Джордж Оруэлл', 2015)
reader3 = Reader('Alex', 'Petrov', '192')
reader2 = Reader('Pavel', 'Kinchev', '92')
reader1 = Reader('Oleg', 'Miheev', '99')

national_library.add_book(book1)
national_library.add_book(book2)
national_library.add_book(book3)
national_library.add_book(book4)
national_library.add_book(book2)
national_library.add_book(book4)

national_library.check_out_book(book4, reader1)
national_library.check_out_book(book4, reader1)
national_library.return_book(book4, reader1)
national_library.return_book(book4, reader1)
national_library.show_available_books()

for debtor in national_library.debtors:
    print(debtor.name)
