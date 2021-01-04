import flask
from jinja2 import Environment, FileSystemLoader, select_autoescape
from library import Library
from book import Book
from reader import Reader


app = flask.Flask(__name__)
app.config['DEBUG'] = True

# Создаем библиотеку
lib = Library('National Library', 'Kyiv')

# lib.add_book(Book('A Byte of Python', 'Swaroop Chitlur', 2003))
# lib.add_book(Book('Лёгкий способ выучить Python', 'Зед Шоу', 2010))
# lib.add_book(Book('Python. Карманный справочник', 'Марк Лутц', 1999))
# lib.add_book(Book('Изучаем Python', 'Марк Лутц', 2005))
#
# lib.add_reader(Reader('Andrii', 'Yaresko', 1994))
# lib.add_reader(Reader('Ivan', 'Nochovkin', 2002))
# lib.add_reader(Reader('Igor', 'Kudrya', 1974))
# lib.add_reader(Reader('Alex', 'Popyuk', 1987))
# lib.add_reader(Reader('Max', 'Polyakov', 1997))

e = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html'])
)
t_books = e.get_template('template.html')

@app.route('/api/books/all', methods=['GET'])
def api_get_all_book():
    return t_books.render(books=lib.get_all_books())

@app.route('/api/books/given', methods=['GET'])
def api_get_given_books():
    return t_books.render(books=lib.get_given_books())

@app.route('/api/books/available', methods=['GET'])
def api_get_available_books():
    return t_books.render(books=lib.get_available_books())

@app.route('/api/books/delete', methods=['GET'])
def api_delete_book():
    if 'id' in flask.request.args:
        id = int(flask.request.args['id'])
    else:
        return f'Error: No id field provided, please specify an id.'
    return lib.delete_book(id)

@app.route('/api/books', methods=['GET'])
def api_sort_books():
    if 'sort' in flask.request.args:
        condition = flask.request.args['sort']
    else:
        return f'Error: No sort field provided, please specify the sort condition.'
    books = lib.sort_books(condition)
    if not books:
        return 'Incorrect parameter'
    return t_books.render(books=books)

@app.route('/', methods=['GET'])
def home_page():
    return '<h1>This is Home Page</h1><p>This is a prototype API...</p>'


if __name__ == "__main__":
    app.run()