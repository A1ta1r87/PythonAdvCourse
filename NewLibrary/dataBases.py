import psycopg2

conn = psycopg2.connect(dbname='postgres', user='postgres', password='postgrespass', host='localhost', port='5432')
curs = conn.cursor()
if conn:
    print('Connected!')
curs.execute("insert into \"Students\" values(Default, 'Olega', 'Bapustin')")

query = "select * from \"Students\""
curs.execute(query)
for i in curs:
    print(i)
conn.commit()
conn.close()