# from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Text, ForeignKey
#
# meta_data = MetaData()
# person = Table('person',
#                meta_data,
#                Column('id', Integer, primary_key=True),
#                Column('name', Text),
#                Column('surname', Text),
#                Column('age', Integer)
#                )
# book = Table('books',
#              meta_data,
#              Column('id', Integer, primary_key=True),
#              Column('title', Text),
#              Column('user_id', Integer, ForeignKey(person.c.id = ))
#              )
# engine = create_engine("postgresql://postgres:postgrespass@localhost:5432/postgres")
# meta_data.create_all(engine)
# # engine.execute("""
# #     create table person (
# #         id serial primary key,
# #         name text,
# #         surname text,
# #         age integer
# #     )
# # """)
# # engine.execute("""
# #     insert into person (name, surname, age) values('Ivasi', 'Volyna', 30),
# #     ('Si', 'Vona', 20)
# # """)
# # result = engine.execute("select * from person where id =: p_id", p_id=2)
# for i in engine.execute(person.select().where(person.c.age == 20)):
#     print(i)
import sqlalchemy

meta_data = sqlalchemy.MetaData()

user_table = sqlalchemy.Table('user',
                   meta_data,
                   sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
                   sqlalchemy.Column('username', sqlalchemy.Text),
                   sqlalchemy.Column('password', sqlalchemy.Text)
                   )

address_table = sqlalchemy.Table('address',
                      meta_data,
                      sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
                      sqlalchemy.Column('user_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('user.id')),
                      sqlalchemy.Column('email_address', sqlalchemy.Text)
                      )

e = sqlalchemy.create_engine('postgresql://postgres:postgrespass@localhost:5432/postgres')

# create user table

# meta_data.create_all(e)

# e.execute(user_table.insert(),
#           [{'username': 'Jack',
#             'password': '123'},
#            {'username': 'Mary',
#             'password': '456'}])
#
#
# e.execute(address_table.insert(),
#           [{'user_id': 1,
#             'email_address': 'jack@gmail'},
#             {'user_id': 2,
#             'email_address': 'mary@gmail'}])
user_address = user_table.join(address_table, user_table.c.id == address_table.c.user_id)

update_obj = address_table.update().values(email_address='Aary@ukr').where(user_table.c.username=='Jack')
e.execute(update_obj)
# for row in e.execute(select([user_table, user_address]).select_from(user_address)):
#     print(row)
#     upd = table1.update()\
#     .values(id=table2.c.id)\
#     .where(table1.c.name == table2.c.name)