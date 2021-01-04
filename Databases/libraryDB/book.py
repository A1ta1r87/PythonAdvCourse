from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from base_class_sql import Base



class Book(Base):
    __tablename__ = 'book'

    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year
        self.reader_id = None
        self.in_stock = True

    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    year = Column(Integer)
    in_stock = Column(Boolean)
    reader_id = Column(Integer, ForeignKey('reader.id'), default=None)

    reader = relationship("Reader", backref="books")

    def get_params_book(self):
        return [self.title, self.author, self.year, self.in_stock, f'{self.reader.name} {self.reader.surname}' if self.reader_id != None else 'In stock']

    def __repr__(self):
        return f'Book: {self.id:^5}, {self.title:<50}{self.author:<20}{self.year:<5}'