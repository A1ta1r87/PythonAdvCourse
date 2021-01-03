from base_class_sql import Base
from book import Book
from reader import Reader
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

class Library:
    def __init__(self):
        self.book_list = []
        self.reader_list = []
        self.e = create_engine('postgresql://postgres:postgrespass@localhost:5432/postgres_orm')

        # create tables
        Base.metadata.create_all(self.e)

        #create session
        self.session = Session(bind=self.e)


    def load_data_from_db(self):
        for reader in self.session.query(Reader):
            self.reader_list.append(reader)
        for book in self.session.query(Reader):
            self.reader_list.append(reader)

        self.book_