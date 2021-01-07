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
    reader_id = Column(Integer, default=None)

    def reader_field(self):
        return self.reader.get_fullname() if self.reader_id is not None else "In stock"

    def __repr__(self):
        return f'{self.id} {self.title} {self.author} {self.year} {self.in_stock} {self.reader_field()}'