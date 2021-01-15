from sqlalchemy import Column, String, Integer, Boolean
from base_class_sql import Base
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Reader(Base):
    __tablename__ = 'reader'

    def __init__(self, name, surname, email, psw, birth_year):
        self.name = name
        self.surname = surname
        self.email = email
        self.psw_hash = generate_password_hash(psw)
        self.birth_year = birth_year
        self.is_debtor = False

    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    email = Column(String)
    psw_hash = Column(String)
    birth_year = Column(Integer)
    is_debtor = Column(Boolean)

    def check_psw(self, psw) -> bool:
        """
        Принимает хэш и пароль в чистом виде, затем сравнивает password и password_hash.
        Если они одинаковые, возвращает True.

        :param psw: пароль в чистом виде
        :return: Если парль верный, возвращаеь True, иначе - False
        """
        return check_password_hash(self.psw_hash, psw)

    def get_fullname(self):
        return f'{self.name} {self.surname}'

    def __repr__(self):
        return f'{self.get_fullname()} {self.birth_year} {self.is_debtor}'