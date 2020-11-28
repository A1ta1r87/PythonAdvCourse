class Book:
    def __init__(self, book_id, title, author, year):
        self.id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.is_in_stock = None
        self.amount = 0
        self.check_outed = 0


print("hello 2")