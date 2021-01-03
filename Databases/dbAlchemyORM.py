from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer, Text, ForeignKey
from sqlalchemy.orm import mapper, relationship, Session
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    def __init__(self, name, fullname):
        self.name = name
        self.fullname = fullname

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)

    def __repr__(self):
        return f'User: {self.name}, {self.fullname}'


e = create_engine('postgresql://postgres:postgrespass@localhost:5432/postgres_orm')

# create user table

# Base.metadata.create_all(e)

user_1 = User('Ivan', 'Ivan Petrov')
print(user_1)

session = Session(bind=e)
session.add(user_1)
session.commit()
session.query(User).u