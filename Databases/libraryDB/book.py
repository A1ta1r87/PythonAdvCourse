from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from base_class_sql import Base


class Book(Base):
    __tablename__ = 'book'

    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year
        self.reader_id = 1

    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    year = Column(Integer)
    reader_id = Column(Integer, ForeignKey('reader.id'))

    reader = relationship("Reader", backref="books")

    def __repr__(self):
        return f'Book: {self.id:^5}, {self.title:<50}{self.author:<20}{self.year:<5}{self.reader_id:<5}'