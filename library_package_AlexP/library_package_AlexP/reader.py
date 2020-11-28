class Reader:
    def __init__(self, name, surname, reader_id):
        self.name = name
        self.surname = surname
        self.reader_id = reader_id
        self.debtor = None
        self.borrowed_books = []

def test1():
    print("hello 1")