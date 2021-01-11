import flask
from jinja2 import Environment, FileSystemLoader, select_autoescape
from library import Library
from book import Book
from reader import Reader

app = flask.Flask(__name__)
app.config['DEBUG'] = True

# Создаем библиотеку
lib = Library()
#
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


def is_number(x):
    """
    Вернуть True, если переданный элемент является числом
    или может быть преобразован в число (например число в виде строки)
    """
    try:
        int(x)
        return True
    except ValueError:
        return False


def get_sort_books(request, needed_books='all'):
    """
    Отсортировать книги, если в запросе есть параметр 'sort'.
    :param request: словарь, содержащий аргументы запроса
    :param needed_books: книги, кот-ые необходимо отсортировать: 'all' - все книги библиотеки (по умолчанию)
                                                                 'given' - выданные книги
                                                                 'available' - доступные книги
    :return: отсортированный словарь книг
    """
    if 'sort' in request:
        condition = request['sort']
        if condition:
            books = lib.sort_books(condition=condition, needed_books=needed_books)
            return books
    return False


@app.route('/books', methods=['GET'])
def api_get_books():
    sort_books = get_sort_books(flask.request.args, 'all')
    if sort_books:
        return flask.render_template('books.html', books=sort_books)
    return flask.render_template('books.html', path='books', books=lib.get_all_books())


@app.route('/given_books', methods=['GET'])
def api_get_given_books():
    sort_books = get_sort_books(flask.request.args, 'given')
    if sort_books:
        return flask.render_template('books.html', books=sort_books)
    return flask.render_template('books.html', path='/given_books', books=lib.get_given_books())


@app.route('/available_books', methods=['GET'])
def api_get_available_books():
    sort_books = get_sort_books(flask.request.args, 'available')
    if sort_books:
        return flask.render_template('books.html', books=sort_books)
    return flask.render_template('books.html', path='/available_books', books=lib.get_available_books())


@app.route('/delete_book', methods=['POST', 'GET'])
def api_delete_book():
    message = ''
    if flask.request.method == 'POST':
        id = flask.request.form['id']
        if not bool(id and is_number(id)):
            message = 'Данные указаны неверно'
        else:
            message = lib.delete_book(int(id))
    elif flask.request.method == 'GET':
        if 'id' in flask.request.args:
            id = flask.request.args['id']
            if is_number(id):
                message = lib.delete_book(int(id))
    return flask.render_template('delete_book.html', message=message, books=lib.get_all_books())


@app.route('/add_book', methods=['POST', 'GET'])
def api_add_book():
    message = ''
    if flask.request.method == 'POST':
        title = flask.request.form['title']
        author = flask.request.form['author']
        year = flask.request.form['year']
        if not (title and author and year and is_number(year)):
            message = 'Данные указаны неверно'
        else:
            message = lib.add_book(Book(title=title, author=author, year=int(year)))
    elif flask.request.method == 'GET':
        if 'title' in flask.request.args and 'author' in flask.request.args and 'year' in flask.request.args:
            title = flask.request.args['title']
            author = flask.request.args['author']
            year = flask.request.args['year']
            if title and author and year and is_number(year):
                message = lib.add_book(Book(title=title, author=author, year=year))
    return flask.render_template('add_book.html', message=message)


@app.route('/take_book', methods=['POST', 'GET'])
def api_give_book():
    message = ''
    if flask.request.method == 'POST':
        book_id = flask.request.form['book_id']
        reader_id = flask.request.form['reader_id']
        if not (book_id and reader_id and is_number(book_id) and is_number(reader_id)):
            message = 'Данные указаны неверно'
        else:
            message = lib.give_book(reader_id=int(reader_id), book_id=int(book_id))
    elif flask.request.method == 'GET':
        if 'reader_id' in flask.request.args and 'book_id' in flask.request.args:
            book_id = flask.request.args['book_id']
            reader_id = flask.request.args['reader_id']
            if is_number(book_id) and is_number(reader_id):
                message = lib.give_book(reader_id=int(reader_id), book_id=int(book_id))
    return flask.render_template('take_book.html', message=message, books=lib.get_available_books())


@app.route('/return_book', methods=['POST', 'GET'])
def api_return_book():
    message = ''
    if flask.request.method == 'POST':
        book_id = flask.request.form['book_id']
        reader_id = flask.request.form['reader_id']
        if not (book_id and reader_id and is_number(book_id) and is_number(reader_id)):
            message = 'Данные указаны неверно'
        else:
            message = lib.return_book(reader_id=int(reader_id), book_id=int(book_id))
    elif flask.request.method == 'GET':
        if 'reader_id' in flask.request.args and 'book_id' in flask.request.args:
            book_id = flask.request.args['book_id']
            reader_id = flask.request.args['reader_id']
            if is_number(book_id) and is_number(reader_id):
                message = lib.return_book(reader_id=int(reader_id), book_id=int(book_id))
    return flask.render_template('return_book.html', message=message, books=lib.get_given_books())


@app.route('/index')
@app.route('/')
def home_page():
    return flask.render_template('index.html')


if __name__ == "__main__":
    app.run()
