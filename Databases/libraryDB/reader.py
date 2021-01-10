from sqlalchemy import Column, String, Integer, Boolean, ARRAY
from base_class_sql import Base


class Reader(Base):
    __tablename__ = 'reader'

    def __init__(self, name, surname, birth_year):
        self.name = name
        self.surname = surname
        self.birth_year = birth_year
        self.is_debtor = False

    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    birth_year = Column(Integer)
    is_debtor = Column(Boolean)



    def get_fullname(self):
        return f'{self.name} {self.surname}'

    def __repr__(self):
        return f'{self.get_fullname()} {self.birth_year} {self.is_debtor}'