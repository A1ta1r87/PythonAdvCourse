from sqlalchemy import Column, String, Integer
from base_class_sql import Base

class Reader(Base):
    __tablename__ = 'reader'

    def __init__(self, name, surname, birth_year):
        self.name = name
        self.surname = surname
        self.birth_year = birth_year

    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    birth_year = Column(Integer)

    def __repr__(self):
        return f'Reader: {self.id:^5}{self.name:<20}{self.surname:<20}{self.birth_year:<5}'